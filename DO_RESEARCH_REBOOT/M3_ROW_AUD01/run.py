"""Bounded exact source-row audit; retained uniform allowance, no formula work."""
import json,sys,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'run_result.json').exists();prior=654.703125;used=0;events=[];failure=None;start=time.monotonic()
    phases=[('binding_audit',120,'binding_audit.json','binding_exit.json'),('construct_witness',300,'source_result.json','source_exit.json'),('verify_witness',300,'independent_verification.json','verification_exit.json')]
    for phase,cap,out,exname in phases:
        budget=min(cap,7200-prior-used-time.process_time()-5)
        if budget<=0:failure={'phase':phase,'status':'UNKNOWN_FINITE_CPU_RESERVE'};break
        log=BASE/f'log_{phase}.txt';args=[sys.executable,'-B',str(BASE/(phase+'.py'))]
        if phase!='binding_audit':args.append(str(budget))
        with log.open('x',encoding='utf-8') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
        ex=read(BASE/exname);used+=ex['whole_process_CPU_seconds'];r=read(BASE/out) if (BASE/out).exists() else None
        e={'phase':phase,'CPU_charged':ex['whole_process_CPU_seconds'],'allocated_cap':budget,'status':r['status'] if r else 'UNKNOWN_OR_FAILED','returncode':p.returncode,'error':ex['error'],'log':log.as_posix()};events.append(e);write(BASE/f'phase_{phase}.json',e);print(json.dumps(e),flush=True)
        if p.returncode or r is None:failure=e;break
        if phase=='construct_witness' and r['status']!='SAT_ORIGINAL_LOW_WEIGHT_PLUS_ONE_ROW':failure=e;break
    verified=(BASE/'independent_verification.json').exists() and read(BASE/'independent_verification.json')['status']=='INDEPENDENT_ORIGINAL_LOW_REALIZABILITY_VERIFIED'
    result={'status':'ORIGINAL_ROW_REALIZABLE_AND_INDEPENDENTLY_VERIFIED' if verified else 'SOURCE_REALIZABILITY_OPEN_OR_UNKNOWN','failure':failure,'events':events,'prior_conservative_uniform_charge':prior,'new_child_process_CPU':used,'controller_CPU_before_result_write':time.process_time(),'finite_CPU_ceiling':7200,'wall_seconds':time.monotonic()-start,'new_J_formula_tried':False,'old_failed_original_root_replayed':False,'old_debt_audits_reused':True,'unrealizability_claimed':False,'original_negative_cycle_certified':False,'M3_status':'OPEN'}
    write(BASE/'run_result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='events'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
