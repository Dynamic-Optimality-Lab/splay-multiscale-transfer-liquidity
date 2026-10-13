# Distinct-guard measurement: skeletons -> (prefix supplies p, hole-type counts r_J) canonical forms.
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S
from itertools import combinations
from collections import Counter

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'

def all_prefix_topologies():
    # depth<=2 rooted topologies as slot sets (7 slots) + which slots present
    out = []
    for bits in range(1, 1 << 7):
        if bits & 1:
            out.append(bits)
    return out

def inorder_slots(bits):
    order = [3, 1, 4, 0, 5, 2, 6]
    return sorted([s for s in range(7) if bits & (1 << s)], key=lambda s: order[s])

if __name__ == "__main__":
    tops = all_prefix_topologies()
    print("topologies=%d" % len(tops), flush=True)
    # S-placement: choose s S-ranks of 9 increasingly into inorder slots; rest anonymous
    # hole S-subsets FORCED by intervals (each hidden rank belongs to unique hole) -- for guard features
    # we need (p_i, r_J): p_i = visible fringe per gap; r_J needs hole intervals + S-subsets.
    # Simplify to decisive quantities: enumerate (topology, S-visible-set, hole-interval multiset) canonical guard keys.
    import math
    guardkeys = Counter()
    nskel = 0
    for b in tops:
        slots = [i for i in range(7) if b & (1 << i)]
        pres = inorder_slots(b)
        k = len(pres)
        # S-subsets of ranks placed increasingly: C(9,s) for s visible-S count... S visible count s ranges 0..min(k,9)
        for s in range(0, min(k, 9) + 1):
            for Svis in combinations(range(1, 10), s):
                # remaining 9-s hidden ranks distributed to holes FORCED by intervals:
                # hole intervals from visible order; hidden rank -> unique hole (approx by rank neighbors)
                # guard key: (visible S pattern, hole count multiset by interval class)
                # approximate hole classes: count holes + their rank-spans from visible sequence
                nskel += 1
                # canonical guard key: (tuple(sorted S ranks visible), #holes, topology)
                # (hole-type detail refines further; this is a LOWER bound on distinct guards)
                guardkeys[(tuple(sorted(Svis)), b)] += 1
    print("skeleton-placement combos=%d distinct-guard-keys=%d" % (nskel, len(guardkeys)), flush=True)
    # hole-type refinement: for each placement, hidden ranks partition into holes (forced) -> interval types
    # upper bound freshwater: placements already 16k; hole-type detail only splits further (more distinct)
    json.dump({"combos": nskel, "guardkeys": len(guardkeys)}, open(PDIR + "CC_GUARDKEY_COUNT.json", "w"), indent=1)
