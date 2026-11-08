"""Immutable publication and ledger only; no mathematical execution."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(n):return json.loads((BASE/n).read_text())
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    r,e,a=read('run_result.json'),read('controller_exit.json'),read('symbolic_audit.json')
    p=read('partition.json')
    assert r['status']=='PASS' and r['error'] is e['error'] is None
    assert a['status']=='ZERO_FRONTIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert a['Gamma1_helper_depth1_zero_global_signed_residual_at_least']==1
    assert a['Gamma1_zero_terminal_depth_exact']==8
    assert a['H1_zero_target_core_height_at_most']==7
    assert a['partition_exhaustive_case_definition'] and a['all_original_quantifiers_retained']
    assert not a['residual_cells_closed'] and not a['Step4_complete'] and not a['current_potential_changed']
    assert not a['hidden_Gamma1_source_cap_below2_claimed'] and not a['target_floor_inferred_from_upper_capacity']
    assert a['nonnegative_residual_algebra']['negative_H1_source_upper1']=={
      'parallel_target_room_to2':1,'negative_residual':1}
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    assert p['number_of_residual_schematic_slots']==52 and not p['all_residual_cells_closed']
    assert all(c['status']=='OPEN' and not c['nonemptiness_asserted'] for c in p['cells'])
    prior=760.8125
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
      'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write('resources.json',resources)

    inherited=json.loads((BASE.parent/'M3_XFER13/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(Path(q) for q in a['reused_proof_hashes'])
    paths.update(Path(q) for q in a['source_hashes_reused_not_executed'])
    paths.update(BASE.parent/n for n in (
      'M3_XFER13/NON_EXTREMAL_EXPOSURE_THEOREM.md','M3_XFER13/PROOF_AUDIT.md',
      'M3_XFER13/certificate.json','M3_XFER13/resources.json','M3_XFER13/symbolic_audit.json',
      'M3_XFER13/final_manifest.json','M3_EXPOSURE02/ADDENDUM_RANGE_ARGUMENT.md'))
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'new_psi_or_bank_facts_required':False,
      'old_signature_potentials_not_imported_into_current_row_proof':True,
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
      'status':'PROVED_ZERO_FRONTIER_REDUCTION_WITH_OPEN_SIGNED_LEAVES',
      'theorem':'UNIVERSAL_ORIGINAL_ZERO_LOW_FRONTIER_AND_EXHAUSTIVE_SCHEMATIC_PARTITION',
      'current_potential':'D_exp from Transfer13 UNCHANGED',
      'all_previously_valid_rows_preserved_literally':True,
      'original_state_graph_or_private_witness_scope_changed':False,
      'Gamma1_helper_B_depth1_zero_global_signed_residual_at_least':1,
      'Gamma1_terminal_pre_B_depth9_zero_impossible':True,
      'Gamma1_helper_B_depth2_Score_empty_zero_impossible':True,
      'Gamma1_helper_B_depth_ge3_zero_impossible_reused':True,
      'Gamma1_depth2_central_root_and_wrong_terminal_side_zero_impossible':True,
      'H1_zero_destination_core_height8_impossible':True,
      'H1_possible_current_failure_requires_seed_drop':[[1,0],[2,0],[2,1]],
      'H1_psi1_source_core_height_at_most':7,'H1_psi2_source_core_height_at_most':5,
      'visible_Gamma1_profiles_source_D_at_most':1,
      'hidden_Gamma1_profiles_source_cap_below2_claimed':False,
      'partition_exhaustive_case_definition':True,
      'public_edge_partition_disjointness':'ordered subtraction after projection of original witness classes',
      'H1_residual_schematic_slots':36,'Gamma1_visible_residual_slots':8,'Gamma1_hidden_residual_slots':8,
      'all_52_slots_closed':False,'any_residual_cell_nonemptiness_asserted':False,
      'signed_repayment_of_residual_cells_proved':False,
      'independent_audit':'PASS: separate universal term/linear/source-scope audit; signed closure gate OPEN',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'Step4_complete':False,'Step4_status':'OPEN','full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'requested_full_completion_achieved':False,
      'remaining_open':['36 critical-seed H1 word/depth schemas, all other original variables quantified',
        '8 source-visible shallow Gamma1 root/side profiles requiring destination repayment',
        '8 originally hidden depth3 Gamma1 helper/terminal profiles permitting source debt2'],
      'R3_stop_reason':'second independent open signed repayment theorem needed to close surviving cells',
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'new_finite_tests':0,'new_original_state_or_psi_queries':0,
      'R1_R4_preserved':True,'h0_correction_preserved':True,
      'full147_ordinary_and127_midpoint_fields_preserved':True,'SAME_actual_midpoint_preserved':True,
      'independent_scopes_free_HIGH_v_weak_LE_G_unused_fields_preserved':True,
      'original_H_q_prices_preserved':True,
      'corrected_h0':{'actual':0,'declared':18,'q':9,'weight':-3},
      'resources':resources,'integrity':integrity}
    write('certificate.json',certificate)
    result=f'''# Exhaustive partition built; Step4 signed closure remains open

The decision tree covers every original zero-weight LOW edge through
the completed H1/Gamma0/Gamma1 normal forms. It retains all old row
theorems with their exact source-credit and incoming qualifications.
It is a partition of universal original-constraint formulas, not a finite
signature census. Projected witness classes are disjointized by priority
without identifying full public states or sharing private inventories.

New universal closures/reductions:

* EVERY Gamma1 zero with initial helper B depth1 has signed residual>=1
  for the current D_exp, by a SAME-full-endpoint parallel NEGATIVE H1 row.
* Gamma1 terminal pre-B depth9 is impossible. Depth2 Score-empty helpers
  have no zero. Core counts eliminate central-root/wrong-side depth2
  cases, leaving exactly eight visible and eight hidden frontier profiles.
* EVERY zero H1 target has core height<=7. Any possible current H1
  failure traces back to seed drops(1,0),(2,0),(2,1), with the proved
  source-height restrictions. No numerical psi label was queried.

The unresolved signed leaves are36 H1 word/depth/seed schemas and16
Gamma1 profiles. Every cell retains arbitrary original masks/topologies,
raw fields, admissible signatures and compatible independent witnesses.
They are52 SCHEMATIC OBLIGATIONS, not52 observed failures or signatures.
No cell is asserted nonempty. They do not yet have signed closure proofs.
Visible Gamma1 source debt is<=1, but its required destination floor is
unproved on the full profile. Hidden-terminal sources can still be2.
The H1 residuals need a general G/inventory-safe repayment theorem.

The new bounded audit PASS covers18 universal constructor identities,
integer/slack arithmetic, arbitrary-subtree counts, coverage/scopes and
dependency provenance, with a separate prose audit. It does NOT certify
the OPEN signed leaves. This is not external review or full compiler
formalization. The unexecuted initial checker was retained and corrected
in v2 before the ONLY new bounded audit run; no completed check was replayed.

R1-R4 require actual row closures. A second independent open repayment
theorem is needed here, so the R3 stop applies. Requested full Step4
completion is NOT ACHIEVED. Step4, M3 and Dynamic Optimality remain OPEN.
No original negative cycle or new whole-signature certificate is claimed.

The current D_exp and original graph are unchanged. Full147-O/127-M,
SAME actual midpoint, independent scopes, free HIGH v, weak LE/G/unused
fields, original H/q/prices, and h0(actual0,declared18,q9,w=-3) remain.
All{len(pins)} pinned prior files, Git HEAD and tracked tree are unchanged.
Finite tests, original source/root/psi queries, fits and bank censuses:0.

New charged CPU={charge}; cumulative={total}/7200; remaining={7200-total},
including reserve5. Per-phase120/300/300,2m query/live-record,4m DAG,5m
edge and32GiB caps are unchanged. Metadata hashes follow the established
accounting convention.

Partition: ZERO_PARTITION.md and partition.json. Proof: ZERO_FRONTIER_THEOREM.md.
Audit: PROOF_AUDIT.md, AUDIT_ADDENDUM.md and symbolic_audit.json.
Exact unmet goal: CLOSURE_STATUS.md. Machine status: certificate.json.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':q.as_posix(),'sha256':sha(q)} for q in sorted(BASE.rglob('*')) if q.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'partition_exhaustive':True,
      'signed_leaves_closed':False,'Step4':'OPEN','M3':'OPEN','new_compute_CPU':charge,
      'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
