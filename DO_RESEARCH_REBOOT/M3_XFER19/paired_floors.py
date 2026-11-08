"""Union of the independently proved complete paired upper family."""
import z3
from target_floor import N,opp,opposite_alpha
def one_orientation(t,a):
    terms=[]
    for u,A,B in [(4,None,N(5,None,N(6))),(4,None,N(6,N(5),None)),(5,N(4),N(6))]:
        S=N(0,None,N(3,N(1,None,N(2)),N(u,A,N(7,B,N(8)))))
        T=N(8,N(3,N(0,None,N(1,None,N(2))),N(7,N(u,A,B),None)),None)
        if t==S:terms.append(z3.And(a[2]==u,a[6]==8))
        if t==T:terms.append(z3.And(a[1]==u,a[3]==0))
    return z3.Or(*terms)
def paired_one(t,a):return z3.Or(one_orientation(t,a),one_orientation(opp(t),opposite_alpha(a)))
