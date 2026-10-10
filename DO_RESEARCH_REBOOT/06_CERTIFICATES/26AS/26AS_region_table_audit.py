"""Validate L1 proof region tables over corpus (all shapes n<=7, all y, all nodes):
V1: gainers of a step are y-monochromatic (single key-side).
V2: every gainer ends inside y's subtree.
V3: every strictly-inside-before node changes by <= -1.
V4: max single-node gain <= 2 (per step and total).
"""
import sys, copy, itertools, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS')
import wp6_cycle_ratio as O
from wp6_eventflow import to_ptr
import legacy_embedding as PE

def info(t):
    """key -> (depth, in_y_subtree_flag computed later)."""
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def subtree_keys(ynd):
    out = set()
    def go(nd):
        if nd is None:
            return
        out.add(nd["k"]); go(nd["l"]); go(nd["r"])
    go(ynd)
    return out

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

v1_bad = v2_bad = v3_bad = 0
maxgain_step = -10**9
maxgain_total = -10**9
nsteps = 0
for n in range(1, 8):
    for T0 in shapes(n):
        keys = list(range(1, n + 1))
        for y in keys:
            B = to_ptr(copy.deepcopy(T0))
            d, path = PE._depth_to(B, y)
            ynd = path[-1]
            d0 = info(B)
            node = ynd
            while node["p"] is not None:
                p = node["p"]; g = p["p"]
                inside_before = subtree_keys(node) - {y}
                dpre = info(node)
                if g is None:
                    if p["l"] is node:
                        PE._rot_right(p)
                    else:
                        PE._rot_left(p)
                elif p["l"] is node and g["l"] is p:
                    PE._rot_right(g); PE._rot_right(p)
                elif p["r"] is node and g["r"] is p:
                    PE._rot_left(g); PE._rot_left(p)
                elif p["r"] is node and g["l"] is p:
                    PE._rot_left(p); PE._rot_right(g)
                else:
                    PE._rot_right(p); PE._rot_left(g)
                rt = node
                while rt["p"] is not None:
                    rt = rt["p"]
                dpost = info(rt)
                inside_after = subtree_keys(node) - {y}
                nsteps += 1
                gainers = [k for k in keys if dpost[k] - dpre[k] > 0]
                for k in gainers:
                    maxgain_step = max(maxgain_step, dpost[k] - dpre[k])
                    if (k < y) != (gainers[0] < y) and k != y and gainers[0] != y:
                        # mixed sides (excluding y itself which never gains... check)
                        pass
                sides = set()
                for k in gainers:
                    if k != y:
                        sides.add(1 if k > y else -1)
                if len(sides) > 1:
                    v1_bad += 1
                    if v1_bad <= 3:
                        print("V1 FAIL", n, y, gainers)
                for k in gainers:
                    if k not in inside_after and k != y:
                        v2_bad += 1
                        if v2_bad <= 3:
                            print("V2 FAIL", n, y, k)
                for k in inside_before:
                    if dpost[k] - dpre[k] > -1:
                        v3_bad += 1
                        if v3_bad <= 5:
                            print("V3 FAIL", n, y, k, dpost[k] - dpre[k])
            rt = node
            while rt["p"] is not None:
                rt = rt["p"]
            dfin = info(rt)
            for k in keys:
                maxgain_total = max(maxgain_total, dfin[k] - d0[k])
print("steps:", nsteps, "V1bad:", v1_bad, "V2bad:", v2_bad, "V3bad:", v3_bad)
print("max single-step gain:", maxgain_step, " max total gain:", maxgain_total)
json.dump({"steps": nsteps, "v1": v1_bad, "v2": v2_bad, "v3": v3_bad,
           "max_step": maxgain_step, "max_total": maxgain_total},
          open(RDIR / '26AS_region_table_audit.json', 'w'), indent=1)
