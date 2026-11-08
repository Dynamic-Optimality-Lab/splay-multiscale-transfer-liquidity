"""Exact signed forward recovery, original physical units, and cut templates.
No source replay; no source queries. Symbolic lifting is a written induction.
"""
import json,time,sys
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def unpack(z):return {tuple(v['demand']):tuple(v['unit']) for v in z}
def pack(z):return [{'demand':d,'unit':u} for d,u in sorted(z.items())]
def peak(a):
    es=[]
    for d,u in a.items():es += [((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)]
    live=set();ans=0
    for _,d in sorted(es):
        if d in live:live.remove(d)
        else:live.add(d);ans=max(ans,len(live))
    assert not live;return ans
def main():
    r=json.loads((B/'nonextremal_source_countercertificate.json').read_text());g=json.loads((B/'source_signed_and_seed_analysis.json').read_text());mm=g['macros'];tag=r['tags'];N=len(r['period'])
    h0={d:tuple(u) for m in mm for d,u in zip(map(tuple,m['demands']),m['units'])};D={tuple(d) for m in mm for d in m['demands']}
    ci=next(i for i,m in enumerate(mm) if tag['comb'] in m['occurrences']);ri=ci+1;recovery=mm[ri];assert recovery['H']==recovery['Q']==1 and recovery['target']==11
    missing=D-set(h0);assert missing=={(tag['comb'],3)}
    H=dict(h0);H[next(iter(missing))]=tuple(recovery['units'][1]);assert len(set(H.values()))==len(H)==66
    pp=[z['macros'] for z in g['simple_forward_packet_receipts']];assert all(z['sigma_E']>=0 for z in g['simple_forward_packet_receipts'])
    # Maximum E construction of an independent raw comparison includes ALL
    # fixed natural values. This is not the supplied smaller-support receipt.
    debts=[(mm[z[0]]['E_before'],mm[z[-1]]['E_after']) for z in pp];K=max(ds for ds,dt in debts);cut=next(i for i,(ds,dt) in enumerate(debts) if ds==K)
    bank=[];result=dict(h0);working=0;records=[]
    for step in range(len(pp)):
        k=(cut+step)%len(pp);ids=pp[k];ds,dt=debts[k];assert len(bank)==K-ds
        units=[tuple(u) for i in ids for u in mm[i]['units'][:2*min(mm[i]['H'],3)]];dd=[tuple(d) for i in ids for d in mm[i]['demands']]
        own={h0[d] for d in dd if d in h0};pool=[u for u in units if u not in own]+bank;working=max(working,len(pool)+len(own));added=[]
        for d in dd:
            if d not in h0:u=pool.pop(0);result[d]=u;added.append((d,u))
        assert len(pool)>=K-dt;bank=pool[:K-dt];records.append({'packet':k,'macros':ids,'E_before':ds,'E_after':dt,'selected_units':units,'pairs':added,'carry':bank[:]})
    assert not bank and result==H and working<=12
    # Align returning blocks immediately after the last genuine full KEEP.
    # The old period's final DELETE tail then occurs first, not after a
    # symbolic seam. All native owners and the new forward seed are local.
    last=mm[-1]['occurrences'][-1];cut_ops=last-r['actual_interval'][0]+1
    def tau(t):return t+N if t<=last else t
    HU={tuple([tau(d[0]),*d[1:]]):tuple([tau(u[0]),*u[1:]]) for d,u in H.items()}
    lo=last+1;hi=last+N
    assert all(lo<=d[0]<=hi and lo<=u[0]<=hi for d,u in HU.items())
    B0=peak(HU);cuts=[]
    for c in range(N):
        start=lo+c
        def tt(t):return t+N if t<start else t
        hx={tuple([tt(d[0]),*d[1:]]):tuple([tt(u[0]),*u[1:]]) for d,u in HU.items()};cuts.append(peak(hx))
    assert B0<=4 and max(cuts)<=2*B0
    current_triple=[next(m for m in mm if tag[k] in m['occurrences']) for k in ('j','helper','comb')]
    forward=next(z for z in g['simple_forward_packet_receipts'] if ci in z['macros']);assert len(forward['macros'])==4 and forward['sigma_E']==0
    # Actual high-arity degrees, not an invented free parameter.
    high=[]
    for i,m in enumerate(mm):
        if m['sigma_E']>=0:continue
        ch=m['marked_before'];pa={v:int(k) for k,vs in ch.items() for v in vs};a=pa.get(m['target']);degrees=[]
        while a is not None:
            if len(ch[str(a)])>=3:degrees.append((a,len(ch[str(a)])))
            a=pa.get(a)
        assert len(degrees)==1;high.append({'macro':i,'end':m['occurrences'][-1],'high_ancestors':degrees,'sigma_E':m['sigma_E']})
    out('forward_recovery_and_period_receipt.json',{'status':'EXACT_FORWARD_RECOVERY_TEMPLATE_PENDING_DISTINCT_AUDIT','full_H_forward':pack(H),'full_H_aligned':pack(HU),
        'original_h0':pack(h0),'forward_seed':H[(tag['comb'],3)],'signed_packets':pp,'bank_receipts':records,'raw_E_max':K,'processing_cut_packet':cut,
        'raw_working':working,'H_original_profile':peak(H),'aligned_profile':B0,'all85_single_word_cut_profiles':cuts,
        'all_m_all_cut_bound':2*B0,'normalized_owner_profile_sufficient':(25-2*B0)//2,
        'aligned_source_interval':[lo,hi],'aligned_cut_ops':cut_ops,'aligned_reaching_prefix':r['reaching_prefix']+r['period'][:cut_ops],
        'aligned_word':r['period'][cut_ops:]+r['period'][:cut_ops],'aligned_initial':next(z for z in r['rows'] if z['occurrence']==last)['after'],
        'negative_high_arity_helpers':high,'helper_only_sum_per_word':sum(z['sigma_E'] for z in high),
        'sigma_E_sum_per_word':sum(m['sigma_E'] for m in mm),'principal_NH30_closed':False,
        'owner_scope':'Given actual supplied normalized a, fixed values stay literal; exact block/transport eligibility and B_a bound remain hypotheses; raw f6 is not substituted'})
    print(json.dumps({'status':'FORWARD_RECOVERY_AND_CUTS','forward_packet':forward,'raw_E_max':K,'raw_working':working,'H_profile':B0,'all_cut_bound':2*B0,
        'helper_degrees':high,'sum_sigma_E':sum(m['sigma_E'] for m in mm),'helper_only_sum':sum(z['sigma_E'] for z in high)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
