"""Read-only reconciliation if a capped audit exits before emitting its report."""
import json,re
from pathlib import Path
BASE=Path(__file__).resolve().parent

def main():
    out=BASE/'resource_accounting.json';assert not out.exists()
    run=json.loads((BASE/'run_result.json').read_text());monitor=json.loads((BASE/'resource_monitor.json').read_text(encoding='utf-8-sig'))
    observed={};validated=0
    for row in monitor['phases']:
        match=re.search(r'(prefix_dp|construct|audit)_v2[.]py\s+(.+)$',row['command'])
        if not match:continue
        phase=match.group(1);args=match.group(2).split();sig=tuple(map(int,args[:10]));budget=float(args[10]);observed[sig,phase]=(row,budget)
        report={'prefix_dp':'build_status.json','construct':'construction.json','audit':'audit.json'}[phase]
        path=BASE/('s'+''.join(map(str,sig)))/report
        if row['CPU_seconds'] is not None and path.exists():
            old=json.loads(path.read_text());assert row['CPU_seconds']+0.05>=old['cpu_seconds'];validated+=1
    failure=run['failure'];extra=0;details=None
    if failure:
        sig=tuple(failure['sigma']);phase=failure['phase'];name={'prefix_dp':'build_status.json','construct':'construction.json','audit':'audit.json'}[phase]
        path=BASE/('s'+''.join(map(str,sig)))/name
        if not path.exists() and failure.get('returncode') is not None:
            row,budget=observed[sig,phase];assert row['CPU_seconds'] is not None,(row['error'],'failed phase CPU unavailable')
            extra=row['CPU_seconds'];text=(BASE/Path(failure['log']).name).read_text()
            details={'sigma':sig,'phase':phase,'allocated_CPU_cap':budget,'whole_process_CPU_seconds':extra,'error':row['error'],
              'independent_CPU_cap_assertion':'UNKNOWN independent' in text and 'cap' in text,
              'last_traceback_line':text.strip().splitlines()[-1],'accounting':'whole process CPU conservatively charged only where main report absent'}
    effective=round(run['accounted_CPU_seconds']+extra,6);assert effective<7200,(effective,run['accounted_CPU_seconds'],extra)
    result={'status':'CPU_LEDGER_RECONCILED_PASS','completed_reported_CPU_seconds':run['accounted_CPU_seconds'],
      'additional_unreported_failed_process_CPU_seconds':extra,'conservative_cumulative_CPU_charge':effective,'ceiling':7200,
      'captured_processes':len(monitor['phases']),'process_CPU_measurements_compared_with_saved_reports':validated,
      'failed_phase_details':details,'source_queries_repeated':0,'finite_phases_repeated':0}
    with out.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
