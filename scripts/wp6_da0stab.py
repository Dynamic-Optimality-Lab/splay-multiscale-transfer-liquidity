"""Stabilization: n=5 vs n=6 da=0 rays on common types (normalized)."""
import sys, copy, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
from wp6_da0cone import build, solve

def main():
    rays={}
    for n in (5,6):
        print(f"[STB] build n={n}",flush=True)
        cons=build(n)
        res,tvars,rvars,Amat=solve(cons)
        g=res.x
        Vv=len(tvars)+len(rvars)
        tot=np.asarray(Amat.sum(axis=0)).ravel()
        s=float(tot@g)
        gn=g/max(1e-300,abs(s))  # normalize: total drops == sign(s)*1
        rays[n]=(gn,tvars,rvars)
        print(f"[STB] n={n} maxsum={-res.fun} normscale={abs(s)}",flush=True)
    g5,t5,r5=rays[5]; g6,t6,r6=rays[6]
    inv5={i:t for t,i in t5.items()}; inv6={i:t for t,i in t6.items()}
    common=sorted(set(t5)&set(t6),key=str)
    print(f"[STB] common types: {len(common)}",flush=True)
    v5=np.array([g5[t5[t]] for t in common])
    v6=np.array([g6[t6[t]] for t in common])
    print("[STB] n=5 ray:",[(str(t),round(float(v),4)) for t,v in zip(common,v5)],flush=True)
    print("[STB] n=6 ray:",[(str(t),round(float(v),4)) for t,v in zip(common,v6)],flush=True)
    # exact / scalar / affine?
    d1=float(np.max(np.abs(v5-v6)))
    # scalar: v6 = a*v5?
    denom=float(v5@v5)
    a=float(v6@v5)/denom if denom>1e-300 else 0
    d2=float(np.max(np.abs(v6-a*v5)))
    print(f"[STB] max|v5-v6|={d1:.6f} best-scalar={a:.6f} max|v6-a*v5|={d2:.6f}",flush=True)
    json.dump({"common":len(common),"d_exact":d1,"scalar":a,"d_scalar":d2,
               "v5":{str(t):float(v) for t,v in zip(common,v5)},
               "v6":{str(t):float(v) for t,v in zip(common,v6)}},
              open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/da0stab.json","w"),indent=1,default=str)
    return 0

if __name__=="__main__":
    import sys as _s
    sys.exit(main())
