"""Positive circulation LP: find y>=1 with y^T A = 0 (weighted balance).
If feasible: structural certificate forcing all gauge drops to zero.
Inspect y's pattern for liftable structure."""
import sys, copy, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))

def main():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    import wp6_cycle_ratio as O
    import wp6_overflow as V
    from wp6_staticR import depths_list, path_nodes
    from wp6_lambda import R_coeffs
    n=5
    Sh=O.shapes_of(list(range(1,n+1))); nS=len(Sh)
    idx={json.dumps(s,sort_keys=True):i for i,s in enumerate(Sh)}
    # reuse enumeration: build Amat (rows x vars) as in gaugecone2 coarse
    import importlib.util
    spec=importlib.util.spec_from_file_location("gc2","scripts/wp6_gaugecone2.py")
    # instead rebuild inline (avoid MODE global issues): replicate coarse enumeration
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
    tvars={}; rvars={}
    def tv(t):
        if t not in tvars: tvars[t]=len(tvars)
        return tvars[t]
    def rv(r):
        if r not in rvars: rvars[r]=len(rvars)
        return rvars[r]
    rows=[]  # (pairs, (r0,r1), kind)
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
                        tv(u); tv(v)
                        if u!=v: pairs.append((u,v))
                    c0,_=lamrows(ib)[y]; c1,_=lamrows(jb)[y]
                    t0=1 if A[0]==B[0] else 0
                    t1=1 if Ap[0]==Bp[0] else 0
                    r0=(c0,t0); r1=(c1,t1)
                    rv(r0); rv(r1)
                    rows.append((pairs,(r0,r1),'K'))
                rD=V.replay(A,B,[("D",x)])
                Ad=rD["endA"]
                daD=depths_list(Ad); paD=parent_map(Ad)
                t0D=1 if A[0]==B[0] else 0
                for y in range(1,n+1):
                    ok=True
                    if da0[y]!=daD[y] or pa0.get(y)!=paD.get(y): ok=False
                    if rel3(A,x,y)!=rel3(Ad,x,y): ok=False
                    if lca(A,x,y)!=lca(Ad,x,y): ok=False
                    if ok:
                        CA=-2*(((daD[y]+1)//2)-((da0[y]+1)//2))
                        if CA!=0: ok=False
                    if not ok: continue
                    tD=1 if Ad[0]==B[0] else 0
                    cB,_=lamrows(ib)[y]
                    r0=(cB,t0D); r1=(cB,tD)
                    rv(r0); rv(r1)
                    rows.append(([],(r0,r1),'D'))
        if (ia+1)%14==0: print(f"[CIRC] ia={ia+1} rows={len(rows)}",flush=True)
    Vv=len(tvars)+len(rvars)
    E=len(rows)
    print(f"[CIRC] rows={E} vars={Vv}",flush=True)
    rd=[]; cd=[]; vd=[]
    for i,(pairs,(r0,r1)) in enumerate([(p,r) for (p,r,k) in rows]):
        for (u,v) in pairs:
            rd.append(i); cd.append(tvars[u]); vd.append(1.0)
            rd.append(i); cd.append(tvars[v]); vd.append(-1.0)
        rd.append(i); cd.append(len(tvars)+rvars[r0]); vd.append(1.0)
        rd.append(i); cd.append(len(tvars)+rvars[r1]); vd.append(-1.0)
    Amat=sp.csr_matrix((np.array(vd),(np.array(rd),np.array(cd))),shape=(E,Vv))
    # find y>=1 with A^T y = 0: LP min 0 s.t. A^T y=0, y>=1
    from scipy.optimize import linprog
    c=np.zeros(E)
    Aeq=Amat.T.tocsr()
    # Aeq y = 0 (Vv equations), y>=1
    res=linprog(c, A_eq=Aeq, b_eq=np.zeros(Vv), bounds=[(1,None)]*E, method="highs")
    print(f"[CIRC] pos-circulation status={res.status}",flush=True)
    json.dump({"rows":E,"vars":Vv,"circ_status":res.status},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/circ.json","w"),indent=1)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
