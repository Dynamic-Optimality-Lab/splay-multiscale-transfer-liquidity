"""Probe the (ii)/(iii) threat: s gains +2 at step k_s, r gains +1 later.
Own bottom-up splay (mirrors wp6_eventflow rotation cases) with per-STEP
pair-depth capture. Exhaustive n<=7."""
import sys, copy, itertools, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS')
import wp6_cycle_ratio as O
from wp6_eventflow import to_ptr
import legacy_embedding as PE

def pdepths(t):
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

def splay_steps(B, y, r, s):
    """Returns list of (dr, ds) after each step (double/single op)."""
    d, path = PE._depth_to(B, y)
    node = path[-1]
    traj = []
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            tag = 'zig'
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
        elif p["l"] is node and g["l"] is p:
            tag = 'LL'
            PE._rot_right(g); PE._rot_right(p)
        elif p["r"] is node and g["r"] is p:
            tag = 'RR'
            PE._rot_left(g); PE._rot_left(p)
        elif p["r"] is node and g["l"] is p:
            tag = 'RL'
            PE._rot_left(p); PE._rot_right(g)
        else:
            tag = 'LR'
            PE._rot_right(p); PE._rot_left(g)
        dd = pdepths(node)
        # find root for full depths
        rt = node
        while rt["p"] is not None:
            rt = rt["p"]
        dd = pdepths(rt)
        traj.append((tag, dd[r], dd[s]))
    while node["p"] is not None:
        node = node["p"]
    return traj, node

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

threat_hits = []
maxsum = -10**9
nsteps_max = 0
for n in range(1, 8):
    for T0 in shapes(n):
        keys = list(range(1, n + 1))
        for y in keys:
            for r, s in itertools.combinations([k for k in keys if k != y], 2):
                if not (r < y < s):
                    continue
                B = to_ptr(copy.deepcopy(T0))
                d0 = pdepths(B)
                traj, _ = splay_steps(B, y, r, s)
                nsteps_max = max(nsteps_max, len(traj))
                seq = [(t, dr - d0[r], ds - d0[s]) for (t, dr, ds) in traj]
                tot = seq[-1][1] + seq[-1][2] if seq else 0
                maxsum = max(maxsum, tot)
                # threat: s-step-gain==+2 at some step, r later gain +1
                cumr = [p[1] for p in seq]
                cums = [p[2] for p in seq]
                for i in range(len(seq)):
                    dr_i = cumr[i] - (cumr[i - 1] if i else 0)
                    ds_i = cums[i] - (cums[i - 1] if i else 0)
                    if ds_i == 2:
                        for j in range(i + 1, len(seq)):
                            dr_j = cumr[j] - cumr[j - 1]
                            if dr_j >= 1:
                                threat_hits.append(
                                    {"n": n, "y": y, "r": r, "s": s,
                                     "seq": seq})
                                break
                        break
print("max steps:", nsteps_max, " max total:", maxsum)
print("threat (s+2 then r+1 later) occurrences:", len(threat_hits))
for h in threat_hits[:5]:
    print(h)
json.dump({"threats": len(threat_hits), "examples": threat_hits[:5]},
          open(RDIR / '26AS_threat_probe.json', 'w'), indent=1)
