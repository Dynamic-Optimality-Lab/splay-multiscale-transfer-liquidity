"""WP-6 GREEDY: block-greedy (E1->E4->K->transient chronological) vs maxflow (C97).

Tests 8AC constructive path: is chronological block-greedy sufficient wherever
maxflow saturates? Greedy fail + maxflow success = sufficiency gap (contention
needs true matching). Greedy == maxflow everywhere = constructive path open.
Priority per B-event: E1 (fresh, least-loaded), E4 (setup), K (x-anchored past),
E2/W/E7 (transients, least-loaded); cap 3; chronological access order.
Artifact: greedy.json. Sealed files untouched.
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
from solver import encode as E


def step(sid, msg):
    print("[WP-6][GREEDY %s] %s" % (sid, msg), flush=True)


from collections import defaultdict


def greedy_shortfall(n, T0, H):
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
    load = defaultdict(int)
    short = 0
    order = sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j))
    for j in order:
        acc = Bevs[j][0]
        e = G["elig"][j]
        xx = pre2[acc]["x"]
        E1s = [i for i in e["E1"] if Aevs[i][1]]
        E4s = [i for i in e["E4"] if Aevs[i][1]]
        E3s = set(i for i in e["E3"] if Aevs[i][1])
        K = [i for i in E3s if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc]
        E1set = set(E1s)
        W = [i for i in E3s if i not in set(K) and i not in E1set]
        E2s = [i for i in e["E2"] if Aevs[i][1]]
        E7s = [i for i in e.get("E7", []) if Aevs[i][1]]
        tiers = [sorted(E1s, key=lambda i: load[i]), sorted(E4s, key=lambda i: load[i]),
                 sorted(K, key=lambda i: load[i]),
                 sorted(set(E2s) | set(W) | set(E7s), key=lambda i: load[i])]
        placed = False
        for tier in tiers:
            for i in tier:
                if load[i] < 3:
                    load[i] += 1
                    placed = True
                    break
            if placed:
                break
        if not placed:
            short += 1
    return short


def greedy_with(n, T0, H, G, Arot, acc_of, seq, tier_order):
    from collections import defaultdict
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    load = defaultdict(int)
    short = 0
    for j in seq:
        acc = Bevs[j][0]
        e = G["elig"][j]
        xx = pre2[acc]["x"]
        E1s = [i for i in e["E1"] if Aevs[i][1]]
        E4s = [i for i in e["E4"] if Aevs[i][1]]
        E3s = set(i for i in e["E3"] if Aevs[i][1])
        K = [i for i in E3s if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc]
        E1set = set(E1s)
        W = [i for i in E3s if i not in set(K) and i not in E1set]
        TR = list(set(i for i in e["E2"] if Aevs[i][1]) | set(W) | set(i for i in e.get("E7", []) if Aevs[i][1]))
        M = {"E1": E1s, "E4": E4s, "K": K, "T": TR}
        placed = False
        for k in tier_order:
            for i in sorted(M[k], key=lambda i: load[i]):
                if load[i] < 3:
                    load[i] += 1
                    placed = True
                    break
            if placed:
                break
        if not placed:
            short += 1
    return short


def main() -> int:
    import json
    step("GR-00", "block-greedy vs maxflow sufficiency")
    gap = 0
    gap_ex = []
    geq = 0
    tot = 0
    cfgs = [(b"gr1", [16, 32, 64], 8, 24, 90), (b"gr2", [64, 128], 10, 28, 60)]
    for tag, nset, Llo, Lhi, NT in cfgs:
        for t in range(NT):
            rng = Rng(("g%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("g%d" % t).encode(), tag + b"h%d" % i)
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
            mf = nb - f
            if mf > 0:
                step("GR-KILL", "maxflow shortfall t=%d (Hall kill!)" % t)
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            g = greedy_shortfall(n, T0, H)
            if g is None:
                continue
            tot += 1
            if g == 0:
                geq += 1
            else:
                gap += 1
                if len(gap_ex) < 8:
                    gap_ex.append({"t": t, "tag": tag.decode(), "n": n, "greedy": g, "nb": nb})
    step("GR-01", "hist=%d greedy==maxflow(saturate) %d (%.3f) gaps=%d" % (
        tot, geq, geq / max(1, tot), gap))
    step("GR-02", "gap_ex=%s" % gap_ex[:4])
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "greedy.json").write_text(
        json.dumps({"hist": tot, "greedy_ok": geq, "gaps": gap, "gap_ex": gap_ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
