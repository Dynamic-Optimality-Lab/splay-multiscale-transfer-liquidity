"""PIVOT-25R-G §6-9: moved-keys exposure + C_B factorization test.

M_x = keys whose depth or subtree-set changes under Splay_x(B).
E_s(x,y) = (c_B(y), exposed coeff mass, exposed R-mass, transport class).
Collision: same E -> same C_B? Then 328-class resolution via exposure.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list
from wp6_lambda import R_coeffs


def step(sid, msg):
    print("[EXP %s] %s" % (sid, msg), flush=True)


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


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    cap = int(_s.argv[2]) if len(_s.argv) > 2 else 0
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    groups = defaultdict(list)
    nacc = 0
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            for x in range(1, n + 1):
                if cap and nacc >= cap:
                    break
                rep = V.replay(A, B, [("K", x)])
                # moved keys: depth or subtree-set changed in B
                db0 = depths_list(B)
                Bp = rep["endB"]
                db1 = depths_list(Bp)
                sk0 = {y: subkeys_list(B, y) for y in range(1, n + 1)}
                sk1 = {y: subkeys_list(Bp, y) for y in range(1, n + 1)}
                Moved = frozenset(
                    y for y in range(1, n + 1)
                    if db0[y] != db1[y] or sk0[y] != sk1[y])
                # per key y: exposure WITH masses+displacements; C_B exact
                dbd = {}
                for yy in range(1, n + 1):
                    dbd[yy] = db1[yy] - db0[yy]
                for y in range(1, n + 1):
                    cB, lamB = R_coeffs(B, y)
                    cP, lamP = R_coeffs(Bp, y)
                    CB = (cP + sum(lamP.values())) - \
                        (cB + sum(lamB.values()))
                    # NOTE unit-mass form; true R weights fringe masses.
                    # Mass-aware exposure: (c, per-moved-key (lam, delta))
                    exp = (cB, tuple(sorted(
                        (lamB.get(z, 0), dbd[z]) for z in Moved)))
                    groups[exp].append(CB)
                nacc += 1
            if cap and nacc >= cap:
                break
        if (ia + 1) % 14 == 0:
            step("G", "ia=%d/%d acc=%d" % (ia + 1, nS, nacc))
        if cap and nacc >= cap:
            break
    amb = {k: v for k, v in groups.items() if len(set(v)) > 1}
    step("R", "acc=%d exp-classes=%d amb=%d" %
         (nacc, len(groups), len(amb)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("expose%d.json" % n)).write_text(
        json.dumps({"acc": nacc, "classes": len(groups), "amb": len(amb)},
                   indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
