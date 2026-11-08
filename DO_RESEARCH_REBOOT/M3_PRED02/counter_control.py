"""Only independent certification of the FIRST counterexample after stop."""
import json,sys,time,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    run=read(BASE/'run_result.json');assert run['status']=='STOPPED_ON_FIRST_NEW_THRESHOLD_COUNTEREXAMPLE' and run['first_counterexample_case']==0
    retained=run['prior_conservative_uniform_charge']+run['new_child_process_CPU']+read(BASE/'controller_exit.json')['whole_process_CPU_seconds'];used=0;events=[];failure=None
    for phase,report in [('audit_endpoints','endpoint_audit.json'),('construct_witness','source_result.json'),('verify_witness','independent_original_verification.json')]:
        cap=min(300,7200-retained-used-time.process_time()-5);assert cap>0
        with (BASE/f'log_{phase}.txt').open('x',encoding='utf-8') as f:proc=subprocess.run([sys.executable,'-B',str(BASE/(phase+'.py')),str(cap)],stdout=f,stderr=subprocess.STDOUT)
        ex=read(BASE/(phase+'_exit.json'));used+=ex['whole_process_CPU_seconds'];r=read(BASE/report) if (BASE/report).exists() else None
        event={'phase':phase,'allocated_cap':cap,'CPU_charged':ex['whole_process_CPU_seconds'],'returncode':proc.returncode,'error':ex['error'],'status':r['status'] if r else 'UNKNOWN_OR_FAILED'};events.append(event);write(BASE/f'phase_{phase}.json',event);print(json.dumps(event),flush=True)
        if proc.returncode or ex['error'] or r is None:failure=event;break
        if phase=='construct_witness' and r['status']!='SAT_ORIGINAL_LOW_THRESHOLD_PREDICATE_COUNTEREXAMPLE':failure=event;break
    result={'status':'ORIGINAL_PREDICATE_REFUTATION_INDEPENDENTLY_CERTIFIED' if failure is None and (BASE/'independent_original_verification.json').exists() else 'PROOF_RELATION_COUNTEREXAMPLE_ORIGINAL_STATUS_OPEN','retained_CPU_before_control':retained,'new_child_process_CPU':used,'events':events,'failure':failure,'later_predicate_tests_executed_after_refutation':False,'M3_status':'OPEN'};write(BASE/'counter_control_result.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'counter_controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
