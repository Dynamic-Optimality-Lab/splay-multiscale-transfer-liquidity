# Hall subset-inequality vs max-flow solver: equivalence fuzz (falsifies §8 if disagree).
# Also: 55-type contiguity check on random hole intervals.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
from AFSP_allocate import solve_allocation

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'

def hall_full(d, Nsets, R):
    # (A) nonnegative supplies; (B) positive-supply gap eligible; (C) subset inequalities
    if any(x < 0 for x in d):
        return False
    for i in range(10):
        if d[i] > 0 and not any(i in Nsets[r] for r in range(len(Nsets))):
            return False
    for mask in range(1 << 10):
        I = set(i for i in range(10) if mask & (1 << i))
        lhs = sum(d[i] for i in I)
        rhs = sum(1 for r in R if Nsets[r] and Nsets[r] <= I)
        if lhs < rhs:
            return False
    return True

if __name__ == "__main__":
    rng = random.Random(2024)
    dis = 0
    tot = 0
    contig_bad = 0
    ntypes = set()
    for trial in range(600):
        R = rng.randint(1, 8)
        # random CONTIGUOUS gap sets (interval model) + occasionally noncontiguous (must be caught)
        Nsets = []
        for r in range(R):
            if rng.random() < 0.85:
                a = rng.randint(0, 9)
                b = rng.randint(a + 1, 10)
                Nsets.append(set(range(a, b)) - {rng.choice(list(range(a, b)))} if False else set(range(a, b)))
            else:
                Nsets.append(set(rng.sample(range(10), rng.randint(1, 4))))
        # contiguity check
        for r in range(R):
            s = sorted(Nsets[r])
            if s != list(range(min(s), max(s) + 1)) if s else False:
                contig_bad += 1
            ntypes.add(tuple(sorted(Nsets[r])))
        S_holes = [[] for _ in range(R)]
        compat = [[i in Nsets[r] for r in range(R)] for i in range(10)]
        p = [rng.randint(0, 4) for _ in range(10)]
        sigma = [p[i] + rng.randint(0, 6) for i in range(10)]
        non = set(r for r in range(R) if rng.random() < 0.4)
        d = [sigma[i] - p[i] for i in range(10)]
        z = solve_allocation(p, S_holes, compat, sigma, non)
        h = hall_full(d, Nsets, non)
        tot += 1
        # agreement required only when model matches (contiguous N sets + exact demands): check
        if all(sorted(Nsets[r]) == list(range(min(Nsets[r]), max(Nsets[r]) + 1)) for r in range(R) if Nsets[r]):
            if (z is not None) != h:
                dis += 1
                print("DISAGREE", trial, "solver:", z is not None, "hall:", h, flush=True)
    print("trials=%d disagreements=%d noncontig-hole-sets=%d distinct-types=%d" % (tot, dis, contig_bad, len(ntypes)), flush=True)
    json.dump({"trials": tot, "disagreements": dis, "noncontiguous": contig_bad,
               "distinct_types": len(ntypes)}, open(PDIR + "AFSP_HALL_TEST.json", "w"), indent=1)
    sys.exit(0 if dis == 0 else 1)
