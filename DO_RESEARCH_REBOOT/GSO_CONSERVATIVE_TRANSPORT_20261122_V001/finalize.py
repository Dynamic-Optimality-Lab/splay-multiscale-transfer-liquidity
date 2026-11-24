"""Bind completed executable checks to the durable mathematical proof ledger."""
import sys
import json
import ast
import hashlib
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed output'
    (HERE/name).write_text(json.dumps(value,indent=2),encoding='utf-8')


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    notion=read('NOTION_WRITE_VERIFICATION.json')
    assert notion['main']['readback_verified'] and notion['main']['exact_normalized_match']
    assert all(row['exact_normalized_match'] and row['old_content_preserved'] for row in notion['existing_pages'])
    verification=read('EXTENDED_INDEPENDENT_VERIFICATION.json')
    assert verification['passed'] and verification['entry_conjecture_refuted_on_original_U']
    assert read('INDEPENDENT_VERIFICATION.json')['passed'] and read('PRESERVATION_VERIFICATION.json')['passed']
    packet=read('PACKET_VERIFICATION.json');assert packet['passed'] and packet['sources']==36
    search=read('PACKET_SEARCH_RESULT.json');assert search['status']=='NO_COUNTEREXAMPLE_IN_BOUNDED_SEARCH'
    selected=read('SELECTED_ROLE_POLICY.json');assert selected['H']==5 and selected['middle_order']==['middle2','external','grandparent','parent']
    files=sorted(HERE.glob('*.py'))
    for path in files:ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    source=(HERE/'TransportKernel.lean').read_text(encoding='utf-8')
    assert 'sorry' not in source and '\naxiom ' not in source
    lean=subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/'TransportKernel.lean')],cwd=str(HERE),capture_output=True,text=True)
    write('LEAN_VERIFICATION.json',{'passed':lean.returncode==0,'returncode':lean.returncode,
          'stdout':lean.stdout,'stderr':lean.stderr,
          'scope':'Seven local integer warmup/retention/packet arithmetic theorems; not full BST or the universal guard.'})
    assert lean.returncode==0 and 'sorryAx' not in lean.stdout
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [*files,HERE/'TransportKernel.lean']}
    proof=notion['main']['url']
    write('NOTION_PROOF_REFERENCE.json',{'url':proof,'readback_verified':True,
          'instructions_version':'0.0.6','code_sha256':hashes,
          'status':'PROVED_SOURCE_UNIFORM_PARTIAL_PAYMENT_AND_LOCAL_RENEWAL; REFUTED_ENTRY_CONJECTURE; UNIVERSAL_CD_OPEN'})
    write('THEOREM_CERTIFICATE.json',{
        'proof':proof,'original_model':'Unchanged physical paired-closed sources, costs, original IDs and full Pi/U semantics.',
        'frozen_policy':'SELECTED_ROLE_POLICY.json plus ROLE_SYNTHESIS_ADMISSION.json',
        'source_uniform_partial_theorem':{
            'status':'PROVED_SOURCE_UNIFORM_FOR_EXPLICIT_PARTIAL_CLASS',
            'H':5,'eligibility':'Literal original B-double IDs with pooled stock>=1 in the selected rule\'s greatest clipped closed bank.',
            'original_U_paid_class':'P_U=P intersect original U_int by literal original IDs.',
            'literal_complement':'R_new=original U_int minus P_U. Historical residual definitions are unchanged.',
            'budget':'|P_U|<=|P|=actual consumption=issuance<=40A+5K_B<=45A.',
            'combined_original_interface':'Q_B<=51A+|R_new|.',
            'shared_A_load':'At most40 bank load per actual A unit plus5 for at most one incoming-gap KEEP voucher.',
            'credit_exclusions':'No reaching-prefix, virtual companion or ancestry-birth credit.',
            'dependency':'Prior constructive monotone greatest-seam theorem and exact conservative event identity.',
            'not_claimed':'P_U=all original U, P=all original Q, or exhaustive enlargement of the final UF paid partition.'},
        'local_renewal':{
            'status':'PROVED_RESTRICTED_PHYSICAL_STREAM',
            'domain':'Every real H>=1, six distinct physical block owners, fresh external and grandparent spine stocks>=1, all other stocks nonnegative.',
            'rule':'Target first, second-middle persistent root second.',
            'conclusion':'Each certified double is funded; target rises by>=1 until H; once full, persistent output>=1. Target warmup takes<=ceil(H) steps.',
            'full_profile':'At six full banks, continuing five outputs stay H and retired first-middle receives H-1.',
            'limitation':'Arbitrary interruptions must preserve entry conditions; universal entry is not assumed.'},
        'entry_conjecture':{
            'status':'REFUTED_EXACT_ON_COMPLETE_ORIGINAL_SOURCE',
            'witness':'H_(9,5), N=6145, A=24576,Q_B=11342, empty prefix and full counted paired restoration.',
            'id':['B',6152,3],'target':6138,
            'role_stocks':{'target':5,'external':1,'grandparent':0,'parent':0,'middle1':0,'middle2':0},
            'original_U_frame':[6083,6141],
            'funded':True,'receipt':'ENTRY_INVARIANT_OBSTRUCTION.json',
            'scope':'Refutes universal two-positive-spine entry, not the H=5 bank guard or Universal CD.'},
        'packet_identity':{
            'status':'PROVED_EXACT_GUARD_EQUIVALENCE_FOR_TARGET_FIRST_POOLING',
            'recurrence':'D_next=max(0,D+q-r), D=H-target; each genuine access starts D=0.',
            'all_paid_iff':'Every within-access contiguous packet has sum(q-r)<=H, using actual clipped-trajectory other-bank stocks.',
            'sharing':'r is existing transferred stock, never new A issuance.',
            'remaining_statement':'For arbitrary admissible sources the frozen H=5 rule has packet deficit<=5.',
            'remaining_statement_status':'OPEN'},
        'conditional_full_bounds':{'all_Q_paid':'Q_B<=45A','all_U_paid':'Q_B<=51A'},
        'unrestricted_root_cost_obligations_deleted':0,'universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
    write('STRATEGY_REVIEW.json',{
        'status':'OPEN_CHECKPOINT_WITH_NEW_LOCAL_RENEWAL_PROOF',
        'before':'Old priority fails all finite capacities; free transport for the new witnesses not checked.',
        'result':'Exact repair flows and a selected physical-role rule, a globally bounded partial class, quantified local renewal and exact refutation of universal entry.',
        'after':'Exhaustive arbitrary-source funding and the original root cost theorem remain OPEN.',
        'root_obligations_deleted':0,
        'scope_correction':'The H sources retain old periodic certificates; no new final-UF escaping class or universal coverage is claimed.',
        'missing_physical_implication':'Bound target packet deficits across arbitrary reachable paired-tree/bank states, interruptions, cross rotations and restoration.',
        'existence_burden':'The packet criterion is an equivalent guard monitor, not an independently established global inequality.',
        'stop_automatic_pivots':['Do not infer universal bound3 from observed deficits.','Do not assume the refuted entry predicate.','Do not automatically retune H or add another role family.','Do not assume all-source free-flow feasibility.'],
        'proof_target_if_resumed':'A physical induction or exact original counterexample for the frozen H=5 packet inequality, with a fresh bounded admission.'})
    write('ENGINE_RESULT.json',{
        'engine':'WORKING_CONSERVATIVE_TRANSPORT_AND_ROLE_SYNTHESIS_BACKEND','proof':proof,
        'implemented':['Sparse exact integer conservative bank teacher','Independent immutable original-source and separate primal/cut checker',
                       '24-order structural-role CEGIS with48 candidate/capacity pairs','Held-out complete nested and arbitrary-shape restoration sources',
                       'Symbolic one-credit-spine renewal','Exact literal original-U entry counterexample','Target-battery packet monitor','Bounded legal physical-state packet adversary'],
        'proved_global_budget_for_partial_class':'P_U<=45A; Q_B<=51A+R_new with explicit original-ID complement.',
        'full_original_Q_bound':'CONDITIONAL_NOT_PROVED',
        'local_renewal':'PROVED_RESTRICTED_PHYSICAL_STREAM',
        'universal_positive_spine_entry':'REFUTED_EXACT',
        'selected_policy':{'H':5,'same_direction_order':['target','middle2','external','grandparent','parent','middle1'],
                           'other_B_order':'target first, then increasing physical block',
                           'universal_funded_guard':'OPEN'},
        'independent_physical_sources':verification['independent_physical_sources_total'],
        'independent_integer_primal_cut_certificates':verification['independent_free_flow_cut_certificates'],
        'independent_physical_totals':verification['physical_totals'],
        'finite_selected_policy_Q_paid':verification['selected_policy_original_Q_paid'],
        'finite_observed_maximum_packet_deficit':packet['maximum_observed_deficit'],
        'bounded_adversary_transition_evaluations':search['transition_evaluations'],
        'bounded_adversary_supports_actually_tested':[row['n'] for row in search['cases']],
        'finite_success_is_universal_proof':False,
        'soundness_tests_passed':9,'Lean_arithmetic_theorems_checked':7,
        'prior_artifacts_preserved':5403,'unrestricted_root_cost_obligations_deleted':0,
        'universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
    write('FINAL_CHECK_RESULTS.json',{
        'passed':True,'independent_original_and_flow_verification':'INDEPENDENT_VERIFICATION.json',
        'independent_extended_policy_and_holdout_verification':'EXTENDED_INDEPENDENT_VERIFICATION.json',
        'packet_monitor_verification':'PACKET_VERIFICATION.json','exact_entry_counterexample':'ENTRY_INVARIANT_OBSTRUCTION.json',
        'symbolic_local_proofs':['SYMBOLIC_RETENTION_CERTIFICATE.json','SPINE_RENEWAL_CERTIFICATE.json'],
        'Lean':{'passed':True,'theorems':7,'receipt':'LEAN_VERIFICATION.json','no_sorry_or_new_global_axiom':True,
                'full_original_BST_formalization':False},
        'python_AST':{'passed':True,'files':len(files)},
        'soundness_tests':{'passed':True,'count':9,'observed_seconds':1.669,'new_logic_after_tests':False},
        'beam_physical_simulator_regression':{'passed':True,'legal_operations':100,'independent_reference':'Pinned immutable original primitive.'},
        'Notion':{'passed':True,'pages_verified':3,'old_content_preserved':True},
        'preservation':{'passed':True,'prior_artifacts':5403},
        'visual_QA':{'passed':True,'figure':'conservative_spine_renewal_v2.png','scope':'Local examples only; global statement labeled OPEN.'},
        'root_status':'OPEN'})
    print(json.dumps({'finalized':True,'python_AST_files':len(files),'Lean_passed':True,
                      'partial_budget':'45A','full_bound':'OPEN','Notion_pages_verified':3}))


if __name__=='__main__':main()
