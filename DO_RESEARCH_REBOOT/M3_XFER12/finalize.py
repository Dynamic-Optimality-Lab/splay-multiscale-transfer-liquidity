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
    assert a['status']=='DEPTH_FIVE_CENTRAL_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for name in ('odd5_top_cases_complete_after_arbitrary_lowest_pair',
      'C5_exception_P8_and_opposite_endpoint_closed','span4_J8_C8_and_opposite_endpoint_closed',
      'Bdry_changes_no_actual_LOW_source','each_previously_valid_LOW_row_preserved_by_each_operation',
      'all_new_region_source_LOW_rows_proved','central_main_all_spans_and_both_B_zero_depths_4_5_proved',
      'all_nonnegative_incoming_new_region_rows_proved'):
        assert a[name],name
    assert a['central_G45_zero_H1_signed_residual']==0
    assert not a['Step4_complete'] and not a['global_zero_LOW_coverage_proved']
    assert (BASE/'STEP4_COVERAGE_AUDIT.md').exists() and (BASE/'PROOF_AUDIT.md').exists()
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    prior=760.1875
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
    inherited=json.loads((BASE.parent/'M3_XFER11/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(BASE.parent/n for n in (
      'M3_XFER11/MARKED_RELAY_THEOREM.md','M3_XFER11/PROOF_AUDIT.md',
      'M3_XFER11/certificate.json','M3_XFER11/resources.json',
      'M3_XFER11/symbolic_audit.json','M3_XFER11/final_manifest.json',
      'M3_XFER08/symbolic_audit.json'))
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
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
      'status':'PROVED_RESTRICTED_DOMAIN',
      'theorem':'COMPLETE_CENTRAL_ALIGNED_MARKED_ANCESTOR_ZERO_RELAY_DEPTH4_AND5',
      'input_class':'any public D_marked<=D<=2; no global LOW feasibility assumption',
      'main_minus':'first marks a<b, b4/5, marked c>b; rootc, A L=b/LL=a, LR/R nonreal, core c,Lb, depth(a)4/5',
      'main_plus':'largest marks a>b, b3/4, marked c<b; rootc, A R=b/RR=a, L/RL nonreal, core c,Rb, depth(a)4/5',
      'main_span_restriction_removed':True,'both_main_ancestors_marked':True,
      'main_G45_sources_outside_S':True,
      'ordered_cap2_operations':['Bdry','Rsh','Q8','P8','C5_or_C8','K','J8','G45'],
      'explicit_current_debt':'D45=max(D_marked,2*1_Bdry,2*1_Rsh,2*1_Q,2*1_P,2*1_C,2*1_K,2*1_J8,2*1_G45), with actual opposite classes',
      'each_previously_valid_LOW_row_preserved_by_each_operation':True,
      'all_new_region_source_original_LOW_rows_proved':True,
      'main_zero_H1_source_and_target_values':2,'main_zero_H1_signed_residual':0,
      'depth5_K_core_c_depth':1,'depth5_K_core_b_depths':[2,3],
      'depth5_root5_exception_closed_by':'K->C5->P8_or_Bdry_or_E1',
      'depth5_span4_root8_exception_closed_by':'K->C8->Rsh_or_E1',
      'depth4_span4_root8_exception_closed_by':'J8->Q8->Rsh_or_old_K_or_E1',
      'C5_only_deep_plus1_exception':'upper roles6<7<8, target8, marked6 -> P8',
      'Bdry_V_guard_implied_at_all_actual_sources':True,
      'Bdry_changes_no_actual_LOW_source':True,
      'new_return_predicates_no_V_filter':True,
      'original_H2_helper_weight_at_least2_on_new_C_K_P_regions':True,
      'all_admissible_signatures_and_full_original_states':True,
      'no_private_inventory_history_or_weak_LE_strengthening':True,
      'all_nonnegative_incoming_new_region_rows_proved':True,
      'negative_incoming_blanket_repair_claimed':False,
      'strict_numeric_old_debt_increase_claimed':False,
      'all_prior_source_and_negative_H1_certificates_preserved':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'user_requested_full_Step4_completion_achieved':False,
      'Step4_status':'OPEN_EXHAUSTIVE_ZERO_LOW_COVERAGE_NOT_PROVED',
      'Step4_coverage_audit':'STEP4_COVERAGE_AUDIT.md',
      'coverage_gap_is_original_negative_edge_or_cycle_claim':False,
      'remaining_original_zero_LOW_obligations':[
        'other H1 zero source classes outside proved domains, including non-extremal grandchild exposures',
        'remaining Gamma1 zero edges with initial helper B depth<=2 and terminal pre-B depth8/9',
        'an exhaustive original-normal-form coverage proof after those residual signs are proved'],
      'global_zero_LOW_coverage_proved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'central aligned marked-root/marked-parent relay closed at both zero B depths4/5 with all spans and endpoint exceptions; exhaustive Step4 claim rejected by coverage audit',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# Depth-five central relay proved; full Step4 remains OPEN

