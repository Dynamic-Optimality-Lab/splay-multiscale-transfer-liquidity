"""Immutable publication and resource ledger; no mathematical execution."""
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
    assert a['status']=='DIRECT_BARRIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert a['each_previously_valid_LOW_row_preserved'] and a['all_G7_source_LOW_rows_proved']
    assert a['remaining_successor_cores']==['B6','B7','B8'] and not a['global_zero_LOW_coverage_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=758.3125+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':758.3125,'new_symbolic_checker_CPU':r['child_CPU'],
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
      'RESEARCH_RULES.md','M3_XFER06/ANONYMOUS_RELEASE_THEOREM.md','M3_XFER06/PROOF_AUDIT.md',
      'M3_XFER06/certificate.json','M3_XFER06/resources.json','M3_XFER06/final_manifest.json',
      'M3_XFER05/RR_RELEASE_THEOREM.md','M3_XFER05/PROOF_AUDIT.md',
      'M3_XFER04/RELEASE_CAPACITY_THEOREM.md','M3_XFER04/PROOF_AUDIT_v2.md',
      'M3_XFER03/BURIED_CUT_THEOREM.md','M3_XFER03/PROOF_AUDIT.md',
      'M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md','M3_AER01/RESULT.md',
      'M3_POP5_RISK01/SOURCE_LIFT.md','M3_COMB_AUD01/AUDIT_REPORT.md',
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
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'DIRECT_BARRIER_J7_LOW_SAFE_ZERO_RELEASE_CAPACITY',
      'input_class':'any public Lambda<=D<=2; no global feasibility assumption',
      'operation_order':['K1','C1','G7_2'],
      'explicit_combined_debt':'D_direct=max(D_anon,1_K,1_C,2*1_G7)',
      'new_capacity_region':'J7=7(4(L,6(5,E)),8); A4L with permitted LL separator OR A4LL; V subset4..8; actual dual',
      'each_previously_valid_original_LOW_row_preserved':True,
      'all_G7_source_original_LOW_rows_proved':True,
      'new_LRR_zero_releases_all_A_positions_and_separator_types_closed':True,
      'LRL_existing_J6_coverage_reused_not_counted_new':True,
      'new_parametric_helper_barrier_weight_bound':2,
      'helper_Score_emptiness_assumed':False,'private_inventory_or_gap_inferred':False,
      'S_family_frontier':{'source_words':8,'distinct_successors':6,'covered_words':4,'remaining_words':4,
        'remaining_cores':['B6','B7','B8'],'remaining_B_depth_of_4':2,'not_a_global_M3_obligation_count':True},
      'both_actual_LOW_orientations_proved':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'global_zero_LOW_coverage_proved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['S zero buried-barrier B6/B7/B8','other zero H1 marked configurations',
        'zero H2/Gamma1 outside completed classes','global zero/+1 completeness'],
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'complete local eight-to-six map and new explicit J7 signed capacity; direct-B-barrier half closed',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# Direct barrier half of the S zero frontier is closed

Step4 is advanced but GLOBAL zero-weight LOW coverage remains OPEN.
The complete eight-spine S-family frontier has six distinct successors.
Four smaller-end words beginning L, and their actual LOW duals, are now
covered: LLL->J5, LLR/LRL->J6, LRR->new J7. LRL is reuse of an existing
all-nonnegative-incoming theorem, not a new certificate.

The new public debt is
    D_direct=max(D_anon,1_K,1_C,2*1_G7).
The J7 successor receives2. Its +1 exits reach E1 or C5/C6 with>=1;
C's possible zero lower return reaches K5/K6 with>=1. An arbitrary-upper-
block helper lemma gives every relevant Gamma1 weight>=2, including
Score-bearing helpers. Each operation preserves every previously valid
LOW inequality and every G7-source LOW row is proved.

Remaining S words RLL,RLR,RRL,RRR have exactly these three core successors:
    B6=6(5(4(L,E),E),7(E,8(E,E)));
    B7=7(5(4(L,E),6(E,E)),8(E,E));
    B8=8(5(4(L,E),7(6(E,E),E)),E).
All have4 at B depth2. They are not presumed solved. Other zero H1
configurations and zero H2/Gamma1 outside completed classes also remain.
The local counts are not a count or percentage of all M3 obligations.

The separate universal symbolic audit passed the six new ordered-role
spine identities and duals, J7 +1 outputs, generalized parity return,
K6 helper eligibility, typed helper-proof substitutions, source provenance
and signed slacks. No finite tests, source roots, psi lookups, numerical
tree/population assignments, label fits or bank censuses were run.
This is not full compiler formalization or external review.

R1-R4/current caps, original weak LE/G/unused fields, H/q/prices,
full147-O/127-M closure, SAME midpoint, independent witnesses, free high v
and corrected h0 remain. All{len(pins)} pinned prior files and HEAD/tracked
tree unchanged. New charged CPU={charge}; cumulative={total}/7200;
remaining={7200-total}, including reserve5. New finite tests=0.

Proof: DIRECT_BARRIER_THEOREM.md. Separate audit: PROOF_AUDIT.md.
Full M3 and Dynamic Optimality remain OPEN. No new whole-signature or
original negative-cycle claim is made.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'direct_barrier_S_words':'CLOSED',
      'remaining_S_successor_cores':['B6','B7','B8'],'global_zero_LOW':'OPEN','M3':'OPEN',
      'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
