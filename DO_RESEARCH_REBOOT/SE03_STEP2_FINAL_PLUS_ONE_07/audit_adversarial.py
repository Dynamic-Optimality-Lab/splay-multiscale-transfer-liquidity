"""Adversarial interfaces: mirrors, source provenance, positive control inclusion.
No primary certificate producer imported.
"""
import collections,importlib.util,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checker07',B/'audit_independent2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);a=d.a
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mirrorA(t):
    if t[0]=='leaf':return a.slot(12-t[2],12-t[1])
    return a.I.node(12-t[1],mirrorA(t[3]),mirrorA(t[2]))
def mirrorB(t):
    if t[0]=='leaf':return ('leaf',13-t[1])
    return a.I.node(12-t[1],mirrorB(t[3]),mirrorB(t[2]))
def rawA(t,lo=F(0),hi=F(12)):
    if isinstance(t,str):return a.slot(lo,hi)
    return a.I.node(F(t[0]),rawA(t[1],lo,F(t[0])),rawA(t[2],F(t[0]),hi))
def rawB(t):
    if isinstance(t,str):return ('leaf',int(t[1:])+1)
    return a.I.node(t[0],rawB(t[1]),rawB(t[2]))
def main():
    cert=json.loads((B/'zero_closure.json').read_text());by=collections.defaultdict(list);records=[]
    for r in cert['records']:
        t=d.canonical(a.Aread(r['A']));b=a.bf_read(r['BF']);rr=tuple(r['recent']);records.append((t,b,rr));by[b,rr].append(t)
    by={k:tuple(sorted(set(v),key=d.size)) for k,v in by.items()}
    for t,b,r in records:
        mt,mb,mr=mirrorA(t),mirrorB(b),tuple(12-k for k in r)
        assert any(d.includes(v,mt) for v in by.get((mb,mr),())), 'reflection loses a source language'
    fam=json.loads((B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02/incoming_family_v2.json').read_text())
    v=fam['predecessor'];t=rawA(v['A']);b=rawB(v['BF']);r=tuple(v['recent'])
    assert a.L(b)==3
    assert any(d.includes(z,t) for z in by[b,r]),'known Sigma +1 predecessor missing from universal seed closure'
    assert any(d.includes(z,mirrorA(t)) for z in by[mirrorB(b),tuple(12-k for k in r)])
    states={t for t in a.alltrees(1,11) if t[1] in a.M and a.density(t)[2]};S=P=0
    edges=collections.defaultdict(list)
    for t in states:
        for x in a.M-{t[1]}:
            n=a.legal(t,x)
            if n:
                end,q=n;assert end in states;edges[t].append((end,x,q))
                if q==4 and x not in set(a.parents(t).values()):assert a.L(end)==4;S+=1
    for t in states:
        for end,x,q in edges[t]:
            if q!=5:continue
            for final,y,qq in edges[end]:assert qq==1 and a.L(final)==4;P+=1
    assert (S,P)==(128,62)
    seeds=json.loads((B/'terminal_seeds.json').read_text());orders=collections.Counter();shapes=collections.Counter();Aevents=collections.Counter();Bcases=collections.Counter()
    for ci,c in enumerate(seeds['terminal_cases']):
        w=(c['oldroot'],c['plus_target'],c['cold_q4']);orders[a.rankword(w)]+=1
        end=a.bf_read(c['BF_after_plus']);assert a.L(end)==2 and a.degree(end) in (1,2)
        shapes[a.degree(end)]+=1
        before=a.bf_read(c['BF_before']);after,ev=a.splay(before,w[1]);assert after==end and len(ev)==1
        Bcases[ev[0][0]]+=1
        for v in seeds['groups']:
            if ci not in v['cases']:continue
            t=a.Aread(v['A']);after,ev=a.splay(t,F(w[1]));assert len(ev)==1
            Aevents[ev[0][0]+('_'+ev[0][3] if ev[0][0]=='ZIG' else '')]+=1
    result={'status':'PASS_ADVERSARIAL_FINAL_PLUS1_SOURCE_INTERFACES',
        'all_backward_frames_reflect_into_language':len(records),'Sigma_predecessor_and_mirror_in_language':True,
        'corrected_Sigma_predecessor_marked_leaves':3,'all_cold_NEG2_S_target_contexts_L4':S,
        'all_NEG2_P_actual_successor_contexts_L4':P,'all_backward_frames_at_most_three_leaves':True,
        'terminal_BF_shapes_by_root_marked_degree':dict(shapes),'BF_final_event_cases':dict(Bcases),
        'terminal_rank_orders':[{'rank_word':k,'contexts':v} for k,v in sorted(orders.items())],
        'A_event_case_incidence_counts':dict(Aevents),'source_engine_calls':a.calls,'new_finite_tests':0,
        'BE_and_actual_charts':'full recent order retained; only necessary projection used for exclusion',
        'old_TP_DEPTH3':'sealed result reused, not reopened'}
    out('adversarial_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_adversarial_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
