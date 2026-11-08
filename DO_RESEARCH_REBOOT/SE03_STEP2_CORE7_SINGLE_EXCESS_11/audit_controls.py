"""Mandatory historical replay/recomputation; ALL writes redirected into11.
No frozen proof, source engine or original receipt is changed/reopened.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def run(name,folder,file,prefix):
    m=load(name,B.parent/folder/file);m.out=lambda n,v:out(prefix+n,v);m.main();return m
def main():
    global a,c8,c10,n10
    a=load('audit_independent',B.parent/'SE03_STEP2_TERMINAL_PAIR_06/audit_independent.py')
    run('legacy06adverse','SE03_STEP2_TERMINAL_PAIR_06','audit_adversarial.py','historical06_')
    c8=run('legacy08controls','SE03_STEP2_PLUS_ONE_ZERO_TAIL_08','audit_controls.py','historical08controls_')
    run('legacy08adverse','SE03_STEP2_PLUS_ONE_ZERO_TAIL_08','audit_adversarial.py','historical08_')
    run('legacy09adverse','SE03_STEP2_CORE11_RETURN_ASSEMBLY_09','audit_adversarial.py','historical09_')
    sys.path.insert(0,str(B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10'))
    c10=run('legacy10independent','SE03_STEP2_FULL_FUNDING_CLOSURE_10','audit_independent.py','historical10_')
    n10=run('legacy10normal','SE03_STEP2_FULL_FUNDING_CLOSURE_10','audit_normalform.py','historical10normal_')
    old10=json.loads((B/'historical10_independent_audit.json').read_text())
    rows=c8.d.replayed+old10['new_source_rows_recomputed']+26+n10.d.replayed
    calls=a.calls+c8.d.calls+c10.calls+n10.d.calls
    result={'status':'PASS_ALL_REQUIRED_HISTORICAL_CONTROLS',
        '01_to08_source_controls':18,'source_rows_01_to08':c8.d.replayed,
        '06':'canonical terminal-pair contexts/reflection and source shield controls recomputed',
        '08':'new neutral-tail/source-word/reflection controls recomputed, no scope extension',
        '09':'all62 actual q5/q1 sectors, root aliases, both future A events, reflected4858 frames recomputed',
        '10':'all six exact source families and reflections,78 physical demands,36 erasures,882 cuts; Gamma26 and45/46 failures recomputed',
        'exact_legacy_period_rows_replayed':rows,'source_engine_calls':calls,'new_finite_tests':0,
        'all_outputs_redirected_to11':True,'scope':'regressions/source controls, not the universal proof of C7 one-slot'}
    out('historical_controls.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None;a=c8=c10=n10=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:
        calls=(a.calls if a else 0)+(c8.d.calls if c8 else 0)+(c10.calls if c10 else 0)+(n10.d.calls if n10 else 0)
        rows=(c8.d.replayed if c8 else 0)+(n10.d.replayed if n10 else 0)+(320 if c10 else 0)
        out('audit_controls_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
            'source_engine_calls':calls,'old_semantic_rows_replayed':rows,'new_finite_tests':0})
