"""Verdict-support queries: smallest isolation obstruction, forced DAG,
twin-destruction rows, A-fiber structure."""
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

def main():
    import wp6_cycle_ratio as O
    n=5
    Sh=O.shapes_of(list(range(1,n+1))); nS=len(Sh)
    # isolation coverage per edge (single-change + root-fixed)
    cover=defaultdict(int)
    for ia in range(nS):
        for ib in range(nS):
            A,B=Sh[ia],Sh[ib]
            for x in range(1,n+1):
                rep=V.replay(A,B,[("K",x)])
                Ap,Bp=rep["endA"],rep["endB"]
                for y in range(1,n+1):
                    ch=[]
                    for z in range(1,n+1):
                        if z==y: continue
                        s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
                        _,l0=R_coeffs(B,y); _,l1=R_coeffs(Bp,y)
                        u=(s0,l0.get(z,0)); v=(s1,l1.get(z,0))
                        if u!=v: ch.append((u,v))
                    if len(ch)!=1: continue
                    (u,v)=ch[0]
                    c0,_=R_coeffs(B,y); c1,_=R_coeffs(Bp,y)
                    t0=1 if A[0]==B[0] else 0
                    t1=1 if Ap[0]==Bp[0] else 0
                    if (c0,t0)==(c1,t1):
                        cover[(u,v)]+=1
        if (ia+1)%14==0: print(f"[VQ] ia={ia+1}",flush=True)
    print(f"[VQ] isolated+rootfixed edge types: {len(cover)}",flush=True)
    # smallest UNCOVERED edge: need full edge list; approximate by hub/fringe relevance:
    # list covered sorted
    for k in sorted(cover,key=str)[:20]:
        print(f"   covered {k} n={cover[k]}",flush=True)
    # twin-destruction A-static DELETE rows?
    ndes=0; exdes=None
    for ia in range(nS):
        for ib in range(nS):
            A,B=Sh[ia],Sh[ib]
            da0=depths_list(A); pa0=parent_map(A)
            t0=1 if A[0]==B[0] else 0
            if t0!=1: continue
            for x in range(1,n+1):
                rD=V.replay(A,B,[("D",x)])
                Ad=rD["endA"]
                tD=1 if Ad[0]==B[0] else 0
                if tD!=0: continue
                daD=depths_list(Ad); paD=parent_map(Ad)
                for y in range(1,n+1):
                    ok=True
                    if da0[y]!=daD[y] or pa0.get(y)!=paD.get(y): ok=False
                    if rel3(A,x,y)!=rel3(Ad,x,y): ok=False
                    if lca(A,x,y)!=lca(Ad,x,y): ok=False
                    if ok:
                        CA=-2*(((daD[y]+1)//2)-((da0[y]+1)//2))
                        if CA!=0: ok=False
                    if ok:
                        ndes+=1
                        if exdes is None: exdes=(ia,ib,x,y)
        if (ia+1)%21==0: print(f"[VQ] twinD ia={ia+1} ndes={ndes}",flush=True)
    print(f"[VQ] twin-destruction A-static DELETE rows: {ndes} ex={exdes}",flush=True)
    # A-fiber structure: fiber = (A-root? twin? A-depths of y+support?) -> use (rtA==rtB, A-shape-class?) coarse: count rows per (ia-twin?) 
    json.dump({"covered":len(cover),"twindes":ndes},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/verdict_q.json","w"),indent=1)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
