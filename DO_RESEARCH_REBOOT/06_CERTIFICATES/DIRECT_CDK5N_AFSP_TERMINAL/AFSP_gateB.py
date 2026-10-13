# GATE B: single-gap boundary signatures + combos (representative concretions + guard checks).
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'python/independent')
import splay as S
from AFSP_allocate import solve_allocation
from AFSP_canonical import canonical_shadow

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'
TSET = [0, 1, 2, 3, 31, 32, 63, 64, 127, 264, 265, 266]

def depth(t, x):
    d = 0
    cur = t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None

def build_concretion(Sset, gap_counts):
    # S=1..9 ranks mapped to keys 1..9; gap-i gets gap_counts[i] float keys in its interval
    keys = list(Sset)
    Ss = sorted(Sset)
    for i, c in enumerate(gap_counts):
        lo = Ss[i - 1] if i > 0 else 0
        hi = Ss[i] if i < 9 else 10 ** 6
        for j in range(c):
            keys.append(lo + (float(j + 1) / (c + 1)) * (hi - lo))
    t = S.LEAF
    ks = sorted(set(keys))
    # deterministic balanced build
    def bal(ks):
        if not ks:
            return S.LEAF
        m = len(ks) // 2
        return S.node(ks[m], bal(ks[:m]), bal(ks[m + 1:]))
    return bal(ks), set(keys)

if __name__ == "__main__":
    Sset = set(range(1, 10))
    rec = {"cases": []}
    # single-gap signatures
    for g in range(10):
        for t in TSET:
            sig = [0] * 10
            sig[g] = t
            # guard feasibility on a canonical 2-hole spec
            p = [0] * 10
            Sh = [[], []]
            compat = [[True, True] for _ in range(10)]
            z = solve_allocation(p, Sh, compat, sig, set())
            feas = z is not None
            row = {"gap": g, "t": t, "guard_feasible": feas}
            # materialize small ones + spot macro
            if t <= 64:
                T, U = build_concretion(Sset, sig)
                # spot: KEEP root-ish S target, record (H, steps)
                v = 5
                d = depth(T, v)
                if d is not None and (d + 1) // 2 <= 2:
                    T2, evs = S.trace(T, v)
                    row["spot"] = {"d": d, "a": (d + 1) // 2, "steps": [e[0] for e in evs]}
                else:
                    row["spot"] = "target-deep"
            else:
                row["spot"] = "symbolic-only (representative not materialized)"
            rec["cases"].append(row)
    # combos
    for name, sig in [("all-ones", [1] * 10), ("all-twos", [2] * 10),
                      ("alternating", [0 if i % 2 == 0 else 266 for i in range(10)])]:
        p = [0] * 10
        Sh = [[], []]
        compat = [[True, True] for _ in range(10)]
        z = solve_allocation(p, Sh, compat, sig, set())
        row = {"combo": name, "guard_feasible": z is not None}
        if name != "alternating":
            T, U = build_concretion(Sset, sig)
            v = 5
            d = depth(T, v)
            row["spot"] = {"d": d, "a": (d + 1) // 2} if d is not None else "deep"
        else:
            row["spot"] = "symbolic-only"
        rec["cases"].append(row)
    # all-266 symbolic membership (no materialization)
    p = [0] * 10
    Sh = [[], []]
    compat = [[True, True] for _ in range(10)]
    z = solve_allocation(p, Sh, compat, [266] * 10, set())
    rec["cases"].append({"combo": "all-266", "guard_feasible": z is not None, "spot": "symbolic-only"})
    nf = sum(1 for r in rec["cases"] if not r["guard_feasible"])
    print("gateB cases=%d infeasible=%d" % (len(rec["cases"]), nf), flush=True)
    json.dump(rec, open(PDIR + "AFSP_GATE_B.json", "w"), indent=1)
