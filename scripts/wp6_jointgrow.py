"""PIVOT-25R-U §6: cross-size constraint growth (batches A-D,F).

A: n=11 range obstruction. B: A-rooted/B-deep x=1 (n=7,8,9,11,16,32,64)
   + x=n mirror (n=11). C: twin-to-twin a=1 (n=9,11,16, x=7).
D: DELETE twins of A/B/C + recharge/tw13 DELETEs.
F: n=7 search for same-(dA,dB,nA,nB) different-omega pairs (<=40).
E (battery/borrowed rows): already in the 67 (documented, not repeated).

Every built tree BST-validated by inorder; every row replay-instantiated.
Saves dual_mine/joint_grow.json {rows:[...], eta distinct, ...} with rows
as (n,A,B,x,mode) for the LP stage.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[JGR %s] %s" % (sid, msg), flush=True)


def inorder(t):
    return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])


def vr(keys):
    t = None
    for k in reversed(list(keys)):
        t = [k, None, t]
    return t


def vl(keys):
    t = None
    for k in list(keys):
        t = [k, t, None]
    return t


def valid(t, n, tag):
    assert inorder(t) == list(range(1, n + 1)), tag
    return t


def main():
    rows = []

    def add(n, A, B, x, mo, tag):
        valid(A, n, tag + "-A")
        valid(B, n, tag + "-B")
        rep = V.replay(A, B, [(mo, x)])
        acc = rep["accesses"][0]
        step("E", "%s n=%d x=%d %s a=%d q=%d w=%d" %
             (tag, n, x, mo, acc["a"], acc["q"], acc["eps"]))
        rows.append({"n": n, "A": A, "B": B, "x": x, "mo": mo, "tag": tag})

    # A: n=11 range obstruction
    n = 11
    A11 = vr(range(1, n + 1))
    B11 = vl(range(1, n + 1))
    add(n, A11, B11, 1, "K", "A-rng11")

    # B: A-rooted/B-deep, x=1 (B=left vine), n=7..64
    for n in (7, 8, 9, 11, 16, 32, 64):
        B = vl(range(1, n + 1))
        A = [1, None, vr(range(2, n + 1))]
        add(n, A, B, 1, "K", "B-deep%d" % n)
    # B mirror x=n at n=11 (A rooted at n, B right-vine => n deepest)
    n = 11
    Bm = vr(range(1, n + 1))
    Am = [n, vl(range(1, n)), None]
    add(n, Am, Bm, n, "K", "B-deep11m")

    # C: twin-to-twin a=1 (x=7, root 1), n=9,11,16
    for n in (9, 11, 16):
        B = vr(range(1, n + 1))
        A = [1, None, [8, [7, vr(range(2, 7)), None], vr(range(9, n + 1))]]
        add(n, A, B, 7, "K", "C-tw%d" % n)

    # D: DELETE twins (same states, B frozen)
    add(11, A11, B11, 1, "D", "D-rng11")
    add(11, Am, Bm, 11, "D", "D-deep11m")
    for n in (7, 8, 9, 11, 16, 32, 64):
        B = vl(range(1, n + 1))
        A = [1, None, vr(range(2, n + 1))]
        add(n, A, B, 1, "D", "D-deep%d" % n)
    for n in (9, 11, 16):
        B = vr(range(1, n + 1))
        A = [1, None, [8, [7, vr(range(2, 7)), None], vr(range(9, n + 1))]]
        add(n, A, B, 7, "D", "D-tw%d" % n)
    # recharge + tw13 DELETE variants (n=7 indices from battery)
    Sh7 = O.shapes_of(list(range(1, 8)))
    add(7, Sh7[0], Sh7[243], 1, "D", "D-recharge")
    add(7, Sh7[0], Sh7[41], 3, "D", "D-tw13")

    # F: n=7 same-(dA,dB,nA,nB) different-omega search (precomputed shapes)
    n = 7
    info = {}
    for ia, s in enumerate(Sh7):
        dd = {}

        def go(nd, d):
            if nd is None:
                return
            dd[nd[0]] = d
            go(nd[1], d + 1)
            go(nd[2], d + 1)
        go(s, 0)

        def sub(nd, x):
            while nd is not None and nd[0] != x:
                nd = nd[1] if x < nd[0] else nd[2]
            ks = []

            def g(m):
                if m is None:
                    return
                ks.append(m[0])
                g(m[1])
                g(m[2])
            g(nd)
            return ks
        for x in range(1, n + 1):
            ks = sub(s, x)
            lo, hi = min(ks), max(ks)
            assert len(ks) == hi - lo + 1
            info[(ia, x)] = (dd[x], lo, hi, len(ks))

    def om(la, ra, lb, rb):
        vals = sorted(set((la, ra, lb, rb)))
        rk = {v: i for i, v in enumerate(vals)}
        return (rk[la], rk[ra], rk[lb], rk[rb])

    groups = defaultdict(list)
    for ia in range(len(Sh7)):
        for ib in range(len(Sh7)):
            for x in range(1, n + 1):
                da, la, ra, na = info[(ia, x)]
                db, lb, rb, nb = info[(ib, x)]
                groups[(x, da, db, na, nb)].append((ia, ib, om(la, ra, lb,
                                                             rb)))
    got = 0
    for key in sorted(groups):
        seen = {}
        for (ia, ib, o) in groups[key]:
            seen.setdefault(o, (ia, ib))
        if len(seen) > 1:
            o1, o2 = sorted(seen)[:2]
            for (ia, ib) in (seen[o1], seen[o2]):
                if got >= 40:
                    break
                add(n, Sh7[ia], Sh7[ib], key[0], "K", "F-ctl%d" % got)
                got += 1
            if got >= 40:
                break
    step("F", "controlled omega-split edges: %d" % got)

    Path(str(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "dual_mine" / "joint_grow.json")).write_text(
        json.dumps({"rows": rows, "count": len(rows)}, indent=1,
                   default=str), encoding="utf-8")
    step("S", "rows=%d saved joint_grow.json" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
