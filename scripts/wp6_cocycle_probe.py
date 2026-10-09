"""Cocycle probes: (1) J3 22/39 Farkas support evaluated in J4 keys (net residual);
(2) exhaustive min(s0pad - s0) over all shapes n<=6, Pad_L/R.
Usage: python scripts/wp6_cocycle_probe.py
"""
import sys, json
from pathlib import Path
from collections import defaultdict
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j3 = load('wp6_j3shared')
j4 = load('wp6_j4shared')

def main():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    import wp6_cycle_ratio as O
    # ---- (2) s0 padding gap ----
    gmin = 1e18
    gdist = defaultdict(int)
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        for B in Sh:
            import copy
            for P, tag in (([0, None, copy.deepcopy(B)], 'L'),
                           ([n + 1, copy.deepcopy(B), None], 'R')):
                for x in range(1, n + 1):
                    Bp = j4.V.replay(B, B, [("K", x)])["endB"]
                    Pp = j4.V.replay(P, P, [("K", x)])["endB"]
                    def s0(T, Tp, x, N):
                        R = j4.R_static(T, x); Rp = j4.R_static(Tp, x)
                        G = N - j4.subsize(T, x); Gp = N - j4.subsize(Tp, x)
                        b = 1 if T[0] == x else 0
                        D0 = R - 2 * (1 - b)
                        return ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
                    a = s0(B, Bp, x, n); b = s0(P, Pp, x, n + 1)
                    gmin = min(gmin, b - a); gdist[round(b - a, 6)] += 1
    print(f"[CC] min(s0pad-s0)={gmin} distinct gaps={len(gdist)}", flush=True)
    print("[CC] gap histogram:", dict(sorted(gdist.items())[:30]), flush=True)
    # ---- (1) J3 farkas in J4 keys ----
    raw3, _ = j3.build_shared([5, 6])
    A3, rhs3, metas3, vmap3 = j3.assemble(raw3)
    E = A3.shape[0]
    t3 = [k for k in vmap3 if k[0] == 't']; r3 = [k for k in vmap3 if k[0] == 'r']
    keep3 = [i for k, i in vmap3.items() if k not in (t3[0], r3[0])]
    Ared = A3[:, keep3]
    Aeq = sp.vstack([Ared.T, np.ones((1, E))]).tocsr()
    beq = np.concatenate([np.zeros(Ared.shape[1]), [1.0]])
    res = linprog(-rhs3, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * E, method="highs")
    y = res.x
    print(f"[CC] J3 farkas value={float(-res.fun)} support={int((y > 1e-9).sum())}", flush=True)
    # J4 net: rebuild J4 rows aligned by meta
    raw4, _ = j4.build_shared([5, 6])
    idx4 = {}
    for i, (terms, rh, m) in enumerate(raw4):
        idx4[(m[0], m[1], m[2], m[3]) if m[0] == 'SELF' else (m[0], m[1], m[2], m[3], m[4])] = i
    net = defaultdict(float)
    tot_rhs = 0.0
    sup = []
    for i in range(E):
        if y[i] > 1e-9:
            m = metas3[i]
            key = (m[0], m[1], m[2], m[3]) if m[0] == 'SELF' else (m[0], m[1], m[2], m[3], m[4])
            j = idx4[key]
            t4, rh4, m4 = raw4[j]
            tot_rhs += y[i] * rhs3[i]
            sup.append((float(y[i]), m, float(rhs3[i])))
            for k, c in t4.items():
                net[k] += y[i] * c
    print(f"[CC] weighted J3 rhs={tot_rhs:.6f}", flush=True)
    print("[CC] J4-space net residual (nonzero entries):", flush=True)
    items = sorted(net.items(), key=lambda kv: -abs(kv[1]))
    nz = [(k, v) for k, v in items if abs(v) > 1e-9]
    print(f"[CC] nonzero={len(nz)}", flush=True)
    for k, v in nz[:40]:
        print(f"   {v:+.4f} {k}", flush=True)
    json.dump({"farkas_value": float(-res.fun), "support": [(float(a), list(b), float(c)) for a, b, c in sup],
               "j4_net": [[str(k), float(v)] for k, v in nz]},
              open(j4.ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine/j4_cocycle_probe.json", "w"), indent=1, default=str)
    print("[CC] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
