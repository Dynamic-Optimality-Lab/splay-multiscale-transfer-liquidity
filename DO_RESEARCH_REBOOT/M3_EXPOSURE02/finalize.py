"""Record exact universal helper reduction and the still-open public debt."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists()
    r=read(BASE/'run_result.json');x=read(BASE/'controller_exit.json');a=read(BASE/'symbolic_audit.json')
    assert r['status']=='UNIVERSAL_HELPER_REDUNDANCY_AUDITED_PUBLIC_DEBT_OPEN' and r['error'] is None and x['error'] is None
    assert a['status']=='UNIVERSAL_ERASED_HELPER_REDUCTION_ALGEBRA_AUDIT_PASS'
    for field in ['source_L_exact_pointer_identity','source_LR_authoritative_shadow_identity','right_max_dual_shadow_identity','G_alias_owner_children_included_in_shadow_interface','minimum_spine_base_and_induction_step_verified','old_root_depth_parity_verified','odd_B_frontier_exact_identity','even_B_frontier_leaf_contradiction','terminal_q_source_dependency_confirmed','endpoint_fresh_bounds_source_dependency_confirmed']:assert a[field]
    assert a['symbolic_weight_gap']==1 and not a['public_debt_constructed'] and not a['full_source_formalization_claimed']
    assert r['new_finite_population_tests']==r['new_source_transition_queries']==r['new_original_root_evaluations']==0
    assert r['new_child_process_CPU']<r['allocated_cap']<=120
    charge=r['new_child_process_CPU']+x['whole_process_CPU_seconds'];total=754.828125+charge;assert total<7200-5
    resources={'prior_uniform_CPU_charge_retained':754.828125,'new_symbolic_checker_CPU':r['new_child_process_CPU'],'new_controller_CPU_through_finally':x['whole_process_CPU_seconds'],'new_compute_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'old_signature_campaign_ledger_unchanged':7195.203125,'new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'new_label_fits':0,'old_completed_certification_checks_repeated':0,'current_caps_preserved':True,'symbolic_phase_CPU_cap':120,'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'};write(BASE/'resources.json',resources)
    names=['RESEARCH_RULES.md','M3_EXPOSURE01/ERASURE_LEMMA.md','M3_EXPOSURE01/PROOF_AUDIT.md','M3_EXPOSURE01/resources.json','M3_GAP01/RESULT.md','M3_GAPINT01/RESULT.md','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_AER01/RESULT.md','M3_H2R01/manifest.json','M3_GAPMULTI01/obstruction.json','M3_CHIB02/RESULT.md','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_INVENTORY.py','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py']
    write(BASE/'dependencies.json',{'old_source_proofs_and_certificates_reused_not_replayed':True,'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in names]})
    old=read(BASE/'entry_baseline.json');pins={e['path'] for e in old['files']}
    for i,e in enumerate(old['files']):
        assert sha(Path(e['path']))==e['sha256'],e['path']
        if (i+1)%1000==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head'] and not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)};write(BASE/'integrity.json',integrity)
    cert={'status':'UNIVERSAL_ERASED_HELPER_CONSTRAINT_REDUCTION_PROVED_PUBLIC_DEBT_OPEN','helper_theorem':'all normalized Gamma1 H2 edges with initially Score-empty helper are range-safe or dominated by an original H1 edge on the SAME FULL endpoints','helper_theorem_premises':['0<=public D<=2','all original H1 signed inequalities','established original source normal forms'],'private_inventory_invariance_assumed_for_helper_theorem':False,'nonrange_helper_residual_margin':1,'full147_endpoint_comparison_including_unused_fields_and_B_bounds':True,'G_aliases_included':True,'terminal_q_only':True,'H2_edge_relabelled_as_H1':False,'new_debt_function_constructed':False,'inventory_independent_universal_debt_gap':'OPEN','both_gaps_closed':False,'M3_status':'OPEN','DynamicOptimality_status':'OPEN','original_negative_cycle_certified':False,'new_signature_certificates':0,'NET_ORIGINAL_M3_REDUCTION_ADVANCEMENT':'erased Gamma1 helper inequalities removed as independent constraints relative to mandatory H1/range conditions','NET_ORIGINAL_SIGNATURE_COVERAGE_ADVANCEMENT':0,'source_formalization_scope':'analytic source proof plus independent universal term/parity audit; not a full compiler formalization','new_finite_population_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,'resources':resources,'integrity':integrity};write(BASE/'certificate.json',cert)
    report=f'''# Exposure02: universal erased-helper reduction; public debt still open

**Both requested gaps are not closed.** A universal erased-helper constraint
reduction is proved and symbolically audited. A universal inventory-independent
debt satisfying H1 has NOT been constructed, so M3 remains unproved.

For ANY public ordinary-state function0<=D<=2 that satisfies the ORIGINAL
H1 inequalities, every normalized H2/Gamma1 edge with an initially
Score-empty anonymous helper satisfies its signed inequality, for ALL
signatures/private inventories. No private erasure invariance is assumed.

The proof classifies the real depth1/2 helper positions. Terminals0/8 or
the old B root have terminal depth<=5/2 respectively, hence q<=2 and w>=2,
so range suffices. In the remaining case, source root is the extreme
Score and terminal x is its opposite actual core child in A. Final B
fringe-leaf validity forces odd source B depth d=2k+1. A separate ORIGINAL
H1 edge has the SAME full shared endpoints, weight w1=2-k, while the
original H2 edge keeps w2=3-k. Therefore

    w2+D(t)-D(s)=[w1+D(t)-D(s)]+1>=1.

Actual H2 H/q/weights are not changed or fused. The source compiler's q
is terminal-only, not summed over events. Source/destination original
states are not quotiented: the A argument includes authoritative alpha7,
slot0 aliases/unused fields; B topology coincides and the same original
endpoint lo/hi fields remain valid. Both outer directions are included.
See HELPER_REDUCTION.md for the source-order, parity and witness proof.

The independent audit verifies universal term identities, arbitrary-spine
induction transitions, alias-aware shadow equality and symbolic weight
cancellation. No population/tree instantiations, fitted labels, bank census
or original-root evaluations were run. It is not a complete formalization
of the compiler; established source normal forms are reused premises.

The public-debt gap remains. A supremum over compatible private projected
potentials is inventory-independent by definition, but its extremizer need
not follow a given original edge. PUBLIC_DEBT_AUDIT.md proves that this
generic lifting inference fails; it does not claim M3 false. A new common
H1 debt and the remaining Score-bearing-helper arguments are still needed.

R1-R4,h0 and all caps retained. All{len(pins)} pinned prior files remain
unchanged; Git HEAD/tracked tree unchanged. New symbolic/controller CPU
{charge}; cumulative uniform allowance{total}/7200; remaining{7200-total}.
New finite tests/source queries/original-root evaluations=0. No new sector
or M3 promotion. The concrete progress is elimination of erased-helper
inequalities as independent constraints once mandatory H1/range hold.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',cert);print(json.dumps({k:v for k,v in cert.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
