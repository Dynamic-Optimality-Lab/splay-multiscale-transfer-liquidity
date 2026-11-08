"""Quantifier-free necessary fresh-source shadow compatibility.

Anonymous gaps are eliminated by interval intersection, never selected
as public data. Formula parameters are only existing alpha/root fields.
"""
import z3
from target_floor import AND,OR
PORT=10;EMPTY=12;F=9
def score(v):return AND(v>=0,v<9)
def ok_grand(v,lo,hi,r):
    return OR(v==PORT,v==F,AND(score(v),lo<=v,v<=hi),
      AND(OR(v==EMPTY,v==r),lo>hi))
def anon_compatible(left,right,lo,hi,r):
    ls=AND(score(left),left!=r);rs=AND(score(right),right!=r)
    le=OR(left==EMPTY,left==r);re=OR(right==EMPTY,right==r)
    low=z3.If(re,hi+1,z3.If(ls,left+1,lo))
    high=z3.If(le,lo,z3.If(rs,right,hi+1))
    # In contradictory simultaneous conditions, retain BOTH bounds,
    # rather than let an If-priority silently drop a score constraint.
    return AND(lo<=hi+1,
      z3.Implies(ls,AND(lo<=left,left<=hi)),
      z3.Implies(rs,AND(lo<=right,right<=hi)),
      z3.Implies(ls,left+1<=high),z3.Implies(re,hi+1<=high),
      z3.Implies(le,low<=lo),z3.Implies(rs,low<=right),low<=high)
def source_compatible(a,r=None):
    r=a[0] if r is None else r
    valid=AND(a[0]==r,r>=0,r<9,*(AND(v>=0,v<=EMPTY,v!=11) for v in a))
    branches=[]
    for side,c,il,ir,lo,hi in [('L',a[1],3,4,z3.IntVal(0),r-1),
                             ('R',a[2],5,6,r+1,z3.IntVal(8))]:
        left,right=a[il],a[ir]
        ghost=AND(c==r,lo>hi,left==(r if side=='L' else a[1]),right==(a[2] if side=='L' else r))
        real_score=OR(*(AND(c==p,lo<=p,p<=hi,
          ok_grand(left,lo,z3.IntVal(p-1),r),ok_grand(right,z3.IntVal(p+1),hi,r)) for p in range(9)))
        branches.append(OR(AND(c==PORT,left==PORT,right==PORT),
          AND(c==EMPTY,lo>hi,left==EMPTY,right==EMPTY),ghost,real_score,
          AND(c==F,anon_compatible(left,right,lo,hi,r))))
    return AND(valid,*branches)
