"""Immutable publication/ledger; no mathematical execution."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(n):return json.loads((BASE/n).read_text())
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    first,fc=read('run_result.json'),read('controller_exit.json')
    r,e,a=read('run_resume_result.json'),read('controller_resume_exit.json'),read('symbolic_audit.json')
    s,g,p=read('checkpoint01_source.json'),read('checkpoint02_sign.json'),read('partition_update.json')
    assert first['status']=='FAILED_OR_UNKNOWN_STOP'
    assert r['status']=='PASS' and r['error'] is e['error'] is None and s['status']==g['status']=='PASS'
    assert a['status']=='TERMINAL_ROOT_NORMALIZATION_UNIVERSAL_AUDIT_PASS'
    assert a['all_original_LOW_destinations_P'] and a['every_previously_valid_LOW_row_preserved']
    assert a['all_unmarked_source_LOW_rows_proved'] and a['HIGH_h0_glue_preserved']
    assert a['psi_floor_at_all_LOW_destinations_preserved'] and a['all_completed_Gamma1_zero_rows_preserved']
    assert not a['global_psi_floor_for_new_debt_claimed'] and not a['global_E1_floor1_for_new_debt_claimed']
    assert not a['Step4_complete'] and not a['requested_full_Step4_closure_achieved']
    assert p['remaining_H1_schematic_slots']==36 and p['remaining_Gamma1_zero_slots']==0
    assert all(v['source_root_must_be_marked'] for v in p['cells'] if v['status']=='OPEN')
    assert not a['completed_source_sign_checkpoints_reexecuted']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    prior=762.53125;first_charge=first['child_CPU']+fc['whole_process_CPU_seconds']
    continuation=r['child_CPU']+e['whole_process_CPU_seconds'];charge=first_charge+continuation;total=prior+charge
    assert first_charge==0.5 and r['prior_uniform_CPU_charge']==prior+first_charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120-first_charge and charge<120 and total<7200-5
    resources={'prior_uniform_CPU_charge_retained':prior,
      'first_checker_CPU_including_failed_run':first['child_CPU'],'first_controller_CPU_through_finally':fc['whole_process_CPU_seconds'],
      'continued_checker_CPU':r['child_CPU'],'continued_controller_CPU_through_finally':e['whole_process_CPU_seconds'],
      'new_compute_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,
      'guaranteed_remaining_CPU':7200-total,'reserve':5,'old_signature_campaign_ledger_unchanged':7195.203125,
      'symbolic_phase_CPU_cap':120,'construction_CPU_cap':300,'audit_source_CPU_cap':300,
      'combined_attempts_within_original_symbolic_cap':True,
      'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'RAM_GiB_limit':32,
      'observed_peak_audit_working_set_bytes':max(first['peak_working_set_bytes_observed'],r['peak_working_set_bytes_observed']),
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'new_saved_psi_queries':0,
      'new_bank_censuses':0,'new_label_fits':0,'completed_semantic_checks_replayed':0,'completed_source_sign_checkpoints_replayed':0,
      'current_caps_preserved':True,'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write('resources.json',resources)
    write('debt_definition.json',{'name':'D_term','input':'D_hid from Transfer16',
      'P':'A root is Score r in0..8, B root is core r, mu marks r',
      'formula':'D_hid(s) if P(s), else0',
      'root_unused_kind_and_all_other_unused_fields_ignored':True,'new_shared_coordinate_or_private_observable':False,
      'range':[0,2],'every_LOW_target_unchanged':True,'every_LOW_source_value_nonincreasing':True,
      'global_psi_floor_claimed':False,'global_Lambda_floor_claimed':False,'global_E1_floor1_claimed':False,
      'all_LOW_destination_psi_and_E1_floors_retained':True,
      'old_signed_rows_transported_directly_not_by_false_global_floor_premise':True})

    old=read('entry_baseline.json');baseline={v['path']:v['sha256'] for v in old['files']}
    dp=BASE.parent/'M3_XFER16/dependencies.json'
    assert sha(dp)==baseline[dp.as_posix()]
    inherited=json.loads(dp.read_text());expected={v['path']:v['sha256'] for v in inherited['files']}
    expected.update(a['reused_proof_hashes']);expected.update(a['source_hashes_reused_not_executed'])
    expected[dp.as_posix()]=baseline[dp.as_posix()]
    for name in ('TERMINAL_ROOT_THEOREM.md',):assert (BASE/name).exists()
    for name in ('HIDDEN_GAMMA1_REPAYMENT.md','PROOF_AUDIT.md','PARTITION_UPDATE.md','debt_definition.json',
      'certificate.json','resources.json','symbolic_audit.json','partition_update.json','final_manifest.json'):
        q=BASE.parent/'M3_XFER16'/name
        expected[q.as_posix()]=baseline[q.as_posix()]
    for q,h in expected.items():assert sha(Path(q))==h,q
    extra_pins={q:h for q,h in expected.items() if q not in baseline}
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'inherited_long_path_pins_supplement_entry_traversal':True,'extra_dependency_pins_not_in_entry_index':len(extra_pins),
      'files':[{'path':q,'sha256':h} for q,h in sorted(expected.items())]})
    for i,(q,h) in enumerate(baseline.items()):
        assert sha(Path(q))==h,q
        if (i+1)%1000==0:print(json.dumps({'entry_listed_prior_files_unchanged':i+1,'listed_total':len(baseline)}),flush=True)
    additions=[q for q in BASE.parent.rglob('*') if q.is_file() and BASE not in q.parents and q.as_posix() not in baseline]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in q.as_posix() for q in additions),[q.as_posix() for q in additions]
    write('concurrent_additions.json',{'not_mathematical_dependencies':True,
      'files':[{'path':q.as_posix(),'sha256':sha(q)} for q in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS_ON_EXPLICIT_PINNED_SCOPE','entry_listed_prior_files_unchanged':len(baseline),
      'all_inherited_mathematical_dependency_pins_verified':len(expected),'additional_long_dependency_pins_verified':len(extra_pins),
      'legacy_entry_directory_index_exhaustive_claimed':False,'HEAD':old['head'],'tracked_tree_clean':True,
      'campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)}
    write('integrity.json',integrity)
    certificate={
      'status':'PROVED_UNIVERSAL_TERMINAL_ROOT_NORMALIZATION_FULL_STEP4_OPEN',
      'theorem':'ALL_ORIGINAL_LOW_DESTINATIONS_MARKED_SYNC_AND_ALL_UNMARKED_SOURCE_LOW_ROWS_VALID',
      'new_debt':'D_term=D_hid on P, 0 outside P; P is marked synchronized Score-root predicate',
      'all_original_LOW_destinations_P':True,'all_unmarked_source_LOW_rows_proved':True,
      'every_previously_valid_LOW_row_preserved':True,'all_completed_Gamma1_zero_rows_preserved':True,
      'all_previous_HIGH_and_h0_rows_preserved_by_range_glue':True,
      'global_psi_Lambda_or_E1_floor_for_new_function_claimed':False,
      'all_LOW_destination_psi_Lambda_as_inherited_and_E1_floors_retained':False,
      'all_LOW_destination_psi_and_E1_floors_retained':True,
      'old_D_hid_not_necessarily_Lambda_floor_is_unchanged_on_each_LOW_target':True,
      'exact_signed_transport':'w+D_term(t)-D_term(s) = old_residual + D_hid(s)-D_term(s)',
      'exact_off_P_nonnegative_residual':'w+D_term(t)>=0',
      'exact_off_P_negative_residual':'(w+psi_t-psi_s)+(D_term(t)-psi_t)+psi_s>=0',
      'all_original_masks_sigmas_private_witnesses_and_raw_fields_retained':True,
      'separate_universal_source_AST_sign_audit':'PASS with completed checkpoints reused after inherited long-pin bookkeeping repair',
      'failed_first_component_retained':True,'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'remaining_H1_schematic_slots':36,'remaining_sources_marked_and_synchronized_only':True,
      'remaining_Gamma1_zero_slots':0,'all_remaining_marked_H1_leaves_closed':False,
      'requested_full_Step4_closure_achieved':False,'Step4_complete':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_exact_implication':'marked-source original zero H1 in one of the36 seed/word/depth schemas => D_hid(t)>=D_hid(s)',
      'remaining_cell_nonemptiness_or_candidate_failure_asserted':False,
      'research_quality_rule3_stop':'a second independent marked-source repayment theorem is needed; no automatic new campaign after OPEN',
      'R1_R4_preserved':True,'h0_correction_preserved':True,'full147_O_127_M_and_SAME_actual_midpoint_preserved':True,
      'independent_scopes_HIGH_free_v_weak_LE_G_unused_fields_original_H_q_weights_preserved':True,
      'corrected_h0':{'actual':0,'declared':18,'q':9,'weight':-3},
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,'new_finite_tests':0,
      'NET_ADVANCEMENT':'entire unmarked-root LOW domain discharged uniformly; no complete Step4 promotion',
      'resources':resources,'integrity':integrity}
    write('certificate.json',certificate)
    result=f'''# Step4 is still open; all unmarked-source LOW rows are closed

The new uniform source theorem proves every original LOW destination
has a marked synchronized Score root. Define D_term=D_hid on that
observable root class P, and0 elsewhere. Every actual LOW target keeps
its old value and each source can only decrease. Thus every completed
signed LOW row survives by exact cancellation. Range preserves HIGH/h0.

Every LOW row from an unmarked root is now directly valid: nonnegative
weights use source0 and range, and negative H1 uses the retained psi
floor at its marked terminal target. This holds for every original
mask/signature/private witness and full raw state, without finite tests.
The global psi/Lambda/E1 floor is NOT asserted for the new function;
destination floors and all old signed rows are retained directly.

The remaining36 H1 schemas now have ONLY MARKED synchronized sources.
Their marked-source endpoint values are unchanged from D_hid, and no
new signed proof for them is supplied. No Gamma1 zero cases remain
open. The36 labels are universal obligations, not tested instances or
asserted counterexamples. COMPLETE Step4 was requested and is NOT
achieved. Step4, M3 and Dynamic Optimality remain OPEN.

The precise gap is the universal marked-source zero-H1 repayment bound.
The Gamma1 auxiliary depth7/core-floor proof does not apply to a single
H1 zero access. Safe row preservation does not prove an unknown row.
The old zero-reset theorem also prevents assuming a blanket psi-only
H1 destination floor. CLOSURE_GAP.md states the missing implication.
Research-quality rule3 requires a stop when another independent open
theorem is necessary; no unsupported completion or automatic pivot follows.

The separate audit passed original terminal/source AST constraints,
same-target/root/shadow wiring and exact signed coefficients. Its first
component stopped only because the legacy entry traversal omitted the
long LDR01 dependency from its index. That failed status remains saved.
The existing inherited pin was verified, and only unfinished provenance/
coverage checks resumed. Completed source/sign checkpoints were NOT rerun.
This is not external review or full compiler formalization.

R1-R4, all147-O/127-M, SAME actual midpoint, independent scopes, HIGH
free v, weak LE/G/unused fields, original H/q/weights and corrected
h0(actual0,declared18,q9,w=-3) remain. All{len(baseline)} ENTRY-LISTED
prior files and all{len(expected)} inherited/current mathematical pins
are unchanged, including{len(extra_pins)} extra dependency paths outside
that legacy index. The directory index is not claimed exhaustive over
all long filesystem names. Writes are confined here; Git HEAD/tracked
tree are unchanged. No finite tests, original root/psi/source queries,
fits, bank censuses or old semantic-check replays ran.

New CPU including BOTH components={charge}; cumulative{total}/7200;
remaining{7200-total}, including reserve5. Per-phase120/300/300,2m
query/live records,4m DAG,5m edges and32GiB remain. Metadata hashing
uses the existing convention. No resource cap was a mathematical blocker.

Proof: TERMINAL_ROOT_THEOREM.md. Separate audit: PROOF_AUDIT.md and
symbolic_audit.json. Exact remaining gap: CLOSURE_GAP.md. New potential:
debt_definition.json. Coverage/status: partition_update.json/certificate.json.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':q.as_posix(),'sha256':sha(q)} for q in sorted(BASE.rglob('*')) if q.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'all_unmarked_source_LOW':'PROVED',
      'remaining_marked_H1_schemas':36,'Step4':'OPEN','requested_full_closure_achieved':False,
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
