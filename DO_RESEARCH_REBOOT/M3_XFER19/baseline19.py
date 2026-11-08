"""Proved lower bounds of the current public baseline after seven closure."""
import z3
from complete_floor import lower_floor as legacy
from target_floor import N,opp,opposite_alpha
from compatibility import source_compatible
from paired_floors import paired_one
from lower_return_floors import lower_return_one
from seven_closure_floors import closure_one
T=N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),N(6,None,N(7,None,N(8)))))
def floor(i,t,a,m,psi,margins,k):
    q=z3.Or(legacy(t,a,m,psi,margins,k),z3.Not(source_compatible(a)))
    if k==1:
        if t==T:q=z3.Or(q,z3.And(z3.Not(m[4]),a[2]==4,a[6]==8))
        if opp(t)==T:
            b=opposite_alpha(a);q=z3.Or(q,z3.And(z3.Not(m[4]),b[2]==4,b[6]==8))
        q=z3.Or(q,paired_one(t,a),lower_return_one(t,a),closure_one(i,t,a,m))
    return q
