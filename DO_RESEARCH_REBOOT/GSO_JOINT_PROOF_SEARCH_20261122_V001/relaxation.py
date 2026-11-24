"""Parametric abstract obstruction and original-domain guardrails.

This excludes proof on the stated scalar relaxation. It is NEVER labeled an
original paired-source counterexample, a false bank theorem or a CD refutation.
"""
import sys
import json
from pathlib import Path
import z3
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    H,T,M,j=z3.Ints('H T M j')
    positive=lambda v:z3.If(v>0,v,0)
    stock=lambda n:positive(H-n)
    ticket=lambda n:positive(T-positive(n-H))
    unpaid=lambda n:positive(n-H-T)
    p=z3.If(stock(j)>=1,1,0)
    u=1-p;v=z3.If(ticket(j)>=u,u,ticket(j))
    queries={
        'target_update':stock(j+1)==stock(j)-p,
        'ticket_update':ticket(j+1)==ticket(j)-v,
        'unfunded_update':unpaid(j+1)==unpaid(j)+1-p-v,
        'path_rank':2*(M-(j+1))==2*(M-j)-2,
        'nonnegative_balances':z3.And(stock(j)>=0,ticket(j)>=0),
    }
    checked=[]
    for name,claim in queries.items():
        solver=z3.Solver();solver.add(H>=0,T>=0,M>H+T,j>=0,j<M,z3.Not(claim));assert solver.check()==z3.unsat
        checked.append(name)
    solver=z3.Solver();solver.add(H>=0,T>=0,M>H+T,unpaid(M)<=0);assert solver.check()==z3.unsat
    checked.append('arbitrary_finite_accounts_exhausted')
    out={'status':'PROVED_ABSTRACT_MODEL_OBSTRUCTION',
         'domain':'The unrestricted scalar access-entry relaxation, which permits arbitrary B depth and no non-target local credit.',
         'parameters':'Every finite nonnegative H,T; choose M>H+T and physical size bound N>=2M+1.',
         'trace':'Start target reserve H, overflow tickets T, path depth2M; perform M legal abstract double cases with other local credit zero.',
         'closed_forms':{'target':'max(H-j,0)','ticket':'max(T-max(j-H,0),0)',
                         'unfunded':'max(j-H-T,0)','remaining_path':'2(M-j)'},
         'symbolic_queries':checked,
         'invariant_consequence':'No inductive invariant containing this relaxed entry and closed under its successors can prove complete q accounting from these accounts. Excluding a successor would be unsound.',
         'physical_concretization':'NOT_ESTABLISHED. Original depth, A/B ancestry and bank stocks have correlations omitted by this scalar entry model.',
         'not_claimed':['No original paired-closed source with these bank stocks is asserted.',
                        'The selected H=5 old policy is not refuted.',
                        'Universal CD is not refuted.',
                        'Other structural energies or stronger original-state invariants are not excluded.'],
         'actual_missing_expressiveness':'A relation between unconsumed original B frames, physical bank ownership and prior original A work, valid for a next target different from both stored B roots.',
         'universal_CD':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'ABSTRACT_OBSTRUCTION.json';assert not p.exists();p.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print({'abstract_queries':len(checked),'original_counterexample':False,'universal_CD':'OPEN'})


if __name__=='__main__':main()
