"""Per-y A-static row-graph SCCs: edges whose drops are forced zero by reversibility.
Row nodes = pair-states; edge (access x, row y) iff A-static for (x,y,support).
SCC analysis per y + condensation DAG edge fraction."""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs

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
    Vcount=nS*nS
    idx={json.dumps(s,sort_keys=True):i for i,s in enumerate(Sh)}
    # cache replays per (ia,ib,x)
    rep_cache={}
    def rep(ia,ib,x):
        k=(ia,ib,x)
        if k not in rep_cache:
            rep_cache[k]=V.replay(Sh[ia],Sh[ib],[("K",x)])
        return rep_cache[k]
    # Lambda rows cache per tree idx
    lam_cache={}
    def lamrows(ti):
        if ti not in lam_cache:
            lam_cache[ti]={y:R_coeffs(Sh[ti],y) for y in range(1,n+1)}
        return lam_cache[ti]
    for y in range(1,n+1):
        adj=[[] for _ in range(Vcount)]
        ne=0
        for ia in range(nS):
            for ib in range(nS):
                u=ia*nS+ib
                A,B=Sh[ia],Sh[ib]
                da0=depths_list(A); pa0=parent_map(A)
                for x in range(1,n+1):
                    r=rep(ia,ib,x)
                    Ap,Bp=r["endA"],r["endB"]
                    ja=idx[json.dumps(Ap,sort_keys=True)]; jb=idx[json.dumps(Bp,sort_keys=True)]
                    v=ja*nS+jb
                    # support keys for row y
                    d0=dict(lamrows(ib)[y][1]); d1={z:v2 for z,v2 in lamrows(jb)[y][1]} if False else None
                    # recompute post lam directly
                    _,lp=R_coeffs(Bp,y)
                    _,l0=R_coeffs(B,y)
                    part=[z for z in set(l0)|set(lp) if lp.get(z,0)-l0.get(z,0)!=0]
                    da1=depths_list(Ap); pa1=parent_map(Ap)
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
                    if ok:
                        adj[u].append(v); ne+=1
        # SCC (iterative Tarjan)
        index_of={}; low={}; onstack=set(); stack=[]; sccs=[]; cnt=[0]
        for root in range(Vcount):
            if root in index_of: continue
            work=[(root,0)]
            while work:
                v,pi=work[-1]
                if pi==0:
                    index_of[v]=low[v]=cnt[0]; cnt[0]+=1
                    stack.append(v); onstack.add(v)
                rec=False
                nbrs=adj[v]
                for i in range(pi,len(nbrs)):
                    t=nbrs[i]
                    if t not in index_of:
                        work[-1]=(v,i+1); work.append((t,0)); rec=True; break
                    elif t in onstack:
                        low[v]=min(low[v],index_of[t])
                if rec: continue
                work.pop()
                if work: u=work[-1][0]; low[u]=min(low[u],low[v])
                if low[v]==index_of[v]:
                    comp=[]
                    while True:
                        w=stack.pop(); onstack.discard(w); comp.append(w)
                        if w==v: break
                    sccs.append(comp)
        # self-loops + cycle-edge fraction: edges with both ends in same SCC (incl singletons w/ self-loop)
        comp_of={}
        for i,c in enumerate(sccs):
            for v in c: comp_of[v]=i
        cyc=0
        for u in range(Vcount):
            for v in adj[u]:
                if comp_of[u]==comp_of[v]: cyc+=1
        print(f"[RSCC] y={y} edges={ne} SCCs={len(sccs)} cyc-edges={cyc} ({100*cyc/max(1,ne):.1f}%) sizes={sorted([len(c) for c in sccs],reverse=True)[:6]}",flush=True)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
