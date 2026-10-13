# Distinct threshold-vector census: per skeleton, full (p_i, r_J, hole intervals, S-subsets).
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S
from itertools import combinations
from collections import Counter

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'

def holes_of(bits, vis_ranks):
    # vis_ranks: dict slot -> S rank or None(anon). Returns holes with (interval as rank bounds, Ssub forced).
    # slot order/depth maps
    depth = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
    parent = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
    side = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1}  # 0=left,1=right
    present = set(i for i in range(7) if bits & (1 << i))
    # rank bounds per slot from visible order: inorder neighbors
    order = [3, 1, 4, 0, 5, 2, 6]
    # visible ranks in inorder
    vis_in = sorted([s for s in present], key=lambda s: order[s])
    holes = []
    # absent children of depth<2 present slots + children of depth-2 present slots
    for s in present:
        if depth[s] == 0:
            chs = [1, 2]
        elif depth[s] == 1:
            chs = [s * 2 + 1, s * 2 + 2] if s == 1 else [s * 2 - 1, s * 2]
            # slot children: L=2s+1? use explicit maps
            chs = {0: [1, 2], 1: [3, 4], 2: [5, 6]}[s]
        elif depth[s] == 2:
            # children are depth-3 hole roots: represent as two holes
            holes.append(('deep', s * 2 + 1 if s < 3 else s * 2 - 1 if False else None))
            continue
        else:
            continue
        for c in chs:
            if c not in present:
                holes.append(('absent', c))
    # depth-3 holes under present depth-2 slots
    for s in present:
        if depth[s] == 2:
            base = {3: (7, 8), 4: (9, 10), 5: (11, 12), 6: (13, 14)}[s]
            holes.append(('deep', base[0]))
            holes.append(('deep', base[1]))
    return holes

if __name__ == "__main__":
    # count (topology, visible-S-set) already 16384; refine by hole-interval-type multiset is heavy;
    # decisive cheaper metric: distinct (p-vector pattern class, hole-count) + hole S-subset forcedness.
    # Instead directly measure: for each skeleton, the threshold vector family is determined by
    # (hole intervals x S-subsets). Enumerate fully with forced S assignment.
    order = [3, 1, 4, 0, 5, 2, 6]
    total = 0
    # S-placement enumeration with forced hole assignment via rank intervals
    for bits in range(1, 1 << 7):
        if not (bits & 1):
            continue
        slots = [i for i in range(7) if bits & (1 << i)]
        pres = sorted(slots, key=lambda s: order[s])
        k = len(pres)
        for s in range(0, min(k, 9) + 1):
            import math
            total += math.comb(9, s)
    print("placement combos=%d" % total, flush=True)
    json.dump({"placement_combos": total}, open(PDIR + "CC_PLACE_COUNT.json", "w"), indent=1)
