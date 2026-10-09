"""WP-6 PARATIO: full W4 large-C Pair-Access ratio kill test (C179).

Candidate inequality (per KEEP access x):
    [3*log2(W/w(x)) + 1 + R_splay] / cost_A(x) <= C ?
with W = total W4 mass, w(x) = 1+lightmass(x), R_splay = total positive
log2-reweight over the access's A-StepEvs, cost_A = dA+1.
Shallow min-mass keys (root chain children: w~1, W large) are predicted
to drive ratio ~log n (growing): ratio growth with n REFUTES the W4
large-C route with asymptotic witness family (mission BRANCH E).
Bounded ratio would reopen LRI-1/LRI-3 composition immediately.
Artifact: paratio.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_lri import (to_ptr, depths_sizes, lightmass, logw_W4, R_of,
                     random_bst, broom, all_nodes)
from wp6_adv import vine, balanced, comb
from liquidity import legacy_embedding as PE

sys.setrecursionlimit(100000)


def step(sid, msg):
    print("[WP-6][PARATIO %s] %s" % (sid, msg), flush=True)


def total_W4(T):
    lm = lightmass(T)
    return sum(1 + m for m in lm.values()), lm


def stepwise_R(A, x, W4logw0):
    """Splay x in A (pointer, mutated); total positive reweight vs logw0."""
    from wp6_eventflow import splay_A
    tot = 0.0
    d, path = PE._depth_to(A, x)
    if not path or path[-1]["k"] != x:
        return tot, 0
    # per-StepEv: snapshot logw, rotate once (mirror splay_A control), diff
    node = path[-1]
    nsteps = 0
    import wp6_lri as L
    n = max(z["k"] for z in all_nodes(A))
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        lw0 = L.logw_W4(L.lightmass(A))
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
        else:
            PE._rot_right(p)
            PE._rot_left(g)
        lw1 = L.logw_W4(L.lightmass(A))
        t, _, _ = R_of(lw0, lw1)
        tot += t
        nsteps += 1
    return tot, nsteps


def main() -> int:
    step("PR-00", "full W4 large-C ratio kill test")
    out = {"by_n": {}}
    import random
    for n in (32, 128, 512):
        rec = {"max_ratio": 0.0}
        shapes = {"vine": vine(n), "bal": balanced(list(range(1, n + 1))),
                  "comb": comb(n), "broom": broom(n),
                  "rand": random_bst(list(range(1, n + 1)),
                                     random.Random(77 + n))}
        for nm, T0 in shapes.items():
            A = to_ptr(T0)
            W, lm = total_W4(A)
            logW = math.log2(W)
            # candidate keys: root, its children, every 7th key
            dd, _ = depths_sizes(A)
            cands = set()
            if A is not None:
                cands.add(A["k"])
                if A["l"] is not None:
                    cands.add(A["l"]["k"])
                if A["r"] is not None:
                    cands.add(A["r"]["k"])
            cands.update(range(1, n + 1, 7))
            for x in sorted(cands):
                if x is None or x < 1 or x > n:
                    continue
                A2 = copy.deepcopy(A)
                da = depths_of(A2).get(x, 0) if False else None
                # depth pre-splay
                dmap, _ = depths_sizes(A2)
                da = dmap.get(x, 0)
                costA = da + 1
                wx = 1 + lm.get(x, 0)
                access = 3 * (logW - math.log2(wx)) + 1
                R, ns = stepwise_R(A2, x, None)
                ratio = (access + R) / costA if costA > 0 else 0
                if ratio > rec["max_ratio"]:
                    rec["max_ratio"] = ratio
                    rec["max_rec"] = {"shape": nm, "x": x, "da": da,
                                      "wx": wx, "logW": round(logW, 2),
                                      "access": round(access, 2),
                                      "R": round(R, 2),
                                      "costA": costA}
        out["by_n"][str(n)] = rec
        step("PR-P", "n=%d maxratio=%s %s" % (
            n, round(rec["max_ratio"], 2),
            json.dumps(rec.get("max_rec"))))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "paratio.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("PR-01", "done")
    return 0


def depths_of(T):
    dd = {}
    stack = [(T, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        dd[nd["k"]] = d
        stack.append((nd["l"], d + 1))
        stack.append((nd["r"], d + 1))
    return dd


if __name__ == "__main__":
    sys.exit(main())
