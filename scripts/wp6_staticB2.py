"""STATIC stage 2: Delta_c/twin, M_static payment, negative-edge, adversarial, ambiguity witnesses."""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, sz, R_static
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
    Vf=json.loads((ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/vfull{n}.json").read_text(encoding="utf-8"))["V"]
    evs=json.loads((ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/carrier{n}.json").read_text(encoding="utf-8"))
    # rebuild static list with full data (recompute filter quickly using cached Ap)
    from wp6_staticB import parent_map_list, anc_set_list, lca_list, path_relation
    # instead reuse: filter by CA==0 + relation checks via quick replay cache
    acc_cache={}
    def getrep(ia,ib,x):
        k=(ia,ib,x)
        if k not in acc_cache:
            acc_cache[k]=V.replay(Sh[ia],Sh[ib],[("K",x)])
        return acc_cache[k]
    def rel(t,a,b):
        ca=anc_set_list(t,a); cb=anc_set_list(t,b)
        return (a in cb, b in ca, lca_list(t,a,b))
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
        if rel(A,x,y)!=rel(Ap,x,y): ok=False
        if lca_list(A,x,y)!=lca_list(Ap,x,y): ok=False
        if ok:
            for z in part:
                if da0[z]!=da1[z] or pa0.get(z)!=pa1.get(z): ok=False; break
                if rel(A,x,z)!=rel(Ap,x,z): ok=False; break
                if rel(A,y,z)!=rel(Ap,y,z): ok=False; break
                if lca_list(A,x,z)!=lca_list(Ap,x,z): ok=False; break
                if lca_list(A,y,z)!=lca_list(Ap,y,z): ok=False; break
        if ok:
            CA=-2*(((da1[y]+1)//2)-((da0[y]+1)//2))
            if CA!=0: ok=False
        if ok: static.append(e)
    print(f"[ST2] static {len(static)}")
    # Delta_c / twin stats
    dcc=Counter(); twinB=Counter()
    for e in static:
        dc=e["brow1"][0]-e["brow0"][0]
        dcc[dc]+=1
        # twin from trees
        ia,ib,x=e["ia"],e["ib"],e["x"]
        A,B=Sh[ia],Sh[ib]
        rep=getrep(ia,ib,x); Ap,Bp=rep["endA"],rep["endB"]
        t0=1 if A[0]==B[0] else 0
        t1=1 if Ap[0]==Bp[0] else 0
        twinB[(t0,t1,dc)]+=1
    print(f"[ST2] Delta_c dist: {dict(sorted(dcc.items()))}")
    print(f"[ST2] (t0,t1,dc) sample: {dict(list(twinB.items())[:8])}")
    # M_static test: M = sum over y of max(0, R_B(y) - baseline?) -> use simplest: total positive Lambda mass per state? Test D_s(x) <= M(s)-M(s') + base/twin on static transitions
    # Define StaticClaims(s) = {(y,z): lam_B(y,z)>0} weighted sum P = sum lam>0. Then M_static(s)=P(s).
    # Test static residual inequality: C_B <= M(s)-M(s') ? Since C_A=0, C=C_B+Ctwin; M should cover C_B.
    bad=0; tot=0; worst=None
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        A,B=Sh[ia],Sh[ib]
        rep=getrep(ia,ib,x); Ap,Bp=rep["endA"],rep["endB"]
        def Pmass(T):
            s=0
            for yy in range(1,n+1):
                _,lam=R_coeffs(T,yy)
                s+=sum(v for v in lam.values() if v>0)
            return s
        m0=Pmass(B); m1=Pmass(Bp)
        # C_B for this y
        RB0=R_static(B,y); RB1=R_static(Bp,y)
        CB=RB1-RB0
        if (m0-m1) < CB:
            bad+=1
            if worst is None or (m0-m1)-CB < worst[0]:
                worst=((m0-m1)-CB,CB,e["ia"],e["ib"],x,y)
        tot+=1
    print(f"[ST2] M_static(pos-lambda-mass) covers C_B: {tot-bad}/{tot} worst={worst}")
    # negative-edge recharge in static subsystem: D<0 KEEP edges that are A-static for their y? Search all accesses for A-static y with D<0 and V rise? Use V.
    neg=0; negV=0; exneg=None
    for ia in range(nS):
        for ib in range(nS):
            A,B=Sh[ia],Sh[ib]
            da0=depths_list(A); t0=1 if A[0]==B[0] else 0
            for x in range(1,n+1):
                rep=V.replay(A,B,[("K",x)])
                Ap,Bp=rep["endA"],rep["endB"]
                u=ia*nS+ib
                ja=idx[json.dumps(Ap,sort_keys=True)]; jb=idx[json.dumps(Bp,sort_keys=True)]
                v=ja*nS+jb
                da1=depths_list(Ap); t1=1 if Ap[0]==Bp[0] else 0
                for y in range(1,n+1):
                    Dpre=R_static(B,y)-2*((da0[y]+1)//2)-2*(1-t0)
                    Dpost=R_static(Bp,y)-2*((da1[y]+1)//2)-2*(1-t1)
                    # A-static for y? need z-participants; approximate by y-only static (depth/parent/relations)
                    if da0[y]!=da1[y]: continue
                    if Dpre<0 and Vf[v]>Vf[u]:
                        neg+=1
                        if exneg is None: exneg=(ia,ib,x,y,Dpre,Vf[u],Vf[v])
    print(f"[ST2] static-y negative-D with V-rise: {neg} ex={exneg}")
    # smallest transport ambiguity witness: (pre-slot,G) with different Delta
    from collections import defaultdict as dd
    groups=dd(list)
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        A,B=Sh[ia],Sh[ib]
        # G-class
        def prel(BB,xx,yy):
            if xx==yy: return 'G1'
            def pset(t,v):
                s=[]; nd=t
                while nd is not None and nd[0]!=v:
                    s.append(nd[0]); nd=nd[1] if v<nd[0] else nd[2]
                if nd is not None: s.append(nd[0])
                return set(s)
            if yy in pset(BB,xx): return 'G2'
            if xx in pset(BB,yy): return 'G3'
            return 'G4'
        d0=dict(e["brow0"][1]); d1=dict(e["brow1"][1])
        for z in set(d0)|set(d1):
            dl=d1.get(z,0)-d0.get(z,0)
            if dl==0: continue
            groups[(slot_of(B,y,z),prel(B,x,y))].append((dl,ia,ib,x,y,z))
    amb={k:v for k,v in groups.items() if len(set(vv[0] for vv in v))>1}
    print(f"[ST2] slot+G determinism: classes={len(groups)} amb={len(amb)}")
    if amb:
        k0=min(amb,key=lambda k:len(amb[k]))
        print(f"[ST2] smallest amb key={k0} members={amb[k0][:4]}")
    out={"M_cover":[tot-bad,tot],"neg_static":neg,"slotG_amb":len(amb),"slotG_classes":len(groups),"Delta_c":dict(dcc)}
    (ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/staticB2.json").write_text(json.dumps(out,indent=1,default=str),encoding="utf-8")
    print("[ST2] saved staticB2.json")

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
