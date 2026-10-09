"""PIVOT-25R-CAR §5-11: counterfactual collision ladder + matched eliminations.

Levels (ascending; stop at singleton-noise floor):
 L0=(x,y); L1=+twin pre/post + B orientation word;
 L2=+A-path nodes (H1); L3a=+hanging masses (H2); L3b=+attachments (H3);
 L4=+y-location (H4); L5=+support placement (H5/H6).
H7/H8 via targeted matched pairs (same-everything-except-shapes/remote).
Outcome: C amount (then Dpost>0 check). Smallest collision per level.
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
    print("[ELM %s] %s" % (sid, msg), flush=True)


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


def main():
    import wp6_cycle_ratio as O
    evs = []
    for n in (5,):
        evs += json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                           "0909c74a" / "dual_mine" /
                           ("carrier%d.json" % n)).read_text())
    step("L", "events=%d" % len(evs))
    Sh = O.shapes_of(list(range(1, 6)))
    # feature cache per (ia,ib,x)
    feat = {}
    for e in evs:
        k = (e["ia"], e["ib"], e["x"])
        if k in feat:
            continue
        A = V.to_ptr(copy.deepcopy(Sh[e["ia"]]))
        B = V.to_ptr(copy.deepcopy(Sh[e["ib"]]))
        x = e["x"]
        # B orientation word + twin pre/post
        rep = V.replay(Sh[e["ia"]], Sh[e["ib"]], [("K", x)])
        acc = rep["accesses"][0]
        morate = tuple(s["pat"] if s["kind"] == "double" else "Z"
                       for s in acc["bsteps"])
        rA0 = ptr_root(A)["k"]
        rB0 = ptr_root(B)["k"]
        tw0 = 1 if rA0 == rB0 else 0
        A2 = V.to_ptr(copy.deepcopy(rep["endA"]))
        B2 = V.to_ptr(copy.deepcopy(rep["endB"]))
        tw1 = 1 if ptr_root(A2)["k"] == ptr_root(B2)["k"] else 0
        # A path nodes + hanging blocks (intervals/sizes/sides per level)
        Ap = V.to_ptr(copy.deepcopy(Sh[e["ia"]]))
        path = []
        nd = ptr_root(Ap)
        while nd is not None and nd["k"] != x:
            path.append(nd["k"])
            nd = nd["l"] if x < nd["k"] else nd["r"]
        path.append(x)
        hangs = []
        for i, pk in enumerate(path[:-1]):
            ndp = find(Ap, pk)
            ch = path[i + 1]
            side = "L" if ndp["l"] is not None and ndp["l"]["k"] == ch \
                else "R"
            other = ndp["r"] if side == "L" else ndp["l"]
            ook = [] if other is None else sorted([])

            def col(m):
                if m is None:
                    return
                ook.append(m["k"])
                col(m["l"])
                col(m["r"])
            col(other)
            ook = sorted(ook)
            hangs.append((side, ook[0] if ook else None,
                          ook[-1] if ook else None, len(ook)))
        feat[k] = {"word": morate, "tw": (tw0, tw1), "path": tuple(path),
                   "hangs": tuple(hangs)}
    step("F", "access features done")
    # y-location per event (needs y + A trees)
    def yloc(e):
        A = V.to_ptr(copy.deepcopy(Sh[e["ia"]]))
        x, y = e["x"], e["y"]
        # y on path?
        nd = ptr_root(A)
        onp = False
        m = nd
        while m is not None and m["k"] != x:
            if m["k"] == y:
                onp = True
            m = m["l"] if x < m["k"] else m["r"]
        if m is not None and m["k"] == y:
            onp = True
        return onp
    levels = ["L0", "L1", "L2", "L3a", "L3b", "L4"]
    for lv in levels:
        groups = defaultdict(list)
        for e in evs:
            f = feat[(e["ia"], e["ib"], e["x"])]
            if lv == "L0":
                k = (e["x"], e["y"])
            elif lv == "L1":
                k = (e["x"], e["y"], f["word"], f["tw"])
            elif lv == "L2":
                k = (e["x"], e["y"], f["word"], f["tw"], f["path"])
            elif lv == "L3a":
                k = (e["x"], e["y"], f["word"], f["tw"], f["path"],
                     tuple(sorted(h[3] for h in f["hangs"])))
            elif lv == "L3b":
                k = (e["x"], e["y"], f["word"], f["tw"], f["path"],
                     tuple((h[0], h[1], h[2], h[3]) for h in f["hangs"]))
            else:
                k = (e["x"], e["y"], f["word"], f["tw"], f["path"],
                     tuple((h[0], h[1], h[2], h[3]) for h in f["hangs"]),
                     yloc(e))
            groups[k].append(e["C"])
        amb = {k: v for k, v in groups.items() if len(set(v)) > 1}
        step(lv, "classes=%d amb=%d amb-ev=%d" %
             (len(groups), len(amb), sum(len(v) for v in amb.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
