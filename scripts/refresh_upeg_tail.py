#!/usr/bin/env python3
"""Repair the frozen uPEG run: retain May, fetch June onward with checked RPC chunks.

All caches, backups and results live below the existing output directory. Failed
requests are never stored as empty successes. Run again to resume completed chunks.
"""
from __future__ import annotations
import concurrent.futures as cf
import json
import os
from pathlib import Path
import shutil
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dotenv import load_dotenv
import requests
from web3 import Web3
from web3._utils.events import get_event_data
from eth_utils import event_abi_to_log_topic
from hexbytes import HexBytes
from src.client import _load_abi

OUT = ROOT / 'output-upeg-may-sep-2026'
WORK = OUT / 'tail_refresh_20260910'
TOKEN = '0x44b28991B167582F18BA0259e0173176ca125505'
MANAGER = '0x000000000004444c5dc75cB358380D2e3dE08A90'
START, END = 24996368, 25878705
JUNE = int(datetime(2026, 6, 1, tzinfo=timezone.utc).timestamp())
RPC = 'https://eth.drpc.org'

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, separators=(',', ':'), default=str))
    tmp.replace(path)

def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default

def rpc(method, params, endpoint=RPC):
    last = None
    for attempt in range(5):
        try:
            response = requests.post(endpoint, json={'jsonrpc':'2.0','id':1,'method':method,'params':params}, timeout=35)
            body = response.json()
            if response.ok and 'result' in body and body['result'] is not None:
                return body['result']
            last = body.get('error', {}).get('message', 'HTTP '+str(response.status_code))
        except Exception as exc:
            last = type(exc).__name__
        time.sleep(min(8, 1 + attempt * 2))
    raise RuntimeError(f'{method} failed: {last}')

def fetch_chunk(job):
    name, a, b, flt = job
    path = WORK / 'rpc_cache' / f'{name}_{a}_{b}.json'
    cached = read(path)
    if cached is not None:
        assert cached['from_block'] == a and cached['to_block'] == b
        return name, a, b, cached['logs']
    q = {**flt, 'fromBlock':hex(a), 'toBlock':hex(b)}
    try:
        logs = rpc('eth_getLogs', [q])
    except RuntimeError:
        if b-a < 100:
            raise
        mid = (a+b)//2
        logs = fetch_chunk((name,a,mid,flt))[3] + fetch_chunk((name,mid+1,b,flt))[3]
    assert isinstance(logs,list)
    assert all(a <= int(x['blockNumber'],16) <= b and not x.get('removed') for x in logs)
    write(path, {'from_block':a,'to_block':b,'logs':logs,'source':RPC})
    return name,a,b,logs

