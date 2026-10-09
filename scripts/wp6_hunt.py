"""PIVOT-13 T2: overflow-cycle hunt -- random closed walks at n=6, 2-lap
creator matching; report full vs lap2-steady-state coverage + Hall cases."""
from __future__ import annotations
import sys
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def find_cycle(adj, rng, maxlen=60):
    nodes = list(adj.keys())
    u0 = rng.choice(nodes)
    u = u0
    seen = {u0: 0}
    hist = []  # (u, mode, key, to)
    for i in range(maxlen):
        e = rng.choice(adj[u])
        to, md, x = e[0], e[1], e[2]
        hist.append((u, md, x, to))
        u = to
        if u in seen:
            cyc = hist[seen[u]:]
            if len(cyc) >= 2:
                return cyc
            return None
        seen[u] = len(hist)
    return None


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    ncyc = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)
    G = O.build(6)
    nS, adj, Sh = G["nS"], G["adj"], G["Sh"]
    V.step("H-0", "hunt seed=%d target=%d" % (seed, ncyc))
    tested = ovf = full_ok = lap2_ok = 0
    lap2_fail_ex = []
    gen_rate = []
    cdist = []
    ovf_cycles = 0
    while tested < ncyc:
        cyc = find_cycle(adj, rng)
        if not cyc:
            continue
        word = [(md, x) for (_, md, x, _) in cyc]
        u0 = cyc[0][0]
        ia0, ib0 = u0 // nS, u0 % nS
        rep = V.replay(Sh[ia0], Sh[ib0], word + word)
        L = len(word)
        legs = rep["accesses"][:L]
        if max(a["eps"] for a in legs) <= 0:
            continue  # want overflow content
        ovf_cycles += 1
        cr = V.creators(rep)
        rfull = V.charge(rep, cr)
        # lap2-restricted: LEFT = lap2 doubles, RIGHT = all credits
        lap2dbl = [d for d in cr if d["acc"] >= L]
        # rebuild charge on sublist: need index remap
        sub = V.charge(rep, lap2dbl)
        tested += 1
        ovf += 1
        if rfull["full"]:
            full_ok += 1
        if sub["full"]:
            lap2_ok += 1
        elif len(lap2_fail_ex) < 5:
            lap2_fail_ex.append({
                "word": word, "u0": u0,
                "eps": [a["eps"] for a in legs],
                "hall": sub.get("hall_detail"),
                "nX": len(sub.get("hall_X", []))})
        gen_rate.append(sum(1 for d in lap2dbl if d["genesis"]) /
                        max(1, len(lap2dbl)))
        for d in lap2dbl:
            if d["creator"] is not None:
                cdist.append(d["acc"] - d["creator"])
        if tested % 25 == 0:
            V.step("H-1", "tested=%d full_ok=%d lap2_ok=%d" %
                   (tested, full_ok, lap2_ok))
    out = {"seed": seed, "tested": tested, "overflow_cycles": ovf_cycles,
           "full_ok": full_ok, "lap2_ok": lap2_ok,
           "gen_rate_mean": sum(gen_rate) / max(1, len(gen_rate)),
           "gen_rate_max": max(gen_rate) if gen_rate else 0,
           "cdist": sorted(cdist),
           "lap2_fail_ex": lap2_fail_ex}
    V.save("hunt_n6.json", out)
    V.step("H-2", "tested=%d full=%d lap2=%d genmean=%.3f genmax=%.3f fails=%d" %
           (tested, full_ok, lap2_ok, out["gen_rate_mean"],
            out["gen_rate_max"], len(lap2_fail_ex)))
    V.step("H-2", "creator distances: %s" % (sorted(set(cdist)),))
    return 0


if __name__ == "__main__":
    sys.exit(main())
