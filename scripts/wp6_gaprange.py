"""Gap polyhedral ranges: min/max of each overlap gap + chain aggregates + one
isolating dual combination. Uses saved SH567 matrix + quotient equalities.
Usage: python scripts/wp6_gaprange.py [pairs|chains|dual]
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def load_sys():
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_sh567_A.npz")
    A = Z["A"].astype(float)
    Amat = sp.csr_matrix(A)
    vm = json.load(open(OUT / "j4_sh567_vmap.json"))["vmap"]
    # rebuild raw for rhs/metas
    import importlib.util
    spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
    raw, info = j4.build_shared([5, 6, 7])
    A2, rhs, metas, vmap = j4.assemble(raw)
    assert A2.shape == Amat.shape
    return Amat, rhs, metas, vmap, j4

def quotient_eqs(vmap):
    """Equality rows: 15 NONE ids + 2 gauge fixes. Returns (Aeq, beq)."""
    from collections import defaultdict
    fams = defaultdict(list)
    for k, i in vmap.items():
        t = eval(k) if isinstance(k, str) else k
        if t[0] == 't' and t[1][0] == ('NONE',):
            fams[t[1][3]].append((t[1][2], i))
    eqs = []
    for dy, lst in sorted(fams.items()):
        base = [i for (dl, i) in lst if dl == -1][0]
        for (dl, i) in lst:
            if dl != -1:
                eqs.append((i, base))
    # gauge: first t-key and first r-key = 0
    tk = [k for k in vmap if (k[0] if not isinstance(k, str) else eval(k)[0]) == 't'][0]
    rk = [k for k in vmap if (k[0] if not isinstance(k, str) else eval(k)[0]) == 'r'][0]
    return eqs, (tk, rk)

def main():
    modes = sys.argv[1:] or ["pairs"]
    Amat, rhs, metas, vmap, j4 = load_sys()
    E, V = Amat.shape
    inv = {i: k for k, i in vmap.items()}
    eqs, (tk, rk) = quotient_eqs(vmap)
    print(f"[GR] E={E} V={V} NONE-eqs={len(eqs)} gauge=({tk},{rk})", flush=True)
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    from scipy.optimize import linprog
    import scipy.sparse as sp
    # build equality matrix: NONE ids + 2 gauge pins
    nEQ = len(eqs) + 2
    er, ec, ev = [], [], []
    beq = np.zeros(nEQ)
    for r, (i, base) in enumerate(eqs):
        er += [r, r]; ec += [i, base]; ev += [1.0, -1.0]
    i1, i2 = vmap[tk], vmap[rk]
    er += [len(eqs), len(eqs) + 1]; ec += [i1, i2]; ev += [1.0, 1.0]
    Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
    if "pairs" in modes:
        out = []
        for (k, dl, d) in dom["overlap"]:
            key1 = ('t', (('F', k), 1, dl, d))
            key2 = ('t', (('F', k), 2, dl, d))
            if key1 not in vmap or key2 not in vmap:
                print(f"[GR] pair k={k} dl={dl} d={d} NOT IN V (unrealized var?)", flush=True)
                continue
            c = np.zeros(V); c[vmap[key2]] = 1.0; c[vmap[key1]] = -1.0
            rmin = linprog(c, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                           bounds=[(None, None)] * V, method="highs")
            rmax = linprog(-c, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                           bounds=[(None, None)] * V, method="highs")
            mn = float(rmin.fun) if rmin.status == 0 else None
            mx = float(-rmax.fun) if rmax.status == 0 else None
            print(f"[GR] gap k={k} dl={dl} d={d}: min={mn} max={mx} "
                  f"(st {rmin.status}/{rmax.status})", flush=True)
            out.append({"k": k, "delta": dl, "d": d, "min": mn, "max": mx})
        json.dump(out, open(OUT / "j4_gapranges.json", "w"), indent=1)
    if "chains" in modes:
        # chain C_m depths 0..m-1; delta = k-d for fixed d; use d=2,k=1 family (overlap deltas -1..2)
        out = []
        d = 2; k = 1
        for m in (1, 2, 3, 4):
            c = np.zeros(V)
            for kk in range(m):
                dl = kk - d
                key1 = ('t', (('F', k), 1, dl, d))
                key2 = ('t', (('F', k), 2, dl, d))
                if key1 not in vmap or key2 not in vmap:
                    print(f"[GR] chain m={m}: missing var dl={dl}", flush=True)
                    c = None; break
                c[vmap[key2]] += 1.0; c[vmap[key1]] -= 1.0
            if c is None:
                out.append({"m": m, "min": None, "max": None}); continue
            rmin = linprog(c, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                           bounds=[(None, None)] * V, method="highs")
            rmax = linprog(-c, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                           bounds=[(None, None)] * V, method="highs")
            mn = float(rmin.fun) if rmin.status == 0 else None
            mx = float(-rmax.fun) if rmax.status == 0 else None
            print(f"[GR] chain d=2,k=1 m={m}: min={mn} max={mx}", flush=True)
            out.append({"m": m, "min": mn, "max": mx})
        json.dump(out, open(OUT / "j4_chainranges.json", "w"), indent=1)
    if "dual" in modes:
        # isolating combination for pair (k=1,dl=0,d=2): min y^T rhs s.t. y^T A = e2-e1 (+gauge-span), y>=0
        k, dl, d = 1, 0, 2
        key1 = ('t', (('F', k), 1, dl, d)); key2 = ('t', (('F', k), 2, dl, d))
        e = np.zeros(V); e[vmap[key2]] = 1.0; e[vmap[key1]] = -1.0
        # allow gauge columns free: add gauge basis to RHS span: y^T A - e in span(NONE-eqs rows, gauge)?
        # Simpler: y^T A_red = e_red on kept cols (gauge-fixed columns dropped).
        keep = [i for i in range(V) if i != i1 and i != i2]
        # NONE quotient: work mod NONE ids by merging columns? approximate: use full Aeq in primal instead.
        # Dual of primal min c^Tx s.t. -Ax<=-rhs, Aeq x=beq:
        # max -rhs^T y + beq^T w s.t. -A^T y + Aeq^T w = c, y>=0.
        # Solve via linprog directly on (y,w).
        import scipy.sparse as _sp
        M = _sp.hstack([-Amat.T, Aeq.T]).tocsr()  # V eqs in (E + nEQ) vars
        c2 = np.concatenate([-rhs, beq])
        # equality constraints M z = c
        res = linprog(c2, A_eq=M, b_eq=e, bounds=[(0, None)] * E + [(None, None)] * nEQ, method="highs")
        print(f"[GR] dual isolating status={res.status} obj={float(res.fun) if res.status==0 else None}", flush=True)
        if res.status == 0:
            y = res.x[:E]
            sup = np.where(y > 1e-7)[0]
            print(f"[GR] support={len(sup)}", flush=True)
            for i in sup[np.argsort(-y[sup])][:14]:
                print(f"    y={float(y[i]):.4f} {metas[i][:7]} rhs={float(rhs[i]):.2f}", flush=True)
            json.dump({"obj": float(res.fun), "support": [[float(y[i]), list(map(str, metas[i][:7])), float(rhs[i])] for i in sup[np.argsort(-y[sup])][:40]]},
                      open(OUT / "j4_gapdual.json", "w"), indent=1, default=str)
    print("[GR] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
