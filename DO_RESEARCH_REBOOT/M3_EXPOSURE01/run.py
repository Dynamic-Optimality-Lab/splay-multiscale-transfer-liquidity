"""Proof-schema audit only; no finite-population campaign or new potential fit."""
import json,sys,time,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    prior=754.46875;cap=min(120,7200-prior-time.process_time()-5);assert cap>0
    with (BASE/'log_symbolic_audit.txt').open('x',encoding='utf-8') as f:p=subprocess.run([sys.executable,'-B',str(BASE/'symbolic_audit.py'),str(cap)],stdout=f,stderr=subprocess.STDOUT)
    ex=read(BASE/'symbolic_audit_exit.json');audit=read(BASE/'symbolic_audit.json') if (BASE/'symbolic_audit.json').exists() else None
    report={'status':'PRIVATE_ERASURE_LEMMA_AUDITED_FULL_M3_DESCENT_NOT_PROVED' if p.returncode==0 and audit else 'SYMBOLIC_AUDIT_FAILED_OR_UNKNOWN','prior_uniform_CPU_charge':prior,'new_child_process_CPU':ex['whole_process_CPU_seconds'],'allocated_cap':cap,'returncode':p.returncode,'error':ex['error'],'full_M3_gate_passed':False,'new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'new_candidate_J_proposed':False,'M3_status':'OPEN','NET_ORIGINAL_M3_SIGNED_PROOF_ADVANCEMENT':0}
    write(BASE/'run_result.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
