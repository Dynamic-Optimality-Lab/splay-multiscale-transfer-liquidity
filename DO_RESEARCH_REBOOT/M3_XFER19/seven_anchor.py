"""Provisional simultaneous constructor family; no private observables."""
import z3,sys
from pathlib import Path
from target_floor import N,dp,opp,opposite_alpha
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'M3_XFER18'))
from audit_spread import replay,path
E=None
US=(N(4,E,N(5,E,N(6))),N(4,E,N(6,N(5),E)),N(5,N(4),N(6)),
    N(6,N(4,E,N(5)),E),N(6,N(5,N(4),E),E))
REGIONS={}
def add(t,kind,x=None):REGIONS.setdefault(t,set()).add((kind,x))
for U in US:
    S=N(0,E,N(3,N(1,E,N(2)),N(7,U,N(8))));add(S,'S')
    for x in (4,5,6):
        if dp(S)[x] not in (4,5):continue
        T=replay(S,path(S,x));add(T,'T')
        if dp(T)[2] in (4,5):add(replay(T,path(T,2)),'K',x)
def orient(t,a):
    q=[]
    for kind,x in REGIONS.get(t,()):
        if kind=='S':q.append(z3.Or(a[2]==7,a[6]==7))
        if kind=='T':q.append(z3.And(a[1]==0,z3.Or(a[2]==7,a[6]==7)))
        if kind=='K':q.append(z3.And(a[1]==0,a[2]==x,a[6]!=8))
    return z3.Or(*q)
def seven_one(t,a):return z3.Or(orient(t,a),orient(opp(t),opposite_alpha(a)))