The entire central same-direction marked-ancestor source class is now
proved at BOTH zero B depths4/5, with NO span restriction. At the smaller
end the first two marks are a<b, b4/5, marked rootc>b; A L=b/LL=a,
nonreal LR/R, core c,Lb, depth(a)4/5. The actual opposite class uses
the two largest marks, b3/4, and right-right geometry. Both ancestors
are marked; every main source is outside S.

The new explicit public debt is the ordered maximum of D_marked with
cap2 on Bdry,Rsh,Q8,P8,C5/C8,K,J8,G45 and their actual opposite classes.
Every operation preserves EVERY previously valid original LOW row.
All new-region source LOW rows and nonnegative incoming rows are proved.
Each main zero H1 row has debt2->2 and exact residual0.

Odd depth5 ends at core c-depth1 and b-depth2/3, rather than the old
even-depth successor. The +1 b return is E1-shallow except c5/c8 endpoint
cases. Both are now closed through explicit C5/C8 return chains. C5's
unique deeper +1 upper exception is P8; its zero return reaches a saved
capacity. The span4 even successor J8 is also closed through Q8/Rsh.
The required low a returns use OLD one-credit K rather than assuming
a new two-credit fixed point.

Bdry removes a V filter that is already mandatory at every actual source
of the stated old Score4-at-grandchild guard. It changes NO actual LOW
source, retaining full G-boundary targets. New returns have no V filter.
All helpers retain original terminal-only q; the new C/K/P bounds are
weight>=2 and Gamma0 uses the completed actual-preterminal floor.
No private inventory or continuing port allocation is inferred.

The fresh universal symbolic audit passed odd last-step identities,
endpoint/core/A guard transfers, the unique C5 exception, shallow-a
transport on published old outputs, helper depths, signed slacks and
new B-decoder AST provenance. Old checkers/maps were reused, not rerun.
A separate prose audit verifies quantifiers, source legality, boundaries,
sharing, dependencies and nonvacuity. No finite tests, source/root/psi
queries, bank censuses or label fits ran. This is not full compiler
formalization or external human/model review.

THE USER'S REQUEST TO COMPLETE ALL OF STEP4 IS NOT ACHIEVED.
The exhaustive coverage audit still leaves original zero rows outside
the proved domains. It gives a legal non-extremal marked-grandchild
source type that exposes another marked descendant and records remaining
initial-helper-depth<=2 Gamma1 zero cases. This is a coverage gap, NOT
a negative residual/cycle. Full Step4, M3 and Dynamic Optimality remain
OPEN. No new whole-signature certificate or original negative cycle
is claimed. Another independent compensation theorem is still needed;
the bounded R1-R4 campaign does not relabel its subclass as global closure.

R1-R4/current caps, full147-O/127-M closure, SAME actual midpoint,
independent scopes, free high v, weak LE/G/unused fields, original H/q/
prices and corrected h0 remain. All{len(pins)} pinned prior files, HEAD
and tracked tree are unchanged. New charged CPU={charge};
cumulative={total}/7200; remaining={7200-total}, including reserve5.
Per-phase120/300/300,2m queries/live records,4m DAG,5m edges and32GiB
caps remain. Metadata hashing uses the established accounting convention.

Proof: DEPTH_FIVE_RELAY_THEOREM.md. Separate audit: PROOF_AUDIT.md.
Exhaustive status and remaining original cases: STEP4_COVERAGE_AUDIT.md.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'central_depth4_and5_all_spans':'PROVED',
      'main_zero_signed_residual':0,'requested_full_Step4_complete':False,
      'Step4':'OPEN','M3':'OPEN','new_compute_CPU':charge,
      'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()

