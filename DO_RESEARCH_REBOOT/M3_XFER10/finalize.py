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
    assert a['status']=='GRANDCHILD_UNMARKED_ANCESTOR_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert {c['case'] for c in a['case_certificates']}=={'LL','LR','RL','RR'}
    for name in ('target_empty_V_for_all_four_cases','each_previously_valid_LOW_row_preserved',
      'all_Z_source_zero_H1_F_residuals_exactly_zero','all_Z_source_LOW_rows_for_current_input_proved',
      'nonnegative_incoming_Z2_rows_proved','newly_exposed_depth1_G_children_checked_LL_RR',
      'Gamma1_from_Z_excluded_by_no_anonymous_source_charge1_target'):
        assert a[name],name
    assert not a['global_zero_LOW_coverage_proved'] and not a['all_outside_S_grandchild_zero_H1_coverage_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    prior=759.515625
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
    inherited=json.loads((BASE.parent/'M3_XFER09/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(BASE.parent/n for n in (
      'M3_XFER09/INTERVAL_CHILD_THEOREM.md','M3_XFER09/PROOF_AUDIT.md',
      'M3_XFER09/certificate.json','M3_XFER09/resources.json',
      'M3_XFER09/symbolic_audit.json','M3_XFER09/final_manifest.json'))
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'published_completed_B_fact_not_queried_or_recomputed':'Transfer01 strictness / LDR01 helper_reset_2',
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
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'UNMARKED_ANCESTOR_GRANDCHILD_LOW_SAFE_CAPACITY_OUTSIDE_S',
      'input_class':'any public Lambda<=D<=2; preserves each previously valid LOW row individually',
      'main_region':'Z: synchronized unmarked Score root r; unmarked Score child p; marked grandchild x; stated cuts/barrier',
      'public_cases':{
        'LL':{'order':'x<p<r','opaque':['LR','R'],'barrier':'marked labels below p exactly {x}'},
        'LR':{'order':'p<x<r','opaque':['LL','R'],'barrier':'marked labels strictly between p,r exactly {x}'},
        'RL':{'order':'r<x<p','opaque':['L','RR'],'barrier':'marked labels strictly between r,p exactly {x}'},
        'RR':{'order':'r<p<x','opaque':['L','RL'],'barrier':'marked labels above p exactly {x}'},
      },
      'explicit_cap':'h_Z=min(2,w_x+2) on Z; 0 elsewhere',
      'explicit_combined_debt':'D_grand=max(D_interval,h_Z)',
      'all_Z_source_H1_targets_have_empty_V':True,
      'target_debt_already_for_old_Lambda_D_and_new_F':2,
      'each_previously_valid_original_LOW_row_preserved':True,
      'all_Z_source_nonnegative_H1_rows_valid_for_old_D_and_F':True,
      'all_Z_source_zero_H1_F_source_and_target_debts':2,
      'all_Z_source_zero_H1_F_signed_residuals':0,
      'all_Z_source_LOW_rows_for_current_D_interval_input_proved':True,
      'all_Z_source_H1_current_F_exact_residual':'max(w,0)',
      'negative_source_cap_uses_previously_valid_actual_negative_H1_row':True,
      'arbitrary_typed_input_D_clamped_to_h_Z':False,
      'nonnegative_incoming_to_Z2_rows_proved':True,
      'all_nonnegative_incoming_to_all_Z_rows_claimed':False,
      'Gamma1_from_Z_excluded':'no actual anonymous source depth1/2 target',
      'Gamma0_may_expose_hidden_marks_original_actual_preterminal_floor_reused':True,
      'LL_RR_depth1_G_second_level_reads_old_root_opaque_children':True,
      'both_actual_LOW_orientations_and_all_four_positions_proved':True,
      'all_admissible_signatures_and_independent_private_completions':True,
      'strict_current_debt_increase':'published helper_reset_2 B fact; source8(1(0(A,B),C),D), marks0/2/4/6/7:0->2',
      'new_bank_or_saved_label_queries_for_strictness':0,
      'private_inventory_or_hidden_rank_inferred':False,
      'prior_complete_S_and_interval_child_coverage_preserved':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_outside_S_grandchild_zero_H1_coverage_proved':False,'global_zero_LOW_coverage_proved':False,
      'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['other uncovered marked-ancestor or anonymous-parent grandchild H1 classes',
        'other uncovered grandchild H1 classes without these cuts/barriers',
        'remaining child and shallow-helper zero/+1 transfer classes','global signed LOW validity'],
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'four guarded outside-S grandchild zero H1 classes discharged; strict public capacity increase; every old LOW row preserved',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# Four guarded marked-grandchild classes outside S are closed

