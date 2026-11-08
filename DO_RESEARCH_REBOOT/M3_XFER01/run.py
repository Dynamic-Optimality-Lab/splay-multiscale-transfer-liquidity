import json,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)

def main():
    prior=756.140625;cap=min(120,7200-prior-time.process_time()-5)
    assert cap>0 and (BASE/'entry_baseline.json').exists() and (BASE/'PRE_EXECUTION_v2.md').exists()
    with (BASE/'log_symbolic_audit.txt').open('x',encoding='utf-8') as stream:
        process=subprocess.run([sys.executable,'-B',str(BASE/'audit.py'),str(cap)],stdout=stream,stderr=subprocess.STDOUT)
    ex=json.loads((BASE/'symbolic_audit_exit.json').read_text())
    a=json.loads((BASE/'symbolic_audit.json').read_text()) if (BASE/'symbolic_audit.json').exists() else {}
    passed=process.returncode==0 and ex['error'] is None and a.get('status')=='UNIVERSAL_OPAQUE_PREFIX_SATURATION_AUDIT_PASS'
    result={'status':'PASS' if passed else 'FAILED_OR_UNKNOWN_STOP','prior_uniform_CPU_charge':prior,'new_child_process_CPU':ex['whole_process_CPU_seconds'],'allocated_cap':cap,'returncode':process.returncode,'error':ex['error'],'new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'M3_status':'OPEN'}
    write('run_result.json',result);print(json.dumps(result,indent=2),flush=True)
    assert passed

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
