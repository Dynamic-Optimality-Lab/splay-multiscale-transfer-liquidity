"""WP-6 GREEDYADV: 8AC-greedy rule vs ADVERSARIAL corpus (C101).

Rule under test: FWD|E1,E4,T,K-least-loaded (T-before-K) saturates wherever
maxflow does. Corpus: banked kill-witnesses (starve_min, m2, entry3) + 300 fresh
adversarial (triple/cycler/steer-style + pressure-biased). Metric: gaps
(greedy>maxflow), worst gap. Any gap => rule-crown revoked (back to drawing).
Artifact: greedyadv.json (+hallkill on Hall kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_greedy import greedy_with


def step(sid, msg):
    print("[WP-6][GREEDYADV %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def load_witnesses():
    import json
    out = []
    try:
        dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
        out.append(("starve", dk["n"], vine(dk["n"], dk["T0left"]), dk["Hmin"]))
    except Exception as e:
        step("GA-W", "starve load fail %s" % e)
    try:
        w = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json"))["witness"]
        for left in (True, False):
            T = vine(w["n"], left)
            G = build_graph(w["n"], T, w["H"])
            if G is not None and len(G["Bevs"]) > 100:
                out.append(("m2", w["n"], T, w["H"]))
                break
    except Exception as e:
        step("GA-W", "m2 load fail %s" % e)
    try:
        ew = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "entryhunt.json"))["witness"]
        for left in (True, False):
            T = vine(ew["n"], left)
            G = build_graph(ew["n"], T, ew["H"])
            if G is not None and len(G["Bevs"]) > 100:
                out.append(("entry3", ew["n"], T, ew["H"]))
                break
    except Exception as e:
        step("GA-W", "entry load fail %s" % e)
    return out


def prep(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
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
    return (G, Arot, acc_of, seq)


TIERS = [["E1", "E4", "T", "K"], ["E1", "T", "E4", "K"], ["E4", "E1", "T", "K"]]


def main() -> int:
    import json
    step("GA-00", "greedy rule vs adversarial corpus")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "greedyadv.json"
    gaps = 0
    worst = 0
    worstex = None
    tot = 0
    tests = [(name, n, T0, H) for (name, n, T0, H) in load_witnesses()]
    step("GA-01", "witnesses=%d" % len(tests))
    for s in range(300):
        rng = Rng(("ga%d" % s).encode(), b"adv")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        xc = 2 + (r >> 16) % (n - 2)
        H = []
        L = 14 + (r >> 24) % 16
        for i in range(L):
            rr = Rng(("ga%d" % s).encode(), b"ah%d" % i)
            q = rr(1000 + i)
            op = (q >> 2) % 10
            if op < 3:
                H.append(["DELETE", xc])
            elif op < 6:
                z = min(n, max(1, xc + [-3, -2, -1, 1, 2, 3][(q >> 9) % 6]))
                H.append(["DELETE", z])
                H.append(["KEEP", z])
            else:
                H.append(["KEEP", xc])
        tests.append(("adv%d" % s, n, T0, H))
    for name, n, T0, H in tests:
        G = build_graph(n, T0, H)
        if G is None:
            continue
        f, nb, _ = maxflow_cap3(G)
        if nb - f > 0:
            step("GA-KILL", "HALL %s shortfall=%d (GC-STATIC DEAD)" % (name, nb - f))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        P = prep(n, T0, H)
        if P is None:
            continue
        G, Arot, acc_of, seq = P
        tot += 1
        best = min(greedy_with(n, T0, H, G, Arot, acc_of, seq, t) for t in TIERS)
        if best > 0:
            gaps += 1
            if best > worst:
                worst = best
                worstex = {"name": name, "n": n, "nb": nb, "short": best}
    step("GA-02", "tested=%d gaps=%d worst=%d %s" % (tot, gaps, worst, worstex))
    TP.write_text(json.dumps({"tested": tot, "gaps": gaps, "worst": worst,
                              "worstex": worstex}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
