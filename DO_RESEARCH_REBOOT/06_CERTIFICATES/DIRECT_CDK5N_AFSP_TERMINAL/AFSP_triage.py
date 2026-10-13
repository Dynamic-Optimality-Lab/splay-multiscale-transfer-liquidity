# Gate C guarded-triage machinery (§13 Gate C): edge-word + guard conjunction + classification.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
from AFSP_allocate import solve_allocation

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'

def triage(edge_guards, sigma, cycle_weight=None, replay_status=None):
    # edge_guards: list of (p, S_holes, compat, nonempty) per edge; sigma shared.
    # Per §13: fixed-sigma feasibility is per-edge independent (private z per edge); conjunction = all pass.
    results = []
    for (p, Sh, compat, non) in edge_guards:
        z = solve_allocation(p, Sh, compat, sigma, non)
        results.append(z is not None)
    feasible = all(results)
    out = {"edges": len(edge_guards), "all_guards_feasible": feasible,
           "per_edge": results, "cycle_weight": cycle_weight}
    if not feasible:
        out["classification"] = "INFEASIBLE-GUARD (no abstract cycle at this sigma)"
    elif cycle_weight is not None and cycle_weight >= 0:
        out["classification"] = "NONNEGATIVE (no obstruction)"
    elif replay_status == "counterexample":
        out["classification"] = "GENUINE ORIGINAL COUNTEREXAMPLE"
    elif replay_status == "not-replayable":
        out["classification"] = "FEASIBLE-BUT-SPURIOUS (guard-level realizable, source unrealizable)"
    else:
        out["classification"] = "UNDECIDED (feasible guards, realizability open)"
    return out

if __name__ == "__main__":
    import random
    rng = random.Random(99)
    # self-test: feasible + infeasible guard sets
    ok = 0
    for trial in range(100):
        R = rng.randint(1, 5)
        Sh = [sorted(rng.sample(range(1, 10), rng.randint(0, 2))) for _ in range(R)]
        compat = [[rng.random() < 0.7 for _ in range(R)] for _ in range(10)]
        p = [rng.randint(0, 3) for _ in range(10)]
        sigma = [p[i] + rng.randint(0, 6) for i in range(10)]
        non = set(r for r in range(R) if not Sh[r] and rng.random() < 0.4)
        e = [(p, Sh, compat, non)]
        r = triage(e, sigma, cycle_weight=-1)
        assert r["all_guards_feasible"] == (solve_allocation(p, Sh, compat, sigma, non) is not None)
        ok += 1
    print("triage self-test: %d/100 consistent" % ok, flush=True)
    json.dump({"selftest": ok}, open(PDIR + "AFSP_TRIAGE_SELFTEST.json", "w"), indent=1)
