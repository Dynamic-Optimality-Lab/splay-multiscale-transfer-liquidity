"""Bind proved physical statements and the still-open unrestricted obligation."""
import sys
import ast
import json
import hashlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))
def write(name,data):
    p=HERE/name;assert not p.exists();p.write_text(json.dumps(data,indent=2),encoding='utf-8')


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    checks=read('FINAL_CHECK_RESULTS.json');assert checks['passed']
    notion=read('NOTION_SAVE_VERIFICATION.json');assert notion['saved'] and notion['main_readback_match']
    assert all(r['append_verified'] and r['prior_content_preserved'] for r in notion['linked_pages'])
    physical=read('INDEPENDENT_VERIFICATION.json');symbolic=read('SYMBOLIC_VERIFICATION.json');zero=read('ZERO_EDGE_INDEPENDENT_VERIFICATION.json')
    assert physical['passed'] and symbolic['passed'] and zero['passed']
    preserve=read('PRESERVATION_VERIFICATION.json');assert preserve['passed'] and preserve['prior_hashes']==5711
    source={
        'status':'PROVED_PARAMETRIC_ORIGINAL_SOURCE_GRAMMAR_OBSTRUCTION',
        'old_source':'Complete original H3q, m=16(q+1)+1, q>=1, common right-vine start, empty prefix and both full restoration scans.',
        'full_source':'Rigid right-vine gap expansion, old gap m-6 has4 vertices; gap16(q-j)-5 has16*(2^j-1), j=0..q-1; all other gaps empty. Keys relabeled by full physical rank; operation word accesses only mapped old keys.',
        'physical_support':'16*2^q+5','original_carrier_support':'16(q+1)+1',
        'A':'64(q+1)','Q_B':'28q+25','source_model_changed':False,
        'original_critical_operation':'m+7, KEEP mapped(m-7), a=1, q_B=q+1',
        'RR_physical_profile':'a=d=7,b=c=16*2^j-9; c_next=2c+9. Proper size pairs are equal, all full hanging subtrees retained.',
        'energy':'Phi_w=-sum_{I in J_X(B) minus J_X(A)} w(|I|), full physical X.',
        'whole_operation_energy_change':'w(16*2^q-1)+w(16*2^q+1); A change0 and every neutral RR change0.',
        'bounded_signed_weights':'For |w|<=M, q_B+DeltaPhi>=q+1-2M; choose q+1>C+2M. No finite C whole-operation certificate.',
        'nonnegative_weights':'DeltaPhi>=0, so q+1>C refutes every finite C even without a bounded-weight assumption.',
        'does_not_refute':['Universal CD','Original-carrier cardinality energies','Arbitrary nonlinear shape energies','Persistent global history banks'],
        'proof_dependencies':['Old H3q j=2/3 comb recurrence','Exact arbitrary rigid-gap rotation substitution','Joint affine induction and physical RR size algebra','Final original LR creates the two A-common child intervals'],
        'full_source_ratio':'Q_B/A<7/16','new_UF_escape_claim':False,'proof':notion['main_page']}
    write('PARAMETRIC_SOURCE_CERTIFICATE.json',source)
    claims=[
        {'claim':'Closed original DELETE excursions restoring the full A tree cannot increase the frozen bank Omega_H at greatest cyclic balances.','status':'PROVED_UNIVERSAL_TRANSFORMATION','funding_assumption':False,'quantity':'All-original-B clipped unpaid cost, not a redefined U/UF residual.'},
        {'claim':'Same-constant lossless DELETE-loop normalization for Universal CD and Omega_H<=K*A.','status':'PROVED_CONSTRUCTIVE_EQUIVALENCE','explicit_construction':'Exact complete-A-state loop erasure; cut after a KEEP with an admissible noncredited prefix.','global_bound_still_open':True},
        {'claim':'Rigid common-gap expansion preserves the complete original cost/credit word and paired closure.','status':'PROVED_UNIVERSAL_SOURCE_TRANSFORMATION','credit_capacity_effect':'The same fixed-capacity cost-based reserve process and cyclic deficits are unchanged.'},
        {'claim':'No bounded signed full-X size-weight defect energy, or any nonnegative such energy, satisfies the attempted whole-operation cost law for any finite C.','status':'REFUTED_PARAMETRIC_ORIGINAL_SOURCE_GRAMMAR','proof':notion['main_page']},
        {'claim':'Exact C=4 minimum cyclic reserve capacity on the explicit all-q family.','status':'PROVED_SOURCE_FAMILY','capacity':'max(8r,12r-4,14r-12,15r-28), r=q+1','is_unrestricted_bound':False},
        {'claim':'Full and cross-block zero-stock directed edge-agreement invariants.','status':'REFUTED_EXACT_ORIGINAL_EVENTS','events':[['B',33,5],['B',34,5]],'bank_funding_refuted':False},
        {'claim':'Universal or relaxed Universal CD, any absolute finite C','status':'OPEN','constant_proved':None},
        {'claim':'Dynamic Optimality','status':'OPEN','complete_reduction_checked_here':False}]
    write('THEOREM_CERTIFICATE.json',{'claims':claims,'root_scope':'unrestricted','new_absolute_root_cost_budgets_proved':0,'all_prior_results_preserved':True,'proof':notion['main_page']})
    first_missing='A quantitative globally shared original-A credit bound for bank-unpaid B demand on DELETE-loop-erased histories, including KEEP-coupled ancestry destruction/recreation, repeated debt, arbitrary interleavings and exact cyclic restoration.'
    engine={
        'engine':'GSO_ORIGINAL_PAIRED_CREDIT_DYNAMICS_ADAPTER','target':'Unrestricted Q_B(W)<=C*A(W), some absolute finite C.',
        'root_scope_restricted':False,'bounded_unpaid_cost_allowed':True,'universal_CD':'OPEN',
        'new_capabilities':['Exact original-gap integer optimization','Joint unbounded physical-size recurrence synthesis','Literal cyclic credit provenance and minimum-storage teacher','Constructive complete-A-state DELETE-gap normalization','Independent full-source and failed-invariant event verification'],
        'proved_source_uniform_rule':'Omega_H(W_with_closed_DELETE_excursions)<=Omega_H(W), at the greatest cyclic seam. Erasure gives a same-constant normalization.',
        'all_parameter_energy_family_rejected':True,'physical_zero_edge_candidates_rejected':2,
        'selected_H5_bank_refuted':False,'absolute_root_cost_budgets_proved':0,
        'first_missing_implication':first_missing,
        'limits':['General arbitrary-predicate invention is not implemented','No end-to-end full original BST formalization','Storage mean-cost criterion does not prove its own mean premise','Local-bank and direct-reserve witness certificates are separate, not duplicate assignments'],
        'checks':{'complete_new_sources':physical['complete_original_sources'],'original_operations':physical['operations'],'real_rotations':physical['real_rotations'],'unbounded_symbolic_checks':len(symbolic['checks']),'soundness_tests':18,'Lean_kernels':2},
        'preserved_prior_artifacts':5711,'proof':notion['main_page']}
    write('ENGINE_RESULT.json',engine)
    review={'before':'Root credit invariant open; no construction connecting arbitrary original ancestry and cyclic credit. Previous scalar and metric architectures insufficient.',
        'result':'Proved a stock-monotone transformation and constructive lossless normalization; learned exact source-size induction; rejected a complete size-weight energy family and two physical zero-edge predicates; reconstructed literal original-A cyclic credit.',
        'after':'Root target still unrestricted and OPEN. The new normalization reduces the search constructively; it is not an absolute unpaid-cost budget.',
        'new_assumptions_on_root':[],
        'exact_first_missing':first_missing,
        'strategy_stop':'Both full and cross-block zero-edge predicates have exact complete-source counterevents. Stop this family; no automatic radius, threshold or capacity weakening.',
        'no_finite_coverage_claim':True,'no_new_hard_UF_paid_class_claim':True,
        'new_absolute_root_cost_budgets_proved':0,'all_prior_results_preserved':True}
    write('STRATEGY_REVIEW.json',review)
    lean=[r for r in checks['checks'] if r['command'][0]=='lean']
    assert len(lean)==2 and all(r['exit_code']==0 and 'sorryAx' not in r['stdout'] for r in lean)
    write('LEAN_VERIFICATION.json',{'passed':True,'builds':lean,'scope':checks['scope']})
    pins=[]
    for p in sorted(HERE.iterdir()):
        if p.suffix in ('.py','.lean'):
            if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
            pins.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    write('PROOF_REFERENCE.json',{'proof':notion['main_page'],'previous_joint_proof':'https://app.notion.com/p/4206251839be81d49a1bcbaa5f734f74','source_H3q_recurrence':'https://app.notion.com/p/41e6251839be81cd96e6e6688cd4e2f9','code_pins':pins,'notion_readback_verified':True,'universal_CD':'OPEN'})
    print(json.dumps({'universal_CD':'OPEN','source_uniform_normalization_proved':True,'new_absolute_root_budgets':0,'preserved_prior_artifacts':5711,'proof':notion['main_page']}))


if __name__=='__main__':main()
