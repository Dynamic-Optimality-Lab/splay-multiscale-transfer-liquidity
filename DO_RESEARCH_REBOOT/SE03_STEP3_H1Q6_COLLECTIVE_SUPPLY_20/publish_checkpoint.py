"""Metadata-only C20 publication. No mathematical verifier or source replay.
All mathematical work was source-paper derivation from existing evidence.
"""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
entry=read(B/'entry.json');prior=read(OLD/'resources_checkpoint.json')
required=['SOURCE_SPEC.md','FROZEN_H1Q6_OBLIGATION.md','U19_RECONSTRUCTION.md',
 'H1Q6_RECOVERY_NORMAL_FORM.md','LOCAL_SPARE_LEDGER.md','LEAF_BIRTH_REDUCTION.md',
 'SECOND_NONLOCAL_DONOR.md','RELAY_ZERO_RUN_BOUNDS.md','SHARED_FIRST_RESET_OBSTRUCTION.md',
 'LOCAL_LEAF_BIRTH_OBSTRUCTION.md','REPEATED_RECOVERY_EXPANSION.md','SHARED_RECOVERY_COLLISIONS.md',
 'COLLECTIVE_SOURCE_SUPPLY.md','NONLOCAL_OWNER_EXCHANGE.md','COMPARISON_SAFE_FRONTIERS.md',
 'SEVEN_KEY_MIXTURE_CONTROL.md','ABSOLUTE_PERIOD_VALIDITY.md','ARBITRARY_R_LIFTING.md',
 'GLOBAL_PHYSICAL_INJECTION.md','GATE_U_DISCHARGE.md','UNIFORM_TRANSFER_VERDICT.md',
 'ADVERSARIAL_AUDIT.md','INDEPENDENT_AUDIT_STATUS.md','FINAL_VERDICT.md','CHECKPOINT.md',
 'IAGS_BOXES.md','ORDERED_ANCESTOR_SUPPLY.md','FIRST_DIRECTION_CHANGE_SUPPLY.md',
 'SECOND_DIRECTION_CHANGE_SUPPLY.md','REMAINING_EXTREME_FRAME.md','SATURATED_SOURCE_WITNESS.md',
 'PADDING_THEOREM.md','dependency_ledger.json','saturated_source_word.json','frozen_local_owner_witness.json']
assert all((B/n).is_file() and (B/n).stat().st_size for n in required)
assert not list(B.glob('run_*_result.json')) and not (B/'run_phase.py').exists()
assert not (B/'FULL_PROOF.md').exists()
for p in B.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
assert not git('status','--porcelain','--untracked-files=no')
assert prior['cumulative_CPU']==3619.171875 and prior['cumulative_group_CPU']=={'symbolic':118.671875,'independent':299.125}
out('resources_checkpoint.json',{
 'status':'U20_OPEN_NEW_SOURCE_DERIVATIONS_NO_NEW_EXECUTABLE_PROOF_RUN',
 'prior_cumulative_CPU':prior['cumulative_CPU'],'campaign_bounded_source_proof_controller_CPU':0.0,
 'cumulative_CPU':prior['cumulative_CPU'],'remaining_CPU':7200-prior['cumulative_CPU'],
 'global_allowance':7200,'reserve':5,'cumulative_group_CPU':prior['cumulative_group_CPU'],
 'group_caps':prior['group_caps'],'group_remaining':prior['group_remaining'],
 'symbolic_controller_reserve':1,'symbolic_before_startup_after_reserve':0.328125,
 'independent_remaining_below_controller_reserve':True,'new_controllers':0,
 'new_symbolic_verifier_or_enumerator_processes':0,'new_independent_runs':0,
 'campaign_source_engine_calls':0,'campaign_fresh_source_rotation_replays':0,'campaign_CD6_backend_rows':0,
 'C15_through_C20_source_engine_calls':prior['C15_through_C19_source_engine_calls'],
 'old_queries_and_failed_charges':'all inherited unchanged in pinned predecessor receipts; no counter reset',
 'new_mathematical_source_constructions':['parametric zero-DELETE refinement and padded-A80 fixed-window obstruction','V167 exact source-word recipe with symbolic A/B closure; not executed'],
 'new_concrete_f6_or_effective_owner_maps_executed':0,
 'new_finite_passing_tests_promoted_to_universal_proof':False,
 'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
 'memory_cap_bytes':32*1024**3,'new_source_process_peak_memory':0,'wall_cap_hours':12,'Bank25':25,
 'general_physical_Bank25_realization':'OPEN_NOT_PROMOTED',
 'C15_integrity_suffix':'PENDING_NOT_COMPLETED_BY_METADATA','C16_through_C20_required_audits':'PENDING',
 'no_cap_reset_extension_or_group_reclassification':True,
 'CPU_ledger_scope':'bounded source/proof/verifier/controller processes; no such process runs in20',
 'metadata_CPU_convention':'inherited entry/publication/provenance exclusion only; no source computation relabeled',
 'entry_metadata_CPU_excluded':entry['metadata_CPU_excluded'],'publication_metadata_CPU_excluded':time.process_time()})
