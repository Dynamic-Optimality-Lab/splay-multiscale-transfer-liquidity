"""Swap-augmented isolation: rows where non-target atoms are fixed-or-swapped.
For each changed atom (u->v) in a row, check remainder is balanced
(every (a->b) paired with (b->a)). Coverage per edge type."""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
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

def main():
    import wp6_cycle_ratio as O
    n=5
    Sh=O.shapes_of(list(range(1,n+1))); nS=len(Sh)
    covered=defaultdict(int)
    total_edges=set()
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
                    for e in ch: total_edges.add(e)
                    # root fixed?
                    c0,_=R_coeffs(B,y); c1,_=R_coeffs(Bp,y)
                    t0=1 if A[0]==B[0] else 0
                    t1=1 if Ap[0]==Bp[0] else 0
                    if (c0,t0)!=(c1,t1): continue
                    # try each changed atom as target
                    for i,(u,v) in enumerate(ch):
                        rest=ch[:i]+ch[i+1:]
                        # balanced? greedy pair check
                        cnt=Counter(rest)
                        ok=True
                        for (a,b) in list(cnt.keys()):
                            if cnt[(a,b)]>0:
                                m=min(cnt[(a,b)],cnt.get((b,a),0))
                                # need full pairing: require cnt[(a,b)]==cnt[(b,a)] for all
                                if cnt[(a,b)]!=cnt.get((b,a),0):
                                    ok=False; break
                        if ok:
                            covered[(u,v)]+=1
        if (ia+1)%14==0: print(f"[SWP] ia={ia+1} covered-edges={len(covered)}",flush=True)
    print(f"[SWP] total edge types={len(total_edges)} swap-isolated={len(covered)}",flush=True)
    print(f"[SWP] uncovered={len(total_edges-set(covered))}",flush=True)
    json.dump({"total":len(total_edges),"covered":len(covered)},open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/gauge_swap.json","w"),indent=1)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
