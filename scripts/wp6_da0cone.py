"""da=0 fiber cone analysis: maxsum, uniqueness (random functionals over
normalized section), n=5 vs n=6 common-type stabilization."""
import sys, copy, json
from pathlib import Path
import numpy as np
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
def parent_map(t):
    par={t[0]:None}; stack=[t]
    while stack:
        nd=stack.pop()
        for ch in (nd[1],nd[2]):
            if ch is not None:
                par[ch[0]]=nd[0]; stack.append(ch)
    return par
def anc_set(t,y):
    s=set(); nd=t
    while nd is not None and nd[0]!=y:
        s.add(nd[0]); nd=nd[1] if y<nd[0] else nd[2]
    if nd is not None: s.add(nd[0])
    return s
def lca(t,a,b):
    c=anc_set(t,a)&anc_set(t,b)
    if not c: return None
    d=depths_list(t)
    return max(c,key=lambda k:d[k])
def rel3(t,a,b):
    ca=anc_set(t,a); cb=anc_set(t,b)
    return (a in cb, b in ca, lca(t,a,b))

def build(n):
    import wp6_cycle_ratio as O
    Sh=O.shapes_of(list(range(1,n+1))); nS=len(Sh)
    idx={json.dumps(s,sort_keys=True):i for i,s in enumerate(Sh)}
    rep_cache={}
    def rep(ia,ib,x):
        k=(ia,ib,x)
        if k not in rep_cache:
            rep_cache[k]=V.replay(Sh[ia],Sh[ib],[("K",x)])
        return rep_cache[k]
    lam_cache={}
    def lamrows(ti):
        if ti not in lam_cache:
            lam_cache[ti]={y:R_coeffs(Sh[ti],y) for y in range(1,n+1)}
        return lam_cache[ti]
    cons=[]
    for ia in range(nS):
        for ib in range(nS):
            A,B=Sh[ia],Sh[ib]
            da0=depths_list(A); pa0=parent_map(A)
            for x in range(1,n+1):
                r=rep(ia,ib,x)
                Ap,Bp=r["endA"],r["endB"]
                da1=depths_list(Ap); pa1=parent_map(Ap)
                jb=idx[json.dumps(Bp,sort_keys=True)]
                for y in range(1,n+1):
                    if da0[y]!=0: continue
                    _,l0=lamrows(ib)[y]; _,l1=lamrows(jb)[y]
                    part=[z for z in set(l0)|set(l1) if l1.get(z,0)-l0.get(z,0)!=0]
                    ok=True
                    if da0[y]!=da1[y] or pa0.get(y)!=pa1.get(y): ok=False
                    if rel3(A,x,y)!=rel3(Ap,x,y): ok=False
                    if lca(A,x,y)!=lca(Ap,x,y): ok=False
                    if ok:
                        for z in part:
                            if da0[z]!=da1[z] or pa0.get(z)!=pa1.get(z): ok=False; break
                            if rel3(A,x,z)!=rel3(Ap,x,z): ok=False; break
                            if rel3(A,y,z)!=rel3(Ap,y,z): ok=False; break
                            if lca(A,x,z)!=lca(Ap,x,z): ok=False; break
                            if lca(A,y,z)!=lca(Ap,y,z): ok=False; break
                    if ok:
                        CA=-2*(((da1[y]+1)//2)-((da0[y]+1)//2))
                        if CA!=0: ok=False
                    if not ok: continue
                    pairs=[]
                    for z in range(1,n+1):
                        if z==y: continue
                        s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
                        u=(s0,l0.get(z,0)); v=(s1,l1.get(z,0))
                        if u!=v: pairs.append((u,v))
                    c0,_=lamrows(ib)[y]; c1,_=lamrows(jb)[y]
                    # twin-blind root
                    cons.append((pairs,(c0,c1)))
        if (ia+1)%22==0: print(f"[DA0] n={n} ia={ia+1} rows={len(cons)}",flush=True)
    return cons

def solve(cons, obj=None):
    from scipy.optimize import linprog
    import scipy.sparse as sp
    tvars={}; rvars={}
    for (pairs,(c0,c1)) in cons:
        for (u,v) in pairs:
            if u not in tvars: tvars[u]=len(tvars)
            if v not in tvars: tvars[v]=len(tvars)
        if c0 not in rvars: rvars[c0]=len(rvars)
        if c1 not in rvars: rvars[c1]=len(rvars)
    Vv=len(tvars)+len(rvars)
    rd=[]; cd=[]; vd=[]
    for i,(pairs,(c0,c1)) in enumerate(cons):
        for (u,v) in pairs:
            rd.append(i); cd.append(tvars[u]); vd.append(1.0)
            rd.append(i); cd.append(tvars[v]); vd.append(-1.0)
        rd.append(i); cd.append(len(tvars)+rvars[c0]); vd.append(1.0)
        rd.append(i); cd.append(len(tvars)+rvars[c1]); vd.append(-1.0)
    Amat=sp.csr_matrix((np.array(vd),(np.array(rd),np.array(cd))),shape=(len(cons),Vv))
    if obj is None:
        cobj=-(np.asarray(Amat.sum(axis=0)).ravel())
    else:
        cobj=np.asarray(obj).ravel()
    res=linprog(cobj, A_ub=-Amat, b_ub=np.zeros(len(cons)),
                bounds=[(-1,1)]*Vv, method="highs")
    return res, tvars, rvars, Amat

def main():
    import sys as _s
    ns=[int(x) for x in _s.argv[1:]] or [5]
    sols={}
    for n in ns:
        cons=build(n)
        res,tvars,rvars,Amat=solve(cons)
        ms=float(-res.fun) if res.status==0 else None
        print(f"[DA0] n={n}: rows={len(cons)} tvars={len(tvars)} maxsum={ms}",flush=True)
        sols[n]=(cons,tvars,rvars,Amat,res)
    # uniqueness: normalize section sum==maxsum? use twin-blind da=0 n=5: fix total drop==ms, random tilts
    n0=ns[0]
    cons,tvars,rvars,Amat,res=sols[n0]
    import scipy.sparse as sp
    from scipy.optimize import linprog
    Vv=len(tvars)+len(rvars)
    tot=np.asarray(Amat.sum(axis=0)).ravel()
    import random
    rng=random.Random(0)
    pts=[]
    for t in range(4):
        d=np.array([rng.uniform(-1,1) for _ in range(Vv)])
        r2=linprog(d, A_ub=sp.vstack([-Amat, -tot.reshape(1,-1)]),
                   b_ub=np.concatenate([np.zeros(Amat.shape[0]), [-float(-res.fun)]]),
                   bounds=[(-1,1)]*Vv, method="highs")
        print(f"[DA0] tilt {t}: status={r2.status} obj={r2.fun if r2.status==0 else None}",flush=True)
        if r2.status==0: pts.append(r2.x)
    if len(pts)>=2:
        import itertools
        mx=max(float(np.max(np.abs(a-b))) for a,b in itertools.combinations(pts,2))
        print(f"[DA0] max pairwise tilt-opt distance: {mx} (0 => unique optimum)",flush=True)
    json.dump({"ns":ns,"done":True},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/da0cone.json","w"),indent=1)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
