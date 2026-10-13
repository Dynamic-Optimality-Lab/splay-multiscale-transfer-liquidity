# Decisive guard census: skeletons w/ F-gap assignment -> hole analysis -> guard features -> distinct count.
import sys, json
sys.path.insert(0, 'python/independent')
from itertools import combinations
from collections import Counter

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
order = [3, 1, 4, 0, 5, 2, 6]
depth = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
children = {0: (1, 2), 1: (3, 4), 2: (5, 6)}

def hole_slots(bits):
    # returns list of holes: ('absent', slot) or ('deep', slot, side); each with inorder position info
    present = set(i for i in range(7) if bits & (1 << i))
    holes = []
    for s in present:
        if depth[s] >= 2:
            continue
        for c in children[s]:
            if c not in present:
                holes.append(('absent', c))
    for s in present:
        if depth[s] == 2:
            holes.append(('deep', s, 0))
            holes.append(('deep', s, 1))
    return holes

def gap_range_of_slot_seq(seq, idx):
    # seq: inorder list of ('S',rank) in increasing rank order... instead compute gap bounds from neighbors
    return None

if __name__ == "__main__":
    # Phase 1: enumerate (topology, Svis assignment) with F-gap assignment via neighbor constraints.
    # For each visible slot in inorder, label S (chosen ranks increasing) or F with gap = determined-or-choice.
    # Gap of an inorder position: (#S-ranks strictly before it) adjusted... precisely: with S ranks placed,
    # a position between consecutive S ranks r_a < r_b (in inorder, possibly with F slots between) lies in a
    # gap g with a <= g < b... ambiguous unless a+1==b. Branch over consistent gaps.
    total_skel = 0
    guardkeys = Counter()
    for bits in range(1, 1 << 7):
        if not (bits & 1):
            continue
        present = [i for i in range(7) if bits & (1 << i)]
        pres_in = sorted(present, key=lambda s: order[s])
        k = len(pres_in)
        # S-subsets placed increasingly: iterate over increasing rank assignments
        # ranks 1..9 into k positions (increasing): C(9+k-1... no: choose k distinct ranks increasingly: C(9,k) subsets, order forced
        from itertools import combinations as comb
        for Sset in comb(range(1, 10), min(k, 9)):
            # Sset assigned increasingly to a SUBSET of positions? No: exactly: choose which positions are S (C(k,s)) x rank values
            pass
    # Restructure: iterate (positions-of-S subset P of pres_in) x (increasing ranks Sset, |Sset|=|P|)
    nskel = 0
    for bits in range(1, 1 << 7):
        if not (bits & 1):
            continue
        present = [i for i in range(7) if bits & (1 << i)]
        pres_in = sorted(present, key=lambda s: order[s])
        k = len(pres_in)
        for nS in range(0, min(k, 9) + 1):
            for P in combinations(range(k), nS):
                for Sset in combinations(range(1, 10), nS):
                    # F slots = complement; each F slot's gap: between neighboring S ranks in inorder (maybe ambiguous range)
                    # compute gap-range (lo_gap, hi_gap) per F slot: lo = #S-ranks strictly before (in inorder), hi likewise after...
                    # gap g = #{S ranks < key}; key between S-order positions: lo_gap = S-ranks before, hi_gap = 9 - S-ranks after... precise:
                    # inorder S ranks (placed): ranks_before = #{r in Sset placed before slot}; then gap g satisfies ranks_before <= g <= ranks_before + (number of S ranks... )
                    # Simplest exact: gap-SEQUENCE consistent assignments: F slot between S_a and S_b (consecutive placed S in inorder, with sentinels 0/10) lies in gap g with a<=g<=b... using rank VALUES a=S_a,b=S_b: gap g means S_g < key < S_{g+1}; key between values a<b lies in gap g iff S_g <= a... precisely g in [a, b-1] intersect [0,9] where a,b are neighboring S VALUES (ranks).
                    nskel += 1
    print("skeleton slots+S placements (pre-gap-assignment, pre-hole-detail)=%d" % nskel, flush=True)
    json.dump({"combos": nskel}, open(PDIR + "CC_SKEL2_COUNT.json", "w"), indent=1)
