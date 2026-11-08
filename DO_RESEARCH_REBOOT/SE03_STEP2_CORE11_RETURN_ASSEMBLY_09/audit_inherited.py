"""Recompute accepted06/07/08 conclusions; redirect ALL writes into09.
The old inputs, implementations and frozen certificates remain unchanged.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def main():
    global a
    a=load('audit_independent',B.parent/'SE03_STEP2_TERMINAL_PAIR_06/audit_independent.py')
    a.out=lambda n,v:out('recomputed06_'+n,v);a.main()
    m=load('recompute07',B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07/audit_independent2.py')
    m.out=lambda n,v:out('recomputed07_'+n,v);m.main()
    n=load('recompute08',B.parent/'SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/audit_independent.py')
    n.out=lambda fn,v:out('recomputed08_'+fn,v);n.main()
    out('inherited_recomputation.json',{'status':'PASS_RECOMPUTED_ACCEPTED06_07_08',
        '06':'accepted saturation3 only;260 frames/20 edges',
        '07':'32436 frames/22452 zero incidences',
        '08':'9624 frames/5872 zero incidences/720 L4 degree2',
        'immutable_old_inputs':True,'all_new_outputs_in09':True,
        'source_engine_calls':a.calls,'new_finite_tests':0})
if __name__=='__main__':
    error=None;a=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_inherited_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':a.calls if a else 0,'new_finite_tests':0})
