"""Bounded fixed-basis predicate discovery; stop at first new failure."""
import json,sys,time,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    prior=665.75;used=0;events=[];failure=None;counter=None;passed=[]
    def phase(name,index,limit,report,exname):
        nonlocal used,failure
        cap=min(limit,7200-prior-used-time.process_time()-5);assert cap>0,'UNKNOWN finite CPU reserve'
        args=[sys.executable,'-B',str(BASE/(name+'.py'))]
        if index is not None:args.append(str(index))
        args.append(str(cap));tag=name if index is None else f'{index:03d}_{name}'
        with (BASE/f'log_{tag}.txt').open('x',encoding='utf-8') as f:proc=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
        folder=BASE if index is None else BASE/f'case_{index:03d}';ex=read(folder/exname);used+=ex['whole_process_CPU_seconds'];r=read(folder/report) if (folder/report).exists() else None
        e={'phase':name,'index':index,'allocated_cap':cap,'CPU_charged':ex['whole_process_CPU_seconds'],'returncode':proc.returncode,'error':ex['error'],'status':r['status'] if r else 'UNKNOWN_OR_FAILED'}
        events.append(e);write(BASE/f'phase_{tag}.json',e);print(json.dumps(e),flush=True)
        if proc.returncode or ex['error'] is not None or r is None:failure=e;return None
        return r
    b=phase('basis',None,120,'basis.json','basis_exit.json')
    if b is not None:
        for i in range(4):
            c=phase('construct',i,120,'construction.json','construct_exit.json')
            if c is None:break
            a=phase('audit',i,300,'audit.json','audit_exit.json')
            if a is None:break
            if a['status']=='THRESHOLD_PREDICATES_REFUTED_IN_SAVED_RELATION':counter=i;break
            assert a['status']=='FINITE_EXACT_THRESHOLD_PREDICATES_SIGNED_PRESERVATION_PASS';passed.append(i)
    status='STOPPED_ON_FIRST_THRESHOLD_PREDICATE_COUNTEREXAMPLE' if counter is not None and failure is None else ('STOPPED_ON_FIRST_NEW_CAP_OR_FAILURE' if failure else 'REGISTERED_FINITE_PREDICATE_TESTS_PASS_UNIVERSAL_PROOF_OPEN')
    result={'status':status,'prior_conservative_uniform_charge':prior,'new_child_process_CPU':used,'finite_CPU_ceiling':7200,'events':events,'passed_case_indices':passed,'first_counterexample_case':counter,'failure':failure,'no_larger_basis_or_sign_horizon_after_failure':True,'old_transition_censuses_not_repeated':True,'new_source_transition_queries':0,'uniform_predicate_preservation_proved':False,'new_original_sector_certificates':0,'negative_cycle_certified':False,'M3_status':'OPEN','NET_ORIGINAL_M3_PROOF_ADVANCEMENT':0}
    write(BASE/'run_result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='events'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
