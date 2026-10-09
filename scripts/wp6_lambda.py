"""PIVOT-25R-COMP §7-9: Lambda coefficient matrices + joint mismatch tests.

R_T(x) = c_T(x) + sum_y lambda_T(x,y)  [fringe masses as key sums].
K_1 = sum max(lB-lA,0); K_abs = sum |lB-lA| over (x,y).
Test K_1(s)-K_1(s') >= D_s(x) (and K_abs) on transitions.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import (path_nodes, sz, depths_list, Tmap)
import wp6_overflow as V


def step(sid, msg):
    print("[LMD %s] %s" % (sid, msg), flush=True)


def subkeys_list(t, x):
    nd = t
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    out = []

    def go(m):
        if m is None:
            return
        out.append(m[0])
        go(m[1])
        go(m[2])
    go(nd)
    return out


def R_coeffs(T, x):
    """(c, {y: lambda}) with R_T(x) = c + sum_y lam[y]."""
    P = path_nodes(T, x)
    d = len(P) - 1
    if d == 0:
        return 0, {}
    dd = depths_list(T)
    q = dd[x] // 2
    xn = P[d]
    Lset, Rset = subkeys_list(T, xn[1][0]) if xn[1] else [], \
        subkeys_list(T, xn[2][0]) if xn[2] else []
    # fringe block key sets from x upward
    fr = []
    for k in range(d):
        par = P[d - 1 - k]
        ch = P[d - k]
        off = par[2] if par[1] is ch else par[1]
        mset = []
        if off is not None:
            mset = subkeys_list(T, off[0])
        fr.append(mset)
    if d % 2 == 0:
        st = (0, 0, [], 0)
    else:
        r0 = P[0][0]
        st = (-1, 0, [1], 0) if x < r0 else (0, -1, [1], 0)
    # double words bottom-up; fold reversed
    pats = []
    for i in range(d, 1, -2):
        gnd, pnd, xnd = P[i - 2], P[i - 1], P[i]
        sp = 0 if gnd[1] is pnd else 1
        sx = 0 if pnd[1] is xnd else 1
        pats.append({(0, 0): "LL", (1, 1): "RR", (0, 1): "LR",
                     (1, 0): "RL"}[(sp, sx)])
    for pat in reversed(pats):
        st = Tmap(pat, st)
    aL, aR, f, c = st
    lam = {}
    for y in Lset:
        lam[y] = lam.get(y, 0) + aL
    for y in Rset:
        lam[y] = lam.get(y, 0) + aR
    for j, fj in enumerate(f):
        if j < len(fr):
            for y in fr[j]:
                lam[y] = lam.get(y, 0) + fj
    return c, lam


def K_of(LA, LB, n, mode):
    tot = 0
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            d = LB[x].get(y, 0) - LA[x].get(y, 0)
            tot += max(d, 0) if mode == "pos" else abs(d)
    return tot


def Lam_all(T, n):
    out = {}
    for x in range(1, n + 1):
        _, lam = R_coeffs(T, x)
        out[x] = lam
    return out


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    K1 = {"k1": [0, 0], "kabs": [0, 0]}
    worst = {"k1": None, "kabs": None}
    # D_s(x) via fold values (reuse R_static through coeffs: value check)
    from wp6_staticR import R_static
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt = {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
    nacc = nd = 0
    for ia in range(nS):
        LA = Lam_all(Sh[ia], n)
        for ib in range(nS):
            LB = Lam_all(Sh[ib], n)
            k1 = K_of(LA, LB, n, "pos")
            ka = K_of(LA, LB, n, "abs")
            da = depths_list(Sh[ia])
            t = 1 if Sh[ia][0] == Sh[ib][0] else 0
            for x in range(1, n + 1):
                # D_s(x) from Lambda rows: R_B(x) = c + sum lam
                cB, lamB = R_coeffs(Sh[ib], x)
                RB = cB + sum(lamB.values())
                if ia == 0 and ib == 0:
                    assert RB == R_static(Sh[ib], x), (x, RB)
                # sanity vs R_static value
                Ds_x = RB - 2 * ((da[x] + 1) // 2) - 2 * (1 - t)
                rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
                LA2 = Lam_all(rep["endA"], n)
                LB2 = Lam_all(rep["endB"], n)
                k12 = K_of(LA2, LB2, n, "pos")
                ka2 = K_of(LA2, LB2, n, "abs")
                nacc += 1
                for name, a, b in (("k1", k1, k12), ("kabs", ka, ka2)):
                    ok = (a - b) >= Ds_x
                    K1[name][0 if ok else 1] += 1
                    if not ok and (worst[name] is None or
                                   (a - b) - Ds_x < worst[name][0]):
                        worst[name] = ((a - b) - Ds_x, Ds_x, ia, ib, x)
        step("G", "ia=%d/%d acc=%d" % (ia + 1, nS, nacc))
    step("R", "K1=%s Kabs=%s" % (K1["k1"], K1["kabs"]))
    step("R", "worst(excess): %s" %
         {k: (v[:2] if v else None) for k, v in worst.items()})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("lambda%d.json" % n)).write_text(
        json.dumps({"K1": K1, "worst": worst, "nacc": nacc}, indent=1,
                   default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
