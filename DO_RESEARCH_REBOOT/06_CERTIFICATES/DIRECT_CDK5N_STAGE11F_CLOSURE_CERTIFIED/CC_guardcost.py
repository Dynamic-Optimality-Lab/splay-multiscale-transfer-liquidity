# Measured marginal guard cost: build real guards for sampled templates into shared DAG.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED')
from CC_dag import DAG

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
import itertools as it

if __name__ == "__main__":
    dag = DAG(budget=4000000)
    sig = [dag.var('s%d' % i) for i in range(10)]
    # shared subset sums over all 1024 subsets (incremental construction for max sharing)
    from functools import lru_cache
    subset = {}
    subset[()] = dag.const(0)
    # build by increasing size for maximal prefix sharing
    for r in range(1, 11):
        for comb in it.combinations(range(10), r):
            prev = comb[:-1]
            subset[comb] = dag.add(subset[prev], sig[comb[-1]])
    n0 = len(dag.nodes)
    print("shared subset-sum nodes for 1024 subsets: %d" % n0, flush=True)
    # per-template guard: AND over 1024 subset conditions (sum_I >= c_I) with template thresholds c_I
    rng = random.Random(31337)
    marg = []
    for t in range(120):
        # random template thresholds c_I in 0..255 (standing in for r_J-derived thresholds)
        n1 = len(dag.nodes)
        conds = []
        for mask in range(1 << 10):
            comb = tuple(i for i in range(10) if mask & (1 << i))
            c = rng.randint(0, 255)
            conds.append(dag.cmp('ge', subset[comb], dag.const(c)))
        g = dag.const(1)
        for c in conds:
            g = dag.mk('and', (g, c))
        marg.append(len(dag.nodes) - n1)
        if len(dag.nodes) >= 4000000:
            print("BUDGET HIT at template %d" % t, flush=True)
            break
    import statistics as st
    print("templates=%d marginal mean=%.0f median=%.0f max=%d total=%d" % (
        len(marg), sum(marg) / max(len(marg), 1),
        sorted(marg)[len(marg) // 2] if marg else 0, max(marg) if marg else 0, len(dag.nodes)), flush=True)
    # projection to 16384 placements (lower bound on distinct guards; hole detail only adds)
    proj = len(marg) and (sum(marg) / len(marg)) * 16384
    print("projected guard-AND nodes for 16384 placements: %.0f (cap 4000000)" % proj, flush=True)
    json.dump({"templates": len(marg), "mean": sum(marg) / max(len(marg), 1),
               "median": sorted(marg)[len(marg) // 2] if marg else 0,
               "max": max(marg) if marg else 0, "total": len(dag.nodes),
               "projection_16384": proj}, open(PDIR + "CC_GUARD_COST.json", "w"), indent=1)
