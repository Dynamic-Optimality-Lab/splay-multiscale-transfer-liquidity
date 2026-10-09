"""PIVOT-25R-U §3b: EXACT cutting-plane loop (integer verdicts throughout).

usage: python wp6_jointexact.py <n> <maxiters> [K]
state: dual_mine/joint_texact<n>.json. INIT copies joint_cut<n>.json rows.
Per iter: minmax LP -> round rationals -> INTEGER full-graph scan (scaled
by denominator lcm). 0 bad => GREEN cert joint_n<n>.json. Else top-K exact
violations appended. LP status 2 => preserved float-infeasible + data.
"""
from __future__ import annotations
import sys
import copy
import json
import math
import heapq
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[JTX %s] %s" % (sid, msg), flush=True)


def omcode(la, ra, lb, rb):
    vals = sorted(set((la, ra, lb, rb)))
    rk = {v: i for i, v in enumerate(vals)}
    return (rk[la], rk[ra], rk[lb], rk[rb])


def minmax_solve(rows):
    import numpy as np
    from scipy.optimize import linprog
    var = {}
    for r in rows:
        for e in r["M"]:
            if e not in var:
                var[e] = len(var)
    E, Vv = len(rows), len(var)
    M = np.zeros((E, Vv))
    bv = np.zeros(E)
    for i, r in enumerate(rows):
        for e, c in r["M"].items():
            M[i, var[e]] = c
        bv[i] = r["b"]
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
    return res, var


