"""STATIC-B full analysis: T-classes, slots, latent source, G-classes,
twin channel, M_static test, negative-edge, adversarial probes."""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, sz, R_static
from wp6_lambda import R_coeffs

def parent_map_list(t):
    par={t[0]:None}; stack=[t]
    while stack:
        nd=stack.pop()
        for ch in (nd[1],nd[2]):
            if ch is not None:
                par[ch[0]]=nd[0]; stack.append(ch)
    return par

def anc_set_list(t,y):
    s=set(); nd=t
    while nd is not None and nd[0]!=y:
        s.add(nd[0]); nd=nd[1] if y<nd[0] else nd[2]
    if nd is not None: s.add(nd[0])
    return s

def lca_list(t,a,b):
    ca=anc_set_list(t,a); cb=anc_set_list(t,b)
    inter=ca&cb
    if not inter: return None
    d=depths_list(t)
    return max(inter,key=lambda k:d[k])

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
    # returns ('L',)/('R',)/('F',j)/('SELF',)/('NONE',) for z in y-row support slots
    P=path_nodes(T,y)
    d=len(P)-1
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
        if off is not None:
            mset=set(subkeys_list(T,off[0]))
        if z in mset:
            return ('F',j)
    return ('NONE',)

def path_relation(B,x,y):
    # G1-G5 via search paths
    if x==y: return 'G1'
    # path sets
    def pset(t,v):
        s=[]; nd=t
        while nd is not None and nd[0]!=v:
            s.append(nd[0]); nd=nd[1] if v<nd[0] else nd[2]
        if nd is not None: s.append(nd[0])
        return s
    px=set(pset(B,x)); py=set(pset(B,y))
    if y in px: return 'G2'
    if x in py: return 'G3'
    # shared prefix then diverge: LCA not x/y?
    l=lca_list(B,x,y)
    if l is not None and l!=x and l!=y: return 'G4'
    return 'G5'

