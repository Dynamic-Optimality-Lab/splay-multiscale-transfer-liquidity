"""Authorized one memory retry, then bounded fixed-predicate tests."""
import json,sys,time,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    prior=713.59375;used=0;events=[];failure=None;counter=None;passed=[]
    def phase(name,index,limit,report,exname):
        nonlocal used,failure
        cap=min(limit,7200-prior-used-time.process_time()-5)
        if cap<=0:failure={'status':'UNKNOWN_FINITE_CPU_RESERVE','phase':name,'index':index};return None
        args=[sys.executable,'-B',str(BASE/(name+'.py'))]
        if index is not None:args.append(str(index))
        args.append(str(cap));tag=name if index is None else f'{index:03d}_{name}'
        with (BASE/f'log_{tag}.txt').open('x',encoding='utf-8') as f:proc=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
        folder=BASE if index is None else BASE/f'case_{index:03d}';ex=read(folder/exname);used+=ex['whole_process_CPU_seconds'];result=read(folder/report) if (folder/report).exists() else None
        event={'phase':name,'index':index,'allocated_cap':cap,'CPU_charged':ex['whole_process_CPU_seconds'],'returncode':proc.returncode,'error':ex['error'],'status':result['status'] if result else 'UNKNOWN_OR_FAILED'}
        events.append(event);write(BASE/f'phase_{tag}.json',event);print(json.dumps(event),flush=True)
        if proc.returncode or ex['error'] or result is None:failure=event;return None
        return result
    p=phase('prepare',None,120,'prepare.json','prepare_exit.json')
    if p is not None:p=phase('critical_budget',None,120,'critical_budget.json','critical_budget_exit.json')
    if p is not None:p=phase('audit_critical',None,300,'independent_critical_budget_audit.json','audit_critical_exit.json')
    if p is not None:
        for i,c in enumerate(read(BASE/'config.json')['cases']):
            if not c['reused_input']:
                if phase('construct',i,120,'construction.json','construct_exit.json') is None:break
            a=phase('audit',i,300,'audit.json','audit_exit.json')
            if a is None:break
            if a['status']=='THRESHOLD_PREDICATES_REFUTED_IN_SAVED_RELATION':counter=i;break
            assert a['status']=='FINITE_EXACT_STREAMED_THRESHOLD_SIGNED_PRESERVATION_PASS';passed.append(i)
    status='STOPPED_ON_FIRST_NEW_THRESHOLD_COUNTEREXAMPLE' if counter is not None and failure is None else ('STOPPED_ON_FIRST_NEW_CAP_OR_FAILURE' if failure else 'REGISTERED_FIXED_PREDICATE_TESTS_PASS_UNIVERSAL_TEST_OPEN')
    result={'status':status,'prior_conservative_uniform_charge':prior,'new_child_process_CPU':used,'finite_CPU_ceiling':7200,'events':events,'passed_case_indices':passed,'first_counterexample_case':counter,'failure':failure,'old_completed_first_case_not_repeated':True,'authorized_old_candidate_construction_reused':True,'no_larger_basis_or_sign_horizon':True,'uniform_preservation_proved':False,'new_original_sector_certificates':0,'original_negative_cycle_certified':False,'M3_status':'OPEN','NET_ORIGINAL_M3_PROOF_ADVANCEMENT':0}
    write(BASE/'run_result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='events'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
