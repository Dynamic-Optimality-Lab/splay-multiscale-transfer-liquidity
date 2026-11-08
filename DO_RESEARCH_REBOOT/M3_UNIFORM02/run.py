"""Retained allowance; fixed sign-run candidate; no post-failure alternation."""
import json,sys,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'run_result.json').exists();prior=622.0625;used=0;events=[];passed=[];counter=None;failure=None;start=time.monotonic()
    def execute(phase,index,cap,report,exname):
        nonlocal used,failure
        budget=min(cap,7200-prior-used-time.process_time()-5)
        if budget<=0:failure={'phase':phase,'index':index,'status':'UNKNOWN_FINITE_CPU_RESERVE'};return None
        log=BASE/f'log_{index:03d}_{phase}.txt'
        with log.open('x',encoding='utf-8') as f:p=subprocess.run([sys.executable,'-B',str(BASE/(phase+'.py')),str(index),str(budget)],stdout=f,stderr=subprocess.STDOUT)
        folder=BASE/f'case_{index:03d}';ex=read(folder/exname);used+=ex['whole_process_CPU_seconds'];r=read(folder/report) if (folder/report).exists() else None
        event={'phase':phase,'index':index,'CPU_charged':ex['whole_process_CPU_seconds'],'allocated_cap':budget,'status':r['status'] if r else 'UNKNOWN_OR_FAILED','returncode':p.returncode,'error':ex['error'],'log':log.as_posix()};events.append(event);write(BASE/f'phase_{index:03d}_{phase}.json',event);print(json.dumps(event),flush=True)
        if p.returncode or r is None:failure=event;return None
        return r
    for i in range(3):
        r=execute('construct',i,120,'construction.json','construct_exit.json')
        if r is None:break
        a=execute('audit',i,300,'audit.json','audit_exit.json')
        if a is None:break
        if a['status']=='SIGN_RUN_CANDIDATE_REFUTED_IN_PROOF_RELATION':
            counter=i
            check=execute('audit_obstruction',i,300,'obstruction_audit.json','obstruction_audit_exit.json')
            if check is not None:execute('original_lift',i,300,'original_control.json','original_lift_exit.json')
            break
        assert a['status']=='FINITE_EXACT_SIGN_RUN_CLOSED_ON_SAVED_RELATION';passed.append(i)
    result={'status':'STOPPED_ON_FIRST_SIGN_RUN_COUNTEREXAMPLE' if counter is not None and failure is None else ('STOPPED_ON_FIRST_NEW_CAP_OR_FAILURE' if failure is not None else 'REGISTERED_CORPUS_PASS_UNIVERSAL_CLOSURE_OPEN'),'completed_finite_cases':passed,'counterexample_case':counter,'failure':failure,'prior_conservative_uniform_charge':prior,'new_child_process_CPU':used,'controller_CPU_before_result_write':time.process_time(),'finite_CPU_ceiling':7200,'events':events,'no_later_corpus_after_first_counterexample':True,'no_added_sign_alternation_or_horizon':True,'wall_seconds':time.monotonic()-start,'M3_status':'OPEN','uniform_J_proved':False}
    write(BASE/'run_result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='events'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
