"""Immutable proof publication and CPU ledger; no mathematical execution."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(n):return json.loads((BASE/n).read_text())
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    r,e,a=read('run_result.json'),read('controller_exit.json'),read('symbolic_audit.json')
    c,p,g=read('hidden_profile_closures.json'),read('partition_update.json'),read('cap_exclusion_registry.json')
    assert r['status']=='PASS' and r['error'] is e['error'] is None
    assert a['status']=='HIDDEN_GAMMA1_SAFE_CEILING_UNIVERSAL_AUDIT_PASS'
    for key in ('all_height_ge7_cores_psi_zero','all_exception_source_old_caps_vanish',
      'new_floor_psi_and_range_preserved','every_previously_valid_original_LOW_row_preserved',
      'HIGH_h0_glue_preserved','all_eight_hidden_profiles_closed','old_eight_visible_profiles_preserved',
      'all_original_quantifiers_and_coordinates_retained'):
        assert a[key],key
    assert not a['new_F_ge_Lambda_claimed'] and not a['Step4_complete']
    assert g['all_current_D_exp_terms_included'] and len(g['entries'])==13
    assert g['exception_D_exp_equals_Lambda_at_most']==1
    assert c['all_eight_hidden_profiles_closed'] and len(c['profiles'])==8
    assert all(v['source_in_H'] and v['source_F_at_most']==1 and v['target_F_at_least']==1
      and not v['old_D_exp_2_to1_claimed_valid_without_ceiling'] for v in c['profiles'])
    assert p['remaining_open_H1_schemas']==36 and p['remaining_open_Gamma1_zero_schemas']==0
    assert p['all_visible_and_hidden_Gamma1_slots_closed']==16 and not p['new_F_ge_Lambda_claimed']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    assert len(a['new_universal_constructor_certificates'])==44
    prior=762.015625;charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=prior+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and charge<120 and total<7200-5
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
      'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write('resources.json',resources)
    write('debt_definition.json',{
      'name':'D_hid','old_debt':'D_exp from Transfer13 unchanged as an inherited function',
      'formula':'min(D_exp(s),1) if H_min(s) or H_max(s), else D_exp(s)',
      'H_min':{'valid_ordered_nine_core_projection':True,'A_Score_root_equals_B_root':True,
        'root_in':[7,8],'core_left_child':0,'core_height_at_least':7,
        'alpha_L_kind':0,'anonymous_clause':'An(LL) or (An(L) and An(LR))',
        'exclude_nonroot_alpha_kind0_isS_true_index':0},
      'H_max':{'valid_ordered_nine_core_projection':True,'A_Score_root_equals_B_root':True,
        'root_in':[0,1],'core_right_child':8,'core_height_at_least':7,
        'alpha_R_kind':0,'anonymous_clause':'An(RR) or (An(R) and An(RL))',
        'exclude_nonroot_alpha_kind0_isS_true_index':8},
      'An_definition':'alpha.kind=0 and alpha.isS=false; unused index unrestricted',
      'new_shared_observable_or_private_witness_coordinate':False,
      'root_unused_kind_and_all_other_unnamed_unused_fields_unrestricted':True,
      'old_invalid_core_totalization_retained':True,'floor_psi_retained':True,
      'E1_floor1_retained':True,'floor_Lambda_retained':False,
      'old_rows_transported_by_safe_ceiling_theorem_not_Lambda_input_premise':True})

    inherited=json.loads((BASE.parent/'M3_XFER15/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(Path(v) for v in a['reused_proof_hashes'])
    paths.update(Path(v) for v in a['source_hashes_reused_not_executed'])
    paths.update(BASE.parent/n for n in (
      'M3_XFER15/VISIBLE_GAMMA1_REPAYMENT.md','M3_XFER15/PROOF_AUDIT.md',
      'M3_XFER15/certificate.json','M3_XFER15/resources.json','M3_XFER15/symbolic_audit.json',
      'M3_XFER15/partition_update.json','M3_XFER15/final_manifest.json',
      'M3_AER01/RESULT.md','M3_XFER16/../RESEARCH_RULES.md'))
    # Resolve the one explicit parent reference into the same prior rule file.
    paths={q.resolve() for q in paths}
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'new_saved_psi_values_or_private_inventory_facts_required':False,
      'old_Lambda_input_premise_not_asserted_for_new_debt':True,
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
      'status':'PROVED_SAFE_PUBLIC_CEILING_AND_ALL_EIGHT_HIDDEN_GAMMA1_ZERO_PROFILES',
      'theorem':'INCOMING_SAFE_TALL_CORE_SOURCE_CEILING_WITH_HIDDEN_GAMMA1_REPAYMENT',
      'new_public_debt':'D_hid=min(D_exp,1) on H, D_exp elsewhere',
      'exact_public_definition':'debt_definition.json and HIDDEN_GAMMA1_REPAYMENT.md equation(1)-(2)',
      'potential_assignment_changed':True,'original_graph_architecture_or_state_coordinates_changed':False,
      'all_height_ge7_core_psi_values_zero_proved_without_queries':True,
      'negative_H1_incoming_to_H_impossible':True,'zero_Gamma1_incoming_to_H_impossible':True,
      'only_zero_H1_incoming_exceptions':a['only_exceptional_zero_H1_incoming'],
      'exceptional_sources_D_exp_at_most':1,'all_old_cap_terms_inspected':True,
      'every_previously_valid_original_LOW_row_preserved':True,'HIGH_and_h0_glue_preserved':True,
      'new_range_0_2_and_psi_floor_preserved':True,'new_E1_floor1_preserved':True,
      'new_Lambda_floor_claimed':False,
      'all_eight_hidden_profiles_closed':True,'closed_hidden_profile_ids':[v['id'] for v in c['profiles']],
      'hidden_original_source_A_terminal_depth':3,'hidden_source_F_at_most':1,'hidden_target_F_at_least':1,
      'exact_original_signed_repayment':'0+F(t)-F(s)=(F(t)-1)+(1-F(s))>=0',
      'old_D_exp_2_to1_rows_claimed_valid_without_ceiling':False,
      'all_previous_visible_profiles_preserved':True,
      'global_zero_Gamma1_rows_proved_using_completed_normal_forms':True,
      'Gamma0_zero_rows_retained_for_any_range_two_psi_floor_debt':True,
      'new_universal_constructor_identities':44,'independent_audit':'PASS: separate universal term/sign audit plus complete analytic source/cap-guard audit',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'R1_R4_preserved':True,'h0_correction_preserved':True,
      'full147_ordinary_and127_midpoint_fields_preserved':True,'SAME_actual_midpoint_preserved':True,
      'independent_scopes_free_HIGH_v_weak_LE_G_unused_fields_preserved':True,
      'original_H_q_weights_preserved':True,'corrected_h0':{'actual':0,'declared':18,'q':9,'weight':-3},
      'requested_hidden_profile_task_achieved':True,'Step4_complete':False,
      'remaining_open_H1_schemas':36,'remaining_open_Gamma1_zero_schemas':0,
      'old_H1_seed_index_bridge':'any D_hid failure is an old D_exp failure; changed targets have no H1 failure',
      'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'any_remaining_cell_nonemptiness_asserted':False,'original_negative_cycle_certified':False,
      'new_whole_signature_certificates':0,'new_finite_tests':0,'new_original_state_or_psi_queries':0,
      'NET_ADVANCEMENT':'all eight hidden Gamma1 zero profiles signed-valid under a proved row-preserving public ceiling; all Gamma1 zero coverage complete',
      'resources':resources,'integrity':integrity}
    write('certificate.json',certificate)
    result=f'''# All eight hidden Gamma1 zero profiles are closed

The new explicit debt is

    D_hid(s)=min(D_exp(s),1) on H, D_exp(s) elsewhere.

H is the public tall-core/anonymous-prefix region defined in the proof.
Every original hidden source belongs to it. This changes the potential
assignment; it does NOT assert an old debt2->1 row was nonnegative with
the old values fixed. The original graph, exact target and architecture
remain unchanged.

The proof audits INCOMING rows before lowering anything. Negative core
accesses end at height<=6, so the completed psi recurrence gives psi0
at height>=7. Thus the ceiling retains the psi floor. Negative H1 and
zero Gamma1 cannot enter H. The exhaustive11 zero-H1 spine schemas
leave only old8->7 at depth4, and actual opposite old0->1. Complete
inspection of every saved cap proves those old sources already have
debt<=1. Positive incoming rows are range-safe at target1; Gamma0 uses
its saved theorem for any psi-floor debt. Hence EVERY previously valid
original LOW row survives, and HIGH/h0 retains the range glue.

The destination floor from Transfer15 is unchanged. Every hidden zero
now has source<=1 and target>=1, so its original signed residual is

    0+D_hid(t)-D_hid(s)
        = (D_hid(t)-1)+(1-D_hid(s)) >=0.

All8 hidden and8 previous visible Gamma1 profiles are CLOSED for D_hid,
for every original admissible signature and compatible private witness.
Together with the completed exclusions/helper-depth1 result, no Gamma1
zero case remains open. The36 H1 schemas still need proofs. Their old
seed indices are retained through ROW-preservation contrapositive,
not by falsely assuming D_hid>=Lambda. The latter is NOT asserted.
The E1 floor1 and all old valid rows are retained. Full Step4/M3/
Dynamic Optimality remain OPEN. No original negative cycle or new
whole-signature certificate is claimed.

The separate new audit passed44 universal constructor identities,
height/count induction, signs, all13 cap interfaces, source semantics,
full-state/G/unused-field scope, and all8 profile bridges. One syntax
issue was fixed in a new file BEFORE execution; only audit_v2.py ran,
once. No completed semantic checker was replayed. This is not external
review or a full compiler formalization. No finite tests, original
source/root/psi queries, bank censuses or label fits ran.

R1-R4, all147-O/127-M, SAME actual midpoint, independent scopes, free
HIGH v, weak LE/G/raw unused fields, original H/q/weights and corrected
h0(actual0,declared18,q9,w=-3) remain. All{len(pins)} old files, Git HEAD
and tracked tree are unchanged. All writes are confined to this new
campaign; previous certificates retain their original potential names.

Charged new CPU={charge}; cumulative{total}/7200; remaining{7200-total},
including reserve5. Per-phase120/300/300,2m queries/live records,4m DAG,
5m edges and32GiB remain. Metadata hashing follows the existing convention.

Proof: HIDDEN_GAMMA1_REPAYMENT.md. Complete cap audit: CAP_EXCLUSION.md.
Separate audit: PROOF_AUDIT.md and symbolic_audit.json. Exact new function:
debt_definition.json. Closures: hidden_profile_closures.json. Correct
remaining-case interface: PARTITION_UPDATE.md and partition_update.json.
Machine certificate: certificate.json. No requested work on the eight
hidden profiles remains; the wider Step4 H1 task is still open.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':q.as_posix(),'sha256':sha(q)} for q in sorted(BASE.rglob('*')) if q.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'hidden_profiles_closed':8,
      'remaining_Gamma1_zero_cases':0,'remaining_H1_schemas':36,'Step4':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