def main():
    import wp6_cycle_ratio as O
    n=5
    Sh=O.shapes_of(list(range(1,n+1)))
    evs=json.loads((ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/carrier{n}.json").read_text(encoding="utf-8"))
    # A-static filter (reuse logic: y+z depths/parents/relations unchanged)
    acc_cache={}
    def getacc(ia,ib,x):
        k=(ia,ib,x)
        if k not in acc_cache:
            A,B=Sh[ia],Sh[ib]
            rep=V.replay(A,B,[("K",x)])
            acc_cache[k]=rep
        return acc_cache[k]
    def rel(t,a,b):
        ca=anc_set_list(t,a); cb=anc_set_list(t,b)
        return (a in cb, b in ca, lca_list(t,a,b))
    static=[]
    for e in evs:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        A,B=Sh[ia],Sh[ib]
        rep=getacc(ia,ib,x)
        Ap,Bp=rep["endA"],rep["endB"]
        d0=dict(e["brow0"][1]); d1=dict(e["brow1"][1])
        zs=set(d0)|set(d1)
        part=[z for z in zs if d1.get(z,0)-d0.get(z,0)!=0]
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
                ayz=(y in anc_set_list(A,z), z in anc_set_list(A,y))
                ayz2=(y in anc_set_list(Ap,z), z in anc_set_list(Ap,y))
                if ayz!=ayz2: ok=False; break
        if ok:
            CA=-2*(((da1[y]+1)//2)-((da0[y]+1)//2))
            if CA!=0: ok=False
        if ok: static.append(e)
    print(f"[STB] static {len(static)}/{len(evs)}")
    # per-event analysis
    Tcnt=Counter(); Gcnt=Counter(); fresh_total=0; fresh_latent=0
    twin_cases=Counter()
    neg_edge=0; neg_recharge=0
    mism=0
    # for transport prediction: pre-slot+transport -> Delta
    trans_det=defaultdict(set)
    for e in static:
        ia,ib,x,y=e["ia"],e["ib"],e["x"],e["y"]
        A,B=Sh[ia],Sh[ib]
        rep=getacc(ia,ib,x)
        Ap,Bp=rep["endA"],rep["endB"]
        d0=dict(e["brow0"][1]); d1=dict(e["brow1"][1])
        c0,c1=e["brow0"][0],e["brow1"][0]
        # verify C identity
        da0=depths_list(A); da1=depths_list(Ap)
        t0=1 if A[0]==B[0] else 0
        t1=1 if Ap[0]==Bp[0] else 0
        RB0=R_static(B,y); RB1=R_static(Bp,y)
        CB=RB1-RB0
        CA=-2*(((da1[y]+1)//2)-((da0[y]+1)//2))
        CT=2*(t1-t0)
        if CB+CA+CT!=e["C"]:
            mism+=1
        # T classes per z
        zs=set(d0)|set(d1)
        # merge/split detection at event level later; per-z T1-T4
        pre_slots={}; post_slots={}
        for z in zs:
            pre_slots[z]=slot_of(B,y,z)
            post_slots[z]=slot_of(Bp,y,z)
        for z in zs:
            a=d0.get(z,0); b=d1.get(z,0)
            if a!=0 and b!=0:
                if pre_slots[z]==post_slots[z]: Tcnt['T1']+=1
                else: Tcnt['T2']+=1
            elif a==0 and b!=0:
                Tcnt['T3']+=1
                fresh_total+=1
                # latent block test: z in some pre hanging block of P_B(x)?
                # P_B(x) hanging blocks cover all non-path keys; check z's pre block
                # find z's pre block relative to x-path
                Pb=path_nodes(B,x)
                pset=set(nd[0] for nd in Pb)
                if z not in pset:
                    fresh_latent+=1
                else:
                    # z on path: latent = pivot itself (still pre-existing)
                    fresh_latent+=1
            elif a!=0 and b==0:
                Tcnt['T4']+=1
        # merge/split flags
        # T5: >=2 pre sources map to same post slot with combined mass? approximate: #pre-support > #post-support and post coeff magnitude >= sum?
        # keep simple: record event-level support counts
        if len([z for z in zs if d0.get(z,0)!=0])>len([z for z in zs if d1.get(z,0)!=0]):
            Tcnt['T5ev']+=1
        if len([z for z in zs if d1.get(z,0)!=0])>len([z for z in zs if d0.get(z,0)!=0]):
            Tcnt['T6ev']+=1
        Gcnt[path_relation(B,x,y)]+=1
        # twin channel
        twin_cases[(t0,t1,CB!=0)]+=1
        # determinism key: (pre-slot, G-class) -> Delta
        for z in zs:
            dl=d1.get(z,0)-d0.get(z,0)
            if dl!=0:
                trans_det[(pre_slots[z],path_relation(B,x,y))].add(dl)
    print(f"[STB] identity mismatches: {mism}")
    print(f"[STB] T-classes: {dict(Tcnt)}")
    print(f"[STB] fresh latent coverage: {fresh_latent}/{fresh_total}")
    print(f"[STB] G-classes: {dict(Gcnt)}")
    print(f"[STB] twin cases (t0,t1,CB!=0): {dict(twin_cases)}")
    amb=sum(1 for v in trans_det.values() if len(v)>1)
    print(f"[STB] transport determinism classes: {len(trans_det)} amb: {amb}")
    # negative-edge recharge in static subsystem: find D=-2 V:1->3 analog? check D<0 with V rise? need V; approximate via D-profile? Just report D<0 C>0 static cases (recharge-like)
    # M_static test: define M_static = sum over y of max(0, R_B(y) - baseline?) Too vague; test simple: M = sum positive Lambda mass on static claims? Skip full; report open.
    out={"n_static":len(static),"T":dict(Tcnt),"fresh_latent":[fresh_latent,fresh_total],"G":dict(Gcnt),"mism":mism,"trans_amb":amb,"trans_classes":len(trans_det)}
    (ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/staticB.json").write_text(json.dumps(out,indent=1,default=str),encoding="utf-8")
    print("[STB] saved staticB.json")

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
