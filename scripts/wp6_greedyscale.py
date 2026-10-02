"""WP-6 GREEDYSCALE: 8AC-greedy rule at scale (C115).

Uncovered domain: all greedy corpora used vine T0 + L<=34. Here balanced/random
BST T0, n=64..512, L=30-70 (M2-like frozen-core + big-n regimes), rule
FWD|E1,E4,T,K-least-loaded vs maxflow. Gap => rule crown revoked at scale.
Artifact: greedyscale.json (+hallkill on Hall kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from wp6_killshot3 import balanced, random_bst
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_greedy import greedy_with


def step(sid, msg):
    print("[WP-6][GREEDYSCALE %s] %s" % (sid, msg), flush=True)


def main() -> int:
    import json
    step("GS-00", "greedy rule at scale (balanced/random T0, long histories)")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "greedyscale.json"
    gaps = 0
    worst = 0
    worstex = None
    tot = 0
    for s in range(150):
        rng = Rng(("gs%d" % s).encode(), b"scale")
        r = rng(0)
        n = [64, 128, 256, 512][r % 4]
        fam = (r >> 5) % 3
        if fam == 0:
            T0 = vine(n, (r >> 8) % 2 == 0)
            fn = "vine"
        elif fam == 1:
            T0 = balanced(n)
            fn = "bal"
        else:
            T0 = random_bst(n, rng, s)
            fn = "rbst"
        L = 30 + (r >> 16) % 41
        x = 1 + (r >> 24) % n
        H = []
        for i in range(L):
            rr = Rng(("gs%d" % s).encode(), b"gh%d" % i)
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
            step("GS-KILL", "HALL s=%d fam=%s shortfall=%d (GC-STATIC DEAD)" % (s, fn, nb - f))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "fam": fn, "H": H}, indent=1, default=str),
                encoding="utf-8")
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
        seq = sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j))
        g = greedy_with(n, T0, H, G, Arot, acc_of, seq, ["E1", "E4", "T", "K"])
        tot += 1
        if g > 0:
            gaps += 1
            if g > worst:
                worst = g
                worstex = {"s": s, "fam": fn, "n": n, "nb": nb, "short": g}
        if tot % 50 == 0:
            step("GS-P", "tested=%d gaps=%d" % (tot, gaps))
    step("GS-01", "tested=%d gaps=%d worst=%d %s" % (tot, gaps, worst, worstex))
    TP.write_text(json.dumps({"tested": tot, "gaps": gaps, "worst": worst,
                              "worstex": worstex}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
