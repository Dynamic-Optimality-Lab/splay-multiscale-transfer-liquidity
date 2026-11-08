"""ONE distinct-implementation BF query for the targeted transient helper.
Saved A facts and arithmetic are reused without another A/BE execution.
"""
import importlib.util,json,sys,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2])
s=importlib.util.spec_from_file_location('FR32_mutable_check',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I)
def tick():
    if I.queries>=min(QCAP,1):raise TimeoutError('FR32 last original-source query')
    I.queries+=1
I.tick=tick
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    p=B/'transient13_source_control.json';v=json.loads(p.read_text());t=I.Tree(v['before_BF']);pa,ev=t.access(13)
    assert pa==v['BF_path'] and ev==v['BF_events'] and t.shape()==I.fr(v['after_BF'])
    parent,ch=I.marked(I.fr(v['before_BF']),I.M);_,after=I.marked(t.shape(),I.M)
    E=lambda c:sum(max(len(v)-2,0) for v in c.values())
    assert E(ch)==1 and E(after)==0 and len(ev)==2
    sig=2*v['A_cost']-len(ev)+E(after)-E(ch);assert sig==-1
    assert I.core(t.shape(),I.M)==set(range(1,14)) and I.queries==1
    out('transient13_independent_audit.json',{'status':'PASS_DISTINCT_BF_AND_TRANSIENT_DEBT_ARITHMETIC','new_source_queries':1,
        'BF_path':pa,'A_H_reused':1,'BF_Q':len(ev),'E_before':1,'E_after':0,'sigma':sig,'intermediate_debt':2,
        'terminal_counterexample':False,'A_reexecuted':False,'BE_reexecuted':False,'complete_closing_loop_replayed':False,
        'trust':'distinct mutable implementation operated by SAME research agent; not external/formal audit',
        'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    print(json.dumps({'status':'DISTINCT_TRANSIENT_HELPER_PASS','queries':1,'terminal_counterexample':False}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
