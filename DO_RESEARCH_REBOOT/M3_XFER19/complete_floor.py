"""All current saved floors, retaining original PORT/EMPTY distinction."""
import z3
from target_floor import dp,opp,opposite_alpha,region_caps,AND,OR
from legacy_floors import legacy_floor
def hidden_min(t,a):
    d=dp(t)
    if t[0] not in (7,8) or t[1] is None or t[1][0]!=0 or max(d.values())<7:return z3.BoolVal(False)
    return AND(a[1]<=9,OR(a[3]==9,AND(a[1]==9,a[4]==9)),*(a[i]!=0 for i in range(1,7)))
def lower_floor(t,a,m,psi,margin,k):
    r=t[0]
    if psi>=k:return z3.BoolVal(True)
    # Ignore root duplicates and every unused/non-Score field exactly.
    c=AND(*(z3.Implies(AND(m[x],OR(*(a[i]==x for i in range(1,7)))),z3.BoolVal(margin[x]>=k))
      for x in range(9) if x!=r))
    tm=opp(t);am=opposite_alpha(a);mm=list(reversed(m))
    old=OR(c,legacy_floor(t,a,m,k),legacy_floor(tm,am,mm,k))
    if k==2:old=AND(old,z3.Not(OR(hidden_min(t,a),hidden_min(tm,am))))
    one,two=region_caps(t,a,m);o,v=region_caps(tm,am,mm);one+=o;two+=v
    return OR(old,*(one if k==1 else []),*two)
