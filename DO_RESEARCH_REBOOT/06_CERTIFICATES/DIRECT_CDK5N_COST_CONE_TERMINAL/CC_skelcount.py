# Skeleton-space enumeration: rank-canonical A-shadows (topologies + S-placement + hole subsets).
import sys, json, itertools
sys.path.insert(0, 'python/independent')
import splay as S
from itertools import combinations

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'

def tops():
    # all rooted ordered topologies through depth 2 (7 slots: presence/absence, BST-intervals implicit later)
    # slot order: root; L,R; LL,LR,RL,RR. Each present/absent with BST feasibility checked at placement.
    out = []
    for bits in range(1 << 7):
        if not (bits & 1):
            continue
        out.append(bits)
    return out

def placements(bits):
    # assign S-ranks 1..9 subset + anonymous fringe to present slots, BST-ordered inorder
    slots = [i for i in range(7) if bits & (1 << i)]
    # inorder of slots in a depth-2 tree: LL,L,LR,root,RL,R,RR -> slot idx to inorder rank
    inorder = [3, 1, 4, 0, 5, 2, 6]
    present_inorder = sorted([s for s in slots], key=lambda s: inorder[s])
    k = len(present_inorder)
    res = []
    # choose s S-keys out of 9 (C(9,s)) placed in increasing inorder; rest anonymous (canonical b's)
    for s in range(0, min(k, 9) + 1):
        for Sset in combinations(range(1, 10), s):
            # anonymous count = k - s
            res.append((tuple(present_inorder), Sset))
    return res

if __name__ == "__main__":
    to = tops()
    print("topologies=%d" % len(to), flush=True)
    tot = 0
    per_top = {}
    for b in to:
        pl = placements(b)
        per_top[b] = len(pl)
        tot += len(pl)
    print("slot+S placements=%d" % tot, flush=True)
    # hole S-subsets: hidden S ranks partitioned into <=8 ordered holes (holes = absent-child positions at depth<=2 + depth-3 fringe)
    # hole positions: for each present slot at depth<2 with absent child, + each present depth-2 slot's 2 children
    # upper bound: for each placement, holes<=8, subsets = set partitions restricted -> use compositions of hidden ranks
    import math
    tot2 = 0
    for b in to:
        slots = [i for i in range(7) if b & (1 << i)]
        # depth of slot: 0,1,1,2,2,2,2
        depth = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
        nholes = 0
        for s in slots:
            if depth[s] < 2:
                for ch in ([1, 2] if s == 0 else ([3, 4] if s == 1 else [5, 6])):
                    if not (b & (1 << ch)):
                        nholes += 1
            else:
                nholes += 2
        # hidden-rank distributions: Sr starsowski: compositions of h hidden into nholes ordered nonnegative parts * rank choices
        # upper bound: sum over h=0..9 of C(9,h)*C(h+nholes-1,nholes-1)
        pl = placements(b)
        for _, Sset in pl:
            h = 9 - len(Sset)
            tot2 += math.comb(h + nholes - 1, nholes - 1) if nholes else (1 if h == 0 else 0)
    print("skeleton upper bound (slots+S+holesubsets)=%d" % tot2, flush=True)
    json.dump({"topologies": len(to), "placements": tot, "skeletons_ub": tot2}, open(PDIR + "CC_SKELETON_COUNT.json", "w"), indent=1)
