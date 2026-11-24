"""Bind verified results without promoting controls or proof-family exclusions."""
import sys
import ast
import json
import hashlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))


def write(name,value):
    path=HERE/name;assert not path.exists();path.write_text(json.dumps(value,indent=2),encoding='utf-8')


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    checks=read('FINAL_CHECK_RESULTS.json');assert checks['passed']
    notion=read('NOTION_SAVE_VERIFICATION.json');assert notion['saved'] and notion['main_content_normalized_readback_match']
    assert len(notion['linked_pages'])==2
    control=read('run_006/CONTROL_CERTIFICATE.json');cold=read('COLD_REPRODUCTION_VERIFICATION.json')
    assert control['status']=='PROVED_SCOPED_SYMBOLIC_CERTIFICATE' and cold['cold_reused_counterconstraints']==0
    assert read('run_006_INDEPENDENT_PROOF_VERIFICATION.json')['passed']
    global_result=read('GLOBAL_ENERGY_SEARCH_RESULT.json');assert global_result['universal_CD']=='OPEN'
    preservation=read('PRESERVATION_VERIFICATION.json');assert preservation['passed'] and preservation['prior_hashes']==5625
    audit=read('INDEPENDENT_AUDIT_VERIFICATION.json');metric=read('INDEPENDENT_METRIC_VERIFICATION.json')
    assert audit['passed'] and metric['passed']
    engine={
        'engine':'WORKING_BOUNDED_JOINT_ACCOUNTING_INVARIANT_INDUCTION_SEARCH',
        'active_target':'Unrestricted Universal CD: exists one finite absolute C, Q_B(W)<=C*A(W) for every admissible exactly paired-closed original source.',
        'target_scope_restricted':False,'unpaid_local_cost_allowed':True,
        'implemented':['Joint finite-grammar accounting/energy/invariant CEGIS','Unbounded symbolic initialization and successor-induction teacher','Original six-case rotation compiler with arbitrary hanging subtrees','Persistent globally shared overflow account','Scope-safe independent checker and Lean emitter','Parametric all-constant original-source energy-grammar teacher','Complete original witness and geodesic verification'],
        'not_implemented':['Automatic invention of arbitrary physical invariant atoms','General proof-program synthesis beyond the declared grammar','End-to-end formalization of the complete original BST model'],
        'unrestricted_attempt':global_result['status'],
        'universal_CD':'OPEN','accepted_global_certificate':None,
        'new_unrestricted_root_cost_obligations_deleted':0,
        'cold_joint_control':{'scope':'At most two B targets, unrestricted physical support and A-only operations','constant':control['constant'],'iterations':len(control['iterations']),'cached_counterconstraints':0,'proof_obligations':len(control['proof_dag']),'is_root_proof':False},
        'original_source_metric_obstruction':'No Phi_N=f_N(D_rot) whole-operation original-q certificate, any arbitrary f_N and any finite C.',
        'metric_obstruction_is_CD_counterexample':False,
        'first_missing_implication':global_result['first_missing_implication'],
        'checks':{'rejection_tests':17,'Lean_kernels':2,'original_complete_sources':audit['complete_sources']+metric['complete_original_sources'],'original_operations':audit['operations']+metric['operations'],'real_rotations':audit['real_rotations']+metric['real_rotations']},
        'preserved_prior_artifacts':5625,'proof':notion['main_page']}
    write('ENGINE_RESULT.json',engine)
    claims=[
        {'claim':'Combined physical local/global actual issuance <=(9H+J+T)A; greatest clipped cyclic balance exists even if unfunded.','status':'PROVED_UNIVERSAL_ACCOUNTING_INTERFACE','funding_guard_assumed':False},
        {'claim':'Q_B <=(c+d)A+R for the explicitly recorded positive original-q energy deficit R.','status':'PROVED_UNIVERSAL_ACCOUNTING_INTERFACE','global_R_bound':'OPEN'},
        {'claim':'Joint compiler learns Q_B<=A control with arbitrary hanging support.','status':'PROVED_SCOPED_CONTROL_RECOVERY','root_cost_obligations_deleted':0},
        {'claim':'Scalar target-OTHER relaxation admits unbounded cost pressure.','status':'PROVED_ABSTRACT_MODEL_BARRIER','original_source_realization':False},
        {'claim':'D(T,left_vine_N)=N-left_spine_length(T), arbitrary physical BST.','status':'PROVED_UNIVERSAL_GEOMETRIC_LEMMA','verification':'Lean construction/lower-bound components plus labeled original rotation verification.'},
        {'claim':'No whole-operation Phi_N=f_N(D_rot) original-q certificate for any arbitrary f_N and finite real C.','status':'REFUTED_PARAMETRIC_ORIGINAL_SOURCE_GRAMMAR','source':'Complete counted capped H3q; A14,Q=q+1,distance flat fragment.','not_refuted':'Global memory banks, arbitrary full-shape energies and Universal CD.'},
        {'claim':'Unrestricted Universal CD or relaxed Universal CD','status':'OPEN','constant_proved':None},
        {'claim':'Dynamic Optimality','status':'OPEN','complete_reduction_verified_here':False}]
    write('THEOREM_CERTIFICATE.json',{'proof':notion['main_page'],'claims':claims,'all_prior_results_preserved':True,'root_scope_restricted':False,'new_unrestricted_root_cost_obligations_deleted':0})
    review={'before':'No working joint accounting/invariant/induction synthesis loop; prior bank guard and global overflow bound open.',
        'user_steering':'Do not scope the target. Continue toward unrestricted Universal CD.',
        'result':'Joint bounded proof compiler implemented and cold-reproduced; scalar model limitation checked; additional unrestricted physical energy grammar excluded by a complete all-q original-source construction.',
        'after':'The original arbitrary-source constant bound remains OPEN. Controls and architecture exclusions do not delete the root cost obligation.',
        'new_assumptions_on_root':[],
        'actual_advancement':'Validated proof-search infrastructure and a new exact original-source accounting-family obstruction; no newly proved global residual budget.',
        'no_automatic_capacity_or_feature_treadmill':True,
        'next_acceptance_obligation':global_result['first_missing_implication'],
        'bounded_unpaid_cost':'Any R<=K*A with absolute finite K suffices. Persistent earlier-A-funded bank depletion is explicitly permitted across the anchored fragment.',
        'resource_checkpoint':'The admitted additional unrestricted source/metric attack is complete. No unsupported universal proof is claimed and no historical result is retracted.',
        'original_complete_sources_new_metric':3,'root_cost_obligations_deleted':0,'universal_CD':'OPEN'}
    write('STRATEGY_REVIEW.json',review)
    pins=[]
    for path in sorted(HERE.iterdir()):
        if path.suffix in ('.py','.lean'):
            if path.suffix=='.py':ast.parse(path.read_text(encoding='utf-8'),filename=path.name)
            pins.append({'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    write('UNIVERSAL_SOURCE_PROOF_REFERENCE.json',{'proof':notion['main_page'],'hub':'https://app.notion.com/p/41f6251839be81d18fd6c910dcaa8a2d','prior_proof':'https://app.notion.com/p/4206251839be81dda9f1d508ecdc1195','H3q_physical_recurrence':'https://app.notion.com/p/41e6251839be81cd96e6e6688cd4e2f9','source_code_pins':pins,'notion_readback_verified':True,'truth_scope':'All mathematical claims are separately typed; this filename is not a Universal-CD proof.','universal_CD':'OPEN'})
    corrections=read('IMPLEMENTATION_CORRECTIONS.json')
    corrections['corrections'].append({'component':'Metric Lean kernel','observation':'The first draft had an unnecessary omega after simp had closed the goal. The build was rejected, including its error-recovery sorryAx dependencies.','correction':'Remove that redundant tactic, then accept only a clean build with all printed dependencies free of sorryAx.','accepted_unsound_result':False})
    (HERE/'IMPLEMENTATION_CORRECTIONS.json').write_text(json.dumps(corrections,indent=2),encoding='utf-8')
    print(json.dumps({'engine':engine['engine'],'universal_CD':'OPEN','target_scope_restricted':False,'preserved_prior_artifacts':5625,'proof':notion['main_page']}))


if __name__=='__main__':main()
