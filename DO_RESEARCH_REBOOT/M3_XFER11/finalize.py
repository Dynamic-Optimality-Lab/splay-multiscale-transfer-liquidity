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
    assert a['status']=='MARKED_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert len(a['complete_depth4_bottom_word_certificates'])==4
    assert len(a['helper_A_depth_and_opposite_block_certificates'])==6
    for name in ('J_no_V_filter_or_private_completion_guard','main_full_G_boundary_targets_still_satisfy_J',
      'each_previously_valid_LOW_row_preserved_by_each_operation','all_J_and_G_source_LOW_rows_proved',
      'both_ancestors_marked','main_G_sources_outside_S','all_nonnegative_incoming_J_G_rows_valid'):
        assert a[name],name
    assert a['G_zero_marked_grandchild_residual_exactly']==0
    assert a['J_Gamma1_original_H2_weight_at_least']==3
    assert not a['all_marked_ancestor_grandchild_zero_H1_coverage_proved']
    assert not a['global_zero_LOW_coverage_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    prior=759.8125
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
    inherited=json.loads((BASE.parent/'M3_XFER10/dependencies.json').read_text())
    paths={Path(v['path']) for v in inherited['files']}
    paths.update(BASE.parent/n for n in (
      'M3_XFER10/GRANDCHILD_THEOREM.md','M3_XFER10/PROOF_AUDIT.md',
      'M3_XFER10/certificate.json','M3_XFER10/resources.json',
      'M3_XFER10/symbolic_audit.json','M3_XFER10/final_manifest.json'))
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
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'MARKED_ANCESTOR_DEPTH4_GRANDCHILD_TWO_CREDIT_RELAY_OUTSIDE_S',
      'input_class':'any public Lambda<=D<=2; preserves each previously valid LOW row individually',
      'minus_mark_guard':'first two marks a<b, b in4/5; marked c>b, c-b<=3',
      'plus_mark_guard':'two largest marks a>b, b in3/4; marked c<b, b-c<=3',
      'main_G_minus':'rootc, A L=b/LL=a, LR/R nonreal; core c,Lb and depth(a)=4',
      'main_G_plus':'rootc, A R=b/RR=a, L/RL nonreal; core c,Rb and depth(a)=4',
      'aux_J_minus':'roota, A R=b/RR=c and core a,Rb,Rc; no V or further A filter',
      'aux_J_plus':'roota, A L=b/LL=c and core a,Lb,Lc; no V or further A filter',
      'both_main_ancestors_marked':True,'all_main_G_sources_outside_S':True,
      'ordered_operations':['D1=max(D,2*1_J)','F=max(D1,2*1_G)'],
      'explicit_current_debt':'D_marked=max(D_grand,2*1_J,2*1_G)',
      'each_previously_valid_LOW_row_preserved_by_each_operation':True,
      'all_J_and_G_source_original_LOW_rows_proved':True,
      'main_zero_H1_source_and_target_debts':2,'main_zero_H1_signed_residual':0,
      'J_H1_b_weight':2,'J_H1_c_weight':1,
      'after_J_c_exit_all_marked_core_depths_at_most':3,
      'after_J_c_exit_existing_E1_floor_at_least':1,
      'J_Gamma1_allowed_terminal':'old a or b only',
      'J_Gamma1_original_terminal_q_at_most':1,
      'J_Gamma1_original_H2_weight_at_least':3,
      'initial_helper_Score_emptiness_assumed':False,
      'G_Gamma1_excluded_by_no_actual_anonymous_source_charge1_target':True,
      'Gamma0_can_expose_other_marks_actual_preterminal_floor_reused':True,
      'main_depth4_bottom_pair_path_words_complete':True,
      'J_G_boundary_without_fresh_source_completion_retained':True,
      'no_private_inventory_or_hidden_weak_LE_rank_inferred':True,
      'all_compatible_core_subtrees_and_admissible_signatures':True,
      'all_nonnegative_incoming_J_G_rows_valid':True,
      'negative_incoming_blanket_repair_claimed':False,
      'strict_numerical_increase_over_old_debt_claimed':False,
      'prior_S_child_unmarked_ancestor_and_negative_H1_coverage_preserved':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_marked_ancestor_grandchild_zero_H1_coverage_proved':False,
      'global_zero_LOW_coverage_proved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['other uncovered depth5 marked-ancestor grandchild zero H1 classes',
        'larger marked spans and zigzag marked-ancestor grandchild classes',
        'other uncovered grandchild/child and shallow-helper zero/+1 classes','global signed LOW validity'],
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'explicit two-credit J/G relay proves uniform marked-root/marked-parent depth4 zero H1 rows outside S, all J/G-source LOW and nonnegative incoming rows',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# A marked-root and marked-parent grandchild class outside S is closed

