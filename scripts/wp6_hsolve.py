"""ATOMIC h-solve: type-level Bellman longest paths + row coverage test."""
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
    # type graph: node=(slot,lam); edge weight = max Delta observed
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
    print(f"[HS] type nodes={len(nodes)} edges={len(best)}")
    # longest-path feasibility: Bellman-Ford for positive cycles (max-weight reachability)
    # h(v) = max path weight from v (must be finite). Detect positive cycle via N relaxations.
    INF_NEG=-10**18
    h={v:0 for v in nodes}  # h>=0 init; longest simple paths from terminals
    # value iteration for longest paths (positive-cycle detection)
    for it in range(len(nodes)+2):
        ch=0
        for (u,v),w in best.items():
            if h[u] < h[v]+w:
                h[u]=h[v]+w
                ch+=1
        if ch==0:
            print(f"[HS] converged iter={it}")
            break
    else:
        print("[HS] NO CONVERGENCE in N+1 iters (checking positive cycle)")
    # positive-cycle check: one more pass
    cyc=[(u,v) for (u,v),w in best.items() if h[u] < h[v]+w]
    print(f"[HS] residual violations after N+1 passes: {len(cyc)}")
    if cyc:
        print(f"[HS] POSITIVE CYCLE witness: {cyc[0]} h={h[cyc[0][0]]},{h[cyc[0][1]]} w={best[cyc[0]]}")
    # row coverage with this h (even if cyc: h may be inflated; test anyway)
    bad=0; tot=0; worst=None
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        B=Sh[ib]
        rep=getrep(ia,ib,x); Bp=rep["endB"]
        RB0=R_static(B,y); RB1=R_static(Bp,y)
        CB=RB1-RB0
        drop=0
        for z in range(1,n+1):
            if z==y: continue
            s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
            _,lam0=R_coeffs(B,y); _,lam1=R_coeffs(Bp,y)
            drop+=h.get((s0,lam0.get(z,0)),0)-h.get((s1,lam1.get(z,0)),0)
        # root token: Delta_c must be covered by rho drop; include here as open
        dc=e["brow1"][0]-e["brow0"][0]
        tot+=1
        if drop < CB-dc:  # atom drops cover sum-Delta part
            bad+=1
            if worst is None or drop-(CB-dc)<worst[0]:
                worst=(drop-(CB-dc),CB-dc,ia,ib,x,y)
    print(f"[HS] atom-drop covers sumDelta: {tot-bad}/{tot} worst={worst}")
    # h stats
    vals=sorted(set(h.values()))
    print(f"[HS] h distinct={len(vals)} range=[{min(vals)},{max(vals)}]")
    json.dump({"nodes":len(nodes),"edges":len(best),"cyc":len(cyc),"cover":[tot-bad,tot],"hmin":min(h.values()),"hmax":max(h.values())},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/hsolve.json","w"),indent=1,default=str)

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
