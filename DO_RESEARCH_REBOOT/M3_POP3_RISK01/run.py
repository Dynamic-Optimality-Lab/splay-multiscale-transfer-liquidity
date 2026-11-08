"""Fixed seven-signature phases, sequential; do not repeat finished work."""
import sys,json,subprocess,time
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_POP3_RISK01')
CASES=tuple(map(tuple,json.loads((BASE/'targets.json').read_text())['canonical_signatures']))
def main():
    out=BASE/'run_result.json';assert not out.exists();completed=[];failure=None;start=time.time();accounted=90.172
    assert json.loads((BASE/'representation_audit.json').read_text())['status']=='PROVED_COMPLETE_SIGNED_REDUCTION_AND_INDEPENDENT_SELECTOR_AUDIT_PASS'
    for sig in CASES:
        folder=BASE/('s'+''.join(map(str,sig)))
        for phase,result,ok in (('prefix_dp','build_status.json','COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED'),('construct','construction.json','CONSTRUCTED_UNAUDITED'),('audit','audit.json','INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS')):
            target=folder/result
            if target.exists():
                report=json.loads(target.read_text());assert report['status']==ok,(sig,phase,report['status']);continue
            log=BASE/('log_s'+''.join(map(str,sig))+'_'+phase+'.txt')
            with log.open('x',encoding='utf-8') as f:process=subprocess.run([sys.executable,'-B',str(BASE/(phase+'.py')),*map(str,sig)],stdout=f,stderr=subprocess.STDOUT,text=True)
            if process.returncode or not target.exists():failure={'sigma':sig,'phase':phase,'returncode':process.returncode,'log':log.as_posix()};break
            report=json.loads(target.read_text());print(json.dumps({'sigma':sig,'phase':phase,'status':report['status'],'CPU':report.get('cpu_seconds')}),flush=True)
            accounted+=report.get('cpu_seconds',0)
            if accounted>=7200:failure={'sigma':sig,'phase':phase,'status':'UNKNOWN_CUMULATIVE_CPU_CAP'};break
            if report['status']!=ok:failure={'sigma':sig,'phase':phase,'status':report['status'],'log':log.as_posix()};break
        if failure:break
        completed.append(sig)
        with (BASE/('completed_'+str(len(completed)).zfill(3)+'.json')).open('x',encoding='utf-8') as f:json.dump({'sigma':sig,'independent_audit':'PASS','completed_canonical_tables':len(completed),'accounted_CPU_seconds':round(accounted,3)},f,indent=2)
        print(json.dumps({'completed':len(completed),'sigma':sig}),flush=True)
    obj={'status':'STOPPED_ON_FIRST_FAILURE' if failure else 'ALL97_REMAINING_TOTAL3_FINITE_CERTIFICATES_PASS','completed_signatures':completed,
      'failure':failure,'prior_accounted_CPU_seconds':90.172,'new_finite_CPU_seconds':round(accounted-90.172,3),'accounted_CPU_seconds':round(accounted,3),'wall_seconds':round(time.time()-start,3),'source_family_audit_pending':True,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    print(json.dumps(obj,indent=2),flush=True)
if __name__=='__main__':main()
