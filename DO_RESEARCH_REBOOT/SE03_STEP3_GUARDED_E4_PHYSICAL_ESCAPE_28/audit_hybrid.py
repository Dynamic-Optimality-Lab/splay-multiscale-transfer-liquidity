"""Repair the refuted catchment forcing by absorbing branch-free closed B
blocks using an independent within-block leaf-channel comparison.
No source replay; the new exact459-operation source receipt is reused.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C28_hybrid_source',OLD/'audit_construct.py')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(z) for z in t) if isinstance(t,list) else t
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def peak(h):
    ee=[]
    for d,u in h.items():ee.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    live=set();ans=0
    for t,d in sorted(ee):
        if d in live:live.remove(d)
        else:live.add(d);ans=max(ans,len(live))
    assert not live;return ans
def main():
    c=json.loads((B/'catchment_forcing_countercertificate.json').read_text());rows=[dict(r,before=fr(r['before']),after=fr(r['after'])) for r in c['rows']]
    blocks=[];H={};size=(len(rows)-199)//4;assert size==65
    for i in range(4):
        rr=rows[i*size:(i+1)*size];assert rr[0]['before'][1:]==rr[-1]['after'][1:]
        v=C.L.build(rr,C.M);assert not v['R'] and set(v['h'])==v['D'];h=v['h']
        active={ch['marked_key'] for ch in v['channels']};beta=max(len(m['branch']) for m in v['macros'])
        assert len(active)<=4 and beta<=2 and peak(h)<=2*len(active)+beta<=10
        H.update(h);blocks.append({'kind':'L','interval':[rr[0]['occurrence'],rr[-1]['occurrence']],
            'B_exact_return':True,'A_exact_return_required':False,'leaf_active_keys':sorted(active),'beta_max':beta,
            'branch_holes':[],'H_cut_peak':peak(h),'source_comparison':pack(h),'channels':v['channels']})
    rr=rows[4*size:];mm=C.L.macros(rr);tags=c['tags'];own={d:u for m in mm for d,u in zip(m['demands'],m['units'])};D={d for m in mm for d in m['demands']}
    frame={k:next(m for m in mm if m['occurrences'][-1]==tags[k]) for k in ('j','h','g','s','t','v','p','e')};fd={d for m in frame.values() for d in m['demands']};outside=sorted((D-set(own))-fd)
    assert len(outside)<=3;h=dict(own)
    critical=[(tags['s'],3)]+[(tags['e'],k) for k in range(3,7)]
    h.update(zip(critical,frame['j']['units'][1:6]));h.update(zip(outside,[frame[k]['units'][1] for k in ('g','t','p')]))
    assert set(h)==D and len(set(h.values()))==len(D) and peak(h)<=10
    H.update(h);blocks.append({'kind':'F','interval':[rr[0]['occurrence'],rr[-1]['occurrence']],
        'outside_native_deficits':outside,'H_cut_peak':peak(h),'source_comparison':pack(h)})
    fullD={(r['occurrence'],k) for r in rows for k in range(1,r['qF']+1)};assert set(H)==fullD and len(set(H.values()))==len(fullD)
    prior=mp(c['prior_before_extra']);inv={u:d for d,u in prior.items()};answer=dict(prior);paths=[]
    for p in sorted(fullD-set(prior)):
        d=p;chain=[];seen=set()
        while True:
            assert d not in seen;seen.add(d);u=H[d];chain.append((d,u))
            if u not in inv:break
            d=inv[u]
        answer[p]=u;paths.append({'root':p,'steps':chain,'terminal':u})
    assert set(answer)==fullD and len(set(answer.values()))==len(fullD) and all(answer[d]==u for d,u in prior.items())
    assert peak(H)<=10 and peak(prior)<=7 and peak(answer)<=25
    out('hybrid_partition_receipt.json',{'status':'EXPLICIT_HYBRID_SOURCE_COMPARISON_REPAIRS_CANDIDATE_COUNTEREXAMPLE_NOT_GLOBAL_COVERAGE',
        'source_id':c['source_id'],'blocks':blocks,'H':pack(H),'H_cut_peak':peak(H),'frozen_historical_prefix':pack(prior),
        'comparison_extension_of_historical_prefix':pack(answer),'owner_walks':paths,'extended_peak':peak(answer),
        'current_complete_a_unchanged':True,'universal_all_source_partition_proved':False})
    print(json.dumps({'status':'HYBRID_PARTITION_REPAIR','kinds':[b['kind'] for b in blocks],
        'L_parameters':[(b.get('leaf_active_keys'),b.get('beta_max'),b['H_cut_peak']) for b in blocks if b['kind']=='L'],
        'H_peak':peak(H),'extension_peak':peak(answer),'unresolved':'source forcing of an admissible hybrid partition'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_hybrid_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
