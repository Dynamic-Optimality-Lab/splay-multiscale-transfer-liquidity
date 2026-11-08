"""Run mandatory historical source controls unchanged, redirect every output."""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    if n=='historical_controls.json':
        v=dict(v);v.pop('all_outputs_redirected_to11',None);v['all_outputs_redirected_to12']=True
        v['scope']='mandatory inherited regressions, not the universal two-slot proof'
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
spec=importlib.util.spec_from_file_location('sealed11_control_replay12',B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11/audit_controls.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.B=B;m.out=out
if __name__=='__main__':
    error=None;m.a=m.c8=m.c10=m.n10=None
    try:m.main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:
        calls=(m.a.calls if m.a else 0)+(m.c8.d.calls if m.c8 else 0)+(m.c10.calls if m.c10 else 0)+(m.n10.d.calls if m.n10 else 0)
        rows=(m.c8.d.replayed if m.c8 else 0)+(m.n10.d.replayed if m.n10 else 0)+(320 if m.c10 else 0)
        out('audit_controls_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
            'source_engine_calls':calls,'old_semantic_rows_replayed':rows,'new_finite_tests':0})
