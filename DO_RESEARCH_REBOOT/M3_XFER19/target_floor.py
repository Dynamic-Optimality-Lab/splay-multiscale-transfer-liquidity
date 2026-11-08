"""Sound lower floors of the existing debt, over symbolic full shadows.

Omitted old caps mean a SAT branch is unresolved, not a refutation.
No reflection of psi, private ranks or witnesses: mirroring below is
only the literal definition of each already-proved opposite guard.
"""
import z3
from symbolic_prefix import P,F
def N(k,l=None,r=None):return (k,l,r)
def opp(t):return None if t is None else N(8-t[0],opp(t[2]),opp(t[1]))
def dp(t,d=0):return {} if t is None else {t[0]:d,**dp(t[1],d+1),**dp(t[2],d+1)}
def opposite_alpha(a):
    return tuple(z3.If(a[i]<9,8-a[i],a[i]) for i in (0,2,1,6,5,4,3))
def AND(*v):return z3.And(*v)
def OR(*v):return z3.Or(*v)
def m_at(m,a):return OR(*(AND(a==k,m[k]) for k in range(9)))
def only_v(a,m,allowed):
    r=a[0]
    return AND(*(z3.Implies(AND(a[i]==k,m[k],r!=k),OR(*(z3.BoolVal(k==j) for j in allowed)))
      for i in range(1,7) for k in range(9)))
def v_exact(a,m,allowed):
    return AND(only_v(a,m,allowed),*(AND(m[k],a[0]!=k,OR(*(a[i]==k for i in range(1,7)))) for k in allowed))
def h_min(t,a):
    d=dp(t);r=t[0]
    if r not in (7,8) or t[1] is None or t[1][0]!=0 or max(d.values())<7:return z3.BoolVal(False)
    return AND(a[1]!=P,OR(a[3]==F,AND(a[1]==F,a[4]==F)),*(a[i]!=0 for i in range(1,7)))
def region_caps(t,a,m):
    one=[];two=[];r=t[0];d=dp(t)
    T=N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),N(7,N(6),N(8))))
    U=N(6,N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),None)),N(7,None,N(8)))
    W=N(6,N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),None)),N(8,N(7),None))
    K=N(6,N(2,N(1,N(0),None),N(5,N(3,None,N(4)),None)),N(7,None,N(8)))
    Q=N(1,N(0),N(2,None,N(5,N(3,None,N(4)),N(7,N(6),N(8)))))
    V=N(8,N(2,N(0,None,N(1)),N(7,N(5,N(3,None,N(4)),N(6)),None)),None)
    if t in (U,W,K):one.append(z3.BoolVal(True))
    if t==Q:one.append(AND(a[1]==0,a[2]==2,a[6]==6))
    if t==V:one.append(AND(a[1]==6,a[3]==2))
    if t==T:two.append(AND(a[1]==0,a[2]==6,a[5]==4,a[6]==8))
    L=N(0,None,N(2,N(1),None))
    CC=N(3,L,N(4,None,N(8,N(7,N(6,N(5),None),None),None)))
    CX=N(5,N(3,L,N(4)),N(8,N(6,None,N(7)),None))
    CY=N(4,N(3,L,None),N(5,None,N(8,N(6,None,N(7)),None)))
    CZ=N(7,N(5,N(4,N(3,L,None),None),N(6)),N(8))
    if t==CC:two.append(AND(a[1]==0,a[2]==4,a[6]==5))
    if t==CX:two.append(AND(a[1]==4,a[3]==3))
    if t==CY:one.append(a[2]==5)
    if t==CZ:one.append(AND(a[1]==5,a[3]==4))
    if r<=4:
        for b in range(5,9):
            if d[b]<=2:two.append(AND(m[b],a[2]==b,v_exact(a,m,{b})))
    return one,two
def lower_floor(t,a,m,psi,margin,k):
    r=t[0]
    if psi>=k:return z3.BoolVal(True)
    c=AND(*(z3.Implies(AND(m[x],OR(*(a[i]==x for i in range(1,7)))),z3.BoolVal(margin[x]>=k)) for x in range(9) if x!=r))
    if k==2:c=AND(c,z3.Not(OR(h_min(t,a),h_min(opp(t),opposite_alpha(a)))))
    one,two=region_caps(t,a,m)
    o,t2=region_caps(opp(t),opposite_alpha(a),list(reversed(m)));one+=o;two+=t2
    return OR(c,*(one if k==1 else []),*two)
