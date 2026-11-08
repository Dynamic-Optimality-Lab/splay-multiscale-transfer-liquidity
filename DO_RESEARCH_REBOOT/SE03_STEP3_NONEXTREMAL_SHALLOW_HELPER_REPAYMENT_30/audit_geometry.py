"""Static signed/physical analysis of saved original source rows. No replay,
tree operation or compiler/root query. All arithmetic is explicitly stored.
"""
import json,time,sys
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(a):return [{'demand':d,'unit':u} for d,u in sorted(a.items())]
def profile(a):
    es=[]
    for d,u in a.items():es += [((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)]
    live=set();peak=0
    for t,d in sorted(es):
        if d in live:live.remove(d)
        else:live.add(d);peak=max(peak,len(live))
    assert not live;return peak
def main():
    r=json.loads((B/'nonextremal_source_countercertificate.json').read_text());rows=r['rows'];al=r['macro_ledger'];mm=[]
    for z in al:
        rr=[next(v for v in rows if v['occurrence']==t) for t in z['occurrences']]
        units=[(v['occurrence'],j,b) for v in rr for j in range(1,v['a']+1) for b in (0,1)];dd=[(v['occurrence'],k) for v in rr for k in range(1,v['qF']+1)]
        mm.append(dict(z,units=units,demands=dd))
    h={d:u for m in mm for d,u in zip(m['demands'],m['units'])};D={d for m in mm for d in m['demands']};missing=sorted(D-set(h))
    prep=next(m for m in mm if r['tags']['preparation_end'] in m['occurrences']);spares=[u for u in prep['units'] if u not in h.values()]
    assert len(spares)>=len(missing);H=dict(h);H.update(zip(missing,spares))
    assert set(H)==D and len(set(H.values()))==len(H)
    # Small exact signed partition by accumulating actual adjacent macros.
    # Cut starts at this SOURCE boundary; no maximal-debt seam is assumed.
    packets=[];pending=[];balance=0
    for i,m in enumerate(mm):
        pending.append(i);balance+=m['sigma_E']
        if balance>=0:packets.append(pending);pending=[];balance=0
    if pending:
        assert packets;packets[-1]+=pending
    receipts=[]
    for ids in packets:
        sigma=sum(mm[i]['sigma_E'] for i in ids);units=sum(2*min(mm[i]['H'],3) for i in ids)
        receipts.append({'macros':ids,'sigma_E':sigma,'selected_units':units,'H':sum(mm[i]['H'] for i in ids),'Q':sum(mm[i]['Q'] for i in ids)})
    out('source_signed_and_seed_analysis.json',{'status':'STATIC_EXACT_SOURCE_ANALYSIS','macros':mm,'native_missing':missing,'seed_macro_occurrences':prep['occurrences'],
        'seed_H':prep['H'],'native_seed_spares':[u for u in spares[:len(missing)]],'full_H_seed':mp(H),'H_seed_profile':profile(H),
        'simple_forward_packet_receipts':receipts,'forward_partition_all_nonnegative':all(z['sigma_E']>=0 for z in receipts),
        'max_forward_packet_units':max(z['selected_units'] for z in receipts),'sum_rho':sum(z['rho'] for z in mm),'sum_sigma_E':sum(z['sigma_E'] for z in mm),
        'negative_sigma_E_macros':[i for i,m in enumerate(mm) if m['sigma_E']<0],
        'principal_NH30_closed':False,'source_queries':0})
    print(json.dumps({'status':'SOURCE_STATIC_ANALYSIS','macros':len(mm),'native_holes':len(missing),'seed_H':prep['H'],'H_peak':profile(H),
        'negative_indices':[i for i,m in enumerate(mm) if m['sigma_E']<0],'sum_sigma_E':sum(z['sigma_E'] for z in mm),'packets':receipts}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_geometry_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
