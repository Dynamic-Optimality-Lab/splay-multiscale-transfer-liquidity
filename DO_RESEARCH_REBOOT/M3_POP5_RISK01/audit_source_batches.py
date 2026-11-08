"""Fixed source batches registered before finite execution; no failed batch retry."""
import json,sys,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'certification_run.json';assert not out.exists();run=read(BASE/'run_result.json');done=run['completed_signatures'];plans=read(BASE/'targets.json')['source_batches']
    certified=[];batches=[];failure=None
    for i,planned in enumerate(plans):
        start=50*i;cases=done[start:start+50]
        if not cases:break
        assert cases==planned[:len(cases)]
        write(BASE/('source_batch_'+str(i).zfill(3)+'_cases.json'),{'batch_index':i,'signatures':cases,'fixed_source_cap':300,'original_queries_replayed':0})
        log=BASE/('log_source_batch_'+str(i).zfill(3)+'.txt')
        with log.open('x') as f:p=subprocess.run([sys.executable,'-B',str(BASE/'source_audit_batch.py'),str(i)],stdout=f,stderr=subprocess.STDOUT)
        target=BASE/'source_audits'/('batch_'+str(i).zfill(3))/'source_audit.json'
        if p.returncode or not target.exists():failure={'batch_index':i,'returncode':p.returncode,'log':log.as_posix()};break
        r=read(target);assert r['status']=='TOTAL5_SOURCE_BATCH_PASS' and r['completed_canonical_signatures']==cases and r['CPU_seconds']<300
        certified.extend(cases);batches.append({'batch_index':i,'report':target.as_posix(),'original_roots':r['unique_original_roots'],'cycles':r['full_closed_mixed_cycles'],'CPU':r['CPU_seconds']})
        print(json.dumps({'source_batches_passed':len(batches),'canonical_cases_source_complete':len(certified),'new_original_roots':r['unique_original_roots']}),flush=True)
    result={'status':'SOURCE_AUDIT_WORKFLOW_COMPLETE' if failure is None else 'STOPPED_ON_FIRST_SOURCE_FAILURE','source_certified_signatures':certified,
      'finite_only_signatures':done[len(certified):],'source_batches':batches,'failure':failure,'old_source_queries_replayed':0,'full_M3_proved':False}
    write(out,result);print(json.dumps({k:v for k,v in result.items() if k not in ('source_certified_signatures','finite_only_signatures')},indent=2),flush=True)
if __name__=='__main__':main()
