"""Record the genuine symbolic lemma and reject an unsupported M3 promotion."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists()
    run=read(BASE/'run_result.json');ctrl=read(BASE/'controller_exit.json');a=read(BASE/'symbolic_audit.json');allocation=read(BASE.parent/'M3_GAPMULTI01/obstruction.json')
    assert run['status']=='PRIVATE_ERASURE_LEMMA_AUDITED_FULL_M3_DESCENT_NOT_PROVED' and run['error'] is None and ctrl['error'] is None
    assert a['status']=='UNIVERSAL_ERASURE_ROTATION_SCHEMAS_SYMBOLICALLY_VERIFIED' and len(a['schemas'])==2
    assert not a['certificate_labels_read'] and not a['shared_state_descent_established'] and not a['full_source_formalization_claimed']
    assert allocation['status']=='REFUTED_EXACT_SHARED_PORT_CORE_SPLIT_DETERMINACY' and allocation['same_full_source_state'] and allocation['same_full_destination_state'] and allocation['complete_original_roots']==allocation['independent_replays']==2
    assert allocation['hidden_core_bills'][0]!=allocation['hidden_core_bills'][1]
    assert run['new_finite_population_tests']==run['new_source_transition_queries']==run['new_original_root_evaluations']==0
    assert run['new_child_process_CPU']<run['allocated_cap']<=120
    charge=run['new_child_process_CPU']+ctrl['whole_process_CPU_seconds'];total=754.46875+charge;assert total<7200-5
    resources={'prior_uniform_CPU_charge_retained':754.46875,'new_symbolic_checker_CPU':run['new_child_process_CPU'],'new_controller_CPU_through_finally':ctrl['whole_process_CPU_seconds'],'new_measured_compute_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'old_signature_campaign_ledger_unchanged':7195.203125,'new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'new_potential_fits':0,'old_certification_checks_repeated':0,'caps_preserved':True,'symbolic_phase_CPU_cap':120,'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'};write(BASE/'resources.json',resources)
    names=['RESEARCH_RULES.md','M3_PRED02/resources.json','M3_PRED02/PROOF_AUDIT.md','M3_PRED02/STRATEGY_REVIEW.md','M3_PRED02/independent_original_verification.json','M3_PRED02/witness.json','M3_POP5_RISK01/DOMAIN_THEOREM.md','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP5_RISK01/certificate.json','M3_GAPMULTI01/RESULT.md','M3_GAPMULTI01/obstruction.json','M3_AER01/RESULT.md','M3_GAP01/core_refinement_v2.py','M3_GAPINT01/RESULT.md','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_OUT01/RESULT.md','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py']
    write(BASE/'dependencies.json',{'completed_certificates_and_source_obstructions_reused_not_replayed':True,'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in names]})
    old=read(BASE/'entry_baseline.json');pins={e['path'] for e in old['files']}
    for i,e in enumerate(old['files']):
        assert sha(Path(e['path']))==e['sha256'],e['path']
        if (i+1)%1000==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write(BASE/'concurrent_additions.json',{'not_math_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head'] and not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)};write(BASE/'integrity.json',integrity)
    cert={'status':'PRIVATE_EXPOSURE_ERASURE_LEMMA_PROVED_UNIVERSAL_M3_PROOF_INCOMPLETE','private_term_lemma':'C(Splay_z(T))=C(Splay_z(C(T))) for targets with initially nonempty Score support','anonymous_population_quantifier':'arbitrary finite, no fixed signature','newly_exposed_Score_free_decorations_handled':True,'all_newly_exposed_anonymous_nodes_handled':False,'universal_rotation_schemas_symbolically_checked':True,'full_original_source_formalization_claimed':False,'shared_state_descent':'NOT_PROVED','Score_empty_helper_simulation':'NOT_ESTABLISHED_BY_THIS_LEMMA','new_candidate_J_proposed':False,'new_finite_population_tests':0,'full_M3_gate_passed':False,'M3_status':'OPEN','DynamicOptimality_status':'OPEN','new_original_signature_certificates':0,'original_negative_cycle_certified':False,'NET_ORIGINAL_M3_SIGNED_PROOF_ADVANCEMENT':0,'R1_R4_preserved':True,'h0_correction_preserved':True,'resources':resources,'integrity':integrity};write(BASE/'certificate.json',cert)
    report=f'''# Exposure01: proof-only analysis; M3 remains unproved

**I did not complete a universal M3 proof. No finite-population tests or
new certificate fits were run.** The proposed erasure route has a genuine
universal private-tree identity, but no established shared-state potential.

The total-five obstruction reveals the issue: a source debt2 must leave
debt1 when a +1 access exposes additional anonymous nodes. In that witness,
three exposed nodes lie below Score0 and have no Score support. Pruning
Score-empty decoration gives the population-independent identity

    C(Splay_z(T))=C(Splay_z(C(T)))

for every target whose initial subtree has nonempty Score support. The
proof uses support/idempotence, both universal rotation identities and
path/context induction. A separate symbolic normalizer checked the local
identities on arbitrary subtree variables, without sampling populations,
reading potential labels or evaluating original roots. The precise scope
and trust boundary are in ERASURE_LEMMA.md.

This is NOT the missing signed invariant yet. C uses private hidden-Score
inventories; existing accepted multi-gap witness pairs have identical full
shared states but different such inventories/projections. A potential
constant on all compatible projections has not been constructed or proved.
Independent witnesses cannot be treated as one persistent hidden history.
Nor does this lemma by itself simulate an erased Score-empty helper.
Additional Score-bearing anonymous structure also survives pruning.

Consequently the public-descent/signed-preservation premise remains open.
Assuming it would conceal the original proof burden. The full-M3 gate
does not pass, and no claim of M3, new sector, negative cycle or universal
J is made. PROOF_AUDIT.md gives the exact failure of the attempted promotion.

R1-R4,h0,current caps retained; all{len(pins)} prior files byte-identical,
Git HEAD/tracked tree unchanged. New symbolic/controller compute CPU={charge};
cumulative uniform allowance{total}/7200; guaranteed remaining{7200-total}.
New finite-population tests/source queries/original-root evaluations=0.
NET ORIGINAL M3 SIGNED PROOF ADVANCEMENT=0. All3761 prior signature
certificates remain valid; full M3/Dynamic Optimality remain OPEN.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',cert);print(json.dumps({k:v for k,v in cert.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
