"""ATOMIC follow-up: dump h, non-tautology check, root token, recharge decode."""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, R_static
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

def main():
    import wp6_cycle_ratio as O
    n=5
    Sh=O.shapes_of(list(range(1,n+1)))
    # rebuild h exactly as hsolve
    evs=json.loads((ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/carrier{n}.json").read_text(encoding="utf-8"))
    # static filter (import from wp6_hsolve logic inline: reuse depths/parents)
    from wp6_atomic import parent_map_list, anc_set_list, lca_list, rel3
    print("SKIP: recompute via wp6_hsolve import not available; dumping from re-solve with print")
    # Instead: re-derive h with labels by re-running core and printing mapping
    # (duplicate minimal logic)
    def rel3a(t,a,b):
        ca=anc_set_list(t,a); cb=anc_set_list(t,b)
        return (a in cb, b in ca, lca_list(t,a,b))
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
        if rel3a(A,x,y)!=rel3a(Ap,x,y): ok=False
        if lca_list(A,x,y)!=lca_list(Ap,x,y): ok=False
        if ok:
            for z in part:
                if da0[z]!=da1[z] or pa0.get(z)!=pa1.get(z): ok=False; break
                if rel3a(A,x,z)!=rel3a(Ap,x,z): ok=False; break
                if rel3a(A,y,z)!=rel3a(Ap,y,z): ok=False; break
                if lca_list(A,x,z)!=lca_list(Ap,x,z): ok=False; break
                if lca_list(A,y,z)!=lca_list(Ap,y,z): ok=False; break
        if ok:
            CA=-2*(((da1[y]+1)//2)-((da0[y]+1)//2))
            if CA!=0: ok=False
        if ok: static.append(e)
    best=defaultdict(lambda: None)
    nodes=set()
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        B=Sh[ib]
        rep=getrep(ia,ib,x); Bp=rep["endB"]
        for z in range(1,n+1):
            if z==y: continue
            s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
            _,lam0=R_coeffs(B,y); _,lam1=R_coeffs(Bp,y)
            l0=lam0.get(z,0); l1=lam1.get(z,0)
            u=(s0,l0); v=(s1,l1); w=l1-l0
            nodes.add(u); nodes.add(v)
            if best[(u,v)] is None or w>best[(u,v)]:
                best[(u,v)]=w
    nodes=list(nodes)
    h={v:0 for v in nodes}
    for it in range(len(nodes)+2):
        ch=0
        for (u,v),w in best.items():
            if h[u] < h[v]+w:
                h[u]=h[v]+w; ch+=1
        if ch==0: break
    print("[HD] h mapping (slot,lambda)->h:")
    for k in sorted(h,key=lambda k:(str(k[0]),k[1])):
        print(f"   {k} -> {h[k]}")
    # non-tautology: same lambda, different slots -> different h?
    from collections import defaultdict as dd
    bylam=dd(set)
    for (s,l),hv in h.items():
        bylam[l].add(hv)
    print("[HD] h-values per lambda:", {l:sorted(v) for l,v in sorted(bylam.items())})
    # root token: (c,twin) transitions and Delta_c coverage
    rt=defaultdict(list)
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        A,B=Sh[ia],Sh[ib]
        rep=getrep(ia,ib,x); Ap,Bp=rep["endA"],rep["endB"]
        t0=1 if A[0]==B[0] else 0
        t1=1 if Ap[0]==Bp[0] else 0
        c0=e["brow0"][0]; c1=e["brow1"][0]
        rt[((c0,t0))].append((c1,t1,c1-c0,t1-t0))
    # root token determinism: (c0,t0,G?) — check amb
    print(f"[HD] root pre-states={len(rt)}")
    # Delta_c coverage by trivial rho-drop? report max dc vs twin
    import collections
    dcc=collections.Counter()
    for e in static:
        dcc[e["brow1"][0]-e["brow0"][0]]+=1
    print("[HD] Delta_c dist:",dict(sorted(dcc.items())))
    # recharge decode (0,0,3,2): D=-5 V:0->3, which atoms gained?
    ia,ib,x,y=0,0,3,2
    A,B=Sh[ia],Sh[ib]
    rep=V.replay(A,B,[("K",x)])
    Ap,Bp=rep["endA"],rep["endB"]
    print(f"[HD] recharge witness hang: A-depths y: {depths_list(A)[y]}->{depths_list(Ap)[y]}")
    for z in range(1,n+1):
        if z==y: continue
        s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
        _,lam0=R_coeffs(B,y); _,lam1=R_coeffs(Bp,y)
        print(f"   z={z} {s0}/{lam0.get(z,0)} -> {s1}/{lam1.get(z,0)} h {h.get((s0,lam0.get(z,0)),'?')}->{h.get((s1,lam1.get(z,0)),'?')}")

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
