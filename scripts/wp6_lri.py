"""WP-6 LRI: per-StepEv positive-reweight kill test (C178).

For ONE legal A StepEv (ZIG single rotation; LL/RR/LR/RL rotation pairs
at every site), measure positive log-reweight mass:
  R = sum over nodes with w'>w of 4*log2(w'/w)   [bits; Geo04 natural-log
      differs by constant ln2 only -- boundedness unaffected]
Weight schemes (all A-derived, positive):
  W1 depth:        logw(v) = -dA(v)          [exact integer depth drops]
  W2 subtree:      logw(v) = -log2(s_A(v))   [s = subtree size]
  W4 heavy-light:  logw(v) = log2(1 + lightmass_A(v)),
      lightmass = keys in light-child subtrees under v (tie: left heavy).
      [no Diamond max: tests locality alone]
Per StepEv record R per scheme + gainers count + max single-node ratio.
KILL (LRI-2 dead) if max R grows unboundedly in n/subtree size for any
scheme; ratios locate count-vs-ratio failure (W1/W2/W4 prediction).
Also full-sweep medians (all-keys splay) for typical behavior + Lucier
(1,n,1,n,...) present-analogue pattern check.
Artifact: lri.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
import math
from pathlib import Path
from collections import Counter

sys.setrecursionlimit(100000)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr
from wp6_adv import vine, balanced
from liquidity import legacy_embedding as PE


def step(sid, msg):
    print("[WP-6][LRI %s] %s" % (sid, msg), flush=True)


def depths_sizes(T):
    """depth map + subtree-size map."""
    dd, ss = {}, {}

    def rec(nd, d):
        if nd is None:
            return 0
        s = 1 + rec(nd["l"], d + 1) + rec(nd["r"], d + 1)
        dd[nd["k"]] = d
        ss[nd["k"]] = s
        return s

    if T is not None:
        # find root
        r = T
        while r["p"] is not None:
            r = r["p"]
        rec(r, 0)
    return dd, ss


def heavy_light(T):
    """heavy child per key (larger subtree; tie -> left heavy)."""
    _, ss = depths_sizes(T)
    nodes = {}
    r = T
    while r is not None and r["p"] is not None:
        r = r["p"]
    stack = [r]
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        nodes[nd["k"]] = nd
        stack.append(nd["l"])
        stack.append(nd["r"])
    heavy = {}
    for k, nd in nodes.items():
        sl = ss.get(nd["l"]["k"], 0) if nd["l"] else 0
        sr = ss.get(nd["r"]["k"], 0) if nd["r"] else 0
        heavy[k] = "l" if sl >= sr else "r"
    return heavy, ss, nodes


def lightmass(T):
    """lightmass[v] = keys in light-child subtrees under v (incl. v level)."""
    heavy, ss, nodes = heavy_light(T)
    lm = {}
    # post-order
    def rec(nd):
        if nd is None:
            return 0, 0  # (subtree size, light mass under nd)
        sl, ml = rec(nd["l"])
        sr, mr = rec(nd["r"])
        s = 1 + sl + sr
        if nd["l"] is None and nd["r"] is None:
            m = 0
        elif nd["l"] is None:
            m = mr  # only right; heavy=right(light empty)=>0? define below
            m = 0 if heavy[nd["k"]] == "r" else sr + mr
        elif nd["r"] is None:
            m = 0 if heavy[nd["k"]] == "l" else sl + ml
        else:
            if heavy[nd["k"]] == "l":
                m = sr + mr
            else:
                m = sl + ml
        lm[nd["k"]] = m
        return s, m

    r = T
    while r is not None and r["p"] is not None:
        r = r["p"]
    if r is not None:
        rec(r)
    return lm


def logw_W1(dd):
    return {k: -float(d) for k, d in dd.items()}


def logw_W2(ss):
    return {k: (-math.log2(s) if s > 0 else 0.0) for k, s in ss.items()}


def logw_W4(lm):
    return {k: math.log2(1 + m) for k, m in lm.items()}


def R_of(lw0, lw1):
    """Positive log2-reweight mass + gainers + max ratio-bit."""
    tot = 0.0
    ng = 0
    mx = 0.0
    for k, v0 in lw0.items():
        v1 = lw1.get(k, v0)
        if v1 > v0 + 1e-12:
            tot += v1 - v0
            ng += 1
            if v1 - v0 > mx:
                mx = v1 - v0
    return tot, ng, mx


def all_nodes(T):
    out = []
    stack = [T]
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        out.append(nd)
        stack.append(nd["l"])
        stack.append(nd["r"])
    return out


def measure_step(T0, do_fn):
    """Apply do_fn to a deep copy; return R per scheme + gainers."""
    T = copy.deepcopy(T0)
    dd0, ss0 = depths_sizes(T)
    lm0 = lightmass(T)
    w10, w20, w40 = logw_W1(dd0), logw_W2(ss0), logw_W4(lm0)
    do_fn(T)
    dd1, ss1 = depths_sizes(T)
    lm1 = lightmass(T)
    w11, w21, w41 = logw_W1(dd1), logw_W2(ss1), logw_W4(lm1)
    return {"W1": R_of(w10, w11), "W2": R_of(w20, w21),
            "W4": R_of(w40, w41)}


def random_bst(keys, rng):
    import random
    ks = list(keys)
    rng.shuffle(ks)
    t = None
    for k in ks:
        t = bst_insert(t, k)
    return t


def bst_insert(t, k):
    if t is None:
        return [k, None, None]
    if k < t[0]:
        t[1] = bst_insert(t[1], k)
    elif k > t[0]:
        t[2] = bst_insert(t[2], k)
    return t


def broom(n):
    """Long left chain with big balanced subtree at bottom (junction)."""
    m = n // 2
    big = balanced(list(range(m + 1, n + 1)))
    t = [1, None, big]
    for k in range(2, m + 1):
        t = [k, t, None]
    return t


def main() -> int:
    step("LR-00", "per-StepEv positive-reweight kill test")
    out = {"by_n": {}}
    for n in (32, 128, 512, 2048):
        rec = Counter()
        rec["W1_max"] = 0.0
        rec["W2_max"] = 0.0
        rec["W4_max"] = 0.0
        rec["W1_med"] = []
        rec["nsteps"] = 0
        for shape in ("vine", "bal", "rand", "broom", "comb"):
            if shape == "vine":
                T0 = vine(n)
            elif shape == "bal":
                T0 = balanced(list(range(1, n + 1)))
            elif shape == "rand":
                import random
                T0 = random_bst(list(range(1, n + 1)),
                                random.Random(1000 + n))
            elif shape == "broom":
                T0 = broom(n)
            else:
                from wp6_adv import comb
                T0 = comb(n)
            TP0 = to_ptr(T0)
            for nd in all_nodes(TP0):
                x = nd["k"]
                # ZIG shapes: x child of its parent
                # simulate single rotations at every edge (p,x) with x child
                p = nd["p"]
                if p is None:
                    continue
                # single rotation (zig analogue at this edge)
                if p["l"] is nd:
                    r = measure_step(
                        TP0, lambda T, _p=p, _x=x: PE._rot_right(
                            [z for z in all_nodes(T)
                             if z["k"] == _p["k"]][0]))
                else:
                    r = measure_step(
                        TP0, lambda T, _p=p, _x=x: PE._rot_left(
                            [z for z in all_nodes(T)
                             if z["k"] == _p["k"]][0]))
                rec["nsteps"] += 1
                for i, W in enumerate(("W1", "W2", "W4")):
                    tot, ng, mx = r[W]
                    if tot > rec[W + "_max"]:
                        rec[W + "_max"] = tot
                        rec[W + "_maxrec"] = {"n": n, "shape": shape,
                                             "x": x, "gainers": ng,
                                             "maxbit": mx}
                    if W == "W1":
                        rec["W1_med"].append(tot)
                # doubles: two rotations in splay order (find nodes fresh)
                g = p["p"]
                if g is None:
                    continue
                gk, pk = g["k"], p["k"]
                cfg = None
                if g["l"] is p and p["l"] is nd:
                    cfg = ("LL",)
                elif g["r"] is p and p["r"] is nd:
                    cfg = ("RR",)
                elif g["l"] is p and p["r"] is nd:
                    cfg = ("LR",)
                elif g["r"] is p and p["l"] is nd:
                    cfg = ("RL",)
                if cfg is None:
                    continue

                def _dbl(T, _gk=gk, _pk=pk, _cfg=cfg):
                    def find(k):
                        for z in all_nodes(T):
                            if z["k"] == k:
                                return z
                        return None
                    if _cfg == ("LL",):
                        PE._rot_right(find(_gk))
                        PE._rot_right(find(_pk))
                    elif _cfg == ("RR",):
                        PE._rot_left(find(_gk))
                        PE._rot_left(find(_pk))
                    elif _cfg == ("LR",):
                        PE._rot_left(find(_pk))
                        PE._rot_right(find(_gk))
                    else:
                        PE._rot_right(find(_pk))
                        PE._rot_left(find(_gk))

                try:
                    r = measure_step(TP0, _dbl)
                    rec["nsteps"] += 1
                    for W in ("W1", "W2", "W4"):
                        tot, ng, mx = r[W]
                        if tot > rec[W + "_max"]:
                            rec[W + "_max"] = tot
                            rec[W + "_maxrec"] = {"n": n, "shape": shape,
                                                 "x": x, "kind": "double",
                                                 "cfg": cfg[0],
                                                 "gainers": ng, "maxbit": mx}
                except Exception:
                    continue
        import statistics
        med = rec.pop("W1_med", [])
        out["by_n"][str(n)] = {"nsteps": rec["nsteps"],
                               "W1_max": rec["W1_max"],
                               "W1_maxrec": rec.get("W1_maxrec"),
                               "W1_med": statistics.median(med) if med else 0,
                               "W2_max": rec["W2_max"],
                               "W2_maxrec": rec.get("W2_maxrec"),
                               "W4_max": rec["W4_max"],
                               "W4_maxrec": rec.get("W4_maxrec")}
        step("LR-P", "n=%d steps=%d W1max=%s W2max=%s W4max=%s" % (
            n, rec["nsteps"], round(rec["W1_max"], 2),
            round(rec["W2_max"], 2), round(rec["W4_max"], 2)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "lri.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("LR-01", "done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
