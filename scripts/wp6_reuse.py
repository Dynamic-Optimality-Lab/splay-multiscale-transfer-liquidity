"""WP-6 REUSE: transient-reuse multiplicity + cover-channel breakdown (C64).

Q1 (contention): per history, per Aev, reuse = #adjacent B-events. Distribution of
max-reuse; fraction of Aevs with reuse>3 (over-subscribed vs cap 3). Low reuse +
anchored base => matchability plausible; high reuse + saturation => maxflow routes
around (assignment nontrivial).
Q2 (which channel covers anchored gaps): for anchored-deficit bursts (cycle-margin<0
or pressure events), decompose covering supply N(burst) into E1/E4/K(anchored) vs
E2/W/E7(transient): counts per channel.
Artifact: reuse.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_eventflow_abl import build_tagged
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid, msg):
    print("[WP-6][REUSE %s] %s" % (sid, msg), flush=True)


from collections import Counter, defaultdict


def main() -> int:
    import json
    step("RU-00", "reuse multiplicity + cover channels")
    maxreuse_dist = Counter()
    over3_frac_num = over3_frac_den = 0
    over3_hist = 0
    chan = Counter()
    chan_tot = Counter()
    nburst = 0
    evals = 0
    cfgs = [(b"ru1", [16, 32, 64], 8, 24, 90), (b"ru2", [64, 128], 10, 28, 60)]
    for tag, nset, Llo, Lhi, NT in cfgs:
        for t in range(NT):
            rng = Rng(("r%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("r%d" % t).encode(), tag + b"h%d" % i)
                q = rr(1000 + i)
                if i % 5 == 4:
                    y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append(["KEEP" if q % 3 else "DELETE", x])
                x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
            G = build_graph(n, T0, H)
            if G is None:
                continue
            f, nb, _ = maxflow_cap3(G)
            if nb - f > 0:
                step("RU-KILL", "HALL t=%d" % t)
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            evals += 1
            # Q1: reuse
            reuse = Counter()
            for j, es in enumerate(G["adj"]):
                for i in es:
                    reuse[i] += 1
            if reuse:
                m = max(reuse.values())
                maxreuse_dist[m] += 1
                o3 = sum(1 for v in reuse.values() if v > 3)
                over3_frac_num += o3
                over3_frac_den += len(reuse)
                if o3:
                    over3_hist += 1
            # Q2: cover channels at E1-empty bursts (trivial demand)
            Aevs, Bevs = G["Aevs"], G["Bevs"]
            byacc = defaultdict(list)
            for j in range(len(Bevs)):
                byacc[Bevs[j][0]].append(j)
            for acc, js in byacc.items():
                e = G["elig"][js[0]]
                E1s = set(i for i in e["E1"] if Aevs[i][1])
                if E1s or not js:
                    continue
                nburst += 1
                N = set()
                for j in js:
                    N |= G["adj"][j]
                E4s = set(i for i in e["E4"] if Aevs[i][1])
                E2s = set(i for i in e["E2"] if Aevs[i][1])
                E3s = set(i for i in e["E3"] if Aevs[i][1])
                E7s = set(i for i in e.get("E7", []) if Aevs[i][1])
                from wp6_eventflow import to_ptr, splay_A, splay_B_push
                pre2 = G["pre"]
                xx = pre2[acc]["x"]
                # K needs Arot; approximate K as E3 members seen at past acc (cheap: use elig only)
                # exact K via rebuild
                A2, B2 = to_ptr(T0), to_ptr(T0)
                Arot = {}
                acc_of = {}
                aid = 0
                for idx, a2 in enumerate(pre2):
                    A2, invs = splay_A(A2, a2["x"])
                    for (S, sited) in zip(invs, a2["sites"]):
                        Arot[aid] = frozenset(S)
                        acc_of[aid] = idx
                        aid += 1
                    if a2["mode"] == "KEEP":
                        B2, _ = splay_B_push(B2, a2["x"])
                K = set(i for i in E3s if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc)
                W = E3s - K - E1s
                for name, S in (("E4", E4s & N), ("K", K & N), ("E2", E2s & N),
                                ("W", W & N), ("E7", E7s & N)):
                    chan[name] += len(S)
                    chan_tot[name] += 1
    step("RU-01", "evals=%d maxreuse=%s over3aev=%d/%d over3hist=%d" % (
        evals, dict(sorted(maxreuse_dist.items())), over3_frac_num, over3_frac_den, over3_hist))
    step("RU-02", "bursts=%d cover_totals=%s" % (nburst, dict(chan)))
    avg = {k: (chan[k] / max(1, nburst)) for k in chan}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "reuse.json").write_text(
        json.dumps({"evals": evals, "maxreuse": dict(sorted(maxreuse_dist.items())),
                    "over3aev": [over3_frac_num, over3_frac_den], "over3hist": over3_hist,
                    "bursts": nburst, "cover_avg_per_burst": avg},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
