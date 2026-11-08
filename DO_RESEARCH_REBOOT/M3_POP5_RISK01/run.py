"""Fixed total-five order, retained finite allowance, stop first new failure."""
import json,sys,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
PHASES={'prefix_dp':('build_status.json','COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED',120),'construct':('construction.json','CONSTRUCTED_UNAUDITED',300),'audit':('audit.json','INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS',300)}
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'run_result.json';assert not out.exists();targets=read(BASE/'targets.json')['canonical_signatures'];prior=4055.96875;accounted=prior;done=[];failure=None;events=[];metadata_CPU=0;start=time.monotonic()
    for sig in targets:
        folder=BASE/('s'+''.join(map(str,sig)))
        for phase,(name,good,cap) in PHASES.items():
            budget=min(cap,7200-accounted-5)
            if budget<=0:failure={'sigma':sig,'phase':phase,'status':'UNKNOWN_CURRENT_CPU_RESERVE','unused_reserve':7200-accounted};break
            log=BASE/('log_s'+''.join(map(str,sig))+'_'+phase+'.txt')
            with log.open('x',encoding='utf-8') as f:p=subprocess.run([sys.executable,'-B',str(BASE/(phase+'.py')),*map(str,sig),str(budget)],stdout=f,stderr=subprocess.STDOUT)
            ep=folder/(phase+'_exit.json')
            if not ep.exists():failure={'sigma':sig,'phase':phase,'status':'UNKNOWN_PROCESS_WITHOUT_CPU_RECORD','returncode':p.returncode};break
            e=read(ep);accounted+=e['whole_process_CPU_seconds'];r=read(folder/name) if (folder/name).exists() else None
            event={'sigma':sig,'phase':phase,'status':r['status'] if r else 'UNKNOWN_OR_FAILED','CPU_charged':e['whole_process_CPU_seconds'],'CPU_cap':e['per_phase_cap'],'error':e['error'],'query_cap':2000000}
            events.append(event);write(BASE/('phase_s'+''.join(map(str,sig))+'_'+phase+'.json'),event);print(json.dumps(event),flush=True)
            if p.returncode or r is None or r['status']!=good or accounted>=7200:
                failure={**event,'log':log.as_posix(),'reason':None if r is None else r.get('reason'),'obstruction':None if r is None else r.get('obstruction'),'returncode':p.returncode,'cumulative_finite_CPU':accounted};break
        if failure:break
        mstart=time.process_time();c=read(folder/'relation.json');a=read(folder/'audit.json')
        write(folder/'metadata.json',{'sigma':sig,'classes':c['classes'],'shadows':c['shadows'],'potential_sha256':a['potential_sha256']})
        dt=time.process_time()-mstart;metadata_CPU+=dt;accounted+=dt
        if accounted>=7200:failure={'sigma':sig,'phase':'metadata','status':'UNKNOWN_CURRENT_CPU_CAP'};break
        done.append(sig)
        write(BASE/('completed_'+str(len(done)).zfill(3)+'.json'),{'sigma':sig,'independent_audit':'PASS','canonical_tables_completed':len(done),'cumulative_finite_CPU':accounted})
        print(json.dumps({'completed':len(done),'new_original_signatures':2*len(done),'cumulative_finite_CPU':accounted}),flush=True)
    result={'status':'ALL_TOTAL5_MULTI_FINITE_PASS' if failure is None else 'STOPPED_ON_FIRST_NEW_FAILURE','completed_signatures':done,'failure':failure,'new_signature_vectors':2*len(done),'cumulative_finite_CPU_charged':accounted,'prior_current_finite_CPU_retained':prior,'additional_finite_CPU_charged':accounted-prior,'metadata_CPU_charged':metadata_CPU,'finite_CPU_ceiling':7200,'query_cap':2000000,'CPU_caps':[120,300,300],'other_caps_unchanged':True,'completed_old_phases_replayed':0,'completed_old_audits_replayed':0,'phase_events':events,'wall_seconds':time.monotonic()-start,'full_M3_proved':False}
    write(out,result);print(json.dumps({k:v for k,v in result.items() if k not in ('completed_signatures','phase_events')},indent=2),flush=True)
if __name__=='__main__':main()
