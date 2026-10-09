"""ATOMIC v2: refined tau with fringe index, orientation, block size, y-depth."""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, sz, R_static
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

def slot_full(T,y,z):
    P=path_nodes(T,y); d=len(P)-1
    if z==y: return ('SELF',)
    xn=P[d]
    Lset=set(subkeys_list(T,xn[1][0])) if xn[1] else set()
    Rset=set(subkeys_list(T,xn[2][0])) if xn[2] else set()
    if z in Lset: return ('L',len(Lset))
    if z in Rset: return ('R',len(Rset))
    for j in range(d):
        par=P[d-1-j]; ch=P[d-j]
        off=par[2] if par[1] is ch else par[1]
        mset=set()
        if off is not None: mset=set(subkeys_list(T,off[0]))
        if z in mset:
            # orientation at that level: side of ch in par + turn
            side=0 if par[1] is ch else 1
            return ('F',j,len(mset),side)
    return ('NONE',)

def parent_map_list(t):
    par={t[0]:None}; stack=[t]
    while stack:
        nd=stack.pop()
        for ch in (nd[1],nd[2]):
            if ch is not None:
                par[ch[0]]=nd[0]; stack.append(ch)
    return par

def anc_set_list(t,y):
    s=set(); nd=t
    while nd is not None and nd[0]!=y:
        s.add(nd[0]); nd=nd[1] if y<nd[0] else nd[2]
    if nd is not None: s.add(nd[0])
    return s

def lca_list(t,a,b):
    ca=anc_set_list(t,a); cb=anc_set_list(t,b)
    inter=ca&cb
    if not inter: return None
    d=depths_list(t)
    return max(inter,key=lambda k:d[k])

def rel3(t,a,b):
    ca=anc_set_list(t,a); cb=anc_set_list(t,b)
    return (a in cb, b in ca, lca_list(t,a,b))

def path_rel(B,x,y):
    if x==y: return 'G1'
    def pset(t,v):
        s=[]; nd=t
        while nd is not None and nd[0]!=v:
            s.append(nd[0]); nd=nd[1] if v<nd[0] else nd[2]
        if nd is not None: s.append(nd[0])
        return set(s)
    if y in pset(B,x): return 'G2'
    if x in pset(B,y): return 'G3'
    return 'G4'

def main():
    import wp6_cycle_ratio as O
    n=5
    Sh=O.shapes_of(list(range(1,n+1)))
    evs=json.loads((ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/carrier{n}.json").read_text(encoding="utf-8"))
    acc_cache={}
    def getrep(ia,ib,x):
        k=(ia,ib,x)
        if k not in acc_cache:
            acc_cache[k]=V.replay(Sh[ia],Sh[ib],[("K",x)])
        return acc_cache[k]
    static=[]
    for e in evs:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        A,B=Sh[ia],Sh[ib]
        rep=getrep(ia,ib,x); Ap,Bp=rep["endA"],rep["endB"]
        d0=dict(e["brow0"][1]); d1=dict(e["brow1"][1])
        part=[z for z in set(d0)|set(d1) if d1.get(z,0)-d0.get(z,0)!=0]
        da0=depths_list(A); da1=depths_list(Ap)
        pa0=parent_map_list(A); pa1=parent_map_list(Ap)
        ok=True
        if da0[y]!=da1[y] or pa0.get(y)!=pa1.get(y): ok=False
        if rel3(A,x,y)!=rel3(Ap,x,y): ok=False
        if lca_list(A,x,y)!=lca_list(Ap,x,y): ok=False
        if ok:
            for z in part:
                if da0[z]!=da1[z] or pa0.get(z)!=pa1.get(z): ok=False; break
                if rel3(A,x,z)!=rel3(Ap,x,z): ok=False; break
                if rel3(A,y,z)!=rel3(Ap,y,z): ok=False; break
                if lca_list(A,x,z)!=lca_list(Ap,x,z): ok=False; break
                if lca_list(A,y,z)!=lca_list(Ap,y,z): ok=False; break
        if ok:
            CA=-2*(((da1[y]+1)//2)-((da0[y]+1)//2))
            if CA!=0: ok=False
        if ok: static.append(e)
    print(f"[AT2] static {len(static)}")
    trans=defaultdict(list)
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        B=Sh[ib]
        rep=getrep(ia,ib,x); Bp=rep["endB"]
        G=path_rel(B,x,y)
        # x orientation word (B path turns to x) as transport context
        PB=path_nodes(B,x)
        turns=tuple(0 if PB[i][1] is PB[i+1] else 1 for i in range(len(PB)-1))
        for z in range(1,n+1):
            if z==y: continue
            s0=slot_full(B,y,z); s1=slot_full(Bp,y,z)
            _,lam0=R_coeffs(B,y); _,lam1=R_coeffs(Bp,y)
            l0=lam0.get(z,0); l1=lam1.get(z,0)
            tau=(s0,l0)
            trans[(tau,G,turns)].append(((s1,l1),l1-l0))
    amb=sum(1 for v in trans.values() if len(set(v))>1)
    print(f"[AT2] refined classes={len(trans)} amb={amb}")
    # also test tau+G only with refined slots (no turns)
    trans2=defaultdict(list)
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        B=Sh[ib]
        rep=getrep(ia,ib,x); Bp=rep["endB"]
        G=path_rel(B,x,y)
        for z in range(1,n+1):
            if z==y: continue
            s0=slot_full(B,y,z); s1=slot_full(Bp,y,z)
            _,lam0=R_coeffs(B,y); _,lam1=R_coeffs(Bp,y)
            l0=lam0.get(z,0); l1=lam1.get(z,0)
            trans2[((s0,l0),G)].append(((s1,l1),l1-l0))
    amb2=sum(1 for v in trans2.values() if len(set(v))>1)
    print(f"[AT2] refined-tau+G classes={len(trans2)} amb={amb2}")
    json.dump({"classes":len(trans),"amb":amb,"classes2":len(trans2),"amb2":amb2},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/atomic2.json","w"),indent=1,default=str)

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
