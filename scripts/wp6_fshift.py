"""Parametric fringe-shift isolation search (vines/combs, n=9..12).
For each row, record atom transitions; flag single-change rows whose edge
shifts fringe index; group by (shift, lambda-change) pattern for lifting."""
import sys, copy, json
from pathlib import Path
from collections import defaultdict, Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs

def subkeys_list(t,x):
    nd=t
    while nd is not None and nd[0]!=x:
        nd=nd[1] if x<nd[0] else nd[2]
    out=[]
    def go(m):
        if m is None: return
        out.append(m[0]); go(m[1]); go(m[2])
    go(nd)
    return frozenset(out)
def slot_of(T,y,z):
    P=path_nodes(T,y); d=len(P)-1
    if z==y: return ('SELF',)
    xn=P[d]
    Lset=set(subkeys_list(T,xn[1][0])) if xn[1] else set()
    Rset=set(subkeys_list(T,xn[2][0])) if xn[2] else set()
    if z in Lset: return ('L',)
    if z in Rset: return ('R',)
    for j in range(d):
        par=P[d-1-j]; ch=P[d-j]
        off=par[2] if par[1] is ch else par[1]
        mset=set()
        if off is not None: mset=set(subkeys_list(T,off[0]))
        if z in mset: return ('F',j)
    return ('NONE',)

def vr(keys):
    t=None
    for k in reversed(list(keys)): t=[k,None,t]
    return t
def vl(keys):
    t=None
    for k in list(keys): t=[k,t,None]
    return t
def inorder(t):
    return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])

def main():
    fams=[]
    for n in (9,10,11,12):
        fams.append((f"rvine{n}",vr(range(1,n+1)),n))
        fams.append((f"lvine{n}",vl(range(1,n+1)),n))
    # combs: alternating backbone
    for n in (9,11):
        t=[5,[3,[1,None,None],[4,None,None]],[7,[6,None,None],[9,[8,None,None],[11 if n==11 else 10,None,None]]]] if n==11 else [4,[2,[1,None,None],[3,None,None]],[6,[5,None,None],[8,[7,None,None],[9,None,None]]]]
        if inorder(t)==list(range(1,n+1)):
            fams.append((f"comb{n}",t,n))
    import random
    rng=random.Random(7)
    tests=[]
    for (tag,B,n) in fams:
        # A: x-rooted vines (A-noop => A-static free) + few others
        for xt in [1,n//2,n]:
            A=[xt,vl(range(1,xt)),vr(range(xt+1,n+1))]
            tests.append((tag,xt,A,B,n))
    shift_iso=defaultdict(int)
    shift_rows=[]
    for (tag,xt,A,B,n) in tests:
        for x in [1,2,n//2,n-1,n]:
            if not (1<=x<=n): continue
            rep=V.replay(A,B,[("K",x)])
            Ap,Bp=rep["endA"],rep["endB"]
            for y in [1,2,n//2,n-1,n]:
                if not (1<=y<=n) or y==x: continue
                ch=[]
                for z in range(1,n+1):
                    if z==y: continue
                    s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
                    _,l0=R_coeffs(B,y); _,l1=R_coeffs(Bp,y)
                    u=(s0,l0.get(z,0)); v=(s1,l1.get(z,0))
                    if u!=v: ch.append((u,v))
                if len(ch)==1:
                    (u,v)=ch[0]
                    s0,s1=u[0],v[0]
                    if isinstance(s0,tuple) and s0[0]=='F' and isinstance(s1,tuple) and s1[0]=='F' and s0[1]!=s1[1]:
                        shift_iso[(s0,s1,u[1],v[1])]+=1
                        if len(shift_rows)<6:
                            shift_rows.append((tag,xt,n,x,y,u,v))
    print(f"[FSH] fringe-shift isolations: {len(shift_iso)}",flush=True)
    for k in sorted(shift_iso,key=str)[:25]:
        print(f"   {k} n={shift_iso[k]}",flush=True)
    json.dump({"n":len(shift_iso)},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/fringe_shift.json","w"),indent=1)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
