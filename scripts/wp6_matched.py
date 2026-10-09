"""PIVOT-25R-CAR §5/§7-9 v2: B-matched counterfactual collisions.

Match on FULL B-side (same B tree, x, y) + A-skeleton; vary ONE A aspect:
 H7: same A-path/hang-intervals/sizes/attachments, different internal shapes.
 MASSvsPOS: same sizes different attachments, and vice versa.
 YLOC: same everything except y-relation class.
 SUP: same support-mass-per-block vs different placement.
Outcome: C amount (then Dpost>0). Smallest collision per test.
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


def step(sid, msg):
    print("[MT2 %s] %s" % (sid, msg), flush=True)


def ptr_root(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return r


def find(P, key):
    P = ptr_root(P)
    stack = [P]
    while stack:
        nd = stack.pop()
        if nd["k"] == key:
            return nd
        if nd["l"] is not None:
            stack.append(nd["l"])
        if nd["r"] is not None:
            stack.append(nd["r"])
    return None


def sz(nd):
    if nd is None:
        return 0
    return 1 + sz(nd["l"]) + sz(nd["r"])


def shape_of_ptr(nd):
    if nd is None:
        return None
    return [shape_of_ptr(nd["l"]), shape_of_ptr(nd["r"])]


def apath(Ap, x):
    Ap = ptr_root(Ap)
    out = []
    nd = Ap
    while nd is not None and nd["k"] != x:
        out.append(nd["k"])
        nd = nd["l"] if x < nd["k"] else nd["r"]
    if nd is not None:
        out.append(nd["k"])
    return tuple(out)


def hangs(Ap, x):
    Ap = ptr_root(Ap)
    p = apath(Ap, x)
    out = []
    for i, pk in enumerate(p[:-1]):
        nd = find(Ap, pk)
        ch = p[i + 1]
        side = "L" if nd["l"] is not None and nd["l"]["k"] == ch else "R"
        other = nd["r"] if side == "L" else nd["l"]
        ook = [] if other is None else sorted([])

        def col(m):
            if m is None:
                return
            ook.append(m["k"])
            col(m["l"])
            col(m["r"])
        col(other)
        ook = sorted(ook)
        out.append((side, ook[0] if ook else None,
                    ook[-1] if ook else None, len(ook),
                    shape_of_ptr(other)))
    return tuple(out)


def main():
    import wp6_cycle_ratio as O
    evs = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                      "0909c74a" / "dual_mine" /
                      "carrier5.json").read_text())
    Sh = O.shapes_of(list(range(1, 6)))
    # attach A-geometry per event (ia from record)
    info = []
    for e in evs:
        A = V.to_ptr(copy.deepcopy(Sh[e["ia"]]))
        B = V.to_ptr(copy.deepcopy(Sh[e["ib"]]))
        x, y = e["x"], e["y"]
        ib = e["ib"]
        p = apath(A, x)
        h = hangs(A, x)
        # y-location class
        if y in p:
            yl = ("onpath", p.index(y))
        else:
            # which hanging block contains y (by interval)?
            loc = None
            for (side, lo, hi, s, sh) in h:
                if lo is not None and lo <= y <= hi:
                    loc = (side, lo, hi)
                    break
            yl = ("hang", loc) if loc else ("outside", None)
        info.append({"e": e, "path": p,
                     "hang_noshape": tuple((s[0], s[1], s[2], s[3])
                                           for s in h),
                     "hang_full": h, "yloc": yl, "ib": ib, "x": x,
                     "y": y})
    step("L", "annotated=%d" % len(info))
    # H7: same (B,x,y,path,hang-noshape) + different internal shapes?
    g7 = defaultdict(list)
    for d in info:
        g7[(d["ib"], d["e"]["x"], d["e"]["y"], d["path"],
            d["hang_noshape"])].append(d)
    var7 = [(k, v) for k, v in g7.items()
            if len(set(str(h) for d in v
                       for h in [d["hang_full"]])) > 1 or True]
    # check C uniformity within groups + shape variation present
    amb7 = tot7 = shpvar = 0
    for k, v in g7.items():
        if len(v) < 2:
            continue
        tot7 += 1
        shapes = set(str(d["hang_full"]) for d in v)
        if len(shapes) > 1:
            shpvar += 1
            if len(set(d["e"]["C"] for d in v)) > 1:
                amb7 += 1
    step("H7", "multi=%d shape-varying=%d C-ambiguous-among-those=%d" %
         (tot7, shpvar, amb7))
    # MASS vs POS: same intervals, subdivide by (masses-only) vs full
    # (mass=y-interval sizes already in hang_noshape; positions=sides+los)
    # YLOC necessity: same all-except-yloc -> C varies?
    gy = defaultdict(list)
    for d in info:
        A = V.to_ptr(copy.deepcopy(Sh[d["e"]["ia"]]))
        B = V.to_ptr(copy.deepcopy(Sh[d["e"]["ib"]]))
        gy[(d["ib"], d["e"]["x"], d["e"]["y"], d["path"],
            d["hang_noshape"])].append((d["yloc"], d["e"]["C"]))
    ylneed = sum(1 for v in gy.values() if len(v) > 1 and
                 len(set(c for _, c in v)) > 1 and
                 len(set(l for l, _ in v)) == 1)
    step("YL", "groups with C-varying but yloc-identical: %d" % ylneed)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "matched5.json").write_text(
        json.dumps([{"ib": d["ib"], "ia": d["e"]["ia"], "x": d["e"]["x"],
                     "y": d["e"]["y"],
                     "C": d["e"]["C"], "path": list(d["path"]),
                     "hang": [[[h[0], h[1], h[2], h[3]], h[4]]
                              for h in d["hang_full"]],
                     "yloc": [d["yloc"][0], list(d["yloc"][1])
                              if isinstance(d["yloc"][1], (list, tuple))
                              else d["yloc"][1]]} for d in info],
                   indent=0, default=str), encoding="utf-8")
    step("S", "saved matched5.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