def main():
    load_dotenv(ROOT / '.env')
    WORK.mkdir(parents=True,exist_ok=True)
    assert read(OUT/'token_profile.json')['address'].lower() == TOKEN.lower()
    assert rpc('eth_chainId', []) == '0x1'
    window = read(WORK/'window.json')
    if window is None:
        lo,hi = START,END
        while lo < hi:
            mid=(lo+hi)//2
            ts=int(rpc('eth_getBlockByNumber',[hex(mid),False])['timestamp'],16)
            if ts < JUNE: lo=mid+1
            else: hi=mid
        window={'from_block':START,'refresh_from_block':lo,'to_block':END,'refresh_from_utc':'2026-06-01T00:00:00Z','token':TOKEN}
        write(WORK/'window.json',window)
    split=window['refresh_from_block']
    print('Frozen window',window,flush=True)
    backup=WORK/'before'
    backup.mkdir(exist_ok=True)
    for path in OUT.iterdir():
        if path.is_file() and path.suffix in {'.json','.html','.md','.csv'} and not (backup/path.name).exists():
            shutil.copy2(path,backup/path.name)
    pools=read(backup/'verified_pools.json')
    ids=[(p.get('pool_id') or p['pool_address']).lower() for p in pools if p.get('verified') and p['version']=='v4']
    abi_maps={}
    filters={}
    for version,abi_name,names in [('v2','uniswap_v2_pair',{'Swap','Mint','Burn'}),('v3','uniswap_v3_pool',{'Swap','Mint','Burn','Collect'}),('v4','uniswap_v4_pool_manager',{'Swap','ModifyLiquidity','Initialize'})]:
        abis=[a for a in _load_abi(abi_name) if a.get('type')=='event' and a['name'] in names]
        abi_maps[version]={'0x'+event_abi_to_log_topic(a).hex():a for a in abis}
        addresses=[p['pool_address'] for p in pools if p.get('verified') and p['version']==version]
        filters[version]={'address':MANAGER if version=='v4' else addresses,'topics':[list(abi_maps[version])]}
        if version=='v4': filters[version]['topics'].append(ids)
    transfer_abi=next(a for a in _load_abi('erc20') if a.get('type')=='event' and a['name']=='Transfer')
    filters['transfer']={'address':TOKEN,'topics':['0x'+event_abi_to_log_topic(transfer_abi).hex()]}
    jobs=[(name,a,min(a+4999,END),flt) for name,flt in filters.items() for a in range(split,END+1,5000)]
    fetched={name:[] for name in filters}
    with cf.ThreadPoolExecutor(max_workers=4) as executor:
        futures={executor.submit(fetch_chunk,j):j for j in jobs}
        for i,f in enumerate(cf.as_completed(futures),1):
            name,a,b,logs=f.result()
            fetched[name].extend(logs)
            if i%20==0 or i==len(jobs):
                status={**window,'phase':'fetch','completed_chunks':i,'total_chunks':len(jobs),'rows':{k:len(v) for k,v in fetched.items()}}
                write(WORK/'status.json',status)
                print('Progress',status,flush=True)
    write(WORK/'status.json',{**window,'phase':'fetched','total_chunks':len(jobs),'rows':{k:len(v) for k,v in fetched.items()}})
    build(window,backup,pools,fetched,abi_maps,transfer_abi)

