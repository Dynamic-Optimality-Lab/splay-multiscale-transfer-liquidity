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
    assert a['status']=='BURIED_BARRIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert a['each_previously_valid_LOW_row_preserved'] and a['all_G_B_source_LOW_rows_proved']
    assert a['complete_eight_word_S_zero_frontier_closed'] and a['all_zero_LOW_with_S_source_covered']
    assert a['global_Gamma1_cheap_helper_initial_B_depth_at_most']==2
    assert not a['global_zero_LOW_coverage_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=758.65625+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':758.65625,'new_symbolic_checker_CPU':r['child_CPU'],
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
    names=[
      'RESEARCH_RULES.md','M3_XFER07/DIRECT_BARRIER_THEOREM.md','M3_XFER07/PROOF_AUDIT.md',
      'M3_XFER07/certificate.json','M3_XFER07/resources.json','M3_XFER07/final_manifest.json',
      'M3_XFER06/ANONYMOUS_RELEASE_THEOREM.md','M3_XFER06/PROOF_AUDIT.md',
      'M3_XFER05/RR_RELEASE_THEOREM.md','M3_XFER05/PROOF_AUDIT.md',
      'M3_XFER04/RELEASE_CAPACITY_THEOREM.md','M3_XFER04/PROOF_AUDIT_v2.md',
      'M3_XFER03/BURIED_CUT_THEOREM.md','M3_XFER03/PROOF_AUDIT.md',
      'M3_EXPOSURE02/HELPER_REDUCTION.md','M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md',
      'M3_AER01/RESULT.md','M3_POP5_RISK01/SOURCE_LIFT.md','M3_COMB_AUD01/AUDIT_REPORT.md',
      '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
      '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_INVENTORY.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ATOM_INVENTORY.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_STRUCTURAL_WITNESS.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py',
    ]
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,
      'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in names]})
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
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'BURIED_B6_B7_B8_LOW_SAFE_CAPACITY_AND_S_ZERO_CLOSURE',
      'input_class':'any public Lambda<=D<=2; no global feasibility assumption',
      'main_region':'B6/B7/B8; first pair a<4, a B depth<=5, stated A barrier, V subset4..8; actual LOW dual',
      'operation_order':['K_B1','R_B1','C_B1','T_B1','G_B2'],
      'explicit_combined_debt':'D_buried=max(D_direct,1_KB,1_RB,1_CB,1_TB,2*1_GB)',
      'each_previously_valid_original_LOW_row_preserved':True,
      'all_G_B_source_original_LOW_rows_proved':True,
      'main_a_depth_guard':5,'C_a_depth_guard':3,'T_a_depth_guard':7,
      'depth_guard_loses_no_original_S_zero_incoming_edge':True,
      'all_same_shaped_states_above_depth_guard_claimed':False,
      'auxiliary_already_debt2_sources_claimed_solved':False,
      'complete_S_eight_word_zero_frontier_closed':True,
      'all_zero_LOW_with_S_source_covered':True,
      'both_separator_types_and_all_three_A_positions':True,
      'both_actual_LOW_orientations_proved':True,
      'extreme_parent_lemma':'final min proxy parent0/max proxy parent8; old proxy final parent terminal or old neighbor',
      'global_deep_helper_Gamma1_cheap_edge_exclusion':'PROVED_UNIVERSAL_ON_ORIGINAL_LOW',
      'Gamma1_weight0_or_plus1_implies_helper_initial_B_depth_at_most':2,
      'helper_Score_emptiness_assumed':False,'private_inventory_or_gap_inferred':False,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'global_zero_LOW_coverage_proved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['zero H1 source classes outside S and previous coverage',
        'shallow-helper zero/+1 Gamma1 not otherwise covered','global signed LOW validity'],
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'complete S-family zero coverage plus global exclusion of deep-helper cheap Gamma1 edges',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# The buried S zero frontier is closed

B6/B7/B8 now have an explicit LOW-safe two-credit capacity on the public
guards inherited from the S-zero incoming family, including a-depth<=5.
The new public debt is
    D_buried=max(D_direct,1_KB,1_RB,1_CB,1_TB,2*1_GB).
Every previously valid LOW inequality is preserved. All main G_B-source
LOW rows are proved, with complete +1 exits and controlled zero returns.

With prior direct-barrier proofs, ALL EIGHT S-family upper zero words,
both separator types, all three A target positions and both actual LOW
orientations are now covered. S has no other unhandled zero LOW form:
the root5/dual3 H1 zeros are absent by count, Gamma1 is positive by the
central-root lemma, and Gamma0 zero rows are already floor-valid.

The new extreme proxy parent lemma also proves a UNIVERSAL restriction:
every original Gamma1 edge of weight0/+1 has initial helper B depth<=2.
A deeper minimum helper can only end at core0; the maximum dual can
only end at8. Those terminals have depth<=5 and price>=2. No assumption
of initially Score-empty helper support or a private gap allocation is used.

The separate universal symbolic audit passed parent/last-step identities,
the seven +1 core exits, return-depth bounds, A/G endpoints, guard transport,
source provenance and signed slacks. No finite test, source root, old psi
lookup, numerical tree/population assignment, label fit or bank census ran.
It is not full compiler formalization or external human/model review.

GLOBAL zero LOW coverage remains OPEN. Other zero H1 configurations and
the remaining shallow-helper zero/+1 Gamma1 cases must still be proved.
Same-shaped main states above the a-depth cap and arbitrary debt2 auxiliary
sources are not declared solved. Full M3/Dynamic Optimality remain OPEN.
No new whole-signature certificate or original negative cycle is claimed.

R1-R4/current caps, original weak LE/G/unused fields, H/q/prices,
full147-O/127-M closure, SAME midpoint, independent witnesses, free high v
and corrected h0 remain. All{len(pins)} pinned prior files and HEAD/tracked
tree unchanged. New charged CPU={charge}; cumulative={total}/7200;
remaining={7200-total}, including reserve5. New finite tests=0.

Proof: BURIED_BARRIER_THEOREM.md. Separate audit: PROOF_AUDIT.md.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'S_zero_frontier':'CLOSED',
      'deep_helper_cheap_Gamma1':'EXCLUDED_UNIVERSALLY','global_zero_LOW':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
