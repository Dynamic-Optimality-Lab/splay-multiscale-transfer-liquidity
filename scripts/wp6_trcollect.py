"""PIVOT-25R-T §4-5: hard-double battery + random harvest with pay labels.

Each B double StepEv (A fixed, rooted at x): transport record (pre) +
twin/Db pre/post + attach deltas + pay label (hard iff twinDrop+DbDrop<1).
Saves dual_mine/transport_bank.json.
"""
from __future__ import annotations
import sys
import copy
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_transport import (record_double, do_step, find, keyset,
                           depth_of, ancestors)


def step(sid, msg):
    print("[TRC %s] %s" % (sid, msg), flush=True)


def totdepth_ptr(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return sum(V.depths_of(r).values())


def rootof(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return r["k"]


def harvest(A0, B0, x, mo, tag, out, cap=None):
    A = V.to_ptr(copy.deepcopy(A0))
    B = V.to_ptr(copy.deepcopy(B0))
    A, _ = V.splay_cap(A, x, 0, [])
    if mo == "K" and rootof(A) != x:
        return 0
    if mo == "D":
        return 0  # B-doubles only occur in KEEP
    n = 0
    while True:
        r = B
        while r["p"] is not None:
            r = r["p"]
        B = r
        nd = find(B, x)
        if nd["p"] is None:
            break
        p = nd["p"]
        g = p["p"]
        if g is None:
            do_step(B, x)  # zig: record-free (twin pays; separate)
            continue
        # B double: determine pattern first (mirror do_step logic)
        if p["l"] is nd and g["l"] is p:
            pat = "LL"
        elif p["r"] is nd and g["r"] is p:
            pat = "RR"
        elif p["r"] is nd and g["l"] is p:
            pat = "LR"
        else:
            pat = "RL"
        rA = rootof(A)
        rB0, D0 = rootof(B), totdepth_ptr(B)
        tw0 = 1 if rA == rB0 else 0
        rec = record_double(A, B, pat, x, p["k"], g["k"])
        do_step(B, x)
        rB1, D1 = rootof(B), totdepth_ptr(B)
        tw1 = 1 if rA == rB1 else 0
        rec["tw0"], rec["tw1"] = tw0, tw1
        rec["twinDrop"] = 2 * (tw1 - tw0)
        rec["DbDrop"] = D0 - D1
        rec["pay"] = rec["twinDrop"] + rec["DbDrop"]
        rec["hard"] = rec["pay"] < 1
        rec["tag"] = tag
        rec["acc"] = {"x": x}
        out.append(rec)
        n += 1
        if cap is not None and n >= cap:
            break
    return n


def main():
    import wp6_cycle_ratio as O
    Sh7 = O.shapes_of(list(range(1, 8)))
    Sh8 = O.shapes_of(list(range(1, 9)))
    Sh6 = O.shapes_of(list(range(1, 7)))
    ev = []
    hard = [(Sh8[255], Sh8[2], 8, "L4c"), (Sh8[1001], Sh8[1359], 1, "L4d"),
            (Sh6[0], Sh6[74], 1, "D2rho"),
            (Sh8[457], Sh8[429], 8, "L2a"), (Sh8[1091], Sh8[1003], 7, "L2b"),
            (Sh8[869], Sh8[910], 2, "L2c"), (Sh8[1093], Sh8[1003], 7, "L3b"),
            (Sh8[90], Sh8[2], 8, "L4a"), (Sh8[0], Sh8[89], 3, "TR8")]
    for (A, B, x, tag) in hard:
        harvest(A, B, x, "K", tag, ev)
    rng = random.Random(21)
    nH = sum(1 for e in ev if e["hard"])
    step("H", "hard-access doubles=%d hard=%d" % (len(ev), nH))
    # random harvest n=7/8
    while len(ev) < 650:
        n = 7 if rng.random() < 0.5 else 8
        Sh = Sh7 if n == 7 else Sh8
        A = Sh[rng.randrange(len(Sh))]
        B = Sh[rng.randrange(len(Sh))]
        x = rng.randint(1, n)
        harvest(A, B, x, "K", "rnd", ev)
    nH = sum(1 for e in ev if e["hard"])
    step("H", "total=%d hard=%d easy=%d" % (len(ev), nH, len(ev) - nH))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "transport_bank.json").write_text(
        json.dumps(ev, indent=1, default=str), encoding="utf-8")
    step("S", "saved transport_bank.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
