"""Renewed fixed-order campaign. Reuse complete inputs; never retry a new failure."""
import json,sys,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
TARGETS=json.loads((BASE/'targets.json').read_text())['canonical_signatures']
OK={'prefix_dp':('build_status.json','COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED',120),
    'construct':('construction.json','CONSTRUCTED_UNAUDITED',300),
    'audit':('audit.json','INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS',120)}
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def metadata(folder):
    start=time.process_time();c=read(folder/'relation.json');a=read(folder/'audit.json')
    assert a['status']==OK['audit'][1]
    write(folder/'metadata.json',{'sigma':a['sigma'],'classes':c['classes'],'shadows':c['shadows'],'potential_sha256':a['potential_sha256']})
    return time.process_time()-start

def main():
    out=BASE/'run_result.json';assert not out.exists();completed=[];failure=None;accounted=0;events=[];packaging=0;start=time.monotonic()
    prior_reuse=read(BASE/'reused_candidate.json');first=tuple(prior_reuse['sigma'])
    for sig in TARGETS:
        folder=BASE/('s'+''.join(map(str,sig)))
        for phase,(filename,ok,phase_cap) in OK.items():
            target=folder/filename;exitfile=folder/(phase+'_exit.json');reused=(tuple(sig)==first and phase in ('prefix_dp','construct'))
            if reused:
                report=read(target);assert report['status']==ok
                events.append({'sigma':sig,'phase':phase,'status':ok,'reused_old_complete_phase':True,'CPU_charged':0})
                print(json.dumps({'sigma':sig,'phase':phase,'status':'REUSED_COMPLETE_OLD_PHASE','CPU_charged':0}),flush=True);continue
            if not exitfile.exists():
                budget=min(phase_cap,7200-accounted-5)
                if budget<=0:failure={'sigma':sig,'phase':phase,'status':'UNKNOWN_RENEWED_CPU_RESERVE','unused_CPU_reserve':7200-accounted};break
                logfile=BASE/('log_s'+''.join(map(str,sig))+'_'+phase+'.txt')
                assert not logfile.exists()
                with logfile.open('x',encoding='utf-8') as f:
                    process=subprocess.run([sys.executable,'-B',str(BASE/(phase+'.py')),*map(str,sig),str(budget)],stdout=f,stderr=subprocess.STDOUT)
                returncode=process.returncode
            else:
                # Only the explicitly authorized bootstrap audit exists at first entry.
                assert tuple(sig)==first and phase=='audit';returncode=0 if read(exitfile)['error'] is None else 1
                logfile=BASE/('log_s'+''.join(map(str,sig))+'_'+phase+'.txt')
            if not exitfile.exists():
                failure={'sigma':sig,'phase':phase,'status':'UNKNOWN_PROCESS_EXIT_WITHOUT_CPU_RECORD','returncode':returncode,'log':logfile.as_posix()};break
            elapsed=read(exitfile);charge=elapsed['whole_process_CPU_seconds'];accounted+=charge
            event={'sigma':sig,'phase':phase,'CPU_charged':charge,'CPU_cap':elapsed['per_phase_cap'],'error':elapsed['error'],'reused_old_complete_phase':False}
            if target.exists():report=read(target);event['status']=report['status']
            else:report=None;event['status']='UNKNOWN_CAP' if elapsed['error'] and 'UNKNOWN' in elapsed['error']['message'] else 'PHASE_FAILED'
            events.append(event);write(BASE/('phase_s'+''.join(map(str,sig))+'_'+phase+'.json'),event)
            print(json.dumps(event),flush=True)
            if accounted>=7200 or returncode or report is None or report['status']!=ok:
                failure={**event,'log':logfile.as_posix(),'returncode':returncode,'renewed_CPU_charged':accounted};break
        if failure:break
        cost=metadata(folder);packaging+=cost;accounted+=cost
        if accounted>=7200:failure={'sigma':sig,'phase':'metadata','status':'UNKNOWN_RENEWED_CPU_CAP','CPU_charged':accounted};break
        completed.append(sig)
        write(BASE/('completed_'+str(len(completed)).zfill(3)+'.json'),{'sigma':sig,'independent_audit':'PASS','canonical_tables_completed':len(completed),'renewed_CPU_charged':accounted})
        print(json.dumps({'completed':len(completed),'new_signature_vectors':len({tuple(v) for s in completed for v in (s,list(reversed(s)))}),'renewed_CPU_charged':round(accounted,6)}),flush=True)
    result={'status':'ALL295_REMAINING_TOTAL4_FINITE_PASS' if failure is None else 'STOPPED_ON_FIRST_NEW_FAILURE','completed_signatures':completed,
      'failure':failure,'new_signature_vectors':len({tuple(v) for s in completed for v in (s,list(reversed(s)))}),
      'renewed_finite_CPU_allowance':7200,'renewed_CPU_charged':round(accounted,6),'metadata_CPU_charged':round(packaging,6),
      'previous_allowance_budget_charge_unchanged':7200,'reused_completed_old_phases':2,'completed_old_audits_replayed':0,
      'interrupted_old_audit_explicitly_retried':True,'whole_process_CPU_captured_on_failure':True,
      'phase_events':events,'wall_seconds':round(time.monotonic()-start,3),'source_audit_workflow_pending':True,'full_M3_proved':False}
    write(out,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('completed_signatures','phase_events')},indent=2),flush=True)
if __name__=='__main__':main()
