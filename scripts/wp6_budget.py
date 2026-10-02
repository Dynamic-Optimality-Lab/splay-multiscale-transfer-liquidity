"""WP-6 BUDGET: per-block reuse-budget measurement (C98b).

For each B-heavy block (o = |Q|-3f > 0): new = first-adjacency sources,
K = x-anchored past, F = E1/E4 fresh-part. Need c = max(0, o/3 - |new|) (reuse
demand beyond disjoint-new). Per history: SUM c vs |R_old| (shared pool).
If SUM c <= |R_old| always with margin => counting closes (finite-strong);
assignment (contention routing) remains the only open piece.
Artifact: budget.json. Sealed files untouched.
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


def step(sid, msg):
    print("[WP-6][BUDGET %s] %s" % (sid, msg), flush=True)


from collections import defaultdict, Counter


def main() -> int:
    import json
    step("BU-00", "reuse-budget census")
    worst_ratio = 0.0
    worst_ex = None
    over = 0
    tot = 0
    cdist = Counter()
    cfgs = [(b"bu1", [16, 32, 64], 8, 26, 120), (b"bu2", [64, 128], 10, 30, 80)]
    for tag, nset, Llo, Lhi, NT in cfgs:
        for t in range(NT):
            rng = Rng(("b%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("b%d" % t).encode(), tag + b"h%d" % i)
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
                step("BU-KILL", "maxflow shortfall (Hall kill!)")
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            tot += 1
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
            byacc = defaultdict(list)
            for j in range(len(Bevs)):
                byacc[Bevs[j][0]].append(j)
            seenN = set()
            sumc = 0.0
            for acc in sorted(byacc):
                js = byacc[acc]
                e = G["elig"][js[0]]
                E1s = set(i for i in e["E1"] if Aevs[i][1])
                E4s = set(i for i in e["E4"] if Aevs[i][1])
                ff = len(E4s) if (acc > 0 and pre2[acc - 1]["x"] == pre2[acc]["x"]) else len(E1s)
                Nacc = set()
                for j in js:
                    Nacc |= G["adj"][j]
                new = Nacc - seenN
                seenN |= Nacc
                o = len(js) - 3 * ff
                if o > 0:
                    c = max(0.0, o / 3.0 - len(new))
                    sumc += c
                    cdist[round(c, 1)] += 1
            R = len(seenN)
            # fresh union size approx: use E1+E4 union across accesses
            ratio = sumc / max(1, R)
            if ratio > worst_ratio:
                worst_ratio = ratio
                worst_ex = {"t": t, "tag": tag.decode(), "n": n, "sumc": sumc, "R": R}
            if sumc > R:
                over += 1
    step("BU-01", "hist=%d over-budget=%d worst_ratio=%.3f %s" % (tot, over, worst_ratio, worst_ex))
    step("BU-02", "c_dist=%s" % dict(sorted(cdist.items())[:20]))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "budget.json").write_text(
        json.dumps({"hist": tot, "over": over, "worst_ratio": worst_ratio,
                    "worst_ex": worst_ex, "c_dist": dict(sorted(cdist.items()))},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
