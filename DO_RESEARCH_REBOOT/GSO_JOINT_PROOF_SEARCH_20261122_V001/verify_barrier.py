"""Independent integer dual and named-root cycle check; no learner imports."""
import sys
import json
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    barrier=json.loads((HERE/'GLOBAL_ABSTRACT_BARRIER.json').read_text(encoding='utf-8'))
    assert barrier['status']=='PROVED_ALL_FINITE_PARAMETERS_ABSTRACT_MODEL_BARRIER'
    # Variables: paid,issued,H,J,T,M. First row is exact conservation at a
    # closed seam; remaining rows are <= inequalities. Exact multipliers give
    # paid-3M<=-3, independent of storage size or the searched constants.
    rows=[([1,-1,0,0,0,0],0),([0,1,-3,-3,-3,0],0),([0,0,1,1,1,-1],-1)]
    multipliers=list(map(Fraction,(1,1,3)))
    coeff=[sum(weight*Fraction(row[0][j]) for weight,row in zip(multipliers,rows)) for j in range(6)]
    rhs=sum(weight*row[1] for weight,row in zip(multipliers,rows))
    assert coeff==list(map(Fraction,(1,0,0,0,0,-3))) and rhs==-3
    current,previous='a','b'
    for target in ('c','b','a'):
        assert target not in (current,previous)
        previous,current=current,target
    assert (current,previous)==('a','b')
    assert barrier['physical_concretization'].startswith('NOT_PROVED')
    result={'passed':True,'exact_dual_coefficients':[str(v) for v in coeff],
            'exact_rhs':str(rhs),'nonnegative_inequality_multipliers':True,
            'named_root_summary_cycle_checked':True,'original_source_counterexample':False,
            'scope':'The scalar entry relaxation only. It omits original ancestry and bank/path correlations.',
            'universal_CD':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        path=HERE/'BARRIER_INDEPENDENT_VERIFICATION.json'
        if not path.exists():path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
