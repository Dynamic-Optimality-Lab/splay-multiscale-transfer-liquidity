"""Post-cap reporting and integrity only; no new mathematical experiment."""
from pathlib import Path
import json,subprocess,hashlib
from entry import BASE,sha
def main():
    out=BASE/'final_manifest.json';assert not out.exists();run=json.loads((BASE/'run_result.json').read_text());assert run['status']=='ALL24_NEW_CANONICAL_FINITE_CERTIFICATES_PASS'
    a=[];c=[];r=[]
    for g,h in run['completed_pairs']:
        folder=BASE/f'p{g}_{h}';aa=json.loads((folder/'audit.json').read_text());cc=json.loads((folder/'construction.json').read_text());rr=json.loads((folder/'relation.json').read_text())
        assert aa['status']=='INDEPENDENT_FINITE_EXACT_PASS' and cc['status']=='CONSTRUCTED_UNAUDITED' and sha(folder/'potential.json')==aa['potential_sha256']
        a.append(aa);c.append(cc);r.append({k:v for k,v in rr.items() if k not in ('shadows','options','families')})
    finite={'status':'ALL24_NEW_CANONICAL_FINITE_CERTIFICATES_PASS','canonical_tables_with_inherited':25,'candidate_unit_pair_supports':45,
      'new_profile_queries':sum(x['profile_queries'] for x in a),'new_access_options':sum(x['access_options'] for x in a),
      'new_explicit_residuals':sum(x['explicit_residuals'] for x in a),'minimum_residual':min(x['minimum_residual'] for x in a),
      'maximum_resident_construction_records':max(x['peak_conservative_resident_records'] for x in c),
      'finite_CPU_seconds':round(sum(x['cpu_seconds'] for x in a+c+r),3),'full_source_audit_passed':False}
    with (BASE/'finite_summary.json').open('x',encoding='utf-8') as f:json.dump(finite,f,indent=2)
    reuse=json.loads((BASE/'reused_controls.json').read_text());allpairs=[(g,h) for g in range(10) for h in range(g+1,10)]
    assert tuple(reuse['completed_pairs'][-1])==(2,7) and allpairs[41]==(6,9)
    stop={'status':'UNKNOWN_REGISTERED_SOURCE_FAMILY_CPU_CAP','limit_CPU_seconds':300,
      'prototype1_CPU_seconds':json.loads((BASE/'source_prototype_stop.json').read_text())['cpu_seconds'],
      'prototype2_CPU_seconds':json.loads((BASE/'source_v2_stop.json').read_text())['cpu_seconds'],
      'outer_helper_CPU_seconds':json.loads((BASE/'outer_helper_controls.json').read_text())['cpu_seconds'],
      'conservative_stop_margin_seconds':2,'version3_last_completed_CPU_seconds':67.578,
      'version3_error':'AssertionError: UNKNOWN shared source family CPU cap','version3_last_completed_pair':[6,9],
      'complete_support_cases_observed':42,'complete_unique_original_roots_observed':130,'fully_closed_mixed_controls_observed':42,
      'completed_supports':allpairs[:42],'incomplete_support_controls':allpairs[42:],
      'no_further_experiments_after_cap':True,'full_family_promotion':False,
      'reproducible_progress_provenance':{'prototype_program_sha256':sha(BASE/'source_audit.py'),'version3_program_sha256':sha(BASE/'source_audit_v3.py'),
         'prototype_completed_first22_supports':True,'version3_completed_next20_supports':True,'lost_prototype_environments_claimed_saved':False}}
    stop['prior_counted_CPU_seconds']=stop['prototype1_CPU_seconds']+stop['prototype2_CPU_seconds']+stop['outer_helper_CPU_seconds']+2
    stop['version3_remaining_budget_seconds']=300-stop['prior_counted_CPU_seconds']
    with (BASE/'source_audit_cap.json').open('x',encoding='utf-8') as f:json.dump(stop,f,indent=2)
    b=json.loads((BASE/'entry_baseline.json').read_text());old={x['path'] for x in b['files']}
    assert all(Path(x['path']).is_file() and sha(Path(x['path']))==x['sha256'] for x in b['files'])
    extra=[p.as_posix() for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old];assert not extra
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==b['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'head':b['head'],'tracked_tree_clean':True,'new_writes_confined_here':True}
    with (BASE/'integrity.json').open('x',encoding='utf-8') as f:json.dump(integrity,f,indent=2)
    verdict={'status':'INCOMPLETE_SOURCE_AUDIT_CAP_FINITE_CANDIDATES_PRESERVED','step3_completed':True,'step3_new_audited_mask_sectors':126,
      'step4_completed':False,'step4_finite_candidates':finite,'step4_source_cap':{k:v for k,v in stop.items() if k not in ('completed_supports','reproducible_progress_provenance')},
      'additional_unit_pair_sign_sectors_promoted':0,'larger_population_experiments_executed':False,'larger_support_experiments_executed':False,
      'negative_original_cycle_certified':False,'full_M3_proved':False,'R1_R4_preserved':True,'h0_correction_retained':True,'integrity':integrity,
      'unexecuted_success_finalizers':['finalize.py','finalize_v2.py'],'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]}
    with out.open('x',encoding='utf-8') as f:json.dump(verdict,f,indent=2)
    print(json.dumps({k:v for k,v in verdict.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