out('research_status_ledger.json',{
 'principal_outcome':'UNRESOLVED','U20_H1Q6_JOINT':'OPEN','Gate_U20':'U-OPEN',
 'CD6_I6':'SEALED_UNCHANGED','Gate_U14':'SEALED_SUFFICIENT_IMPLICATION_UNCHANGED',
 'Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
 'G20_guarded_joint_source_donor':'PROVED-DERIVATION_AUDIT_PENDING',
 'O20_order_G_R_C_x':'MATHEMATICAL_DERIVATION_COMPLETE_FOR_CLASS_AUDIT_PENDING',
 'F20_order_G_R_x_C':'MATHEMATICAL_DERIVATION_COMPLETE_FOR_CLASS_AUDIT_PENDING',
 'M20_order_G_C_x_R':'MATHEMATICAL_DERIVATION_COMPLETE_FOR_CLASS_AUDIT_PENDING',
 'all_proved_classes_joint_donor_noncollision':'five-predecessor windows are disjoint for actual deep accesses; all reflections included',
 'remaining_order_G_x_C_R':'OPEN',
 'local_effective_spare_claim':'false if confused with comparison spare; exact old source occupies both bits',
 'fixed_original_operation_window_strategy':'REFUTED_BY_PARAMETRIC_SOURCE_DERIVATION_AUDIT_PENDING',
 'two_predecessor_automatic_coverage':'REFUTED_AT_ORIGINAL_A_B_SOURCE_DERIVATION_SCOPE_BY_V167; no numeric new BE/f6 receipt',
 'V167_third_supplier_comparison_payment':'PROVED-DERIVATION_NOT_EXECUTED_AUDIT_PENDING',
 'larger_support_fixed_Q6_nondeep_beta1_z0':'OPEN','larger_arrival_loads_and_other_full_cores':'OPEN',
 'extra_immutable_comparison_policy_compatibility':'OPEN','general_E_r3_physical_working':'OPEN',
 'main_theorem_refuted':False,'new_independent_audits':0,'new_executable_proof_checks':0,
 'next_bounded_theorem':'joint original-source second-donor supply for G<x<C<R saturated extreme-return frame G(A,C(x(B0,B1),R(D,E)))',
 'superseded_internal_target':'FLIP_FRAME_OBLIGATION G<R<x<C is CLOSED by F20; do not redo',
 'manifest_is_proof_seal':False})
out('publication_provenance.json',{'branch':entry['branch'],'HEAD':entry['head'],
 'tracked_status':git('status','--porcelain','--untracked-files=no'),
 'entry_untracked_inventory':'entry.json','new_write_scope':B.relative_to(ROOT).as_posix(),
 'entry_pins_verified':entry['pins_verified'],'entry_all_pin_check_not_repeated':True,
 'metadata_is_independent_audit':False,'no_new_source_or_verifier_processes':True,
 'old_certificates_and_owner_files_modified':False,'no_destructive_git_operation':True,
 'all_new_results_audit_pending':True,'publication_metadata_CPU_excluded':time.process_time()})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
 for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'CONTENT_CHECKPOINT_NOT_PROOF_SEAL','U20':'OPEN','files':files})
print(json.dumps({'status':'PUBLISHED_U20_OPEN','global_CPU':prior['cumulative_CPU'],
 'group_CPU':prior['cumulative_group_CPU'],'new_source_or_audit_processes':0,'files':len(files)}))
