"""Immutable publication/resource accounting; no mathematical execution."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(n):return json.loads((BASE/n).read_text())
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    first,first_c=read('run_result.json'),read('controller_exit.json')
    r,e,a=read('run_resume_result.json'),read('controller_resume_exit.json'),read('symbolic_audit.json')
    pref,closures,p=read('successful_prefix_checkpoint.json'),read('profile_closures.json'),read('partition_update.json')
    assert first['status']=='FAILED_OR_UNKNOWN_STOP' and first['error']['type']=='AssertionError'
    assert r['status']=='PASS' and r['error'] is e['error'] is None
    assert a['status']=='VISIBLE_GAMMA1_ROOT_REMOVAL_UNIVERSAL_AUDIT_PASS'
    assert pref['status']=='COMPLETED_PREFIX_REUSED_NOT_RERUN' and not pref['mathematical_prefix_reexecuted']
    assert sha(Path(pref['executed_source']))==pref['executed_source_sha256']
    assert sha(BASE/'log_symbolic_audit.txt')==pref['traceback_log_sha256']
    assert a['all_Gamma1_zero_destination_psi_at_least']==1
    assert a['all_eight_visible_profiles_closed'] and a['all_original_quantifiers_retained']
    assert not a['current_potential_changed'] and not a['hidden_source2_destination2_claimed']
    assert not a['D_of_C_used'] and not a['internal_helper_projected_as_leaf']
    assert closures['all_eight_visible_profiles_closed'] and len(closures['profiles'])==8
    assert all(v['status']=='CLOSED_UNIVERSAL' and v['signed_residual_at_least']==0 for v in closures['profiles'])
    assert p['remaining_open']==44 and p['newly_closed']==8 and p['remaining_H1']==36 and p['remaining_hidden_Gamma1']==8
    assert not a['Step4_complete'] and not p['Step4_complete']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0

    prior=761.171875
    first_charge=first['child_CPU']+first_c['whole_process_CPU_seconds']
    continuation_charge=r['child_CPU']+e['whole_process_CPU_seconds']
    charge=first_charge+continuation_charge;total=prior+charge
    assert first_charge==0.453125 and r['prior_uniform_CPU_charge']==prior+first_charge
    assert charge<120 and r['child_CPU']<r['allocated_CPU_cap']<=120-first_charge
    assert total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':prior,'first_audit_status_retained':first['status'],
      'first_checker_CPU_including_failed_run':first['child_CPU'],
      'first_controller_CPU_through_finally':first_c['whole_process_CPU_seconds'],
      'continuation_checker_CPU':r['child_CPU'],'continuation_controller_CPU_through_finally':e['whole_process_CPU_seconds'],
      'new_compute_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,
      'guaranteed_remaining_CPU':7200-total,'reserve':5,'old_signature_campaign_ledger_unchanged':7195.203125,
      'symbolic_phase_CPU_cap':120,'construction_CPU_cap':300,'audit_source_CPU_cap':300,
      'combined_audit_attempts_within_same_symbolic_cap':True,
      'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,
      'RAM_GiB_limit':32,'observed_peak_audit_working_set_bytes':max(first['peak_working_set_bytes_observed'],r['peak_working_set_bytes_observed']),
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,'new_completed_math_prefix_replayed':0,
      'current_caps_preserved':True,
      'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write('resources.json',resources)

    inherited=json.loads((BASE.parent/'M3_XFER14/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(Path(q) for q in a['reused_proof_hashes'])
    paths.update(Path(q) for q in a['source_hashes_reused_not_executed'])
    paths.update(BASE.parent/n for n in (
      'M3_XFER14/ZERO_FRONTIER_THEOREM.md','M3_XFER14/ZERO_PARTITION.md',
      'M3_XFER14/PROOF_AUDIT.md','M3_XFER14/RULE_LABEL_CORRECTION.md',
      'M3_XFER14/certificate.json','M3_XFER14/resources.json','M3_XFER14/symbolic_audit.json',
      'M3_XFER14/final_manifest.json','M3_XFER14/partition.json'))
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'all_core_negative_law_used_without_new_table_query':True,
      'original_full_state_realization_of_auxiliary_C_required':False,
      'files':[{'path':q.as_posix(),'sha256':sha(q)} for q in sorted(paths)]})

    old=read('entry_baseline.json');pins={v['path'] for v in old['files']}
    for i,v in enumerate(old['files']):
        assert sha(Path(v['path']))==v['sha256'],v['path']
        if (i+1)%1000==0:print(json.dumps({'prior_files_unchanged':i+1,'total':len(pins)}),flush=True)
    additions=[q for q in BASE.parent.rglob('*') if q.is_file() and BASE not in q.parents and q.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in q.as_posix() for q in additions),[q.as_posix() for q in additions]
    write('concurrent_additions.json',{'not_mathematical_dependencies':True,
      'files':[{'path':q.as_posix(),'sha256':sha(q)} for q in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],
      'tracked_tree_clean':True,'campaign_writes_confined_here':True,
      'unrelated_concurrent_U4_additions':len(additions)}
    write('integrity.json',integrity)

    certificate={
      'status':'PROVED_UNIVERSAL_ON_ALL_EIGHT_VISIBLE_GAMMA1_ZERO_PROFILES',
      'theorem':'EXTREME_HELPER_ROOT_REMOVAL_DESTINATION_FLOOR_AND_VISIBLE_SIGNED_REPAYMENT',
      'fixed_current_potential':'D_exp from Transfer13 UNCHANGED',
      'all_eight_visible_profiles_closed':True,
      'closed_profile_ids':[v['id'] for v in closures['profiles']],
      'universal_scope':'all original masks, admissible sigma and compatible independent private witnesses of each original profile',
      'auxiliary_C':'proper ordered nine-core tree from the nonempty child of the intermediate extreme helper root',
      'auxiliary_C_terminal_depth':7,'auxiliary_C_ordinary_splay_equals_original_final_core':True,
      'all_original_Gamma1_zero_destination_psi_at_least':1,
      'visible_profile_source_D_at_most':1,'all_visible_profile_original_signed_residuals_at_least':0,
      'exact_repayment':'(D_t-psi_t)+(psi_t-psi_C-1)+psi_C+(1-D_s) = D_t-D_s >=0',
      'original_H2_q_and_weight':{'H':2,'q':4,'weight':0},
      'auxiliary_core_weight_minus1_does_not_reprice_original_edge':True,
      'auxiliary_C_needs_new_original_full_state_or_private_inventory':False,
      'D_of_C_or_private_erasure_invariance_used':False,
      'independent_audit':'PASS: separate universal constructor/coefficient checks plus analytic source/quantifier audit',
      'failed_first_component_preserved':'dependency long-path lookup; mathematical prefix reused without rerun; source/coverage continuation passed',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'current_potential_or_original_graph_changed':False,'all_previously_valid_rows_preserved_literally':True,
      'R1_R4_preserved':True,'h0_correction_preserved':True,
      'full147_ordinary_and127_midpoint_fields_preserved':True,'SAME_actual_midpoint_preserved':True,
      'independent_scopes_free_HIGH_v_weak_LE_G_unused_fields_preserved':True,
      'corrected_h0':{'actual':0,'declared':18,'q':9,'weight':-3},
      'requested_eight_visible_profile_task_achieved':True,
      'Step4_complete':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_H1_schematic_slots':36,'remaining_hidden_Gamma1_schematic_slots':8,
      'hidden_only_possible_failure':{'source_D':2,'target_D':1},
      'any_remaining_cell_nonemptiness_asserted':False,'hidden_source2_repayment_claimed':False,
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'new_finite_tests':0,'new_original_state_or_psi_queries':0,
      'NET_ADVANCEMENT':'all eight visible original Gamma1 zero profiles signed-valid; target0 excluded on every Gamma1 zero by the same lemma',
      'resources':resources,'integrity':integrity}
    write('certificate.json',certificate)
    result=f'''# All eight visible Gamma1 zero profiles are proved

The fixed current D_exp requires no change. Removing the extreme helper
ROOT from the intermediate B tree leaves a proper nine-core tree C with
terminal depth7. Its ordinary core splay equals the ACTUAL final B core:
three common core pairs commute with projection, and the final helper
RR/LL pair becomes the last ordinary core zig after the valid proxy
leaf is removed. The saved complete negative-core law therefore gives

    psi(core(B_t)) >= psi(C)+1 >=1.

Each visible source already has D(s)<=1 through its separate original
negative H1. Thus the original H2,q4,w0 row has the exact repayment

    D(t)-D(s)
      = (D(t)-psi_t)+(psi_t-psi_C-1)+psi_C+(1-D(s)) >=0.

This closes ALL eight MIN/MAX visible profiles for every original mask,
admissible signature and compatible private witness. No inventory for C,
D(C), shared witness or helper-erasure invariant is introduced. C is a
pure core-tree argument of the old psi, not a new graph vertex. Original
H/q/weights/full endpoints remain unchanged. Raw G, unused fields and
source-incompatible target alpha boundaries are included.

The separate audit passes12 universal constructor identities, depth/price
arithmetic, exact signed coefficients, source semantics/provenance and
all eight profile interfaces. The first component stopped ONLY at an
unprefixed Windows long-path dependency lookup. It remains FAILED in
its immutable record. Its completed math/source prefix was retained,
not rerun; the unfinished provenance/coverage continuation passed with
extended-path handling. Both attempts are charged. This is not external
review or a full compiler formalization.

The SAME global target floor excludes debt0 on every Gamma1 zero,
including hidden-terminal profiles. It does NOT repay a hidden source2:
their only possible failure is now2->1. The updated old52-slot partition
records8 CLOSED and44 OPEN:36 H1 plus8 hidden Gamma1. These are universal
schemas, not finite signature jobs, tests or asserted counterexamples.
Full Step4, M3 and Dynamic Optimality remain OPEN. No new original
negative cycle or whole-signature certificate is claimed.

R1-R4, full147-O/127-M, SAME actual midpoint, independent scopes, free
HIGH v, weak LE/G/raw unused fields, original prices and corrected h0
(actual0,declared18,q9,w=-3) remain. All{len(pins)} old files, HEAD and
tracked tree are unchanged. No finite tests, original source/root/psi
queries, fits, bank censuses or completed semantic-check replays ran.

Charged new CPU including BOTH audit attempts={charge}; cumulative
{total}/7200; remaining{7200-total}, including reserve5. Per-phase
120/300/300,2m queries/live records,4m DAG,5m edges and32GiB remain.
Metadata bookkeeping follows the existing accounting convention.

Proof: VISIBLE_GAMMA1_REPAYMENT.md. Separate audit: PROOF_AUDIT.md,
AUDIT_RESUME_RECORD.md, successful_prefix_checkpoint.json and symbolic_audit.json.
Exact eight closures: profile_closures.json. Updated partition: partition_update.json.
Machine certificate: certificate.json. Frozen prior files remain untouched.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':q.as_posix(),'sha256':sha(q)} for q in sorted(BASE.rglob('*')) if q.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'visible_profiles_closed':8,
      'remaining_H1':36,'remaining_hidden_Gamma1':8,'Step4':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
