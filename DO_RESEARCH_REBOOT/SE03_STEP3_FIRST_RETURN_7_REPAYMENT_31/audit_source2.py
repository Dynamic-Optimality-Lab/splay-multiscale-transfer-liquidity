"""Eight original tuple-source queries checking the revised legal suffix.
The full new mutable prefix is reused; no old completed source rerun.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2])
sp=importlib.util.spec_from_file_location('FR31_tuple_suffix',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('FR31 suffix cap')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t
def main():
    d=json.loads((B/'prefix_candidate_rows.json').read_text());expected=[z for z in d['rows'] if z['occurrence']>=128]
    rows,end=C.replay(*fr(expected[0]['before']),[('K',5),('K',7),('K',11)])
    for z in rows:z['occurrence']+=127
    assert rows==[dict(z,before=fr(z['before']),after=fr(z['after'])) for z in expected]
    assert C.queries==8
    assert all(C.p.labels(C.p.core(z['after'][1],C.M))==set(range(1,14)) for z in rows)
    assert [z['a'] for z in rows]==[1,1,1] and [z['qF'] for z in rows]==[1,2,2]
    out('tuple_suffix_check.json',{'status':'PASS_SECOND_SOURCE_IMPLEMENTATION_REVISED_SUFFIX','rows':rows,'source_queries':8,
        'scope':'KEEP5,KEEP7,KEEP11 after the checked activation of9; not a full second replay of the closed completion'})
    print(json.dumps({'status':'REVISED_SUFFIX_MATCHES','queries':8,'return7_B_path':rows[1]['BF_path'],'all_core13':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
