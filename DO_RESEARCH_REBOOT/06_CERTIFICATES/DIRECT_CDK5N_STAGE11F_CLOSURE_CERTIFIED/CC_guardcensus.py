# Decisive guard census: per-placement (p-vector, r_J hole-type multiset) distinct count.
import sys, json
sys.path.insert(0, 'python/independent')
from itertools import combinations

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
order = [3, 1, 4, 0, 5, 2, 6]
depth = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
children = {0: (1, 2), 1: (3, 4), 2: (5, 6)}

def analyze(bits, Svis):
    # Svis: dict slot -> S rank (increasing in inorder); other present slots anonymous.
    # Returns (p_tuple(10), rJ_tuple(sorted interval types), holes_detail) or None if infeasible.
    present = set(i for i in range(7) if bits & (1 << i))
    pres_in = sorted(present, key=lambda s: order[s])
    # visible sequence with labels: (slot, kind, rank-or-None); ranks: S ranks for S slots, None for anon
    # inorder key order positions: assign order indices
    # holes: absent children (depth<2 slots) + depth-3 children of depth-2 present slots
    holes = []  # (lo_desc, hi_desc, Ssub(set of ranks))
    # rank bounds: represent bounds as ('S', rank) / ('B', beta_index) / ('MIN',) / ('MAX',)
    # beta indices by inorder among anonymous visible
    anos = [s for s in pres_in if s not in Svis]
    beta = {s: i for i, s in enumerate(anos)}
    def desc(s):
        if s in Svis:
            return ('S', Svis[s])
        return ('F', beta[s])
    # walk to find holes with neighbor descriptors
    # neighbor tracking: inorder predecessor/successor visible keys
    vislist = [(s, desc(s)) for s in pres_in]
    holes = []
    # absent children
    for s in present:
        if depth[s] >= 2:
            continue
        for c in children[s]:
            if c in present:
                continue
            # hole at absent slot c: bounds = nearest visible inorder neighbors
            ic = order[c]
            # find predecessor/successor among pres_in by inorder
            pred = [t for t in pres_in if order[t] < ic]
            succ = [t for t in pres_in if order[t] > ic]
            lo = desc(pred[-1]) if pred else ('MIN',)
            hi = desc(succ[0]) if succ else ('MAX',)
            holes.append((('absent', c), lo, hi))
    # depth-3 children of present depth-2 slots
    for s in present:
        if depth[s] != 2:
            continue
        k = desc(s)
        # left hole bounds (parent-lo, k): parent-lo = nearest visible inorder predecessor of the left-subtree region...
        # approximate with slot's own inorder neighbors extended: use (pred_of_s_region, k) and (k, succ_of_s_region)
        # where region bounds come from s's parent chain: simpler: lo = desc of inorder predecessor slot (or MIN), hi likewise
        ip = order[s]
        pred = [t for t in pres_in if order[t] < ip]
        succ = [t for t in pres_in if order[t] > ip]
        # left hole: (pred_bound, k); right hole: (k, succ_bound); bounds as descriptors (conservative: use slot neighbors)
        plo = desc(pred[-1]) if pred else ('MIN',)
        phi = desc(succ[0]) if succ else ('MAX',)
        holes.append((('deep', s, 0), plo, k))
        holes.append((('deep', s, 1), k, phi))
    # S-subsets forced: hidden S ranks (1..9 not visible) each belong to the hole whose interval contains them.
    # rank r hidden: find hole with lo < S_r < hi in canonical rank order. lo/hi may be F/MIN/MAX descriptors:
    # resolve via order: build full canonical order line: MIN, then visible slots in inorder (S ranks + F slots), MAX.
    # A hidden rank s falls between consecutive visible S ranks => gap; hole containing gap-interval...
    # SIMPLIFICATION (sound for counting distinct guard features): assign hidden rank to holes whose descriptor
    # interval spans its gap, choosing deterministically the FIRST such hole in canonical order (forcedness check below).
    visranks = sorted(Svis.values())
    Ssub = {i: set() for i in range(len(holes))}
    for r in range(1, 10):
        if r in visranks:
            continue
        # find holes whose (lo,hi) strictly contains rank r (comparing via canonical order with F as wildcards handled by trying)
        cands = []
        for i, (_, lo, hi) in enumerate(holes):
            if _contains(lo, hi, r, visranks):
                cands.append(i)
        if len(cands) != 1:
            return None  # ambiguous/not-forced (excluded from this census; counted separately)
        Ssub[cands[0]].add(r)
    # gap-compatibility per hole + p vector + rJ
    p = [0] * 10
    for s in pres_in:
        if s not in Svis:
            # visible anonymous fringe: which gap? determined by neighboring S ranks (approx: rank position between S ranks)
            # use inorder rank-slot: count per gap via neighbor S ranks
            pass
    return holes, Ssub

def _contains(lo, hi, r, visranks):
    # lo/hi descriptors vs S rank r: True iff interval strictly contains rank r, treating F as opaque (return True only if forced)
    return False

if __name__ == "__main__":
    print("scaffold written; full census needs interval resolution -- see analysis", flush=True)
