# Realistic guard cost: folded (vacuous dropped) guards from real hole structures.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED')
from CC_dag import DAG
import itertools as it

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'

if __name__ == "__main__":
    dag = DAG(budget=4000000)
    sig = [dag.var('s%d' % i) for i in range(10)]
    subset = {}
    subset[()] = dag.const(0)
    for r in range(1, 11):
        for comb in it.combinations(range(10), r):
            prev = comb[:-1]
            subset[comb] = dag.add(subset[prev], sig[comb[-1]])
    rng = random.Random(777)
    marg = []
    nfold = []
    for t in range(400):
        # realistic hole structure: 0-8 holes, contiguous N(r), few needy
        R = rng.randint(0, 8)
        Nsets = []
        for _ in range(R):
            a = rng.randint(0, 9)
            b = rng.randint(a + 1, 10)
            Nsets.append(frozenset(range(a, b)))
        needy = set(rng.sample(range(R), rng.randint(0, R))) if R else []
        # thresholds c_I = |{r in needy: N(r) <= I}|
        n1 = len(dag.nodes)
        conds = []
        for mask in range(1 << 10):
            I = frozenset(i for i in range(10) if mask & (1 << i))
            c = sum(1 for r in needy if Nsets[r] <= I)
            if c == 0:
                continue  # folded (vacuous)
            conds.append(dag.cmp('ge', subset[tuple(sorted(I))], dag.const(c)))
        g = dag.const(1)
        for c in conds:
            g = dag.mk('and', (g, c))
        marg.append(len(dag.nodes) - n1)
        nfold.append(len(conds))
    import statistics as st
    print("guards=%d marginal mean=%.0f median=%.0f max=%d total=%d" % (
        len(marg), sum(marg) / len(marg), sorted(marg)[len(marg) // 2], max(marg), len(dag.nodes)), flush=True)
    print("conditions/guard mean=%.1f" % (sum(nfold) / len(nfold)), flush=True)
    # projection: 16384 placements (lower bound on distinct guards)
    proj = (sum(marg) / len(marg)) * 16384
    print("projected guard nodes for 16384 placements: %.0f (cap 4000000)" % proj, flush=True)
    json.dump({"guards": len(marg), "mean": sum(marg) / len(marg),
               "median": sorted(marg)[len(marg) // 2], "max": max(marg),
               "conds_mean": sum(nfold) / len(nfold), "total": len(dag.nodes),
               "projection_16384": proj}, open(PDIR + "CC_GUARD_COST2.json", "w"), indent=1)
