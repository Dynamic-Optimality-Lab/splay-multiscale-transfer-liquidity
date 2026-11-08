"""Immutable dependency/resource publication; no mathematical tests."""
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
    assert a['status']=='UNIVERSAL_RR_RELEASE_AUGMENTATION_SYMBOLIC_AUDIT_PASS'
    assert a['each_previously_valid_LOW_inequality_preserved'] and a['all_Z_source_LOW_inequalities_proved']
    assert a['Z_exceptional_marked5_child_to_C_included'] and a['C_zero_endpoint_K_has_no_V_filter']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=757.515625+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':757.515625,'new_symbolic_checker_CPU':r['child_CPU'],
      'new_controller_CPU_through_finally':e['whole_process_CPU_seconds'],'new_compute_CPU':charge,
      'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,
      'guaranteed_remaining_CPU':7200-total,'reserve':5,
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
      'RESEARCH_RULES.md','M3_XFER04/RELEASE_CAPACITY_THEOREM.md','M3_XFER04/PROOF_AUDIT_v2.md',
      'M3_XFER04/certificate.json','M3_XFER04/resources.json','M3_XFER04/final_manifest_v2.json',
      'M3_XFER03/BURIED_CUT_THEOREM.md','M3_XFER03/PROOF_AUDIT.md',
      'M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md','M3_AER01/RESULT.md',
      'M3_POP5_RISK01/SOURCE_LIFT.md','M3_COMB_AUD01/AUDIT_REPORT.md',
      '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
      '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py',
      '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_INVENTORY.py',
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
      'status':'PROVED_RESTRICTED_DOMAIN','theorem':'UNIVERSAL_LOW_SAFE_THREE_REGION_AUGMENTATION_FOR_P5_P6_RR_RELEASES',
      'public_regions':{
        'Z':'J5/J6, root5/6, Score4 at LL, L kind0, V subset4..8; actual order-duals',
        'C':'C5, root5, Score4 at L, first pair a<4,5 marked; actual order-dual',
        'K':'root a, first pair a<4,5 marked, Score4 R,Score5 RR,both B depths<=3; actual order-dual; no V filter'},
      'input_class':'any public Lambda<=D<=2; no global feasibility assumption',
      'safe_operation_order':['max(D,1_K)','max(previous,1_C)','max(previous,2*1_Z)'],
      'explicit_combined_debt':'D_RR=max(D_release,1_K,1_C,2*1_Z)',
      'each_previously_valid_original_LOW_row_preserved':True,
      'all_Z_source_original_LOW_rows_proved':True,
      'all_named_P5_P6_A_RR_zero_releases_closed':True,
      'marked5_intervening_node_and_plus1_exit_included':True,
      'arbitrary_already_debt2_K_or_C_source_coverage_claimed':False,
      'Score_bearing_Gamma1_helpers_covered_in_theorem_regions':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_audit_claimed':False,
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'all_debt2_releases_solved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['general anonymous-separator releases outside this RR theorem','other core arrangements','global zero and +1 coverage'],
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_state_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'removes the named P5/P6 A-RR debt2 zero family while preserving every previously valid LOW inequality',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# The P5 and P6 RR zero releases are closed

An explicit public debt operation is proved and separately symbolically
audited for both P5/P6 A-RR releases and their actual LOW order-duals:

    D_RR=max(D_release,1_K,1_C,2*1_Z).

The zero successor Z keeps two credits after the separator disappears
below the shadow. A marked intervening Score5 is included: its +1 exit
reaches C with at least one credit; C's possible zero return reaches K
with at least one. A parity lemma bounds old-child depth by3. K's guard
includes full boundary states with old-owner G observations. No private
inventory, hidden separator identity or persistent witness is read.

Every previously valid original LOW inequality is preserved. All Z-source
LOW inequalities and all nonnegative incoming-to-Z inequalities hold,
including Score-bearing helper cases and the original Gamma0 floor law.
This closes the complete named RR family without rerunning old checks.
The separate audit checks universal term identities, parity endings,
source provenance, helper eligibility, aliases and signed slacks. It is
not a formalization of the entire original compiler or an external review.

The inherited HIGH/h0 bridge gives finite weight>=-7 and closed weight>=0
for the stated covered LOW legs. Full147-O/127-M closure, SAME midpoint,
independent witnesses, weak LE, G/unused fields and free high v remain.

Full M3 and Dynamic Optimality remain OPEN. General anonymous-separator
releases outside this RR theorem, other core arrangements and global
zero/+1 coverage remain. No whole-signature count or cycle claim changes.

R1-R4/current caps preserved. New finite tests/source transition queries/
root evaluations/old psi lookups/label fits/bank censuses=0. New charged
CPU={charge}; cumulative={total}/7200; remaining={7200-total}, including
reserve5. All{len(pins)} pinned prior files and HEAD/tracked tree unchanged.

Proof: RR_RELEASE_THEOREM.md. Independent derivation and scope audit:
PROOF_AUDIT.md. Machine-readable certificate: certificate.json.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'RR_family':'CLOSED','M3':'OPEN',
          'new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,
          'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
