"""Resolve the failed first-root-return falsifier at the original source.
One candidate transition and six exact marked search paths; not a new family
enumeration. Core loss excludes this transition from the closed core13 domain.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=min(9,int(sys.argv[2]))
sp=importlib.util.spec_from_file_location('C30_source5_engine',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('nine-query source-exclusion control')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t
def main():
    r=json.loads((B/'nonextremal_source_countercertificate.json').read_text());c=next(z for z in r['rows'] if z['occurrence']==119);s=fr(c['after'])
    rr,end=C.replay(*s,[('K',7)]);z=rr[0];z['occurrence']=120
    before=C.p.labels(C.p.core(s[1],C.M));after=C.p.labels(C.p.core(end[1],C.M));assert after<before
    paths=[]
    for x in sorted(C.M-{5}):
        pa=C.path(s[1],x);ss=len(pa)%2==0 and all(pa[i:i+2] in ('LL','RR') for i in range(0,len(pa),2))
        paths.append({'target':x,'path':pa,'SS_necessary_condition':ss})
    assert [v['target'] for v in paths if v['SS_necessary_condition']]==[1,3,11,13]
    out('first_root_return_source_exclusion.json',{'status':'SOURCE_EXCLUSION_NOT_A_COUNTEREXAMPLE_TO_FIRST_RETURN_REPAYMENT',
        'candidate_transition':z,'full_marked_core_before':sorted(before),'full_marked_core_after':sorted(after),'lost_labels':sorted(before-after),
        'all_other_marked_paths':paths,'permitted_immediate_SS_targets':[1,3,11,13],
        'closed_domain_exclusion':'fixed-mark ancestor core cannot grow under marked full-B accesses; strict loss cannot return to the same full tree',
        'population_scope':'this exact B anchor configuration plus arbitrary ordered external-gap substitution and reflection',
        'first_return_signed_theorem':'OPEN; the immediate low-cost return was invalid, not a refutation',
        'source_queries':C.queries})
    print(json.dumps({'status':'FIRST_RETURN_FALSIFIER_EXCLUDED','queries':C.queries,'B_path':z['BF_path'],'A_events':z['a'],
        'QF':z['qF'],'lost_core_labels':sorted(before-after),'necessary_next_targets':[1,3,11,13]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source5_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