The new principal theorem supplies an explicit two-credit relay. At the
smaller end a<b are the first two marks, b is4/5, and marked c>b has
c-b<=3. Main source G has rootc, marked childb at L, marked grandchilda
at LL, nonreal LR/R, core childb immediately underc and core depth(a)=4.
The actual opposite-end theorem uses the two largest marks, b3/4, a
right-right grandchild and the corresponding stated cuts/core guard.
Both ancestors are marked and every main G source is outside S.

Its zero a-access ends at J: root a, b/c at A R/RR and core depths1/2
(actual opposite orientation L/LL). First saturate J to2, then G to2:
    D_marked=max(D_grand,2*1_J,2*1_G).
Every operation preserves every previously valid original LOW row.
All J/G-source LOW rows are proved, every main zero H1 row has debt2->2
and exact residual0, and nonnegative incoming J/G rows are range-safe.

J has NO V filter. G aliases may report old marked c in an incoming
boundary that lacks a fresh source completion; it remains an original
full target and receives cap2. For actual J sources, b/c are the only H1
targets, with weights2/1. Every c exit places ALL marked B keys at depth<=3,
so its existing E1 floor>=1 repays the +1. Possible extreme J helpers
leave only old a/b eligible at terminal A charge1; their preterminal B
depths<=2/3 give ORIGINAL H2 weight>=3. Score-bearing helper support is
allowed. Main G has no actual anonymous charge1 source target. Gamma0
retains its actual-preterminal floor even when other marks are exposed.

The separate audit passed universal paired identities, all four depth4
bottom path words in both actual top orientations, six arbitrary-block
helper identities, count/slack algebra, signed rows and targeted source
charge provenance. A separate prose audit checks full boundaries,
quantifiers, source legality, nonvacuity, dependencies and sharing.
Completed source/kind/G/price checks were reused by immutable hashes.
This is not full compiler formalization or external human/model review.
No finite tests, source/root/psi queries, label fits, bank censuses or
completed semantic checker replays ran.

The nine ordered-role construction supplies actual original zero rows
with both ancestors marked outside S. A strict numerical increase over
the old debt is not claimed; the advancement is the new uniform original
row theorem and safe relay formula. No new global existence premise enters.

Depth5, larger marked spans, zigzag marked ancestors and other uncovered
cheap transfers remain. Full marked-grandchild coverage, global zero LOW,
M3 and Dynamic Optimality are OPEN. No new whole-signature certificate or
original negative cycle is claimed.

R1-R4/current caps, full147-O/127-M closure, SAME actual midpoint,
independent witnesses, free high v, original weak LE/G/unused fields,
H/q/prices and corrected h0 remain. All{len(pins)} pinned prior files,
HEAD and tracked tree are unchanged. New charged CPU={charge};
cumulative={total}/7200; remaining={7200-total}, including reserve5.
Per-phase120/300/300,2m queries/live records,4m DAG,5m edges and32GiB
caps remain. Metadata hashing follows the existing accounting convention.

Proof: MARKED_RELAY_THEOREM.md. Separate audit: PROOF_AUDIT.md.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'marked_ancestor_depth4_relay':'PROVED',
      'both_ancestors_marked':True,'main_zero_signed_residual':0,
      'all_marked_ancestor_zero_H1':'OPEN','global_zero_LOW':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()

