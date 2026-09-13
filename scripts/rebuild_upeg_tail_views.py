#!/usr/bin/env python3
"""Rebuild the existing uPEG views from the merged event tables, offline."""
from pathlib import Path
import sys
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'output-upeg-may-sep-2026'

def read(path): return json.loads(Path(path).read_text())
def write(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(obj,indent=2,default=str));temp.replace(path)

def build_withdrawal_plot_data(output_dir=OUT):
    """Always derive plot data from current artifacts, never the legacy notebook cache."""
    from src.models import VerifiedPool
    from src.analysis.metrics import calculate_withdrawal_severity,from_block_tvl_by_pool
    out=Path(output_dir);liquidity=read(out/'liquidity_events.json')
    snapshots=read(out/'tvl_timeline.json');pools=[VerifiedPool(**p) for p in read(out/'verified_pools.json')]
    source=read(out/'index_source.json');token=read(out/'token_profile.json')
    severity=calculate_withdrawal_severity(liquidity,0,0,verified_pools=pools,target_token=token['address'],token_decimals=token['decimals'],tvl_by_pool=from_block_tvl_by_pool(snapshots,source['from_block']),timeline=snapshots)
    events=severity['withdrawal_events']
    start=datetime(2026,5,1,tzinfo=timezone.utc);days=[start+timedelta(days=i) for i in range(123)]
    prices={datetime.fromtimestamp(r['block_timestamp'],timezone.utc).date():r.get('price_usd') for r in snapshots if r['pool_address'].lower()=='0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775'}
    daily=defaultdict(lambda:defaultdict(float))
    for e in events:
        actor=(e.get('actor') or '').lower()
        if actor and e.get('ts'):
            day=datetime.fromtimestamp(e['ts'],timezone.utc).date()
            daily[actor][day]+=float(e.get('removed_target_decimal') or 0)
    top=[]
    for rank,row in enumerate(sorted(severity['per_address_removals'],key=lambda x:float(x.get('removed_target_decimal') or 0),reverse=True)[:20],1):
        address=row['address'].lower();cum=[];total=0
        for d in days:
            total+=daily[address].get(d.date(),0);cum.append(total)
        top.append({'rank':rank,'address':address,'label':address[:8]+'…'+address[-4:],'upeg':row['removed_target_decimal'],'usd':row.get('removed_usd'),'events':row['num_withdrawals'],'versions':row.get('versions',[]),'cum':cum})
    result={'days':[d.isoformat() for d in days],'price':[prices.get(d.date()) for d in days],'top':top,'ranking_basis':'gross target-token removals; addresses are event actors, not verified beneficial owners','source':'current liquidity_events.json and tvl_timeline.json'}
    write(out/'notebook_cache'/'top20-withdrawals.json',result)
    return result

def main():
    from src.models import VerifiedPool,to_dict
    from src.analysis.metrics import calculate_withdrawal_severity,from_block_tvl_by_pool,calculate_volume_metrics,calculate_wallet_activity
    from src.analysis.labels import analyze_labels
    from src.analysis.timeline import analyze_timeline
    from src.analysis.risk import compute_risk
    from src.report.generator import generate_report
    from src.analysis.dashboard import generate_dashboard
    from src.data.artifacts import combine_event_tables
    status=read(OUT/'tail_refresh_20260910/status.json');assert status['phase']=='merged'
    meta=read(OUT/'token_profile.json');poolrows=read(OUT/'verified_pools.json');pools=[VerifiedPool(**p) for p in poolrows]
    swaps=read(OUT/'swaps.json');liquidity=read(OUT/'liquidity_events.json');transfers=read(OUT/'transfers.json')
    positions=read(OUT/'positions.json');assert not positions,'Existing positions need typed conversion before rebuilding'
    all_events=combine_event_tables(swaps,liquidity,transfers,read(OUT/'position_events.json'))
    metrics=read(OUT/'metrics.json');snapshots=read(OUT/'tvl_timeline.json')
    metrics['withdrawal_severity']=calculate_withdrawal_severity(liquidity,int(metrics['pool_concentration'].get('total_tvl',0)),0,verified_pools=pools,target_token=meta['address'],token_decimals=18,tvl_by_pool=from_block_tvl_by_pool(snapshots,status['from_block']),timeline=snapshots)
    volume=calculate_volume_metrics(swaps,pools,meta['address'],18,bucket_seconds=86400)
    volume.update(chart_span='month',bucket='day',source='local_swaps_with_rpc_tail_verification')
    metrics['volume']=volume
    metrics['wallet_activity']=calculate_wallet_activity(swaps,pools,meta['address'],18,timeline=snapshots)
    metrics['tail_refresh']=status
    write(OUT/'metrics.json',metrics);write(OUT/'volume_timeline.json',volume['volume_timeline'])
    labels=analyze_labels(meta['address'],pools,[],swaps,liquidity,transfers,output_dir=OUT)
    timeline=analyze_timeline(all_events,swaps,liquidity,transfers,pools,meta['address'],from_block=status['from_block'],to_block=status['to_block'],output_dir=OUT)
    risk=compute_risk(metrics['pool_concentration'],metrics['lp_concentration'],metrics['withdrawal_severity'],snapshots,[to_dict(x) for x in labels],migration=timeline.get('liquidity_migration'),output_dir=OUT)
    risk['coverage_note']='Provisional: cached May coverage is not revalidated; LP identity incomplete; V4 tail principal amounts estimated from prior pool price. Holdings snapshots were retained.'
    write(OUT/'risk_assessment.json',risk)
    generate_report(meta,poolrows,swaps,liquidity,transfers,[],[to_dict(x) for x in labels],metrics,timeline,risk,output_dir=OUT)
    with (OUT/'report.md').open('a') as f:f.write('\n\n## Partial refresh coverage\n\n'+status['scope']+'\n\n'+risk['coverage_note']+'\n')
    plot=build_withdrawal_plot_data(OUT)
    generate_dashboard(output_dir=OUT)
    print('Views rebuilt',status['counts'],'plot addresses',len(plot['top']),flush=True)

if __name__=='__main__':main()
