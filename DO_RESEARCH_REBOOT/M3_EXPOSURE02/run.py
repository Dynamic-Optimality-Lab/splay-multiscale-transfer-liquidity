"""Proof-only independent schema audit, no finite instances."""
import json,sys,time,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    prior=754.828125;cap=min(120,7200-prior-time.process_time()-5);assert cap>0
    with (BASE/'log_symbolic_audit.txt').open('x',encoding='utf-8') as f:p=subprocess.run([sys.executable,'-B',str(BASE/'symbolic_audit.py'),str(cap)],stdout=f,stderr=subprocess.STDOUT)
    ex=read(BASE/'symbolic_audit_exit.json');a=read(BASE/'symbolic_audit.json') if (BASE/'symbolic_audit.json').exists() else None
    result={'status':'UNIVERSAL_HELPER_REDUNDANCY_AUDITED_PUBLIC_DEBT_OPEN' if p.returncode==0 and a else 'SYMBOLIC_AUDIT_FAILED_OR_UNKNOWN','prior_uniform_CPU_charge':prior,'new_child_process_CPU':ex['whole_process_CPU_seconds'],'allocated_cap':cap,'returncode':p.returncode,'error':ex['error'],'new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'both_gaps_closed':False,'public_debt_constructed':False,'M3_status':'OPEN'}
    write(BASE/'run_result.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
