# Pilot guard compiler: template schemata x H<=2 words -> guard DAG nodes (measured, capped).
# Scope: single mask (odd), signatures small ({0,1,2}^10 sample) + saturation spot checks.
import sys, json, time, itertools
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED')
sys.path.insert(0, 'python/independent')
import splay as S
from CC_dag import DAG

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
NODE_CAP = 4000000
T0 = time.time()

def shapes7():
    # all rooted topologies through depth 2 (slot presence patterns): 2^7-1 with root
    out = []
    for bits in range(1, 1 << 7):
        if bits & 1:
            out.append(bits)
    return out

def placements(bits):
    # inorder slot order for depth-2 tree: slots indexed [root,L,R,LL,LR,RL,RR] -> inorder [LL,L,LR,root,RL,R,RR]
    order = [3, 1, 4, 0, 5, 2, 6]
    present = [s for s in range(7) if bits & (1 << s)]
    pres_in = sorted(present, key=lambda s: order[s])
    # assign S-ranks (increasing subset) + anonymous rest; count assignments
    k = len(pres_in)
    n = 0
    for s in range(0, min(k, 9) + 1):
        # C(9,s) S-choices... but S must include... just count: placements bounded
        import math
        n += math.comb(9, s)
    return n

if __name__ == "__main__":
    tops = shapes7()
    print("topologies=%d" % len(tops), flush=True)
    tot_place = sum(placements(b) for b in tops)
    print("slot+S placements (ub, pre-interval-filter)=%d" % tot_place, flush=True)
    # hole counts per topology + S-subset distributions (upper bound compositions as before)
    import math
    depth = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
    tot_skel = 0
    for b in tops:
        slots = [i for i in range(7) if b & (1 << i)]
        nh = 0
        for s in slots:
            if depth[s] < 2:
                ch = [1, 2] if s == 0 else ([3, 4] if s == 1 else [5, 6])
                nh += sum(1 for c in ch if not (b & (1 << c)))
            else:
                nh += 2
        # placements for this topology (recompute exactly)
        order = [3, 1, 4, 0, 5, 2, 6]
        pres_in = sorted(slots, key=lambda s: order[s])
        k = len(pres_in)
        npl = sum(math.comb(9, s) for s in range(0, min(k, 9) + 1))
        # hole S-subset distributions over nh holes (compositions, interval-filter ignored => UB)
        tot_skel += npl  # (hole distributions multiply further; measured separately below)
    print("skeleton-placement UB=%d" % tot_skel, flush=True)
    # guard DAG cost model: per template = shared atoms (amortized ~0 marginal if shared) + template-specific AND-tree
    # measure: build shared subset-sum atoms once, then per-template guard assembly cost
    dag = DAG(budget=NODE_CAP)
    sig = [dag.var('s%d' % i) for i in range(10)]
    # all 1024 subset sums with sharing
    from functools import lru_cache
    subset_nodes = {}
    import itertools as it
    for r in range(11):
        for comb in it.combinations(range(10), r):
            if not comb:
                subset_nodes[comb] = dag.const(0)
            else:
                # incremental: sum(comb) = sum(comb[:-1]) + sig[comb[-1]] via sharing
                prev = comb[:-1]
                subset_nodes[comb] = dag.add(subset_nodes[prev], sig[comb[-1]])
    print("shared subset-sum nodes: %d (total dag %d)" % (len(subset_nodes), len(dag.nodes)), flush=True)
    # per-template marginal: 1024 threshold cmps (shared atoms: 1024 subsets x 256 thresholds -> shared pool) + AND tree
    # build the shared threshold-atom pool incrementally and count
    n_before = len(dag.nodes)
    for c in (0, 1, 2, 5):
        for comb in [tuple(range(10))]:
            dag.cmp('ge', subset_nodes[comb], dag.const(c))
    print("sample threshold atoms: total dag %d" % len(dag.nodes), flush=True)
    json.dump({"topologies": len(tops), "placements_ub": tot_place,
               "dag_probe_nodes": len(dag.nodes),
               "time": round(time.time() - T0, 1)},
              open(PDIR + "CC_PILOT_COUNT.json", "w"), indent=1)