def build(window,backup,pools,fetched,abi_maps,transfer_abi):
    from src.indexer.dune_index import _normalize_transfer, _normalize_liquidity, enrich_v4_modify_amounts
    from src.analysis.v3_math import get_amounts_for_liquidity
    split=window['refresh_from_block']
    prior_swaps=read(backup/'swaps.json')
    prior_liq=read(backup/'liquidity_events.json')
    stamp={int(x['block_number']):int(x['block_timestamp']) for x in prior_swaps+prior_liq if x.get('block_timestamp')}
    stamp.update({int(k):int(v) for k,v in read(WORK/'timestamps.json',{}).items()})
    missing=sorted({int(x['blockNumber'],16) for rows in fetched.values() for x in rows}-stamp.keys())
    print('Missing timestamps',len(missing),flush=True)
    def headers(blocks):
        payload=[{'jsonrpc':'2.0','id':b,'method':'eth_getBlockByNumber','params':[hex(b),False]} for b in blocks]
        for attempt in range(5):
            try:
                result=requests.post(os.environ['ETH_RPC_URL'],json=payload,timeout=60).json()
                values={int(x['id']):int(x['result']['timestamp'],16) for x in result if x.get('result')}
                if set(values)==set(blocks):return values
            except Exception:
                pass
            time.sleep(2+attempt)
        raise RuntimeError('Timestamp batch incomplete; raw log caches retained')
    batches=[missing[i:i+40] for i in range(0,len(missing),40)]
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for i,values in enumerate(ex.map(headers,batches),1):
            stamp.update(values)
            write(WORK/'timestamps.json',stamp)
            if i%5==0 or i==len(batches):print('timestamp batches',i,'/',len(batches),flush=True)
    write(WORK/'timestamps.json',stamp)
    codec=Web3().codec
    poolmap={p['pool_address'].lower():p for p in pools}
    old_index={(x['transaction_hash'].lower(),x['log_index']):x for x in prior_swaps}
    old_liq_index={(x.get('transaction_hash','').lower(),x.get('log_index')):x for x in prior_liq if x.get('transaction_hash')}
    cached_transfer={}; cached_v4={}; price_rows=[]
    cache=OUT/'dune_cache'/f'index_{START}_{END}'/'cache'
    for path in cache.glob('*.json'):
        doc=read(path); rows=doc.get('rows',[]) if isinstance(doc,dict) else doc
        for row in rows:
            b=int(row.get('block_number') or 0)
            if not START<=b<split: continue
            if 'amount_raw' in row and 'recipient' in row:
                cached_transfer[(row['transaction_hash'].lower(),row['log_index'])]=_normalize_transfer(row)
            elif 'salt' in row and row.get('pool_id','').lower() in poolmap and row.get('transaction_hash'):
                key=(row['transaction_hash'].lower(),row['log_index'])
                if key not in cached_v4 or 'caller_delta' in row:cached_v4[key]=row
            elif 'sqrt_price_x96' in row: price_rows.append(row)
    v4early=[_normalize_liquidity(x,'liquidity_uniswap_v4_modify') for x in enrich_v4_modify_amounts(list(cached_v4.values()),price_rows)]
    for x in v4early:
        if int(x['liquidity_delta'])==0: x['event_type']='COLLECT_FEES'
        x['coverage_source']='retained_dune_cache'
    swaps=[x for x in prior_swaps if x['block_number']<split]
    liq=[x for x in prior_liq if x['block_number']<split and x['version'] not in ('v4','4')]+v4early
    transfers=list(cached_transfer.values())
    fresh_keys=set(); price_state={}
    for row in sorted(price_rows,key=lambda x:int(x['block_number'])):
        price_state[row['pool_id'].lower()]=int(row['sqrt_price_x96'])
    for version,logs in fetched.items():
        logs.sort(key=lambda x:(int(x['blockNumber'],16),int(x['logIndex'],16)))
        for raw in logs:
            abi=transfer_abi if version=='transfer' else abi_maps[version][raw['topics'][0]]
            fmt={**raw,'blockNumber':int(raw['blockNumber'],16),'logIndex':int(raw['logIndex'],16),'transactionIndex':int(raw['transactionIndex'],16),'transactionHash':HexBytes(raw['transactionHash']),'blockHash':HexBytes(raw['blockHash']),'topics':[HexBytes(t) for t in raw['topics']]}
            evt=get_event_data(codec,abi,fmt);args=evt['args'];b=fmt['blockNumber'];key=(raw['transactionHash'].lower(),fmt['logIndex']);name=abi['name']
            if version=='transfer':
                transfers.append(_normalize_transfer({'block_number':b,'block_timestamp':stamp[b],'transaction_hash':raw['transactionHash'],'log_index':fmt['logIndex'],'actor':args['from'],'recipient':args['to'],'amount_raw':str(args['value'])}))
                continue
            poolid=('0x'+bytes(args['id']).hex()).lower() if version=='v4' else raw['address'].lower()
            pool=poolmap[poolid]
            if name=='Initialize':
                price_state[poolid]=int(args['sqrtPriceX96']);continue
            base={'block_number':b,'block_timestamp':stamp[b],'transaction_hash':raw['transactionHash'],'log_index':fmt['logIndex'],'protocol':'uniswap','version':version,'pool_address':pool['pool_address'],'verified':True,'source_event':name,'nft_token_id':None,'liquidity_delta':'0','actor':args.get('owner',args.get('sender','')),'recipient':args.get('recipient',args.get('to',args.get('owner','')))}
            if name=='Swap':
                fresh_keys.add(key)
                if key in old_index:
                    row={**old_index[key],'pool_address':pool['pool_address'],'version':version,'coverage_source':'rpc_log_verified'}
                else:
                    if version=='v2':amounts=[int(args['amount0In'])-int(args['amount0Out']),int(args['amount1In'])-int(args['amount1Out'])]
                    else:amounts=[int(args['amount0']),int(args['amount1'])]
                    row={**base,'event_type':'SWAP','token0_amount':str(abs(amounts[0])),'token1_amount':str(abs(amounts[1])),'token0_address':pool['token0'],'token1_address':pool['token1'],'amount_usd':0,'coverage_source':'rpc_added_usd_unavailable'}
                swaps.append(row)
                if version=='v4':price_state[poolid]=int(args['sqrtPriceX96'])
                continue
            row={**base,'event_type':'LIQUIDITY_ADD' if name=='Mint' else 'LIQUIDITY_REMOVE','aggregation_scope':'row','event_count':1,'token0_amount':'0','token1_amount':'0','coverage_source':'rpc_tail_refresh'}
            if version=='v4':
                delta=int(args['liquidityDelta']);row.update(liquidity_delta=str(delta),tick_lower=int(args['tickLower']),tick_upper=int(args['tickUpper']),salt='0x'+bytes(args['salt']).hex(),actor_source='pool_manager_sender_not_beneficial_owner')
                row['event_type']='LIQUIDITY_ADD' if delta>0 else 'LIQUIDITY_REMOVE' if delta<0 else 'COLLECT_FEES'
                price=price_state.get(poolid)
                if price and delta:
                    a0,a1=get_amounts_for_liquidity(price,row['tick_lower'],row['tick_upper'],abs(delta))
                    row.update(token0_amount=str(a0),token1_amount=str(a1),amounts_available=True,quantification_status='estimated',amount_source='prior_pool_swap_tick_math')
                else:row.update(amounts_available=False,quantification_status='liquidity_delta_only')
            else:
                row.update(token0_amount=str(args['amount0']),token1_amount=str(args['amount1']),amounts_available=True,quantification_status='quantified',amount_source='pool_event')
                if version=='v3':
                    row.update(tick_lower=int(args['tickLower']),tick_upper=int(args['tickUpper']),actor_source='pool_position_owner_not_beneficial_owner')
                    row['liquidity_delta']=str(int(args.get('amount',0)) * (-1 if name=='Burn' else 1))
                    if name=='Collect':row['event_type']='COLLECT_FEES'
                    prior=old_liq_index.get(key)
                    if prior:
                        for field in ['actor','actor_source','nft_token_id']:
                            if prior.get(field) is not None: row[field]=prior[field]
            liq.append(row)
    # Preserve other DEX trades; the RPC scope is the existing verified Uniswap pools.
    keep_other=[x for x in prior_swaps if x['block_number']>=split and (x['transaction_hash'].lower(),x['log_index']) not in fresh_keys]
    swaps.extend(keep_other)
    tables={'swaps':swaps,'liquidity_events':liq,'transfers':transfers}
    for name,rows in tables.items():
        rows.sort(key=lambda x:(x['block_number'],x.get('log_index',0)))
        if name!='liquidity_events':
            keys=[(x['transaction_hash'].lower(),x['log_index']) for x in rows]
            assert len(keys)==len(set(keys)),name+' duplicate keys'
        assert all(START<=x['block_number']<=END for x in rows)
        assert all(x.get('block_timestamp',0)>0 for x in rows)
        write(WORK/(name+'.json'),rows)
    summary={**window,'phase':'validated','counts':{k:len(v) for k,v in tables.items()},'rpc_swap_count':len(fresh_keys),'retained_tail_swaps_not_rpc_verified':len(keep_other),'may_v4_restored':len(v4early),'may_transfers_restored':len(cached_transfer),'scope':'May reused local cache; June-August RPC for 106 verified Uniswap pools and all target-token Transfers. Existing other-DEX swaps retained. LP beneficial-owner history is incomplete; V4 amounts are prior-price estimates.'}
    write(WORK/'status.json',summary)
    print('VALIDATED',summary,flush=True)
    for name in tables:shutil.copy2(WORK/(name+'.json'),OUT/(name+'.json'))
    source=read(backup/'index_source.json');source.update(source='dune_cache_and_rpc_tail_refresh',counts={**source.get('counts',{}),**summary['counts']},tail_refresh=summary)
    for name in tables:
        if name in source.get('artifacts',{}):source['artifacts'][name]['rows']=len(tables[name])
    write(OUT/'index_source.json',source)
    summary['phase']='merged';write(WORK/'status.json',summary)

if __name__=='__main__':main()
