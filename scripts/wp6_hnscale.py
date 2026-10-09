"""PIVOT-25R-HN scale-up: X-collision statistics on random accesses n=9-11.

Streams doubles (no full records kept): per double X4-tuple + outcome.
Split discovery/held-out 70/30 by access hash. Reports occupancy and
ambiguity per descriptor level + smallest ambiguous witnesses.
"""
from __future__ import annotations
import sys
import copy
import json
import random
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_hnrec import state_of


def step(sid, msg):
    print("[HNS %s] %s" % (sid, msg), flush=True)


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


def do_double(Bptr, x):
    import liquidity.legacy_embedding as PE
    B = reroot(Bptr)
    nd = find(B, x)
    p = nd["p"]
    g = p["p"]
    if p["l"] is nd and g["l"] is p:
        PE._rot_right(g)
        PE._rot_right(p)
    elif p["r"] is nd and g["r"] is p:
        PE._rot_left(g)
        PE._rot_left(p)
    elif p["r"] is nd and g["l"] is p:
        PE._rot_left(p)
        PE._rot_right(g)
    else:
        PE._rot_right(p)
        PE._rot_left(g)
    return reroot(B)


def keyX(X, level):
    base = (X["pat"], X["L"], X["R"], X["U"], X["V"], X["tw"])
    fr = X["fr"]
    if level == "X3":
        return base
    if level == "X4":
        return base + (tuple(tuple(f) for f in fr), X["rem"])
    if level == "V1":
        return base + (tuple(t for (_, _, t) in fr),)
    if level == "V2":
        return base + (tuple(s for (_, s, _) in fr),)
    raise AssertionError(level)


def main():
    import wp6_cycle_ratio as O
    rng = random.Random(77)
    SH = {}
    for n in (9, 10, 11):
        SH[n] = O.shapes_of(list(range(1, n + 1)))
        step("S", "n=%d shapes=%d" % (n, len(SH[n])))
    stats = {}
    wit = {}
    N = {"n9": 6000, "n10": 6000, "n11": 4000}
    cnt = 0
    for n, total in (("n9", 6000), ("n10", 6000), ("n11", 4000)):
        nn = int(n[1:])
        Sh = SH[nn]
        for t in range(total):
            ia = rng.randrange(len(Sh))
            ib = rng.randrange(len(Sh))
            x = rng.randint(1, nn)
            held = (t % 10 >= 7)
            A = V.to_ptr(copy.deepcopy(Sh[ia]))
            B = V.to_ptr(copy.deepcopy(Sh[ib]))
            A, _ = V.splay_cap(A, x, 0, [])
            rA = reroot(A)["k"]
            tw = 1 if rA == reroot(B)["k"] else 0
            D0 = sum(V.depths_of(reroot(B)).values())
            while True:
                nd = find(B, x)
                if nd["p"] is None or nd["p"]["p"] is None:
                    break
                X = state_of(A, B, x)
                B = do_double(B, x)
                tw1 = 1 if rA == reroot(B)["k"] else 0
                D1 = sum(V.depths_of(reroot(B)).values())
                pay = 2 * (tw1 - tw) + (D0 - D1)
                nd2 = find(B, x)
                if nd2["p"] is None or nd2["p"]["p"] is None:
                    Xn = "END"
                else:
                    Xn = state_of(A, B, x)
                for lv in ("X3", "V1", "V2", "X4"):
                    k = (lv, keyX(X, lv))
                    st = stats.setdefault(k, {"n": 0, "out": set(),
                                              "held": held})
                    st["n"] += 1
                    st["held"] = st["held"] and held
                    Xn_k = Xn if Xn == "END" else keyX(Xn, "X4")
                    st["out"].add((pay, str(Xn_k)))
                    if len(st["out"]) == 2 and k not in wit and not held:
                        wit[k] = (nn, ia, ib, x)
                tw, D0 = tw1, D1
            cnt += 1
            if (cnt + 1) % 4000 == 0:
                step("G", "accesses=%d states=%d" % (cnt, len(stats)))
    step("G", "accesses=%d states=%d" % (cnt, len(stats)))
    for lv in ("X3", "V1", "V2", "X4"):
        sub = {k[1]: v for k, v in stats.items() if k[0] == lv}
        multi = sum(1 for v in sub.values() if v["n"] > 1)
        amb = sum(1 for v in sub.values()
                  if v["n"] > 1 and len(v["out"]) > 1)
        step(lv, "states=%d multi=%d amb=%d" % (len(sub), multi, amb))
    heldamb = sum(1 for k, v in stats.items()
                  if v["held"] and len(v["out"]) > 1)
    step("H", "held-out-only ambiguous states: %d" % heldamb)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "hnscale.json").write_text(
        json.dumps({"states": len(stats),
                    "witnesses": {str(k): v for k, v in
                                  list(wit.items())[:40]}},
                   indent=1, default=str), encoding="utf-8")
    step("S", "saved hnscale.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
