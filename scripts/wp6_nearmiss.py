"""WP-6 STEP NM-00: near-miss feeder (negative-margin seeds -> falsifier).

Re-runs MG corpus, collects margin<=0 events with full (n,T0,H,bev) (cap 40),
then hillclimbs each (400 evals) + generic pool (3000), objective = max minload
(tie-break: min margin). Kill: minload>=3 (starve.json + exit 2).
Rationale: negative optimistic-margin moments are arithmetically starvable;
waste/churn rescued them -- mutate to remove the rescue (freeze N, extend e_B,
suppress refreshment).
NEW artifact: nearmiss.json (+starve.json ONLY on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_margin import gen_corpus
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def eval_hist(n, T0, H):
    """(minload_best, min_margin, starve_flag). -2 Beasties on illegal."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return -2, None, None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    from collections import defaultdict
    byacc = defaultdict(list)
    for j in range(len(Bevs)):
        byacc[Bevs[j][0]].append(j)
    load = {}
    best = -1
    minmargin = 10 ** 9
    for acc, js in sorted(byacc.items()):
        for p, j in enumerate(js):
            e = elig[j]
            N = set(i for k in e for i in e[k] if Aevs[i][1])
            if not N:
                continue
            ls = [load.get(i, 0) for i in N]
            R = len(js) - p
            m = 3 * len(N) - sum(ls) - R
            minmargin = min(minmargin, m)
            cands = sorted((load.get(i, 0), i) for i in N)
            best = max(best, cands[0][0])
            if cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
            else:
                return 99, m, True
    return best, minmargin, False


def mutate(H, n, r):
    H2 = copy.deepcopy(H)
    op = r % 5
    if op == 0 and H2:
        i = (r >> 5) % len(H2)
        H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
    elif op == 1 and H2:
        i = (r >> 5) % len(H2)
        H2[i][1] = 1 + (r >> 13) % n
    elif op == 2 and len(H2) < 70:
        H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
    elif op == 3 and H2:
        # freeze-N bias: repeat a recent KEEP key (stable geometry, extend drain)
        keeps = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
        if keeps:
            H2.append(["KEEP", keeps[(r >> 5) % len(keeps)]])
        else:
            H2.append(["KEEP", 1 + (r >> 13) % n])
    elif len(H2) > 4:
        del H2[(r >> 5) % len(H2)]
    return H2


def main() -> int:
    step("NM-00", "Near-miss feeder")
    import json
    seeds = []
    for t in range(300):
        tag = b"mg" if t % 2 == 0 else b"mg2"
        n, T0, H = gen_corpus(t, tag)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            continue
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        from collections import defaultdict
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        load = {}
        for acc, js in sorted(byacc.items()):
            for p, j in enumerate(js):
                e = elig[j]
                N = set(i for k in e for i in e[k] if Aevs[i][1])
                if not N:
                    continue
                ls = [load.get(i, 0) for i in N]
                R = len(js) - p
                m = 3 * len(N) - sum(ls) - R
                if m <= 0 and len(seeds) < 40:
                    seeds.append((m, n, T0, H, j))
                cands = sorted((load.get(i, 0), i) for i in N)
                if cands and cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
    seeds.sort(key=lambda z: z[0])
    step("NM-01", "neg-margin seeds=%d worst=%s" % (len(seeds), seeds[0][0] if seeds else None))
    best = -1
    bestmargin = 10 ** 9
    evals = 0
    holders = [(s[1], s[2], s[3]) for s in seeds[:12]]
    # generic pool
    for s in range(40, 80):
        n, T0, H = gen_corpus(s, b"nm")
        holders.append((n, T0, H))
    it = 0
    while evals < 8000:
        it += 1
        r = int.from_bytes(_h.sha256(b"nmm|%d" % it).digest(), "big")
        n, T0, H = holders[(r >> 2) % len(holders)]
        H2 = mutate(H, n, r)
        v, m, st = eval_hist(n, T0, H2)
        evals += 1
        if v == -2:
            continue
        if v == 99 or st:
            step("NM-KILL", "STARVATION it=%d" % it)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if (v, -m) > (best, -bestmargin):
            best, bestmargin = v, m
            holders.append((n, T0, H2))
            holders = holders[-14:]
        if it % 2000 == 0:
            step("NM-02", "it=%d evals=%d best=%d bestmargin=%d" % (it, evals, best, bestmargin))
    step("NM-03", "evals=%d best=%d bestmargin=%d" % (evals, best, bestmargin))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "nearmiss.json").write_text(
        json.dumps({"evals": evals, "best": best, "bestmargin": bestmargin,
                    "nseeds": len(seeds),
                    "worst_seed_margin": (seeds[0][0] if seeds else None)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
