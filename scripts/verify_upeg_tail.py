#!/usr/bin/env python3
"""Check the refreshed Transfer ledger against independent historical balances."""
import json
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
import os
from scripts.refresh_upeg_tail import OUT,WORK,TOKEN,rpc,write,read

def main():
    load_dotenv(ROOT/'.env')
    status=read(WORK/'status.json');assert status['phase']=='merged'
    first,last=status['refresh_from_block'],status['to_block']
    pools=read(OUT/'verified_pools.json')
    addresses=sorted({(p.get('custody_address') or p['pool_address']).lower() for p in pools if p.get('verified') and len(p.get('custody_address') or p['pool_address'])==42})
    transfers=read(OUT/'transfers.json');net=defaultdict(int)
    for x in transfers:
        if first<=x['block_number']<=last:
            amount=int(x['token0_amount']);net[x['actor'].lower()]-=amount;net[x['recipient'].lower()]+=amount
    result=[]
    for address in addresses:
        call={'to':TOKEN,'data':'0x70a08231'+address.removeprefix('0x').zfill(64)}
        before=int(rpc('eth_call',[call,hex(first-1)],endpoint=os.environ['ETH_RPC_URL']),16)
        after=int(rpc('eth_call',[call,hex(last)],endpoint=os.environ['ETH_RPC_URL']),16)
        result.append({'custody_address':address,'start_balance_raw':str(before),'end_balance_raw':str(after),'transfer_net_raw':str(net[address]),'residual_raw':str(after-before-net[address]),'exact_match':after-before==net[address]})
        print('Balance reconciliation',address,result[-1]['exact_match'],flush=True)
    monthly={}
    for name in ['swaps','liquidity_events','transfers']:
        c=Counter()
        for x in read(OUT/(name+'.json')):
            month=datetime.fromtimestamp(x['block_timestamp'],timezone.utc).strftime('%Y-%m')
            c[month]+=1
        monthly[name]=dict(sorted(c.items()))
    audit={'balance_reconciliation':result,'all_exact':all(x['exact_match'] for x in result),'monthly_counts':monthly,'note':'Exact net-balance reconciliation is a consistency check, not proof against offsetting missing transfers. May is reused, not re-scanned.'}
    write(WORK/'validation.json',audit)
    assert audit['all_exact'],'Transfer balance reconciliation failed; inspect residuals'
    print('PASS',len(result),'custody addresses',monthly,flush=True)

if __name__=='__main__':main()
