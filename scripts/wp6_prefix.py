"""WP-6 PREFIX: mincut-prefix structure + prefix-slack census (C155).

Two prongs: (a) MINCUT-PREFIX: are min-cut/tight B-sets access-prefixes
(downward-closed in acc: Q = {bevs acc <= t} for some t, possibly plus
fragments)? Check tight candidates (min slack over cut/access/K/class/
random) for prefix-ness (max acc t with all bevs <= t included? or exact
prefix equality). If mincuts are always prefixes, Hall reduces structurally.
(b) PREFIX-SLACK: min over t of 3|sites<=t| - |bevs<=t| (cumulative margin;
8AC-PREFIX needs >= 0). Distribution of the minimum + at which t it binds.
Artifact: prefix.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, cands_from_cut
from wp6_trap import gen_walk, gen_seed


def step(sid, msg):
    print("[WP-6][PREFIX %s] %s" % (sid, msg), flush=True)


def analyze(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f)
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    # prefix slack
    maxacc = max([a for (a,) in Bevs] + [0])
    nbev = Counter()
    for (a,) in Bevs:
        nbev[a] += 1
    nsite = Counter()
    for (ai, sited) in Aevs:
        if sited:
            nsite[ai] += 1
    cb = cs = 0
    minslack = None
    mint = None
    for t in range(maxacc + 1):
        cb += nbev[t]
        cs += nsite[t]
        sl = 3 * cs - cb
        if minslack is None or sl < minslack:
            minslack = sl
            mint = t
    # tight candidates + prefix-ness
    cands = []
    for name, Q in cands_from_cut(G, lv):
        if Q:
            cands.append((name, set(Q)))
    # add K/class/random probes for tightness diversity
    import random
    rng = random.Random(12345)
    for _ in range(30):
        k = rng.randint(1, max(1, nb))
        cands.append(("rnd", set(rng.sample(range(nb), min(k, nb)))))
    tight = []
    for name, Q in cands:
        d, N = delta_of(G, Q)
        tight.append((d, name, Q))
    tight.sort(key=lambda r: r[0])
    # prefix-ness of the tightest few: exact-prefix? downward-closed?
    preinfo = []
    for (d, name, Q) in tight[:6]:
        accs = sorted(Bevs[j][0] for j in Q)
        lot = max(accs)
        # is Q exactly {bevs acc <= t} for some t? is it downward closed?
        dc = True
        for j in range(nb):
            if Bevs[j][0] < lot and j not in Q:
                dc = False
                break
        exact = (Q == set(j for j in range(nb) if Bevs[j][0] <= lot))
        preinfo.append({"d": d, "name": name, "Q": len(Q),
                        "downclosed": dc, "exactprefix": exact})
    return {"minslack": minslack, "mint": mint, "tight": preinfo,
            "tightest": tight[0][0] if tight else None}


def main() -> int:
    step("PX-00", "mincut-prefix structure + prefix-slack census")
    totmin = []
    ndc = nexp = 0
    ntight = 0
    done = kills = 0
    for s in range(150):
        for fam in (0, 1):
            n, T0, H = gen_walk(6000 + s) if fam == 0 else gen_seed(6000 + s, b"px")
            v = analyze(n, T0, H)
            if v is None:
                continue
            if isinstance(v, tuple):
                kills += 1
                continue
            done += 1
            totmin.append(v["minslack"])
            for t in v["tight"]:
                ntight += 1
                if t["downclosed"]:
                    ndc += 1
                if t["exactprefix"]:
                    nexp += 1
    totmin.sort()
    out = {"evals": done, "kills": kills, "ntight": ntight,
           "downclosed_frac": (ndc / max(1, ntight)),
           "exactprefix_frac": (nexp / max(1, ntight)),
           "prefixslack_min": (totmin[0] if totmin else None),
           "prefixslack_med": (totmin[len(totmin) // 2] if totmin else None)}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "prefix.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("PX-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
