"""Row-config mutual pairs + structured circulation test.
(1) Row-config graph (config=(atoms,root)): mutual-pair edge fraction.
(2) Structured circulation: uniform within (mode,G-class,twin-change) cells?"""
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
    # row-config graph per y: nodes=configs, edges with (G-class, twin-change, mode)
    for y in [3]:
        edges=[]  # (cfg_pre, cfg_post, cell)
        for ia in range(nS):
            for ib in range(nS):
                A,B=Sh[ia],Sh[ib]
                da0=depths_list(A); pa0=parent_map(A)
                for x in range(1,n+1):
                    r=rep(ia,ib,x)
                    Ap,Bp=r["endA"],r["endB"]
                    ja=idx[json.dumps(Ap,sort_keys=True)]; jb=idx[json.dumps(Bp,sort_keys=True)]
                    da1=depths_list(Ap); pa1=parent_map(Ap)
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
                    cfg0=tuple(sorted((z,slot_of(B,y,z),l0.get(z,0)) for z in range(1,n+1) if z!=y))
                    cfg1=tuple(sorted((z,slot_of(Bp,y,z),l1.get(z,0)) for z in range(1,n+1) if z!=y))
                    t0=1 if A[0]==B[0] else 0
                    t1=1 if Ap[0]==Bp[0] else 0
                    c0,_=lamrows(ib)[y]; c1,_=lamrows(jb)[y]
                    edges.append(((cfg0,(c0,t0)),(cfg1,(c1,t1)),(path_rel(B,x,y),(t0,t1),'K')))
                # DELETE rows
                for x in range(1,n+1):
                    rD=V.replay(A,B,[("D",x)])
                    Ad=rD["endA"]
                    daD=depths_list(Ad); paD=parent_map(Ad)
                    ok=True
                    if da0[y]!=daD[y] or pa0.get(y)!=paD.get(y): ok=False
                    if rel3(A,x,y)!=rel3(Ad,x,y): ok=False
                    if lca(A,x,y)!=lca(Ad,x,y): ok=False
                    if ok:
                        CA=-2*(((daD[y]+1)//2)-((da0[y]+1)//2))
                        if CA!=0: ok=False
                    if not ok: continue
                    tD=1 if Ad[0]==B[0] else 0
                    t0=1 if A[0]==B[0] else 0
                    cB,_=lamrows(ib)[y]
                    cfg=tuple(sorted((z,slot_of(B,y,z),lamrows(ib)[y][1].get(z,0)) for z in range(1,n+1) if z!=y))
                    edges.append(((cfg,(cB,t0)),(cfg,(cB,tD)),('D',(t0,tD),'D')))
            if (ia+1)%14==0: print(f"[MUT] y={y} ia={ia+1} edges={len(edges)}",flush=True)
        eset=set((a,b) for (a,b,c) in edges)
        mut=sum(1 for (a,b) in eset if (b,a) in eset)
        print(f"[MUT] y={y} transitions={len(eset)} mutual={mut} ({100*mut/max(1,len(eset)):.1f}%)",flush=True)
        # structured circulation: balance within cells?
        cells=defaultdict(list)
        for (a,b,c) in edges:
            cells[c].append((a,b))
        print(f"[MUT] cells={len(cells)}",flush=True)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
