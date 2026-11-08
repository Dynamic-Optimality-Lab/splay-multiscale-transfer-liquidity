"""Precisely TWO original-source queries: A and BF KEEP13 from saved after9.
No erased operation is hidden: its exact state is left as S_13(BE), not
numerically evaluated. No whole word/source search/compiler runs here.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2])
s=importlib.util.spec_from_file_location('FR32_exact_source',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
def path(t,x):
    if C.queries>=min(QCAP,2):raise TimeoutError('FR32 TWO-query target budget')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def fr(t):return tuple(fr(x) for x in t) if isinstance(t,list) else t
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    old=json.loads((P/'SE03_STEP3_FIRST_RETURN_7_REPAYMENT_31/prefix_first_return_countercertificate_v2.json').read_text())
    z=next(r for r in old['new_rows'] if r['occurrence']==127);A,F,E=fr(z['after'])
    A1,pa,ae=C.tr(A,13);F1,pf,fe=C.tr(F,13)
    assert pa=='RR' and pf=='RRRR' and len(ae)==1 and len(fe)==2
    assert all(v['kind']=='DOUBLE' and v['case']=='RR' and v['G'] in C.M and v['P'] not in C.M for v in fe)
    assert C.p.labels(C.p.core(F1,C.M))==set(range(1,14))
    assert C.queries==2
    out('transient13_source_control.json',{'status':'PASS_EXACT_TRANSIENT_DEBT_TWO_OPERATION','source_queries':2,
        'source_before_short_occurrence':128,'target':13,'mode':'K','before_A':A,'before_BF':F,'short_BE_before':E,
        'A_path':pa,'A_events':ae,'A_cost':1,'BF_path':pf,'BF_events':fe,'QF':2,'after_A':A1,'after_BF':F1,
        'BE_after':{'ordinary_splay':13,'input':'short_BE_before'},'BE_after_evaluated':False,
        'inherited_sigma_through9':-1,'new_E_before':1,'new_E_after':0,'new_sigma':-1,'intermediate_total_sigma':-2,
        'is_first_return7':False,'is_FR32_counterexample':False,
        'scope':'new actual A/BF access from accepted reachable after9; erased state is an exact unevaluated original operation; closure supplied by written inverse loop'})
    print(json.dumps({'status':'TRANSIENT13_PASS','H':1,'Q':2,'intermediate_debt':2,'terminal_counterexample':False,'queries':2}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
