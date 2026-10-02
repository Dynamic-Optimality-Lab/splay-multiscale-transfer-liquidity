"""WP-6 RESIDUAL: post-E1K residual size + transient-cover measurement (C98).

Run E1+E4+K-only greedy (no transients, FWD): residual unassigned demand per
history. Then check transients cover it (they do: FWD|E1E4TK perfect). Quantify:
residual distribution, max residual, residual-vs-overflow, small-residual rate.
If residuals are tiny, T-residual Hall reduces to small-set expansion (floors).
Artifact: residual.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_greedy import greedy_with


def step(sid, msg):
    print("[WP-6][RESIDUAL %s] %s" % (sid, msg), flush=True)


from collections import Counter, defaultdict


def main() -> int:
    import json
    step("RS-00", "post-E1K residual measurement")
    res_dist = Counter()
    resmax = 0
    resmax_ex = None
    tot = 0
    zeroы = 0
    cfgs = [(b"rs1", [16, 32, 64], 8, 26, 120), (b"rs2", [64, 128], 10, 30, 80)]
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
                step("RS-KILL", "maxflow shortfall (Hall kill!)")
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            Aevs, Bevs = G["Aevs"], G["Bevs"]
            pre2 = G["pre"]
            A2, B2 = to_ptr(T0), to_ptr(T0)
            Arot = {}
            acc_of = {}
            aid = 0
            for idx, acc in enumerate(pre2):
                A2, invs = splay_A(A2, acc["x"])
                for (S, sited) in zip(invs, acc["sites"]):
                    Arot[aid] = frozenset(S)
                    acc_of[aid] = idx
                    aid += 1
                if acc["mode"] == "KEEP":
                    B2, _ = splay_B_push(B2, acc["x"])
            # E1+E4+K-only greedy = greedy_with tiers [E1,E4,K] + count unplaced.
            # greedy_with has fixed 4 tiers; emulate 3-tier here via big-T-block:
            # instead call with T-tier emptied by temporarily... simplest: replicate:
            load = defaultdict(int)
            resid = 0
            seq = sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j))
            for j in seq:
                acc = Bevs[j][0]
                e = G["elig"][j]
                xx = pre2[acc]["x"]
                E1s = [i for i in e["E1"] if Aevs[i][1]]
                E4s = [i for i in e["E4"] if Aevs[i][1]]
                E3s = set(i for i in e["E3"] if Aevs[i][1])
                K = [i for i in E3s if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc]
                placed = False
                for tier in (sorted(E1s, key=lambda i: load[i]), sorted(E4s, key=lambda i: load[i]),
                             sorted(K, key=lambda i: load[i])):
                    for i in tier:
                        if load[i] < 3:
                            load[i] += 1
                            placed = True
                            break
                    if placed:
                        break
                if not placed:
                    resid += 1
            tot += 1
            res_dist[resid] += 1
            if resid == 0:
                zeroы += 1
            if resid > resmax:
                resmax = resid
                resmax_ex = {"t": t, "tag": tag.decode(), "n": n, "nb": nb}
    step("RS-01", "hist=%d zero-resid=%d (%.3f) maxresid=%d %s" % (
        tot, zeroы, zeroы / max(1, tot), resmax, resmax_ex))
    step("RS-02", "resid_dist=%s" % dict(sorted(res_dist.items())))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "residual.json").write_text(
        json.dumps({"hist": tot, "zero_resid": zeroы, "maxresid": resmax,
                    "maxresid_ex": resmax_ex, "dist": dict(sorted(res_dist.items()))},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
