"""All-finite-constant barrier in the declared scalar entry relaxation.

The globally shared overflow reserve is included. This is an exact abstraction
obstruction, NOT a paired-closed original BST witness or a refutation of CD.
"""
import sys
import json
from pathlib import Path
import z3
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    H,J,T,g,N,M,C,issued,paid,before,after=z3.Ints('H J T g N M C issued paid before after')
    base=[H>=0,J>=0,T>=0,g>=0,C>=0,M>H+J+T,M>C,N==2*M+1]
    claims={
        'path_depth_is_legal_size_bound':z3.And(N>=3,2*M<=N-1),
        'closed_accounts_cannot_cover_demands':z3.Implies(z3.And(after==before,after-before==issued-paid,issued<=3*(H+J+T)),paid<3*M),
        'arbitrary_trial_constant_violated_in_relaxation':3*M>3*C,
        'account_capacity_does_not_change_closed_conservation':z3.Implies(z3.And(after==before,after-before==issued-paid),paid==issued)
    }
    checked=[]
    for name,claim in claims.items():
        solver=z3.Solver();solver.add(*base,z3.Not(claim));assert solver.check()==z3.unsat
        checked.append(name)
    out={'status':'PROVED_ALL_FINITE_PARAMETERS_ABSTRACT_MODEL_BARRIER',
         'accounts':'Both local capacity-H block banks and persistent globally shared G<=gN. A issuance J and genuine-KEEP issuance T are included.',
         'abstract_cycle':'Three successive target-OTHER accesses cycle named roots a,b,c. Each has a=1,k=1,d_B=2M,q=M; the scalar model recreates that depth and permits all non-target local stock zero. This is not a physically closed paired-BST source.',
         'parameters':'For any finite H,J,T,g and trial C, choose M>max(H+J+T,C), N=2M+1.',
         'resource_dual':'On any closed account trajectory paid=issued<=3(H+J+T)<3M=Q. The abstract cost ratio Q/A=M exceeds arbitrary trial C.',
         'capacity_role':'Finite storage gN can postpone failure from the full upper vector but cannot supply net payment on a closed/repeated cycle.',
         'symbolic_queries':checked,
         'physical_concretization':'NOT_PROVED; full B ancestry and its destruction/recreation have been forgotten at the scalar target-OTHER boundary.',
         'invariant_consequence':'A proof over this permissive scalar model cannot close the root claim. A stronger original-state relation must reject or account for free repeated deep ancestry; simply increasing constants or solving more scalar inequalities cannot repair the abstraction.',
         'not_a_claim':'No original source with unbounded Q_B/A is asserted. The selected H=5 physical policy remains unrefuted. Richer structural energies and invariants are not excluded.',
         'universal_CD':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'GLOBAL_ABSTRACT_BARRIER.json';assert not p.exists();p.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print({'abstract_parametric_queries':len(checked),'original_counterexample':False,'universal_CD':'OPEN'})


if __name__=='__main__':main()
