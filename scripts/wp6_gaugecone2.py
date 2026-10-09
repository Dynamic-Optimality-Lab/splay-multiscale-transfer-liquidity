"""Gauge-cone LP probe, refined types + n parameter.
tau = (kind, idx, lambda, turnkey): F_j carries turn-pair at its level;
NONE carries ancestor distance; L/R carry side (in kind).
Usage: python wp6_gaugecone2.py <n> [coarse|refined]"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs

MODE="refined"

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
def tau_of(T,y,z):
    s=slot_of(T,y,z)
    if MODE=="coarse" or s in (('L',),('R',),('SELF',)):
        return s
    P=path_nodes(T,y); d=len(P)-1
    dd=depths_list(T)
    if s==('NONE',):
        return (s,dd[y]-dd[z])
    # F_j: turn pair at that level (side of path child, turn into it)
    j=s[1]
    par=P[d-1-j]; ch=P[d-j]
    side=0 if par[1] is ch else 1
    turn=None
    if d-1-j-1>=0:
        gp=P[d-1-j-1] if False else None
    # turn = (side of par in grandpar, side): need grandparent
    if d-1-j-1>=0:
        gp=P[d-2-j]
        ps=0 if gp[1] is par else 1
        turn=(ps,side)
    return (s,turn)
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

def main():
    import numpy as np
    from scipy.optimize import linprog
    import wp6_cycle_ratio as O
    global MODE
    import sys as _s
    n=int(_s.argv[1]) if len(_s.argv)>1 else 5
    MODE=_s.argv[2] if len(_s.argv)>2 else "refined"
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
    tvars={}; rvars={}
    def tv(t):
        if t not in tvars: tvars[t]=len(tvars)
        return tvars[t]
    def rv(r):
        if r not in rvars: rvars[r]=len(rvars)
        return rvars[r]
    cons=[]
    nrows=0
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
                    _,l0=lamrows(ib)[y]
                    _,l1=lamrows(jb)[y]
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
                        u=(tau_of(B,y,z),l0.get(z,0)); v=(tau_of(Bp,y,z),l1.get(z,0))
                        tv(u); tv(v)
                        if u!=v: pairs.append((u,v))
                    c0,_=lamrows(ib)[y]; c1,_=lamrows(jb)[y]
                    t0=1 if A[0]==B[0] else 0
                    t1=1 if Ap[0]==Bp[0] else 0
                    r0=(c0,t0); r1=(c1,t1)
                    rv(r0); rv(r1)
                    cons.append((pairs,(r0,r1)))
                    nrows+=1
                # DELETE rows
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
                    cons.append(([],(r0,r1)))
                    nrows+=1
        if (ia+1)%22==0: print(f"[CN2] n={n} {MODE} ia={ia+1} rows={nrows} tv={len(tvars)} rv={len(rvars)}",flush=True)
    print(f"[CN2] rows={nrows} tvars={len(tvars)} rvars={len(rvars)}",flush=True)
    Vv=len(tvars)+len(rvars)
    import scipy.sparse as sp
    rd=[]; cd=[]; vd=[]
    for i,(pairs,(r0,r1)) in enumerate(cons):
        for (u,v) in pairs:
            rd.append(i); cd.append(tvars[u]); vd.append(1.0)
            rd.append(i); cd.append(tvars[v]); vd.append(-1.0)
        rd.append(i); cd.append(len(tvars)+rvars[r0]); vd.append(1.0)
        rd.append(i); cd.append(len(tvars)+rvars[r1]); vd.append(-1.0)
    Amat=sp.csr_matrix((np.array(vd),(np.array(rd),np.array(cd))),shape=(len(cons),Vv))
    cobj=-(np.asarray(Amat.sum(axis=0)).ravel())
    res=linprog(cobj, A_ub=-Amat, b_ub=np.zeros(len(cons)),
                bounds=[(-1,1)]*Vv, method="highs")
    print(f"[CN2] status={res.status} maxsum={-res.fun if res.status==0 else None}",flush=True)
    json.dump({"n":n,"mode":MODE,"rows":nrows,"tvars":len(tvars),"rvars":len(rvars),
               "status":res.status,"maxsum":float(-res.fun) if res.status==0 else None},
              open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/gauge_cone_{n}_{MODE}.json","w"),indent=1,default=str)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
