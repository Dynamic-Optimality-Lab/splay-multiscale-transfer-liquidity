"""Record the aggregate CPU-reserve stop; no experimental phase is repeated."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
r=read(BASE/'run_result.json');f=r['failure'];sig=f['sigma'];folder=BASE/('s'+''.join(map(str,sig)))
assert sig==[0,0,0,4,0,0,1,0,0,0] and f['phase']=='audit'
assert f['CPU_cap']==3.5625 and r['cumulative_finite_CPU_charged']==7195.203125
assert len(r['completed_signatures'])==70 and not (folder/'audit.json').exists()
d=read(folder/'build_status.json');c=read(folder/'construction.json')
assert d['status']=='COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED' and c['status']=='CONSTRUCTED_UNAUDITED'
log=[]
for line in Path(f['log']).read_text().splitlines():
    if line.startswith('{'):log.append(json.loads(line))
assert log[-1]['canonical_queries']==67380
note={'status':'UNKNOWN_FINITE_ALLOWANCE_RESERVE_NOT_MATHEMATICAL_REFUTATION','sigma':sig,'gap_multiplicities':{'3':4,'6':1},'phase':'audit','current_maximum_audit_CPU_cap':300,'allocated_audit_CPU_from_remaining_balance':3.5625,'whole_failed_audit_process_CPU':3.765625,'finite_CPU_ceiling':7200,'prior_finite_CPU_retained':4055.96875,'cumulative_finite_CPU_charged':7195.203125,'CPU_left_reserved':4.796875,'guard_reserve':5,'canonical_query_cap_unchanged':2000000,'complete_enumeration_queries':d['queries'],'last_persisted_independent_family_query_count':67380,'exact_partial_independent_query_count_not_persisted':True,'independent_grammar_and_residual_audit_unfinished':True,'candidate_not_promoted':True,'original_negative_cycle_certified':False,'next_finite_case_started':False,'failed_phase_retried_or_split':False,'completed_input_files_saved_for_future_explicit_continuation':[{'path':(folder/n).as_posix(),'sha256':hashlib.sha256((folder/n).read_bytes()).hexdigest()} for n in ('relation.json','potential.json','build_status.json','construction.json')],'only_pre_registered_source_checks_for_completed70_cases_follow':True}
with (BASE/'STOP_NOTE.json').open('x',encoding='utf-8') as out:json.dump(note,out,indent=2)
print(json.dumps({k:v for k,v in note.items() if k!='completed_input_files_saved_for_future_explicit_continuation'},indent=2))
