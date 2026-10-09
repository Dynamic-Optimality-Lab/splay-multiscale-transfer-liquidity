"""Deep-row balance test: do deep-fringe atom transitions cancel within rows?
Per row: deep atoms (fringe idx>=3 pre or post) -> check Eulerian balance
(indeg==outdeg per type) and static fraction. n=6 census + n=7 sample."""
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
def fridx(s):
    return s[1] if (isinstance(s,tuple) and s[0]=='F') else -1

def analyze(n, Sh, sample=None):
    nS=len(Sh)
    idx={json.dumps(s,sort_keys=True):i for i,s in enumerate(Sh)}
    import random
    rng=random.Random(11)
    pairs=[(ia,ib,x) for ia in range(nS) for ib in range(nS) for x in range(1,n+1)]
    if sample:
        rng.shuffle(pairs); pairs=pairs[:sample]
    stat=Counter(); bal=Counter(); deep_rows=0
    for (ia,ib,x) in pairs:
        A,B=Sh[ia],Sh[ib]
        rep=V.replay(A,B,[("K",x)])
        Ap,Bp=rep["endA"],rep["endB"]
        for y in range(1,n+1):
            _,l0=R_coeffs(B,y); _,l1=R_coeffs(Bp,y)
            deep_trs=[]
            static_deep=0; deep_n=0
            for z in range(1,n+1):
                if z==y: continue
                s0=slot_of(B,y,z); s1=slot_of(Bp,y,z)
                if fridx(s0)>=3 or fridx(s1)>=3:
                    deep_n+=1
                    u=(s0,l0.get(z,0)); v=(s1,l1.get(z,0))
                    if u==v: static_deep+=1
                    else: deep_trs.append((u,v))
            if deep_n>0:
                deep_rows+=1
                stat['rows_with_deep']+=1
                if not deep_trs:
                    stat['all_static']+=1
                else:
                    # Eulerian check on deep transitions
                    io=Counter()
                    for (u,v) in deep_trs:
                        io[u]-=1; io[v]+=1
                    if all(v==0 for v in io.values()):
                        stat['balanced']+=1
                    else:
                        stat['unbalanced']+=1
    print(f"[BAL] n={n} rows_with_deep={stat['rows_with_deep']} all_static={stat['all_static']} balanced={stat['balanced']} unbalanced={stat['unbalanced']}",flush=True)
    return dict(stat)

def main():
    import sys as _s
    import wp6_cycle_ratio as O
    out={}
    for n in (6,):
        Sh=O.shapes_of(list(range(1,n+1)))
        out[n]=analyze(n,Sh)
    Sh7=O.shapes_of(list(range(1,8)))
    out[7]=analyze(7,Sh7,sample=6000)
    json.dump(out,open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/deep_balance.json","w"),indent=1,default=str)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
