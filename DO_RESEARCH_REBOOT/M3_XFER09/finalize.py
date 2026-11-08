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
    assert a['status']=='INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for name in ('each_previously_valid_LOW_row_preserved','all_I_source_nonnegative_H1_rows_proved',
      'all_I_source_zero_H1_residuals_exactly_zero','all_I_source_LOW_rows_for_current_input_proved',
      'nonnegative_incoming_I2_rows_proved','Gamma1_from_I_excluded_by_present_interval'):
        assert a[name],name
    assert not a['global_zero_LOW_coverage_proved'] and not a['all_outside_S_zero_H1_coverage_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=759.203125+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':759.203125,'new_symbolic_checker_CPU':r['child_CPU'],
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
      'RESEARCH_RULES.md',
      'M3_XFER08/BURIED_BARRIER_THEOREM.md','M3_XFER08/PROOF_AUDIT.md',
      'M3_XFER08/certificate.json','M3_XFER08/resources.json','M3_XFER08/final_manifest.json',
      'M3_XFER07/DIRECT_BARRIER_THEOREM.md','M3_XFER07/PROOF_AUDIT.md',
      'M3_XFER06/ANONYMOUS_RELEASE_THEOREM.md','M3_XFER06/PROOF_AUDIT.md',
      'M3_XFER05/RR_RELEASE_THEOREM.md','M3_XFER05/PROOF_AUDIT.md',
      'M3_XFER04/RELEASE_CAPACITY_THEOREM.md','M3_XFER04/PROOF_AUDIT_v2.md',
      'M3_XFER03/BURIED_CUT_THEOREM.md','M3_XFER03/PROOF_AUDIT.md',
      'M3_XFER02/CUT_PAIR_THEOREM.md','M3_XFER02/PROOF_AUDIT.md',
      'M3_XFER01/SATURATION_THEOREM.md','M3_XFER01/PROOF_AUDIT.md',
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
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'INTERVAL_CHILD_LOW_SAFE_CAPACITY_OUTSIDE_S',
      'input_class':'any public Lambda<=D<=2; preserves each previously valid LOW row individually',
      'main_region':'I_L or I_R: synchronized Score root, marked child, opaque exterior cuts, V={child}',
      'root_required_marked':False,'marked_pair_required_extremal':False,
      'real_unmarked_or_anonymous_middle_and_present_marked_descendants_allowed':True,
      'explicit_cap':'h_I=min(2,w_child+2) on I; 0 elsewhere',
      'explicit_combined_debt':'D_interval=max(D_buried,h_I)',
      'each_previously_valid_original_LOW_row_preserved':True,
      'all_I_source_nonnegative_H1_rows_proved':True,
      'all_I_source_zero_H1_source_and_target_debts':2,
      'all_I_source_zero_H1_signed_residuals':0,
      'all_I_source_LOW_rows_for_current_D_buried_input_proved':True,
      'negative_I_source_coverage_uses_previously_valid_negative_H1_rows':True,
      'arbitrary_input_D_clamped_to_h_I':False,
      'nonnegative_incoming_to_I2_rows_proved':True,
      'all_nonnegative_incoming_to_all_I_rows_claimed':False,
      'Gamma1_from_I_excluded':'middle helper strictly between two present Score endpoints; interior gap',
      'Gamma0_can_expose_hidden_marked_descendants':True,
      'empty_V_target_floor_for_unmarked_old_root':2,
      'G_old_slot0_duplicates_and_non_source_admissible_boundaries_retained':True,
      'both_actual_LOW_orientations_proved':True,'all_admissible_signatures_and_private_completions':True,
      'strict_current_debt_increase':'published helper_reset_2 B fact reused, real middle1, marks0/2/4/6/8:0->2',
      'private_inventory_or_hidden_gap_inferred':False,
      'prior_complete_S_zero_coverage_preserved':True,
      'prior_deep_Gamma1_cheap_helper_exclusion_preserved':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_outside_S_zero_H1_coverage_proved':False,'global_zero_LOW_coverage_proved':False,
      'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['other uncovered marked-grandchild zero H1 source classes',
        'other uncovered marked-child zero H1 classes without these exterior guards',
        'remaining shallow-helper zero/+1 Gamma1 classes','global signed LOW validity'],
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'uniform outside-S guarded child zero H1 family discharged; strict public capacity increase; old LOW rows preserved',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# A new outside-S zero H1 class is closed

The interval-child theorem gives an explicit public LOW-safe augmentation
    D_interval=max(D_buried,h_I),
    h_I=min(2,w_child+2) on I, and0 elsewhere.
I has a synchronized Score root and marked child, nonreal cuts on the two
exterior sides and V={{child}}. The middle root may be real unmarked or
anonymous, with marked descendants below it. Neither an extreme marked
pair nor a marked source root is required. All admissible signatures and
independent private completions are included.

Every I-source zero H1 row has source and target debt2, residual0.
Every I-source LOW row holds for the current D_buried input. The max
operation preserves EVERY previously valid original LOW row, including
completed S coverage and global negative H1. All nonnegative incoming
rows to I2={{s in I:h_I(s)=2}} are range-safe; no blanket incoming-I claim
or typed boundary downward cap is made.

The exact zigs keep the middle root at depth2. A marked old root gives
an opposite-I target whose return B depth<=2 supplies two credits; an
unmarked old root gives the empty-V floor2. Any possible anonymous first
helper is strictly between two present Score endpoints, hence has an
interior gap and cannot be Gamma1. Gamma0 retains its original actual-
preterminal floor even when hidden marked nodes become exposed.

The separate universal symbolic/source/sign audit passed. It checked
term identities with arbitrary subtree variables and both actual
orientations, source kind/G/gap/pricing provenance and exact affine
slacks. The separate prose audit covers order, boundary and scope
obligations. This is not full compiler formalization or external review.
No finite tests, source queries, original-root evaluations, saved psi
queries, label fits or bank censuses ran. Old checks were reused.

A formal ordered-role family establishes outside-S nonvacuity. Reusing
the published helper_reset_2 B fact gives a strict current-debt increase
0->2 with a real middle and marks0/2/4/6/8; that completed fact is not
queried or recomputed. The universal theorem does not rely on the example.

Other marked-grandchild classes, unprotected child configurations and
remaining shallow-helper cheap Gamma1 classes remain. Global zero LOW,
full M3 and Dynamic Optimality are OPEN. No new whole-signature
certificate or certified original negative cycle is claimed.

R1-R4/current caps, full147-O/127-M closure, SAME actual midpoint,
independent witnesses, free high v, original weak LE/G/unused fields,
H/q/prices and corrected h0 remain. All{len(pins)} pinned prior files,
HEAD and tracked tree are unchanged. New charged CPU={charge};
cumulative={total}/7200; remaining={7200-total}, including reserve5.
Per-phase120/300/300,2m queries/live records,4m DAG,5m edges and32GiB
caps remain. Metadata hashing follows the existing accounting convention.

Proof: INTERVAL_CHILD_THEOREM.md. Separate audit: PROOF_AUDIT.md.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'outside_S_I_zero_H1':'PROVED',
      'all_outside_S_zero_H1':'OPEN','global_zero_LOW':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()

