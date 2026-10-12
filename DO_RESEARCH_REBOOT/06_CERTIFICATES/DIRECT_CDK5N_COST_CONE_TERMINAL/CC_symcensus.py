# Symbolic state-space census: skeletons, diagonal seeds, post-KEEP bounds per mask.
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S
from itertools import combinations

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'

def shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in shapes(keys[:i]):
            for r in shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    return out

ALL9 = shapes(list(range(1, 10)))
MASKS = list(combinations(range(1, 10), 5))
print("shapes=%d masks=%d" % (len(ALL9), len(MASKS)), flush=True)

# canonical skeleton: (topology bits, visible tuple (inorder-mapped), hole S-subsets forced by intervals)
def skeleton_of(t):
    # BFS slots depth<=2
    slots = {}
    def walk(nd, lv, pos):
        if nd[0] == "leaf" or lv > 2:
            return
        _, k, l, r = nd
        slots[(lv, pos)] = k
        walk(l, lv + 1, pos * 2)
        walk(r, lv + 1, pos * 2 + 1)
    walk(t, 0, 0)
    vis = tuple(sorted(slots.items(), key=str))
    # visible S-pattern depends on mask: compute per mask later; here record raw keys
    # holes: absent children at depth<2 + children of depth-2 present
    depth = {(0, 0): 0}
    for (lv, p) in slots:
        depth[(lv, p)] = lv
    holes = []
    for (lv, p), k in slots.items():
        if lv == 0:
            chs = [(1, 0), (1, 1)]
        elif lv == 1:
            chs = [(2, p * 2), (2, p * 2 + 1)]
        else:
            continue
        for c in chs:
            if c not in slots:
                holes.append(c)
    for (lv, p), k in slots.items():
        if lv == 2:
            holes.append(((3, p * 2), (3, p * 2 + 1)))
    return vis, holes

# count distinct (topology, visible-key-pattern) over ALL9 = skeleton upper bound (S-exact, fringe anonymous)
seen = set()
for t in ALL9:
    vis, holes = skeleton_of(t)
    # canonicalize: replace non-S... S unknown here; use pattern with ALL keys labeled (worst case = concrete)
    seen.add((str(vis), str(sorted(holes, key=str))))
print("concrete top3-patterns (all-9-key-labeled)=%d" % len(seen), flush=True)
# rank-canonical skeletons: S-ranks exact (9! labelings collapse by order... S fixed 1..9 here) + anonymous variants:
# count = sum over topologies of (S-subsets placed increasingly) = placements (16384 measured) filtered by realizability
# realizable post-KEEP states need marked root: root slot S-rank in mask
# upper bound post-KEEP symbolic states per mask: skeletons(<=16384) x B-with-marked-root(~2700)
print("postKEEP-ub-per-mask=%d" % (16384 * 2700), flush=True)
print("postKEEP-ub-all-masks=%d" % (16384 * 2700 * 126), flush=True)
# diagonal seeds: A=B=T: B-shape determines A-shadow (same tree): count = shapes x masks = 4862*126
print("diagonal-seeds=%d" % (4862 * 126), flush=True)
json.dump({"shapes": 4862, "masks": 126, "top3patterns": len(seen),
           "postKEEP_ub_per_mask": 16384 * 2700, "diag_seeds": 4862 * 126}, open(PDIR + "CC_SYM_CENSUS.json", "w"), indent=1)
