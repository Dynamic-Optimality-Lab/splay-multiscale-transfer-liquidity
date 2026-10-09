"""PIVOT-25R-U §6: free context-coefficient feasibility (sparse LP).

Vars g_eta (FREE) + slack t. maximize t s.t. M[e]*g - t >= b_e.
Exact rational reconstruction + verification after float solve.
Edge set: 42-cert + POS/POSA/L4 witnesses + battery A-variants + PR904.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O

CERT = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointcert/"
            "joint_depth_template_countercertificate.json")


def step(sid, msg):
    print("[JLP %s] %s" % (sid, msg), flush=True)


def shift(t):
    if t is None:
        return None
    return [t[0] + 1, shift(t[1]), shift(t[2])]


def depths_list(t):
    out = {}

    def go(nd, d):
        if nd is None:
            return
        out[nd[0]] = d
        go(nd[1], d + 1)
        go(nd[2], d + 1)
    go(t, 0)
    return out


def subkeys(t, x):
    nd = t
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    assert nd is not None
    out = []

    def go(m):
        if m is None:
            return
        out.append(m[0])
        go(m[1])
        go(m[2])
    go(nd)
    return out


def eta_of(A, B, x):
    da, db = depths_list(A), depths_list(B)
    ka, kb = subkeys(A, x), subkeys(B, x)
    la, ra, na = min(ka), max(ka), len(ka)
    lb, rb, nb = min(kb), max(kb), len(kb)
    assert na == ra - la + 1 and nb == rb - lb + 1
    assert la <= x <= ra and lb <= x <= rb
    vals = sorted(set((la, ra, lb, rb)))
    rk = {v: i for i, v in enumerate(vals)}
    return (da[x], db[x], na, nb, (rk[la], rk[ra], rk[lb], rk[rb]))


def edge_row(A, B, x, mo, n):
    rep = V.replay(A, B, [(mo, x)])
    acc = rep["accesses"][0]
    a, q = acc["a"], acc["q"]
    w = (q - 2 * a) if mo == "K" else -2 * a
    t0 = 1 if A[0] == B[0] else 0
    t1 = 1 if rep["endA"][0] == rep["endB"][0] else 0
    b = w - 2 * (t1 - t0)
    h = Counter()
    h0 = Counter(eta_of(A, B, y) for y in range(1, n + 1))
    h1 = Counter(eta_of(rep["endA"], rep["endB"], y)
                 for y in range(1, n + 1))
    for e, c in h0.items():
        h[e] += c
    for e, c in h1.items():
        h[e] -= c
    return h, b


def main():
    import numpy as np
    from scipy.optimize import linprog
    SH = {7: O.shapes_of(list(range(1, 8))),
          8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    rows = []  # (hist-diff Counter, b, tag)
    D = json.loads(CERT.read_text())
    for it in D["items"]:
        A, B = shift(it["A"]), shift(it["B"])
        x = it["key"] + 1
        mo = "K" if it["mode"] == "KEEP" else "D"
        h, b = edge_row(A, B, x, mo, 8)
        rows.append((h, b, "cert"))
    wit8 = [(457, 429, 8, "K"), (1091, 1003, 7, "K"), (869, 910, 2, "K"),
            (1093, 1003, 7, "K"), (90, 2, 8, "K"), (255, 2, 8, "K"),
            (1001, 1359, 1, "K"), (1003, 1359, 1, "K"), (480, 560, 3, "K"),
            (581, 598, 6, "K"), (786, 785, 8, "K"), (1175, 1429, 1, "K"),
            (160, 358, 2, "K"), (651, 649, 6, "K"), (581, 602, 4, "K"),
            (496, 560, 3, "K"), (0, 89, 3, "K")]
    for (ia, ib, x, mo) in wit8:
        h, b = edge_row(SH[8][ia], SH[8][ib], x, mo, 8)
        rows.append((h, b, "wit8"))
    bat7 = [(109, 0, 7, "K", "S4a1"), (0, 0, 7, "K", "S4a3"),
            (110, 0, 7, "K", "S2nv"), (48, 0, 7, "K", "ACTL"),
            (0, 243, 1, "K", "recharge"), (0, 428, 1, "K", "tw03"),
            (0, 41, 3, "K", "tw13")]
    # resolve constructed-A indices by JSON match
    idx7 = {json.dumps(s, sort_keys=True): i for i, s in enumerate(SH[7])}
    for (ia, ib, x, mo, tag) in bat7:
        h, b = edge_row(SH[7][ia], SH[7][ib], x, mo, 7)
        rows.append((h, b, tag))
    h, b = edge_row(SH[9][3432], SH[9][0], 9, "K", 9)
    rows.append((h, b, "PR904"))
    G = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                    "0909c74a" / "dual_mine" /
                    "joint_grow.json").read_text())["rows"]
    for r in G:
        h, b = edge_row(r["A"], r["B"], r["x"], r["mo"], r["n"])
        rows.append((h, b, r["tag"]))
    var = {}
    for h, _, _ in rows:
        for e in h:
            if e not in var:
                var[e] = len(var)
    Vv, E = len(var), len(rows)
    step("M", "edges=%d vars=%d" % (E, Vv))
    M = np.zeros((E, Vv))
    bv = np.zeros(E)
    for i, (h, b, _) in enumerate(rows):
        for e, c in h.items():
            M[i, var[e]] = c
        bv[i] = b
    c = np.zeros(Vv + 1)
    c[-1] = -1.0
    Aub = np.zeros((E, Vv + 1))
    Aub[:, :-1] = -M
    Aub[:, -1] = 1.0
    bub = -bv
    res = linprog(c, A_ub=Aub, b_ub=bub,
                  bounds=[(None, None)] * Vv + [(None, 1e6)],
                  method="highs")
    step("LP", "status=%s t*=%s" % (res.status, -res.fun if res.success or
                                    res.status == 3 else None))
    out = {"edges": E, "vars": Vv, "lp_status": res.status,
           "t_star": float(-res.fun) if res.fun is not None else None}
    if res.status == 3:
        step("LP", "UNBOUNDED slack => feasible (no exact assignment yet)")
    elif res.status == 0 and -res.fun >= 1e-9:
        g = res.x[:-1]
        G = [Fraction(x).limit_denominator(10 ** 9) for x in g]
        bad = 0
        for i, (h, b, tag) in enumerate(rows):
            lhs = sum(G[var[e]] * c for e, c in h.items())
            if lhs < b:
                bad += 1
                step("V", "FAIL %s lhs=%s b=%s" % (tag, lhs, b))
                if bad > 5:
                    break
        step("V", "exact rational check: %d/%d violated" % (bad, E))
        out["exact_violations"] = bad
        out["rational_ok"] = bad == 0
        if bad == 0:
            inv = {str(k): str(G[v]) for k, v in var.items()}
            Path(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     "joint_g_feasible.json")).write_text(
                json.dumps({"g": inv, "t_star": out["t_star"]}, indent=1),
                encoding="utf-8")
            step("V", "saved joint_g_feasible.json "
                      "(feasible on sparse set ONLY)")
    else:
        step("LP", "float-INFEASIBLE-or-marginal: NOT a certificate; "
                   "exact dual reconstruction due (not attempted here)")
    Path(str(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "dual_mine" / "joint_lp.json")).write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
