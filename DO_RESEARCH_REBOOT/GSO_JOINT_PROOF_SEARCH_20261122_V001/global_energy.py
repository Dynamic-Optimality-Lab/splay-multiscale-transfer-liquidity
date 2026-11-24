"""Full-domain acceptance constraints and the original-source metric teacher.

The descriptor grammar is declared, not invented automatically. The teacher
rejects its complete arbitrary-value family using a proved all-q source,
without a coefficient search cap. Memory banks are explicitly not excluded.
"""
import sys
import json
from pathlib import Path
import z3
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def verify():
    obstruction=json.loads((HERE/'UNRESTRICTED_METRIC_OBSTRUCTION.json').read_text())
    physical=json.loads((HERE/'INDEPENDENT_METRIC_VERIFICATION.json').read_text())
    assert obstruction['status']=='PROVED_PARAMETRIC_ORIGINAL_SOURCE_METRIC_GRAMMAR_OBSTRUCTION'
    assert physical['passed'] and physical['complete_original_sources']==3
    assert obstruction['unrestricted_original_cost_obligations_deleted']==0
    C=z3.Int('integerUpperBoundForAnyFiniteRealConstant')
    q=14*C+1
    checks=[]
    for name,assumptions in (
        ('chosen_q_is_positive',[C>=0,q<1]),
        ('flat_fragment_rejects_every_integer_C',[C>=0,q+1<=14*C])):
        s=z3.Solver();s.add(*assumptions);assert s.check()==z3.unsat
        checks.append({'name':name,'negation':'UNSAT'})
    residual,credit=z3.Ints('fragmentDemand availableShapeOrBankDecrease')
    s=z3.Solver();s.add(residual==q+1,C>=0,residual-credit<=14*C,credit<residual-14*C)
    assert s.check()==z3.unsat
    checks.append({'name':'bounded_unpaid_cost_may_use_prior_global_credit','negation':'UNSAT',
                   'necessary_condition':'shape decrease plus globally conserved bank decrease >= q+1-14C'})
    return {'status':'UNRESTRICTED_GLOBAL_SEARCH_OPEN_WITH_EXACT_ORIGINAL_SOURCE_FAMILY_REJECTION',
        'target':'Q_B(W)<=C*A(W), one finite absolute C, arbitrary admissible exactly paired-closed original sources.',
        'scope_restriction_added_to_target':False,
        'joint_search_implemented':'Bounded accounting/energy/invariant grammar plus initialization and successor-induction CEGIS; parameterized original-source grammar teacher added.',
        'original_metric_family_rejected':obstruction['grammar'],'checks':checks,
        'rejected_family':'q+Delta f_N(D_rot)<=C*a on every whole original operation',
        'reason_every_real_constant_is_covered':'If a real C worked, the same law would work with an integer upper bound ceil(max(C,0)). Integer C is contradicted symbolically.',
        'permanent_constraint':'An unrestricted candidate must distinguish the two original anchored B shapes, or prove a globally bounded earlier-A-funded bank depletion across the flat fragment. Equal distance alone supplies no payment.',
        'not_excluded':['Arbitrary shape-dependent invariant/energy','Persistent original-A-funded overflow accounts','Aggregate proofs not expressed as a whole-operation state potential'],
        'first_missing_implication':'A source-uniform inductive relation between the full paired-tree ancestry and a globally conserved credit state, proving original-q accounting through every target-OTHER transition, restoration and cyclic seam.',
        'finite_corpus_is_not_proof':True,'new_unrestricted_root_cost_obligations_deleted':0,
        'universal_CD':'OPEN','dynamic_optimality':'OPEN'}


def main():
    result=verify()
    if not (HERE/'FINAL_MANIFEST.json').exists():
        path=HERE/'GLOBAL_ENERGY_SEARCH_RESULT.json'
        if path.exists():assert json.loads(path.read_text())==result
        else:path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','scope_restriction_added_to_target','new_unrestricted_root_cost_obligations_deleted','universal_CD')}))


if __name__=='__main__':main()
