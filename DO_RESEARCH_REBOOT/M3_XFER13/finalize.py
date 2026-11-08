"""Immutable publication/resource accounting only; no mathematical execution."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(name):return json.loads((BASE/name).read_text())
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    r,e,a=read('run_result.json'),read('controller_exit.json'),read('symbolic_audit.json')
    assert r['status']=='PASS' and r['error'] is e['error'] is None
    assert a['status']=='NON_EXTREMAL_EXPOSURE_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for name in ('EB_ER_change_no_actual_LOW_source','one_credit_rows_proved_when_source_newly_raised_to1',
      'each_previously_valid_LOW_row_preserved_by_each_operation','all_T_G_source_original_LOW_rows_proved',
      'target_non_extremal_and_new_lower_mark_exposure_included',
      'all_admissible_signatures_upper_U_and_private_completions'):
        assert a[name],name
    assert not a['all_already_debt2_auxiliary_sources_claimed_solved']
    assert a['scope_countercheck_floor1_does_not_pay_arbitrary_source2_zero']=={'constant':-1}
    assert a['main_G_zero_H1_signed_residual']==0
    assert not a['Step4_complete'] and not a['all_non_extremal_H1_zero_coverage_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    prior=760.5625
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=prior+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':prior,'new_symbolic_checker_CPU':r['child_CPU'],
      'new_controller_CPU_through_finally':e['whole_process_CPU_seconds'],'new_compute_CPU':charge,
      'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'reserve':5,
      'old_signature_campaign_ledger_unchanged':7195.203125,
      'symbolic_phase_CPU_cap':120,'construction_CPU_cap':300,'audit_source_CPU_cap':300,
      'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,
      'RAM_GiB_limit':32,'observed_peak_audit_working_set_bytes':r['peak_working_set_bytes_observed'],
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,'current_caps_preserved':True,
      'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously',
    }
    write('resources.json',resources)
    inherited=json.loads((BASE.parent/'M3_XFER12/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(BASE.parent/n for n in (
      'M3_XFER12/DEPTH_FIVE_RELAY_THEOREM.md','M3_XFER12/STEP4_COVERAGE_AUDIT.md',
      'M3_XFER12/PROOF_AUDIT.md','M3_XFER12/certificate.json','M3_XFER12/resources.json',
      'M3_XFER12/symbolic_audit.json','M3_XFER12/final_manifest.json'))
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'saved_coverage_gap_now_closed_on_its_exact_stated_source_family':True,
      'new_psi_or_bank_facts_required':False,
      'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(paths)]})
    old=read('entry_baseline.json');pins={v['path'] for v in old['files']}
    for i,v in enumerate(old['files']):
        assert sha(Path(v['path']))==v['sha256'],v['path']
        if (i+1)%1000==0:print(json.dumps({'prior_files_unchanged':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write('concurrent_additions.json',{'not_mathematical_dependencies':True,
      'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],
      'tracked_tree_clean':True,'campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)}
    write('integrity.json',integrity)
    certificate={
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'NON_EXTREMAL_MARKED_GRANDCHILD_LOWER_MARK_EXPOSURE_SIGNED_RELAY',
      'input_class':'any public D45<=D<=2; no global LOW feasibility assumption',
      'mask_minus':[0,2,4,5,8],'mask_actual_opposite':[0,3,4,6,8],
      'main_G_minus':'root5, A L4/LL2, nonreal LR/R; core5,L4,L3,L0,R1,R2 with arbitrary upper U6..8',
      'main_G_actual_opposite':'root3, A R4/RR6, nonreal L/RL; core3,R4,R5,R8,L7,L6 with arbitrary lower U0..2',
      'target_non_extremal':True,'both_ancestors_marked':True,'main_sources_outside_S':True,
      'main_B_target_depth':5,'main_original_H':1,'main_original_terminal_q':2,'main_original_weight':0,
      'newly_exposed_lower_mark_private_position_not_restricted':True,
      'ordered_operations':['floor1_EB_ER','floor1_H','floor1_CA_CB','floor1_R','cap2_T','cap2_G'],
      'explicit_current_debt':'D_exp=max(D45,1_EB,1_ER,1_H,1_CA,1_CB,1_R,2*1_T,2*1_G), including actual opposite classes',
      'each_previously_valid_LOW_row_preserved_by_each_operation':True,
      'all_T_G_source_original_LOW_rows_proved':True,
      'main_zero_H1_source_and_target_values':2,'main_zero_H1_signed_residual':0,
      'T_left_branch_unrestricted':True,'CA_right_branch_unrestricted':True,
      'ER_parent_type_and_label_unrestricted_in_public_guard':True,
      'all_return_predicates_no_V_filter_or_fresh_completion_test':True,
      'EB_ER_all_actual_sources_E1':True,'EB_ER_change_no_actual_LOW_source':True,
      'H_zero2_all_marked_core_depths_at_most':2,
      'one_credit_auxiliary_rows_proved_when_newly_raised_to1':True,
      'all_already_debt2_auxiliary_sources_claimed_solved':False,
      'T_CA_CB_Score_bearing_Gamma1_handled_by_completed_global_deep_helper_theorem':True,
      'T_minimum_initial_B_proxy_depth':3,'CB_minimum_initial_B_proxy_depth':4,
      'CA_CB_maximum_initial_B_proxy_depth_lower_bound':3,
      'H_R_shallow_helpers_original_H2_weight_at_least':3,
      'Gamma0_actual_preterminal_floor_reused':True,
      'all_admissible_signatures_and_arbitrary_upper_U_private_completions':True,
      'all_nonnegative_incoming_T_G_rows_valid':True,
      'all_incoming_weight_ge1_auxiliary_rows_valid':True,
      'blanket_zero_incoming_floor1_or_invalid_negative_incoming_repair_claimed':False,
      'private_inventory_persistence_or_weak_LE_strengthening':False,
      'strict_numeric_old_debt_increase_claimed':False,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'saved_Step4_non_extremal_exposure_gap_closed_for_this_family':True,
      'all_non_extremal_H1_zero_coverage_proved':False,
      'Step4_status':'OPEN','global_zero_LOW_coverage_proved':False,
      'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['other non-extremal masks/core topologies and original H1 zero classes',
        'auxiliary already-debt2 zero rows not otherwise proved',
        'remaining shallow Gamma1 zeros and exhaustive original zero-LOW coverage'],
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_row_coverage':-7,'full_closed_walk_bound_with_stated_row_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'saved non-extremal marked-grandchild exposure family uniformly repaid for arbitrary signatures/private completions, including anonymous-separated0, with explicit safe one-credit/two-credit construction',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# The saved non-extremal exposure family is closed

The new theorem covers mu={{0,2,4,5,8}}, marked source root5, marked
parent4 at A L, non-extremal marked target2 at LL, nonreal LR/R, and
the displayed core path5,L4,L3,L0,R1,R2 with arbitrary upper U6..8.
The ACTUAL opposite family has mask{{0,3,4,6,8}} and target6 exposing8.

The original zero2 access puts the full endpoint in T: root2, A R4/RR5,
with its left branch UNRESTRICTED. Mark0 may be a child, a grandchild
under an anonymous/unmarked parent, hidden in a port or deeper. Every
compatible private witness and original admissible sigma is included.
The exact saved coverage-audit exposure example is therefore discharged
uniformly; no finite instance or saved potential label is evaluated.

The explicit ordered public construction adds floor1 to EB/ER,H,CA/CB,R,
then cap2 to T,G:
    D_exp=max(D45,1_EB,1_ER,1_H,1_CA,1_CB,1_R,2*1_T,2*1_G).
Every operation preserves EVERY previously valid original LOW row.
All T/G-source LOW rows hold. Every main zero H1 row has debt2->2 and
exact residual0; nonnegative incoming T/G rows are protected.

The +1 exits of T use one-credit returns, not an unknown two-credit
fixed point. CA has NO right guard: R's next hidden branch can change
under a fresh witness. ER has no parent type/label guard. All returns
retain full G boundaries. EB/ER change NO actual LOW source because
every actual source is already E1. The completed global deep-helper
theorem handles Score-bearing helpers that expose0; original q, final
validity and Gamma0 floor remain intact.

SCOPE: cap1 stages prove newly raised source1 rows and preserve old
valid rows. They do NOT declare every auxiliary source already at2
solved. Incoming weight>=1 to cap1 is safe; zero incoming needs source
debt<=1. The independent audit explicitly checks this distinction.

The fresh universal symbolic/source/sign audit passed all new core/A
identities, three lower-mark return positions, three upper return
positions, helper exclusions/depths, boundary/floor reasoning and signed
slacks. A separate prose audit checks quantifiers, source legality,
sharing, dependencies and nonvacuity. Completed semantics/deep-helper
proofs were reused by pinned hashes, not rerun. No finite tests, source/
root/psi queries, bank censuses or label fits ran. This is not full
compiler formalization or external human/model review.

Other non-extremal masks/topologies, auxiliary already-debt2 zeros not
otherwise proved, and remaining shallow Gamma1 zeros are OPEN. Full
Step4, M3 and Dynamic Optimality remain OPEN. No new whole-signature
certificate or original negative cycle is claimed.

R1-R4/current caps, full147-O/127-M closure, SAME actual midpoint,
independent scopes, free high v, weak LE/G/unused fields, original H/q/
prices and corrected h0 remain. All{len(pins)} pinned prior files, HEAD
and tracked tree are unchanged. New charged CPU={charge};
cumulative={total}/7200; remaining={7200-total}, including reserve5.
Per-phase120/300/300,2m queries/live records,4m DAG,5m edges and32GiB
caps remain. Metadata hashing uses the established accounting convention.

Proof: NON_EXTREMAL_EXPOSURE_THEOREM.md. Separate audit: PROOF_AUDIT.md.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'saved_non_extremal_exposure_family':'PROVED',
      'main_zero_signed_residual':0,'all_auxiliary_debt2_rows_claimed':False,'Step4':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()

