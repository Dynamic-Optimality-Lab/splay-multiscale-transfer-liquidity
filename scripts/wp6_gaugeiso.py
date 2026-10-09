"""Gauge-rigidity stage 1: single-atom isolation search + type-graph SCCs.
For all n=5 KEEP rows x all y: count atoms (y,z) with changed (tau,lam).
Report single-change rows; per-edge isolation coverage; type-graph SCCs."""
import sys, copy, json
from pathlib import Path
from collections import defaultdict, Counter
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
    Sh=O.shapes_of(list(range(1,n+1))); nS=len(Sh)
    idx={json.dumps(s,sort_keys=True):i for i,s in enumerate(Sh)}
    # type graph edges + single-change rows
    tedge=defaultdict(set)  # tau_pre -> set(tau_post)
    single=defaultdict(list)  # (u,v) -> [row ids isolating it]
    rowchange=Counter()
    iso_rows=0
    iso_by_edge=Counter()
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
                        tedge[u].add(v)
                        if u!=v: ch.append((u,v))
                    rowchange[len(ch)]+=1
                    if len(ch)==1:
                        iso_rows+=1
                        (u,v)=ch[0]
                        iso_by_edge[(u,v)]+=1
                        if len(single[(u,v)])<2:
                            single[(u,v)].append((ia,ib,x,y))
        if (ia+1)%14==0: print(f"[ISO] ia={ia+1} iso_rows={iso_rows}",flush=True)
    print(f"[ISO] row-change-count hist: {dict(sorted(rowchange.items()))}")
    print(f"[ISO] single-change rows: {iso_rows}")
    print(f"[ISO] isolated edge types: {len(iso_by_edge)}")
    # SCCs of type graph (nodes with self-loops included)
    nodes=set(tedge)|{v for vs in tedge.values() for v in vs}
    print(f"[ISO] type nodes={len(nodes)}")
    # Tarjan iterative
    index_of={}; low={}; onstack=set(); stack=[]; sccs=[]; cnt=[0]
    for root in nodes:
        if root in index_of: continue
        work=[(root,0)]
        while work:
            v,pi=work[-1]
            if pi==0:
                index_of[v]=low[v]=cnt[0]; cnt[0]+=1
                stack.append(v); onstack.add(v)
            rec=False
            nbrs=sorted(tedge.get(v,[]),key=str)
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
    print(f"[ISO] SCCs={len(sccs)} sizes={sorted([len(c) for c in sccs],reverse=True)[:15]}")
    big=[c for c in sccs if len(c)>1]
    print(f"[ISO] nontrivial SCCs={len(big)}")
    for c in big[:5]:
        print("   SCC:", c)
    json.dump({"rowchange":dict(rowchange),"iso_rows":iso_rows,
               "iso_edges":len(iso_by_edge),
               "sccs":len(sccs),
               "scc_sizes":sorted([len(c) for c in sccs],reverse=True),
               "big": [list(map(str,c)) for c in big[:8]]},
              open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/gauge_iso.json","w"),indent=1,default=str)
    print("[ISO] saved gauge_iso.json")

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
