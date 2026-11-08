"""Public one-credit floors proved by LOWER_RETURN_FAMILY and audit v2."""
import z3
from target_floor import N,opp,opposite_alpha

def orientation(t,a):
    E=None;L=N(0,E,N(1,E,N(2)));terms=[]
    for H in (N(7,E,N(8)),N(8,N(7),E)):
        K=N(2,N(1,N(0),E),N(3,E,N(4,E,N(5,E,N(6,E,H)))))
        T5=N(5,N(3,L,N(4)),N(6,E,H))
        T4=N(4,N(3,L,E),N(5,E,N(6,E,H)))
        if t==K:terms.append(z3.And(a[2]==4,a[6]==6))
        if t==T5:terms.append(z3.And(a[1]==0,z3.Or(a[2]==6,a[6]==6)))
        if t==T4:terms.append(z3.And(a[1]==0,z3.Or(a[2]==5,a[2]==6,a[6]==5,a[6]==6)))
        for A in (N(4,E,N(5)),N(5,N(4),E)):
            S=N(0,E,N(3,N(1,E,N(2)),N(6,A,H)))
            if t==S:terms.append(z3.Or(a[2]==6,a[6]==6))
    return z3.Or(*terms)

def lower_return_one(t,a):
    return z3.Or(orientation(t,a),orientation(opp(t),opposite_alpha(a)))
