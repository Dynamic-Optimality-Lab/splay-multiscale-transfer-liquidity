"""One count-free mechanism, exact resource ledger and first-obstruction stop."""
import json,sys,time,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    prior=665.296875;used=0;events=[];failure=None
    def phase(name,limit,report):
        nonlocal used,failure
        cap=min(limit,7200-prior-used-time.process_time()-5)
        assert cap>0,'UNKNOWN finite reserve'
        with (BASE/f'log_{name}.txt').open('x',encoding='utf-8') as f:
            proc=subprocess.run([sys.executable,'-B',str(BASE/(name+'.py')),str(cap)],stdout=f,stderr=subprocess.STDOUT)
        ex=read(BASE/(name+'_exit.json'));used+=ex['whole_process_CPU_seconds']
        result=read(BASE/report) if (BASE/report).exists() else None
        event={'phase':name,'CPU_charged':ex['whole_process_CPU_seconds'],'allocated_cap':cap,'returncode':proc.returncode,'error':ex['error'],'status':result['status'] if result else 'UNKNOWN_OR_FAILED'}
        events.append(event);write(BASE/f'phase_{name}.json',event);print(json.dumps(event),flush=True)
        if proc.returncode or ex['error'] is not None or result is None:failure=event;return None
        return result
    p=phase('preflight',120,'preflight.json');a=None
    if p is not None:a=phase('audit_preflight',300,'independent_preflight_audit.json')
    if p is not None and a is not None and p['status']=='EXACT_COUNT_FREE_CORPUS_LOWER_BOUND_EXCEEDS_QUERY_CAP':
        assert a['status']=='INDEPENDENT_INJECTIVE_SUBGRAMMAR_SIZE_AUDIT_PASS' and a['size_exceeds_cap']
        status='STOPPED_ON_INDEPENDENTLY_VERIFIED_COUNT_FREE_SIZE_OBSTRUCTION'
    elif failure is not None:status='STOPPED_ON_FIRST_NEW_FAILURE_OR_UNKNOWN'
    else:status='SUBGRAMMAR_FITS_FULL_COUNT_FREE_PREFLIGHT_REQUIRED'
    result={'status':status,'events':events,'failure':failure,'prior_conservative_uniform_charge':prior,'new_child_process_CPU':used,'finite_CPU_ceiling':7200,'no_enumeration_after_size_obstruction':True,'no_new_transport_horizon':True,'new_J_table_constructed':False,'uniform_J_proved':False,'new_signature_certificates':0,'negative_cycle_certified':False,'M3_status':'OPEN','NET_ORIGINAL_M3_PROOF_ADVANCEMENT':0}
    write(BASE/'run_result.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
