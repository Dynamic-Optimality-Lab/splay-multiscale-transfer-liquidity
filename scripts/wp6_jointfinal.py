"""PIVOT-25R-U §4: exact finite certificate from cutting-plane active set.

usage: python wp6_jointfinal.py <n>
1. Load joint_cut<n>.json active rows (status must be FEASIBLE-SCAN).
2. Min-max magnitude LP -> round rationals -> exact-verify ACTIVE rows.
3. Integer-scaled INDEPENDENT full-graph scan (recompute contexts, rows,
   rewards, twin, Phi drops from scratch): GREEN iff 0 bad.
4. Save dual_mine/joint_n<n>.json certificate.
"""
from __future__ import annotations
import sys
import copy
import json
import math
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[JFN %s] %s" % (sid, msg), flush=True)


def omcode(la, ra, lb, rb):
    vals = sorted(set((la, ra, lb, rb)))
    rk = {v: i for i, v in enumerate(vals)}
    return (rk[la], rk[ra], rk[lb], rk[rb])


def main():
    import sys as _s
    import pickle
    import numpy as np
    from scipy.optimize import linprog
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 7
    SP = (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
          "dual_mine" / ("joint_cut%d.json" % n))
    st = json.loads(SP.read_text())
    assert st["status"] == "FEASIBLE-SCAN", st["status"]
    rows = st["rows"]
    var = {}
    for r in rows:
        for e in r["M"]:
            if e not in var:
                var[e] = len(var)
    E, Vv = len(rows), len(var)
    step("M", "active rows=%d vars=%d" % (E, Vv))
    M = np.zeros((E, Vv))
    bv = np.zeros(E)
    for i, r in enumerate(rows):
        for e, c in r["M"].items():
            M[i, var[e]] = c
        bv[i] = r["b"]
    # minmax: min U s.t. Mg>=b, |g|<=U
    c = np.zeros(Vv + 1)
    c[-1] = 1.0
    A1 = np.zeros((E, Vv + 1))
    A1[:, :-1] = -M
    A2 = np.zeros((Vv, Vv + 1))
    A2[:, :-1] = np.eye(Vv)
    A2[:, -1] = -1.0
    A3 = np.zeros((Vv, Vv + 1))
    A3[:, :-1] = -np.eye(Vv)
    A3[:, -1] = -1.0
    Aub = np.vstack([A1, A2, A3])
    bub = np.concatenate([-bv, np.zeros(2 * Vv)])
    res = linprog(c, A_ub=Aub, b_ub=bub,
                  bounds=[(None, None)] * Vv + [(0, None)], method="highs")
    assert res.status == 0, res.status
    step("MM", "minmax|g|=%.6g" % res.fun)
    G = [Fraction(x).limit_denominator(10 ** 6) for x in res.x[:-1]]
    bad = sum(1 for i, r in enumerate(rows)
              if sum(G[var[e]] * c for e, c in r["M"].items()) < r["b"])
    step("MM", "active-row exact violations: %d/%d" % (bad, E))
    assert bad == 0
    dens = set(g.denominator for g in G)
    D = 1
    for d in dens:
        D = D * d // math.gcd(D, d)
    step("MM", "distinct dens=%d lcm D=%d range=[%s,%s]" %
         (len(dens), D, min(G), max(G)))
    W = {e: G[i] * D for e, i in var.items()}  # integers
    # independent full-graph integer scan
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    Dp = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                              "0909c74a" / ("trans%d.pkl" % n)), "rb"))
    Atrans, Btrans = Dp["Atrans"], Dp["Btrans"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd, LI = {}, {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
        for x in range(1, n + 1):
            nd = Sh[ia]
            while nd is not None and nd[0] != x:
                nd = nd[1] if x < nd[0] else nd[2]
            ks = []

            def go(m):
                if m is None:
                    return
                ks.append(m[0])
                go(m[1])
                go(m[2])
            go(nd)
            a, b = min(ks), max(ks)
            assert len(ks) == b - a + 1
            LI[(ia, x)] = (dd[ia][x], a, b, len(ks))
    nbad = 0
    checked = 0
    first = None
    for ia in range(nS):
        for ib in range(nS):
            twu = 1 if rt[ia] == rt[ib] else 0
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                assert a == (dd[ia].get(x, 0) + 1) // 2
                # DELETE
                twd = 1 if rt[ia2] == rt[ib] else 0
                bd = (-2 * a - 2 * (twd - twu)) * D
                lh = 0
                for y in range(1, n + 1):
                    da, la, ra, na = LI[(ia, y)]
                    db, lb, rb, nb = LI[(ib, y)]
                    da2, la2, ra2, na2 = LI[(ia2, y)]
                    va = sorted(set((la, ra, lb, rb)))
                    ka = {v: i for i, v in enumerate(va)}
                    vb = sorted(set((la2, ra2, lb, rb)))
                    kb = {v: i for i, v in enumerate(vb)}
                    e0 = (da, db, na, nb, (ka[la], ka[ra], ka[lb], ka[rb]))
                    e1 = (da2, db, na2, nb, (kb[la2], kb[ra2], kb[lb],
                                             kb[rb]))
                    if e0 != e1:
                        lh += W.get(str(e0), 0) - W.get(str(e1), 0)
                if lh < bd:
                    nbad += 1
                    if first is None:
                        first = ("D", ia, ib, x, lh, bd)
                checked += 1
                # KEEP
                ib2 = Btrans[(ib, x)][0]
                q = dd[ib].get(x, 0) // 2
                twk = 1 if rt[ia2] == rt[ib2] else 0
                bk = (q - 2 * a - 2 * (twk - twu)) * D
                lh = 0
                for y in range(1, n + 1):
                    da, la, ra, na = LI[(ia, y)]
                    db, lb, rb, nb = LI[(ib, y)]
                    da2, la2, ra2, na2 = LI[(ia2, y)]
                    db2, lb2, rb2, nb2 = LI[(ib2, y)]
                    va = sorted(set((la, ra, lb, rb)))
                    ka = {v: i for i, v in enumerate(va)}
                    vb = sorted(set((la2, ra2, lb2, rb2)))
                    kb = {v: i for i, v in enumerate(vb)}
                    e0 = (da, db, na, nb, (ka[la], ka[ra], ka[lb], ka[rb]))
                    e1 = (da2, db2, na2, nb2, (kb[la2], kb[ra2], kb[lb2],
                                               kb[rb2]))
                    if e0 != e1:
                        lh += W.get(str(e0), 0) - W.get(str(e1), 0)
                if lh < bk:
                    nbad += 1
                    if first is None:
                        first = ("K", ia, ib, x, lh, bk)
                checked += 1
        if (ia + 1) % 60 == 0:
            step("SC", "%d/%d bad=%d" % (ia + 1, nS, nbad))
    step("SC", "checked=%d bad=%d (expect %d)" %
         (checked, nbad, nS * nS * n * 2))
    assert checked == nS * nS * n * 2
    cert = {"n": n, "checked": checked, "bad": nbad,
            "first": None if first is None else [first[0], first[1],
                                                 first[2], first[3],
                                                 str(first[4]), str(first[5])],
            "active_rows": E, "vars": Vv, "D": D,
            "minmax": float(res.fun),
            "g": {str(k): str(G[v]) for k, v in var.items()},
            "green": nbad == 0}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("joint_n%d.json" % n)).write_text(
        json.dumps(cert, indent=1, default=str), encoding="utf-8")
    step("S", "CERTIFICATE: %s" % ("GREEN" if nbad == 0 else "RED"))
    return 0 if nbad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