def main():
    import sys as _s
    import pickle
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 7
    maxit = int(_s.argv[2]) if len(_s.argv) > 2 else 2
    K = int(_s.argv[3]) if len(_s.argv) > 3 else 400
    AD = (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
          "dual_mine")
    SP = AD / ("joint_texact%d.json" % n)
    if SP.exists():
        st = json.loads(SP.read_text())
        rows, done, log = st["rows"], st["iters_done"], st["log"]
        step("L", "resumed n=%d rows=%d iters=%d" % (n, len(rows), done))
    else:
        prev = json.loads((AD / ("joint_cut%d.json" % n)).read_text())
        assert prev["status"] == "FEASIBLE-SCAN"
        rows, done, log = prev["rows"], 0, []
        step("L", "init n=%d rows=%d" % (n, len(rows)))
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    AB = (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a")
    Dp = pickle.load(open(str(AB / ("trans%d.pkl" % n)), "rb"))
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
    for it in range(maxit):
        res, var = minmax_solve(rows)
        if res.status != 0:
            st = {"rows": rows, "iters_done": done, "status":
                  "LP-INFEASIBLE-FLOAT", "log": log}
            SP.write_text(json.dumps(st, indent=1, default=str),
                          encoding="utf-8")
            step("LP", "status=%s: float-infeasible, data preserved" %
                 res.status)
            return 2
        active_sigs = set()
        for r in rows:
            active_sigs.add((frozenset(r["M"].items()), r["b"]))
        # Fixed-denominator rounding (S=1024): exact verification decides;
        # free denominators explode the lcm (observed ~400 digits).
        S = 1024
        GI = [int(round(x * S)) for x in res.x[:-1]]
        G = [Fraction(v, S) for v in GI]
        D = S
        W = {e: GI[i] for e, i in var.items()}
        nbad = 0
        checked = 0
        heap = []
        nd = {}
        for ia in range(nS):
            for ib in range(nS):
                twu = 1 if rt[ia] == rt[ib] else 0
                for x in range(1, n + 1):
                    ia2, a = Atrans[(ia, x)]
                    # DELETE
                    twd = 1 if rt[ia2] == rt[ib] else 0
                    bd = (-2 * a - 2 * (twd - twu)) * D
                    d = nd
                    d.clear()
                    for y in range(1, n + 1):
                        da, la, ra, na = LI[(ia, y)]
                        db, lb, rb, nb = LI[(ib, y)]
                        da2, la2, ra2, na2 = LI[(ia2, y)]
                        va = sorted(set((la, ra, lb, rb)))
                        ka = {v: i for i, v in enumerate(va)}
                        vb = sorted(set((la2, ra2, lb, rb)))
                        kb = {v: i for i, v in enumerate(vb)}
                        e0 = (da, db, na, nb,
                              (ka[la], ka[ra], ka[lb], ka[rb]))
                        e1 = (da2, db, na2, nb,
                              (kb[la2], kb[ra2], kb[lb], kb[rb]))
                        if e0 != e1:
                            d[e0] = d.get(e0, 0) + 1
                            d[e1] = d.get(e1, 0) - 1
                    lh = 0
                    for e, c in d.items():
                        lh += W.get(str(e), 0) * c
                    if lh < bd:
                        nbad += 1
                        df = bd - lh
                        if len(heap) < K:
                            heapq.heappush(heap, (df, ia, ib, x, "D",
                                                  dict(d), bd))
                        else:
                            heapq.heappushpop(heap, (df, ia, ib, x, "D",
                                                     dict(d), bd))
                    checked += 1
                    # KEEP
                    ib2 = Btrans[(ib, x)][0]
                    q = dd[ib].get(x, 0) // 2
                    twk = 1 if rt[ia2] == rt[ib2] else 0
                    bk = (q - 2 * a - 2 * (twk - twu)) * D
                    d.clear()
                    for y in range(1, n + 1):
                        da, la, ra, na = LI[(ia, y)]
                        db, lb, rb, nb = LI[(ib, y)]
                        da2, la2, ra2, na2 = LI[(ia2, y)]
                        db2, lb2, rb2, nb2 = LI[(ib2, y)]
                        va = sorted(set((la, ra, lb, rb)))
                        ka = {v: i for i, v in enumerate(va)}
                        vb = sorted(set((la2, ra2, lb2, rb2)))
                        kb = {v: i for i, v in enumerate(vb)}
                        e0 = (da, db, na, nb,
                              (ka[la], ka[ra], ka[lb], ka[rb]))
                        e1 = (da2, db2, na2, nb2,
                              (kb[la2], kb[ra2], kb[lb2], kb[rb2]))
                        if e0 != e1:
                            d[e0] = d.get(e0, 0) + 1
                            d[e1] = d.get(e1, 0) - 1
                    lh = 0
                    for e, c in d.items():
                        lh += W.get(str(e), 0) * c
                    if lh < bk:
                        nbad += 1
                        df = bk - lh
                        if len(heap) < K:
                            heapq.heappush(heap, (df, ia, ib, x, "K",
                                                  dict(d), bk))
                        else:
                            heapq.heappushpop(heap, (df, ia, ib, x, "K",
                                                     dict(d), bk))
                    checked += 1
            if (ia + 1) % 120 == 0:
                step("SC", "n=%d iter=%d %d/%d bad=%d" %
                     (n, done, ia + 1, nS, nbad))
        exp = nS * nS * n * 2
        step("IT", "iter=%d checked=%d/%d exactbad=%d rows=%d D=%d U=%.4g" %
             (done, checked, exp, nbad, len(rows), D, res.fun))
        log.append({"iter": done, "checked": checked, "bad": nbad,
                    "rows": len(rows), "D": D, "U": float(res.fun)})
        if nbad == 0:
            cert = {"n": n, "checked": checked, "bad": 0,
                    "active_rows": len(rows), "vars": len(var), "D": D,
                    "minmax": float(res.fun),
                    "g": {str(k): str(G[v]) for k, v in var.items()},
                    "green": True, "log": log}
            (AD / ("joint_n%d.json" % n)).write_text(
                json.dumps(cert, indent=1, default=str), encoding="utf-8")
            st = {"rows": rows, "iters_done": done + 1, "status": "GREEN",
                  "log": log}
            SP.write_text(json.dumps(st, indent=1, default=str),
                          encoding="utf-8")
            step("S", "GREEN CERTIFICATE %d/%d" % (checked, exp))
            return 0
        out, seen = [], set()
        for item in sorted(heap, reverse=True):
            _, ia, ib, x, mo, d, b = item
            sig = (frozenset((str(k), v) for k, v in d.items()), b // D)
            if sig in seen or sig in active_sigs:
                continue
            seen.add(sig)
            out.append((ia, ib, x, mo, d, b))
        for (ia, ib, x, mo, d, b) in out:
            rows.append({"M": {str(k): v for k, v in d.items()},
                         "b": b // D,
                         "tag": "xcut%d-%d" % (done, len(rows)),
                         "wit": {"n": n, "ia": ia, "ib": ib, "x": x,
                                 "mo": mo}})
        done += 1
        st = {"rows": rows, "iters_done": done, "status": "PROGRESS",
              "log": log}
        SP.write_text(json.dumps(st, indent=1, default=str), encoding="utf-8")
        step("L", "added=%d rows=%d" % (len(out), len(rows)))
    step("L", "call budget out: iters=%d rows=%d" % (done, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
