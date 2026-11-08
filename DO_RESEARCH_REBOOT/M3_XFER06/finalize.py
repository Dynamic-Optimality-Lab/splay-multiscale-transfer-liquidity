"""Immutable dependency/resource publication only; no mathematical tests."""
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
    assert a['status']=='ANONYMOUS_RELEASE_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert a['depth6_final_proxy_has_real_core_child'] and a['depth6_contradiction_applied_only_at_final_endpoint']
    assert a['each_previously_valid_LOW_row_preserved'] and a['all_N_source_LOW_rows_proved']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=757.90625+charge
    assert r['child_CPU']<r['allocated_CPU_cap']<=120 and total<7200-5
    resources={
      'prior_uniform_CPU_charge_retained':757.90625,'new_symbolic_checker_CPU':r['child_CPU'],
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
      'RESEARCH_RULES.md','M3_XFER05/RR_RELEASE_THEOREM.md','M3_XFER05/PROOF_AUDIT.md',
      'M3_XFER05/certificate.json','M3_XFER05/resources.json','M3_XFER05/final_manifest.json',
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
      'status':'PROVED_RESTRICTED_DOMAIN',
      'theorem':'LOW_SAFE_TWO_CREDIT_ANONYMOUS_P5_P6_RELEASE_AUGMENTATION',
      'N':'J5/J6; root5/6, Score4 at L, kind0 anonymous at LL,V subset4..8; actual LOW order-dual',
      'input_class':'any public Lambda<=D<=2; no global feasibility assumption',
      'operation':'F=max(D,2*1_N)',
      'explicit_combined_debt':'D_anon=max(D_RR,2*1_N)',
      'private_separator_gap_or_inventory_inferred':False,
      'each_previously_valid_original_LOW_row_preserved':True,
      'all_N_source_original_LOW_rows_proved':True,
      'minimum_helper_signed_weight_bound':2,
      'minimum_helper_key_mechanism':'only possible +1 case at depth6 forces nonempty FINAL proxy child, contradicting b_valid',
      'Score_bearing_helper_support_allowed':True,
      'anonymous_P5_P6_R_RL_closed_by_N':True,
      'anonymous_P5_P6_RR_closed_by_existing_Z':True,
      'both_actual_LOW_orientations_proved':True,
      'independent_universal_symbolic_audit':'PASS',
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_anonymous_separator_core_patterns_solved':False,
      'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
      'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'remaining_open':['other core arrangements','general zero/+1 coverage','universal LOW completeness theorem'],
      'finite_walk_bound_with_stated_LOW_coverage':-7,'full_closed_walk_bound_with_stated_LOW_coverage':0,
      'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'NET_ADVANCEMENT':'removes anonymous P5/P6 debt2 zero releases in all three target positions while preserving every previously valid LOW inequality',
      'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    result=f'''# Anonymous P5 and P6 zero releases are closed

A public two-credit rule is proved and separately symbolically audited:

    D_anon=max(D_RR,2*1_N).

N has core J5/J6, root5/6, Score4 at L and an anonymous kind0 node at LL,
with the stated public V guard; include actual LOW order-duals. No private
gap, inventory, hidden separator identity or persistent witness is read.
Every previously valid LOW inequality is preserved and all N-source LOW
rows hold. H1 +1 exits reach E1; maximum helpers cost at least2.

The new minimum-helper case also costs at least2. Its only possible +1
terminal depth is6. Two determined final pairs leave a real core child
under the gap proxy, contradicting ORIGINAL final gap-leaf validity.
The proof retains Score-bearing support and permits a nonleaf proxy at
the intermediate boundary. Terminal-only original q and H are unchanged.

Anonymous P5/P6 zero releases at R/RL end in N. Those at RR end in the
already proved Z, whose guard is separator-independent. All three have
residual2-D_anon(source)>=0, including the debt2 equality case, for all
compatible original signatures/private witnesses and both orientations.

The separate audit covers universal parity/leaf identities, anonymous
visibility on either side of a, source semantics and signed slacks. No
finite test, source root, old psi lookup, bank census or label fit ran.
It is not a formalization of the entire compiler or an external review.

Other core arrangements and global zero/+1 completeness remain OPEN.
Full M3/Dynamic Optimality remain OPEN. No whole-signature or cycle claim
changes. The inherited HIGH/h0 bridge applies with the stated LOW coverage;
full147-O/127-M closure, SAME midpoint and independent witnesses remain.

R1-R4/current caps preserved. New charged CPU={charge}; cumulative={total}
of7200; remaining={7200-total}, including reserve5. All{len(pins)} pinned
prior files and HEAD/tracked tree unchanged. New finite tests=0.

Proof: ANONYMOUS_RELEASE_THEOREM.md. Separate derivation/scope audit:
PROOF_AUDIT.md. Machine-readable certificate: certificate.json.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(result)
    manifest=dict(certificate)
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',manifest)
    print(json.dumps({'status':certificate['status'],'anonymous_P5_P6_family':'CLOSED',
      'M3':'OPEN','new_compute_CPU':charge,'cumulative_CPU':total,
      'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
