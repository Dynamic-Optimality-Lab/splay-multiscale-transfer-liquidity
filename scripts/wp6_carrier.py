"""PIVOT-25R-CAR §1-3: gateway-event dataset with A-transport mapping.

For each KEEP access with created future deficit (C_s(x,y)>0 for some y):
B-tracer (x, y, C amount, B support change), A-transport partition per key
(depth/set changed? path membership? hanging/Remote), support->A mapping,
y-location class (on-path/hanging/outside, LCA, boundaries).
Saves dual_mine/carrier_bank.json.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list
from wp6_lambda import R_coeffs


def step(sid, msg):
    print("[CAR %s] %s" % (sid, msg), flush=True)


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
    return frozenset(out)


def pathset(t, x):
    p = set()
    nd = t
    while nd is not None and nd[0] != x:
        p.add(nd[0])
        nd = nd[1] if x < nd[0] else nd[2]
    if nd is not None:
        p.add(nd[0])
    return p


def lca_of(t, a, b):
    def anc(y):
        s = set()
        nd = t
        while nd is not None and nd[0] != y:
            s.add(nd[0])
            nd = nd[1] if y < nd[0] else nd[2]
        if nd is not None:
            s.add(nd[0])
        return s
    cands = anc(a) & anc(b)
    if not cands:
        return None
    d = depths_list(t)
    return max(cands, key=lambda k: d[k])


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    cap = int(_s.argv[2]) if len(_s.argv) > 2 else 0
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    evs = []
    nacc = 0
    for ia in range(nS):
        for ib in range(nS):
            for x in range(1, n + 1):
                if cap and nacc >= cap:
                    break
                A, B = Sh[ia], Sh[ib]
                da = depths_list(A)
                t = 1 if A[0] == B[0] else 0
                rep = V.replay(A, B, [("K", x)])
                Ap, Bp = rep["endA"], rep["endB"]
                nacc += 1
                # A-transport partition per key
                da2 = depths_list(Ap)
                skA0 = {y: subkeys_list(A, y) for y in range(1, n + 1)}
                skA1 = {y: subkeys_list(Ap, y) for y in range(1, n + 1)}
                pa0, pa1 = pathset(A, x), pathset(Ap, x)
                t2 = 1 if Ap[0] == Bp[0] else 0
                for y in range(1, n + 1):
                    Dpre = R_static(B, y) - 2 * ((da[y] + 1) // 2) - \
                        2 * (1 - t)
                    Dpost = R_static(Bp, y) - 2 * ((da2[y] + 1) // 2) - \
                        2 * (1 - t2)
                    C = Dpost - Dpre
                    if C <= 0:
                        continue
                    # B support change (Lambda row coeffs pre/post)
                    cB, lamB = R_coeffs(B, y)
                    cP, lamP = R_coeffs(Bp, y)
                    # A region of y
                    in0 = y in pa0
                    in1 = y in pa1
                    dc = da[y] != da2[y]
                    sc = skA0[y] != skA1[y]
                    evs.append({
                        "n": n, "ia": ia, "ib": ib, "x": x, "y": y,
                        "C": C, "Dpre": Dpre, "Dpost": Dpost,
                        "brow0": [cB, sorted(lamB.items())],
                        "brow1": [cP, sorted(lamP.items())],
                        "areg": [in0, in1, dc, sc],
                        "lca": lca_of(A, x, y),
                        "lca2": lca_of(Ap, x, y),
                    })
            if cap and nacc >= cap:
                break
        step("G", "ia=%d/%d acc=%d events=%d" % (ia + 1, nS, nacc,
                                                 len(evs)))
        if cap and nacc >= cap:
            break
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("carrier%d.json" % n)).write_text(
        json.dumps(evs, indent=0, default=str), encoding="utf-8")
    step("S", "n=%d accesses=%d C>0 events=%d" % (n, nacc, len(evs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
