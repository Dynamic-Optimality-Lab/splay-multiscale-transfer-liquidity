"""Sequential registered phases; stop on first cap/refutation/check failure."""
import sys,json,subprocess,time
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def main():
    out=BASE/'run_result.json';assert not out.exists();counts=json.loads((BASE/'counts.json').read_text());assert counts['status']=='COUNTS_WITHIN_REGISTERED_CAPS'
    completed=[];failure=None;start=time.time()
    for pair in counts['pairs']:
        g,h=pair['g'],pair['h']
        if (g,h)==(0,1):continue
        folder=BASE/f'p{g}_{h}'
        for phase,resultfile,ok in (('build','relation.json','COMPLETE_PREFIX_RELATION_UNAUDITED'),('construct','construction.json','CONSTRUCTED_UNAUDITED'),('audit','audit.json','INDEPENDENT_FINITE_EXACT_PASS')):
            target=folder/resultfile
            if target.exists():
                report=json.loads(target.read_text());assert report['status']==ok,(g,h,phase,report['status']);continue
            log=BASE/f'log_p{g}_{h}_{phase}.txt'
            with log.open('x',encoding='utf-8') as f:
                run=subprocess.run([sys.executable,'-B',str(BASE/(phase+'.py')),str(g),str(h)],stdout=f,stderr=subprocess.STDOUT,text=True)
            if run.returncode or not target.exists():failure={'g':g,'h':h,'phase':phase,'returncode':run.returncode,'log':log.as_posix()};break
            report=json.loads(target.read_text())
            print(json.dumps({'g':g,'h':h,'phase':phase,'status':report['status'],'cpu_seconds':report['cpu_seconds']}),flush=True)
            if report['status']!=ok:failure={'g':g,'h':h,'phase':phase,'status':report['status'],'log':log.as_posix()};break
        if failure:break
        completed.append([g,h]);print(json.dumps({'certificates_finitely_audited':len(completed),'last':[g,h]}),flush=True)
    result={'status':'STOPPED_ON_FIRST_FAILURE' if failure else 'ALL24_NEW_CANONICAL_FINITE_CERTIFICATES_PASS',
      'completed_pairs':completed,'failure':failure,'wall_seconds':round(time.time()-start,2),'source_family_audit_pending':True,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
