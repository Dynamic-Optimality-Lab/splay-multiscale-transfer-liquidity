"""Independent all-constraint and actual physical-comparison audit.
Pair LOW is checked by fresh relational composition, not producer groups.
Accepted original source rows/events are reused without semantic replay.
"""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return None if t is None else (t[0],tup(t[1]),tup(t[2]))
def main():
    a=read(F/'branch_H1_r7.json');h2=read(F/'branch_H2_r7.json');bm=read(F/'active_a10_model.json');bg=read(F/'maximal_B_grammar.json')
    parts=[read(F/f'independent_H2_checked_{i:02d}.json') for i in (1,2,3)]
    assert [p['checked_source_A_interval'] for p in parts]==[[0,1100],[1100,5100],[5100,5947]]
    assert parts[-1]['status']=='PASS_COMPLETE_H1_H2_SOURCE_COVER' and parts[-1]['H1_checked']==12400 and parts[-1]['H2_checked']==64654
    for part in parts:
        for p,h in part['input_sha256'].items():assert sha(F/p)==h
    with (F/'paired_branch_search_01.pkl').open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE_CANDIDATE' and not z['pending'] and z['cycle'] is None
    assert z['model_sha256']==sha(F/'paired_branch_model.pkl')
    classes=[np.flatnonzero(np.array(a['A_roots'])==g) for g in range(7)]
    for b in range(3876):
        floor=z['floors'][b];row=z['rows'][b];g=(bm['B_roots'][b]-1)//2
        assert all(a['A_roots'][aa]==g and v>floor for aa,v in row.items())
    assert sum(map(len,z['rows']))+5947+3876<2000000
    def level(b,aa):
        return np.array([z['rows'][b].get(int(v),z['floors'][b]) for v in aa],dtype=np.int32)
    def maxlevel(b):return max(z['floors'][b],max(z['rows'][b].values(),default=0))
    base={}
    for h,rows in ((1,a['H1_rows']),(2,h2['H2_rows'])):
        for g in range(7):
            for x in range(7):
                chosen=[(s,t) for s,k,t in rows if a['A_roots'][s]==g and k==x]
                base[h,g,x]=(np.array([v[0] for v in chosen],dtype=np.int64),np.array([v[1] for v in chosen],dtype=np.int64))
    outgoing=[[] for _ in range(3876)]
    for eid,e in enumerate(bm['B_edges']):outgoing[e['source']].append((eid,e))
    checks=high=sectors=six=0
    for e in bm['B_edges']:
        b,bt,q=e['source'],e['target'],e['q'];g=(bm['B_roots'][b]-1)//2;x=(e['key']-1)//2
        if q!=6:
            for h in (1,2):
                src,dst=base[h,g,x];margin=2*h-q+level(bt,dst)-level(b,src)
                assert margin.min(initial=0)>=0;checks+=len(src)
            assert 6-q+z['floors'][bt]-maxlevel(b)>=0;high+=1
            continue
        six+=1
        for eid2,e2 in outgoing[bt]:
            assert e2['q']==1;end=e2['target'];y=(e2['key']-1)//2;sectors+=1
            for ha,hb in ((1,1),(1,2),(2,1)):
                src,mid=base[ha,g,x];mm,dd=base[hb,x,y]
                best=np.full(5947,-1000000,dtype=np.int32);np.maximum.at(best,mid,level(b,src))
                valid=best[mm]>-1000000;margin=2*(ha+hb)-7+level(end,dd[valid])-best[mm[valid]]
                assert margin.min(initial=0)>=0;checks+=int(valid.sum())
            assert 1+z['floors'][end]-maxlevel(b)>=0;high+=1
    assert six==64 and sectors==126
    K=max(maxlevel(b) for b in range(3876));assert K==4 and K+8==12<=25
    # New comparison on already independently replayed real source I66..130.
    sourcepath=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'
    assert sha(sourcepath)=='5e00eb81aed692ab9982b5b4e3401e89827245a52748cf770ac21fa26d00e4b4'
    source=read(sourcepath);rows=source['period_rows'];by={r['t']:r for r in rows};M=sorted({r['key'] for r in rows if r['genuine_F']});assert len(M)==7
    ai={tup(t):i for i,t in enumerate(a['A_branch_trees'])};bi={tup(t):i for i,t in enumerate(bg['trees'])}
    def project(t):
        if t is None:return None
        v=t[0];l,r=project(t[1]),project(t[2])
        if v in M:return (1000*(M.index(v)+1),l,r)
        if l is None:return r
        if r is None:return l
        return (1000*sum(k<v for k in M)+500,l,r)
    def debt(A,BF):
        aa=ai[project(A)];bb=bi[tup(BF)];return z['rows'][bb].get(aa,z['floors'][bb])
    mm=source['funding']['macros'];n=len(mm);consumed={(i+1)%n for i,m in enumerate(mm) if m['Q']==6};packets=[]
    for i in range(n):
        if i in consumed:continue
        ix=[i,(i+1)%n] if mm[i]['Q']==6 else [i]
        if len(ix)==2:assert mm[ix[1]]['Q']==1
        times=sum([mm[j]['rows_t'] for j in ix],[]);rr=[by[t] for t in times];H=sum(r['a'] for r in rr);Q=sum(r['qF'] for r in rr)
        units=[(r['t'],j,b) for r in rr for j in range(1,r['a']+1) for b in (0,1)];demands=[(r['t'],k) for r in rr for k in range(1,r['qF']+1)]
        ds=debt(rr[0]['A_before'],rr[0]['BF_before']);dt=debt(rr[-1]['A_after'],rr[-1]['BF_after']);assert 2*min(H,4)-Q+dt-ds>=0
        packets.append({'macro_indices':ix,'times':times,'H':H,'Q':Q,'units':units,'demands':demands,'D_source':ds,'D_target':dt})
    h0={tuple(p['demand']):tuple(p['unit']) for p in source['funding']['h0']};h=dict(h0)
    top=max(p['D_source'] for p in packets);cut=next(i for i,p in enumerate(packets) if p['D_source']==top);bank=[];receipt=[];peak=0
    for k in range(len(packets)):
        p=packets[(cut+k)%len(packets)];assert len(bank)==top-p['D_source']
        owned={h0[d] for d in p['demands'] if d in h0};budget=2*min(p['H'],4);assert len(owned)<=budget
        spare=[u for u in p['units'] if u not in owned][:budget-len(owned)];assert len(owned)+len(spare)==budget
        pool=spare+bank;missing=[d for d in p['demands'] if d not in h0];peak=max(peak,len(owned)+len(spare)+len(bank))
        assert len(pool)>=len(missing)+top-p['D_target'];additions=[]
        for d in missing:u=pool.pop(0);h[d]=u;additions.append({'demand':d,'unit':u})
        bank=pool[:top-p['D_target']];receipt.append({'macro_indices':p['macro_indices'],'H':p['H'],'Q':p['Q'],
          'D_source':p['D_source'],'D_target':p['D_target'],'old_own_units':sorted(owned),'selected_spares':spare,'new_pairs':additions,'carry':bank[:]})
    assert not bank and peak<=12
    D={(r['t'],k) for r in rows for k in range(1,r['qF']+1)};U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U and all(h[d]==u for d,u in h0.items())
    assert collections.Counter(t for p in packets for t in p['times'])==collections.Counter(by.keys())
    actual={'status':'PASS_NEW_INDEPENDENT_COMPARISON_ONLY','period':source['period'],'actual_A_units':len(U),'full_demands':len(D),'natural_owners_preserved':len(h0),
      'working_peak':peak,'internal_max_D_cut':cut,'source_rows_replayed':False,'old_primitives_reused':True,
      'historical_full_owner_map_modified':False,'full_comparison':[{'demand':d,'unit':u} for d,u in sorted(h.items())],'packets':receipt,'source_sha256':sha(sourcepath)}
    with (F/'new_paired_branch_physical_comparison.json').open('x',encoding='utf-8') as f:json.dump(actual,f,indent=2)
    report={'status':'PASS_ALL_A_SEVEN_KEY_MAXIMAL_CORE_CERTIFICATE','A_branch_states':5947,'B_states':3876,'H1_rows':12400,'H2_rows':64654,
      'q6_actions':six,'actual_q6_q1_sectors':sectors,'LOW_numeric_inequalities':checks,'HIGH_endpoint_constraints':high,'D_width':K,'Bank25_working_bound':12,
      'actual_control_demands':len(D),'actual_control_natural_owners_preserved':len(h0),'actual_control_working_peak':peak,
      'source_queries':0,'source_engine_calls':0,'source_scope':'all original paired-closed seven-genuine-key full B maximal-core13 histories, arbitrary A unary/private populations and helpers',
      'other_seven_key_B_cores':'OPEN','all_support_JR35':'OPEN','reservation_compatibility':'DEFERRED_UNCHANGED',
      'trust':'independent full LOW2 source regeneration, independent all-constraint composition, and new physical comparison on accepted source rows; same agent, not external/formal review',
      'input_sha256':{p:sha(F/p) for p in ('branch_H1_r7.json','branch_H2_r7.json','paired_branch_search_01.pkl','independent_H2_checked_03.json','new_paired_branch_physical_comparison.json')}}
    with (F/'independent_paired_branch_certificate.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify110_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