The unmarked-ancestor theorem proves a new uniform class at LL, LR, RL
and RR. Source root r and parent p are unmarked Scores, grandchild x is
marked, and the specified two public opaque cuts and marked-label
barrier prevent newly exposed marked observations. The original source
requires a Score root, not that mu marks it.

Every such H1 destination has V empty and hence the EXISTING debt floor2.
The new explicit public debt is
    D_grand=max(D_interval,h_Z),
    h_Z=min(2,w_x+2) on Z, and0 elsewhere.
Every Z-source zero H1 row has new debt2->2 and exact signed residual0.
The old debt also satisfies those nonnegative rows by the newly proved
empty-target structural theorem; no old violated row is alleged.
All current Z-source LOW rows hold, every previously valid LOW row is
preserved, and all nonnegative incoming rows to Z2 are protected.

LL/RR include second-level G: an exposed depth1 alias reads old unmarked
r, whose CURRENT children are both opaque. LR/RL expose only unmarked
interior blocks at depth2. The present mark barriers use no private
inventory or weak-LE strengthening. Gamma1 cannot start because no actual
source anonymous node exists at depth1/2. Gamma0 retains its original
actual-preterminal floor even if H2 exposes other marked nodes.

The separate universal symbolic audit passed all four exact pair
identities, symbolic interval containment/exclusion, source anonymous
absence, two-level G children, signed slacks and new source root/mask and
primitive-order provenance. The separate prose audit checks legality,
quantifiers, all boundaries, sharing, nonvacuity, dependencies and scope.
Completed kind/G/price checks were reused by immutable hashes.
This is not full compiler formalization or external human/model review.

A formal ordered-role family supplies original zero edges outside S.
Reusing the PUBLISHED helper_reset_2 B fact supplies a strict current
source-capacity gain0->2 with marks0/2/4/6/7 and source8(1(0(A,B),C),D).
No finite tests, original-root or source queries, saved psi queries, label
fits or bank censuses ran. No completed semantic check was replayed.

Marked-ancestor, anonymous-parent and unshielded grandchild configurations
outside previous coverage remain. A V-empty target can still start H2 or
HIGH and is not declared a solved sink. Full outside-S grandchild coverage,
global zero LOW, M3 and Dynamic Optimality are OPEN. No new whole-signature
certificate or certified original negative cycle is claimed.

R1-R4/current caps, full147-O/127-M closure, SAME actual midpoint,
independent witnesses, free high v, original weak LE/G/unused fields,
H/q/prices and corrected h0 remain. All{len(pins)} pinned prior files,
HEAD and tracked tree are unchanged. New charged CPU={charge};
cumulative={total}/7200; remaining={7200-total}, including reserve5.
Per-phase120/300/300,2m queries/live records,4m DAG,5m edges and32GiB
caps remain. Metadata hashing follows the existing accounting convention.

Proof: GRANDCHILD_THEOREM.md. Separate audit: PROOF_AUDIT.md.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'outside_S_Z_grandchild_zero_H1':'PROVED',
      'cases':['LL','LR','RL','RR'],'all_outside_S_grandchild_zero_H1':'OPEN','global_zero_LOW':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()

