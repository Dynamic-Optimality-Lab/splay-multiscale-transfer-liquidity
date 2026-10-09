"""PIVOT-25R-T §10: common-refinement motion on hard vs easy doubles.

Laminar families (all subtree intervals) of A and B -> common refinement
pieces. Per double: per-piece B-depth displacement + A-depth profile.
Question: do hard doubles move pieces characteristically?
Hard accesses (indexed) vs fresh easy doubles (matched orientation).
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

LOGP = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/trrefine.log")


def step(sid, msg):
    line = "[TRF %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        with open(LOGP, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def lamfam(t):
    out = set()

    def go(nd):
        if nd is None:
            return (None, None)
        l = go(nd[1])
        r = go(nd[2])
        lo = nd[0] if l[0] is None else l[0]
        hi = nd[0] if r[1] is None else r[1]
        out.add((lo, hi))
        return (lo, hi)
    go(t)
    return out


def pieces_of(fa, fb, n):
    bounds = {1, n + 1}
    for (a, b) in fa | fb:
        bounds.add(a)
        if b + 1 <= n:
            bounds.add(b + 1)
    bounds = sorted(bounds)
    return [(bounds[i], bounds[i + 1] - 1) for i in range(len(bounds) - 1)]


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


def reroot(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return r


def find(P, key):
    P = reroot(P)
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


def ptr_to_list(P):
    r = P
    if r is not None:
        while r["p"] is not None:
            r = r["p"]

    def go(m):
        if m is None:
            return None
        return [m["k"], go(m["l"]), go(m["r"])]
    return go(r)


def main():
    import wp6_cycle_ratio as O
    import liquidity.legacy_embedding as PE
    Sh7 = O.shapes_of(list(range(1, 8)))
    Sh8 = O.shapes_of(list(range(1, 9)))
    Sh6 = O.shapes_of(list(range(1, 7)))
    jobs = [("H-L4c", Sh8[255], Sh8[2], 8, 8), ("H-L4d", Sh8[1001],
            Sh8[1359], 1, 8), ("H-D2", Sh6[0], Sh6[74], 1, 6),
            ("H-L2a", Sh8[457], Sh8[429], 8, 8),
            ("E-vine7", Sh7[0], Sh7[0], 7, 7),
            ("E-vine8", Sh8[0], Sh8[0], 8, 8)]
    recs = []
    for (tag, A0, B0, x, n) in jobs:
        step("J", "start %s x=%d" % (tag, x))
        A = V.to_ptr(copy.deepcopy(A0))
        B = V.to_ptr(copy.deepcopy(B0))
        A, _ = V.splay_cap(A, x, 0, [])
        nd = find(B, x)
        while nd["p"] is not None:
            p = nd["p"]
            g = p["p"]
            if g is None:
                break
            if p["l"] is nd and g["l"] is p:
                pat = "LL"
            elif p["r"] is nd and g["r"] is p:
                pat = "RR"
            elif p["r"] is nd and g["l"] is p:
                pat = "LR"
            else:
                pat = "RL"
            LA, LB = ptr_to_list(A), ptr_to_list(B)
            pcs = pieces_of(lamfam(LA), lamfam(LB), n)
            da, db = depths_list(LA), depths_list(LB)
            rA = [k for k, v in da.items() if v == 0][0]
            tw0 = 1 if rA == [k for k, v in db.items() if v == 0][0] \
                else 0
            D0 = sum(db.values())
            if pat == "LL":
                PE._rot_right(g)
                PE._rot_right(p)
            elif pat == "RR":
                PE._rot_left(g)
                PE._rot_left(p)
            elif pat == "LR":
                PE._rot_left(p)
                PE._rot_right(g)
            else:
                PE._rot_right(p)
                PE._rot_left(g)
            B = reroot(B)
            LB2 = ptr_to_list(B)
            db2 = depths_list(LB2)
            tw1 = 1 if rA == [k for k, v in db2.items() if v == 0][0] \
                else 0
            D1 = sum(db2.values())
            mv = []
            for (lo, hi) in pcs:
                ks = list(range(lo, hi + 1))
                d0 = sum(db[y] for y in ks) / len(ks)
                d1 = sum(db2[y] for y in ks) / len(ks)
                a0 = sum(da[y] for y in ks) / len(ks)
                mv.append({"r": [lo, hi], "sz": len(ks),
                           "dd": round(d1 - d0, 3), "ad": round(a0, 3)})
            mv.sort(key=lambda m: -m["dd"])
            recs.append({"tag": tag, "pat": pat, "x": x,
                         "tw": 2 * (tw1 - tw0), "db": D0 - D1,
                         "pay": 2 * (tw1 - tw0) + D0 - D1,
                         "npieces": len(pcs), "move": mv})
            nd = find(B, x)
        step("E", "%s %s pay=%d pieces=%d" %
             (tag, pat, recs[-1]["pay"], len(pcs)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "refine_motion.json").write_text(
        json.dumps(recs, indent=1, default=str), encoding="utf-8")
    for r in recs:
        print("[TRF %s %s tw=%d db=%d pay=%d pieces=%d]" %
              (r["tag"], r["pat"], r["tw"], r["db"], r["pay"], r["npieces"]))
        for m in r["move"][:7]:
            print("    range=%s sz=%d dB=%+g dA~%.2f" %
                  (m["r"], m["sz"], m["dd"], m["ad"]))
    step("S", "saved refine_motion.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
