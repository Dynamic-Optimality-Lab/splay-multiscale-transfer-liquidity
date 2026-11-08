"""Metadata-only publication of C19 receipts, scopes and explicit open status.
No source execution, proof replay, verification bypass or independent audit.
"""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()

entry=read(B/'entry.json');prior=read(OLD/'resources_checkpoint.json')
total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);runs=[];peak=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
    charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge
    peak=max(peak,r['peak_working_set_bytes_observed'])
    assert r['status']=='PASS'
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],
      'child_CPU':r['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,
      'source_engine_calls':r['source_engine_calls'],'old_semantic_rows_replayed':r['old_semantic_rows_replayed'],
      'peak_working_set_bytes':r['peak_working_set_bytes_observed'],
      'legacy_unused_test_flag':r['new_finite_tests']})
assert len(runs)==6 and groups['independent']==299.125
assert all(groups[k]<=entry['group_caps'][k] for k in groups)
assert total<7200-entry['reserve'] and sum(x['source_engine_calls'] for x in runs)==0
required=['SOURCE_SPEC.md','FROZEN_LOW_BUNDLE_OBLIGATION.md','U18_RECONSTRUCTION.md',
 'LOW_BUNDLE_CLASSIFICATION.md','LOW_WITNESS_REPLAY.md','JOINT_COLLISION_LEDGER.md',
 'COLLECTIVE_SOURCE_SUPPLY.md','MULTIBUNDLE_REPAYMENT.md','COMPARISON_SAFE_FRONTIERS.md',
 'HIGH_LOW_INTERFACE.md','ZERO_WEIGHT_NONLOCAL_TRANSFER.md','FROZEN_OWNER_PRESERVATION.md',
 'ABSOLUTE_PERIOD_VALIDITY.md','ARBITRARY_R_LIFTING.md','GLOBAL_PHYSICAL_INJECTION.md',
 'GATE_U_DISCHARGE.md','UNIFORM_TRANSFER_VERDICT.md','ADVERSARIAL_AUDIT.md',
 'INDEPENDENT_AUDIT_STATUS.md','FINAL_VERDICT.md','CHECKPOINT.md','IAGS_BOXES.md',
 'LEAF_RECOVERY_BARRIER.md','BIRTH_GROUP_REDUCTION.md','dependency_ledger.json']
assert all((B/n).is_file() and (B/n).stat().st_size for n in required)
assert not (B/'FULL_PROOF.md').exists()
for p in B.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
assert not git('status','--porcelain','--untracked-files=no')
out('resources_checkpoint.json',{
 'status':'U19_OPEN_RESTRICTED_FAMILY_AND_SOURCE_REDUCTIONS_AUDIT_PENDING',
 'prior_cumulative_CPU':entry['prior_uniform_CPU'],'campaign_CPU':total-entry['prior_uniform_CPU'],
 'cumulative_CPU':total,'remaining_CPU':7200-total,'global_allowance':7200,'reserve':5,
 'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
 'group_remaining':{g:entry['group_caps'][g]-v for g,v in groups.items()},
 'symbolic_controller_reserve_seconds':1,
 'remaining_symbolic_before_controller_startup':entry['group_caps']['symbolic']-groups['symbolic']-1,
 'independent_remaining_below_controller_reserve':True,'new_independent_runs':0,
 'C15_integrity_suffix':'PENDING_NOT_COMPLETED_BY_METADATA','C16_C17_C18_C19_audits':'PENDING',
 'campaign_source_engine_calls':0,'campaign_fresh_source_rotation_replays':0,
 'campaign_CD6_backend_rows':0,'campaign_new_concrete_erased_owner_variants':0,
 'C15_through_C19_source_engine_calls':prior['C15_through_C18_source_engine_calls'],
 'older_query_ledgers':'preserved in pinned receipts, no reset; no new original splay/table query',
 'new_distinct_composite_source_word_patterns':5,'composite_patterns':['AB','BA','ABBA','BB','BBB'],
 'formula_counter_records':6,'duplicate_source_description':'BBB appears in collision and seam records; one history, not extra capacity',
 'reindexed_stored_rows_for_seam_formula_controls':894,
 'legacy_test_flag_correction':'unused zero flag is NOT zero new composite source constructions; no finite pass promoted to universal theorem',
 'canonical_query_cap':entry['canonical_query_cap'],'live_record_cap':entry['live_record_cap'],
 'DAG_cap':entry['DAG_cap'],'stored_edge_cap':entry['stored_edge_cap'],
 'memory_cap_bytes':entry['memory_cap_bytes'],'max_observed_memory_this_campaign':peak,
 'wall_cap_hours':12,'Bank25':25,'general_Bank25_realization':'OPEN',
 'no_cap_reset':True,'all_six_producer_controller_runs_charged':True,
 'inherited_failed_charges':'preserved in C18 and older pinned cumulative receipts','runs':runs,
 'metadata_CPU_convention':'inherited entry/publication exclusion only; no mathematical producer or independent process relabeled',
 'publication_metadata_CPU_excluded':time.process_time()})
out('research_status_ledger.json',{
 'principal_outcome':'UNRESOLVED','U19_JOINT_LOW':'OPEN','Gate_U19':'U-OPEN',
 'CD6_I6':'SEALED_UNCHANGED','Gate_U14':'SEALED_SUFFICIENT_IMPLICATION_UNCHANGED',
 'Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
 'F19_restricted_mixed_closed_family':'MATHEMATICAL_DERIVATION_COMPLETE_AUDIT_PENDING',
 'T19_distinct_leaf_birth_pressure':'PROVED-DERIVATION_AUDIT_PENDING',
 'R19_old_root_immediate_restriction':'PROVED-DERIVATION_AUDIT_PENDING',
 'leaf_recovery_barrier':'PROVED-DERIVATION_AUDIT_PENDING',
 'birth_group_source_partial_supply':'PROVED-DERIVATION_AUDIT_PENDING',
 'shared_first_reset_and_local_birth_tail_candidates':'REFUTED-DERIVATION_AUDIT_PENDING',
 'main_theorem_refuted':False,'full_LOW_source_language':'OPEN',
 'general_nonlocal_arrival_supply':'OPEN','all_r_funding_lifting':'OPEN','general_E_r3_working':'OPEN',
 'source_specific_remaining_birth_demands':{'A80':[45,4],'B82':[47,4]},
 'next_bounded_theorem':'joint source-forced second-arrival nonlocal repayment at H1/Q6 seven-key deep recovery, preserving required original and comparison policies',
 'new_independent_audits':0,'new_concrete_f6_maps':0,'manifest_is_proof_seal':False})
out('publication_provenance.json',{'branch':entry['branch'],'HEAD':entry['head'],
 'tracked_status':git('status','--porcelain','--untracked-files=no'),
 'entry_untracked_inventory':'entry.json','new_write_scope':B.relative_to(ROOT).as_posix(),
 'entry_pins_verified':entry['pins_verified'],'all_pin_entry_check_not_repeated':True,
 'metadata_is_independent_audit':False,'frozen_original_owner_files_modified':False,
 'all_new_results_audit_pending':True,'no_destructive_git_operation':True,
 'publication_metadata_CPU_excluded':time.process_time()})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
 for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'CONTENT_CHECKPOINT_NOT_PROOF_SEAL',
 'U19_JOINT_LOW':'OPEN','files':files})
print(json.dumps({'status':'PUBLISHED_U19_OPEN','cumulative_CPU':total,'groups':groups,
 'group_remaining':{g:entry['group_caps'][g]-v for g,v in groups.items()},'files':len(files)}))
