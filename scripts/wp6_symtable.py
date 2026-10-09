"""PIVOT-25R-R §9: symbolic StepEv payment tables, engine-checked.

Per orientation, with arbitrary attached-subtree SIZES, total-depth change
and DbDrop = -(change). Recharge classification + minimal instances.
Formulas (pivots x,p,g; T1..T4 attached; s.=sizes):
  LL: DbDrop = +2s1+s2-s3-2s4   (T1=x.left,T2=x.right,T3=p.right,T4=g.right)
  RR: DbDrop = -2s1-s2+s3+2s4   (mirror: T1=g.left outer)
  LR: DbDrop = +1+s1+s2-s4      (T1=x.left,T2=x.right,T4=g.right)
  RL: mirror of LR.
  ZigR: DbDrop = s1-s3 (total w/ twin+2: 2+s1-s3); ZigL mirror.
Engine check: random steps, measured DbDrop vs formula.
"""
from __future__ import annotations
import sys
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[SPT %s] %s" % (sid, msg), flush=True)


def size(nd):
    if nd is None:
        return 0
    return 1 + size(nd["l"]) + size(nd["r"])


def totdepth(ptr):
    return sum(V.depths_of(ptr).values())


def totdepth_from(node):
    r = node
    while r["p"] is not None:
        r = r["p"]
    return totdepth(r)


def formula(pat, s1, s2, s3, s4):
    if pat == "LL":
        return 2 * s1 + s2 - s3 - 2 * s4
    if pat == "RR":
        return -2 * s1 - s2 + s3 + 2 * s4
    if pat in ("LR", "RL"):
        return 1 + s1 + s2 - s4
    if pat == "Z":
        return s1 - s3
    raise AssertionError(pat)


def main():
    import wp6_cycle_ratio as O
    import liquidity.legacy_embedding as PE
    n = 8
    Sh = O.shapes_of(list(range(1, n + 1)))
    rng = random.Random(9)
    chk = {"LL": [0, 0], "RR": [0, 0], "LR": [0, 0], "RL": [0, 0],
           "Z": [0, 0]}
    rech = {"LL": 0, "RR": 0, "LR": 0, "RL": 0, "Z": 0}
    worst = {}
    for t in range(400):
        P = V.to_ptr(copy.deepcopy(Sh[rng.randrange(len(Sh))]))
        x = rng.randint(1, n)
        d, path = PE._depth_to(P, x)
        if not path or path[-1]["k"] != x:
            continue
        node = path[-1]
        if node["p"] is None:
            continue
        p = node["p"]
        g = p["p"]
        D0 = totdepth_from(node)
        if g is None:
            pat = "Z"
            if p["l"] is node:
                s1, s3 = size(node["l"]), size(p["r"])
            else:
                # mirror: use s1=x.outer-opposite? record mirrored
                s1, s3 = size(node["r"]), size(p["l"])
            PE._rot_right(p) if p["l"] is node else PE._rot_left(p)
            pred = s1 - s3
        else:
            xk = node["k"]
            if p["l"] is node and g["l"] is p:
                pat = "LL"
                s1, s2, s3, s4 = (size(node["l"]), size(node["r"]),
                                  size(p["r"]), size(g["r"]))
                PE._rot_right(g)
                PE._rot_right(p)
            elif p["r"] is node and g["r"] is p:
                pat = "RR"
                s1, s2, s3, s4 = (size(g["l"]), size(p["l"]),
                                  size(node["l"]), size(node["r"]))
                PE._rot_left(g)
                PE._rot_left(p)
            elif p["r"] is node and g["l"] is p:
                pat = "LR"
                s1, s2, s3, s4 = (size(node["l"]), size(node["r"]),
                                  size(p["l"]), size(g["r"]))
                PE._rot_left(p)
                PE._rot_right(g)
            else:
                pat = "RL"
                s1, s2, s3, s4 = (size(node["r"]), size(node["l"]),
                                  size(p["r"]), size(g["l"]))
                PE._rot_right(p)
                PE._rot_left(g)
            pred = formula(pat, s1, s2, s3, s4)
        D1 = totdepth_from(node)
        got = D0 - D1
        chk[pat][1] += 1
        if got == pred:
            chk[pat][0] += 1
        else:
            if pat not in worst:
                worst[pat] = (s1, s2, s3, s4, pred, got)
        need = 1 if pat != "Z" else -2  # double needs drop>=1 (twin 0);
        # zig needs total>=0 i.e. DbDrop>=-2 given twin +2
        if got < need:
            rech[pat] += 1
    step("S", "formula agreement: %s" %
         {k: "%d/%d" % (v[0], v[1]) for k, v in chk.items()})
    step("S", "recharge/fail-to-pay counts: %s mismatches: %s" %
         (rech, worst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
