"""WP-6 ZONE2: violator-zone hunt via claim pools (C153).

8AC-ZONE (OPEN): every Q with mindeg(N(Q))>=4 has Delta<=0. Best wall-thinning:
K2B max -8 (vine-only). Falsifiable with continuous objective: maximize Delta
over mindeg>=4. Candidates per history: (i) claim pools: top plotted sites by
claimant count (all eligible bevs), Q=claimants, N=N(Q); (ii) one-access
slices; (iii) mincut-derived sets (cands_from_cut). Filter mindeg>=4, track
max Delta (;pid>=1 kill (refutes GC-STATIC); >=-7 thins vs K2B). Families:
walks n<=512 L70 + pushers n<=128 (beyond K2B vine-only).
Artifact: zone2.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, degrees, cands_from_cut
from wp6_trap import gen_walk, gen_seed


def step(sid, msg):
    print("[WP-6][ZONE2 %s] %s" % (sid, msg), flush=True)


def analyze(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f)
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    adj = G["adj"]
    # invert adjacency: site -> claimant bevs
    claim = defaultdict(list)
    for j, es in enumerate(adj):
        for i in es:
            claim[i].append(j)
    cands = []
    # (i) top claim pools
    pools = sorted(claim.items(), key=lambda kv: -len(kv[1]))[:20]
    for i, js in pools:
        Q = set(js)
        cands.append(Q)
    # (ii) one-access slices
    byacc = defaultdict(list)
    for j in range(len(Bevs)):
        byacc[Bevs[j][0]].append(j)
    for acc, js in byacc.items():
        cands.append(set(js))
    # (iii) mincut-derived
    if lv is not None:
        for _, Q in cands_from_cut(G, lv):
            if Q:
                cands.append(set(Q))
    best = None
    for Q in cands:
        if not Q:
            continue
        d, N = delta_of(G, Q)
        deg = degrees(G, Q)
        if not deg:
            continue
        md = min(deg.values())
        if md >= 4:
            if best is None or d > best[0]:
                best = (d, len(Q), len(N), md)
    return ("OK", best)


def main() -> int:
    step("Z2-00", "violator-zone hunt (claim pools + slices + cuts)")
    best = None
    bestex = None
    nzone = 0
    done = 0
    kills = 0
    for s in range(200):
        for fam in (0, 1):
            n, T0, H = gen_walk(9000 + s) if fam == 0 else gen_seed(9000 + s, b"z2")
            v = analyze(n, T0, H)
            if v is None:
                continue
            done += 1
            if v[0] == "KILL":
                kills += 1
                step("Z2-KILL", "HALL seed %d fam %d (GC-STATIC REFUTED)" % (s, fam))
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            b = v[1]
            if b is not None:
                nzone += 1
                if best is None or b[0] > best[0]:
                    best = b
                    bestex = (s, fam, n)
        if s % 25 == 24:
            step("Z2-P", "s=%d done=%d zone=%d best=%s" % (s, done, nzone, best))
    out = {"evals": done, "zonecands": nzone, "kills": kills,
           "best": best, "bestex": bestex}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "zone2.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("Z2-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
