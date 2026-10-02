"""WP-6 TRAP/TOTALITY: greedy stuck-point census + totality sweep (C123).

TA (trap): CLOSED alternating traps from stuck greedy matchings are VACUOUS
when maxflow saturates: Berge's theorem guarantees an augmenting path from any
non-maximum matching, so the BFS closure from an unmatched bev ALWAYS opens.
Verified: 4 stuck events (FWD|E1E4KT, n=512 walks) all opened. Trap sealed REFUTED.
TB (totality): sweep greedy tier-orders x FWD/REV x scales for stuck rate.
A never-stick rule = constructive matcher = decision procedure for 8AC/GC-STATIC.
Artifacts: trapanat.json (TA anatomy + Berge note), totality.json (TB sweep).
Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, degrees
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push


def step(sid, msg):
    print("[WP-6][TRAP %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict, Counter, deque


def greedy_M(n, T0, H, G, Arot, acc_of, tier_order, rev=False):
    """Greedy (FWD or REV) with tier order; maximal matching; returns short + M + loads."""
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    load = defaultdict(int)
    M = {}
    short = []
    order = sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j), reverse=rev)
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
        TR = list(set(i for i in e["E2"] if Aevs[i][1]) | set(W) | set(i for i in e.get("E7", []) if Aevs[i][1]))
        Mtiers = {"E1": E1s, "E4": E4s, "K": K, "T": TR}
        placed = False
        for k in tier_order:
            for i in sorted(Mtiers[k], key=lambda i: load[i]):
                if load[i] < 3:
                    load[i] += 1
                    M[j] = i
                    placed = True
                    break
            if placed:
                break
        if not placed:
            short.append(j)
    return short, M, load


def chan_of(j, i, G, Arot, acc_of):
    """Channel labels for edge (bev j, aev i). Returns set of labels."""
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    acc = Bevs[j][0]
    e = G["elig"][j]
    xx = pre2[acc]["x"]
    out = set()
    if i in e["E1"]:
        out.add("E1")
    if i in e["E4"]:
        out.add("E4")
    if i in e["E3"]:
        if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc:
            out.add("K")
        elif i not in set(e["E1"]):
            out.add("W")
        else:
            out.add("E3E1")
    if i in e["E2"]:
        out.add("E2")
    if i in e.get("E7", []):
        out.add("E7")
    return out


def trap_from(G, Arot, acc_of, M, loads, b0):
    """Alternating BFS closure from unmatched b0. Returns dict or None."""
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    seenB = {b0}
    seenA = set()
    q = deque([("B", b0)])
    parent = {}
    chan = Counter()
    Amate = defaultdict(list)
    for j, i in M.items():
        Amate[i].append(j)
    while q:
        typ, v = q.popleft()
        if typ == "B":
            for i in G["adj"][v]:
                if i in seenA:
                    continue
                if not Aevs[i][1]:
                    continue  # unplotted: no capacity, not part of the matching graph
                seenA.add(i)
                parent[("A", i)] = ("B", v)
                for c in chan_of(v, i, G, Arot, acc_of):
                    chan[c] += 1
                q.append(("A", i))
        else:
            if loads.get(v, 0) < 3:
                return {"open": True, "at": v}
            for j in Amate.get(v, []):
                if j not in seenB:
                    seenB.add(j)
                    parent[("B", j)] = ("A", v)
                    q.append(("B", j))
    return {"open": False, "B": seenB, "A": seenA, "chan": dict(chan),
            "parent": {str(k): str(val) for k, val in parent.items()}}


def eval_hist(n, T0, H, tier_order, rev=False):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, _ = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
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
    short, M, loads = greedy_M(n, T0, H, G, Arot, acc_of, tier_order, rev)
    if not short:
        return ("OK", 0, nb)
    traps = []
    for b0 in short[:6]:
        t = trap_from(G, Arot, acc_of, M, loads, b0)
        if t is None:
            continue
        if t.get("open"):
            traps.append({"open": True})
            continue
        Qs = set(t["B"])
        d, N = delta_of(G, Qs)
        deg = degrees(G, Qs)
        traps.append({"open": False, "Q": len(Qs), "N": len(N), "Delta": d,
                      "mindeg": min(deg.values()) if deg else None,
                      "chan": t["chan"],
                      "Wpresent": (t["chan"].get("W", 0) > 0)})
    return ("STUCK", len(short), nb, traps)


def gen_seed(s, tag):
    rng = Rng(("tp%d" % s).encode(), tag)
    r = rng(0)
    n = [16, 32, 64, 128][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % (n - 2)
    H = []
    L = 14 + (r >> 24) % 16
    for i in range(L):
        rr = Rng(("tp%d" % s).encode(), tag + b"h%d" % i)
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
    return n, T0, H


def gen_walk(s):
    """gr1-style plain random walk (t75's family): uniform random KEEP/DELETE."""
    rng = Rng(("tw%d" % s).encode(), b"tw")
    r = rng(0)
    n = [64, 128, 512][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    H = []
    L = 70
    for i in range(L):
        rr = Rng(("tw%d" % s).encode(), b"tw" + bytes([i % 250]))
        q = rr(2000 + i)
        x = 1 + (q % n)
        if (q >> 7) % 3 == 0:
            H.append(["DELETE", x])
        else:
            H.append(["KEEP", x])
    return n, T0, H


def main() -> int:
    import json
    step("TA-00", "typed alternating traps from greedy stuck points (REV + K-hoard + walks)")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "trapanat.json"
    configs = [(["E1", "E4", "K", "T"], True), (["K", "E1", "E4", "T"], False),
               (["E1", "E4", "K", "T"], False)]
    ntraps = 0
    wpresent = 0
    chan_tot = Counter()
    deltas = []
    mindegs = []
    evals = 0
    stuck = 0
    for s in range(100):
        hists = [gen_seed(s, b"tp"), gen_walk(s)]
        for (n, T0, H) in hists:
            for (tiers, rev) in configs:
                v = eval_hist(n, T0, H, tiers, rev)
                evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("TA-KILL", "HALL seed %d (GC-STATIC REFUTED)" % s)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "OK":
            continue
        _, ns, nb, traps = v
        stuck += 1
        for t in traps:
            if t.get("open"):
                continue
            ntraps += 1
            if t["Wpresent"]:
                wpresent += 1
            for k, c in t["chan"].items():
                chan_tot[k] += c
            deltas.append(t["Delta"])
            if t["mindeg"] is not None:
                mindegs.append(t["mindeg"])
        if s % 25 == 24:
            step("TA-P", "s=%d evals=%d stuck=%d traps=%d Wpresent=%d" % (s, evals, stuck, ntraps, wpresent))
    import statistics
    step("TA-01", "evals=%d stuck=%d traps=%d Wpresent=%d (%.3f) channels=%s" % (
        evals, stuck, ntraps, wpresent, wpresent / max(1, ntraps), dict(chan_tot)))
    step("TA-02", "trapDelta med=%s min=%s max=%s; mindeg med=%s" % (
        (sorted(deltas)[len(deltas) // 2] if deltas else None),
        (min(deltas) if deltas else None), (max(deltas) if deltas else None),
        (sorted(mindegs)[len(mindegs) // 2] if mindegs else None)))
    TP.write_text(json.dumps({"evals": evals, "stuck": stuck, "traps": ntraps, "Wpresent": wpresent,
                              "channels": dict(chan_tot),
                              "delta_med": (sorted(deltas)[len(deltas) // 2] if deltas else None),
                              "delta_min": (min(deltas) if deltas else None),
                              "delta_max": (max(deltas) if deltas else None),
                              "berge_note": ("closed traps vacuous when maxflow saturates: all %d stuck "
                                             "closures opened via augmenting paths (Berge)" % stuck)},
                             indent=1, sort_keys=True, default=str), encoding="utf-8")
    totality()
    return 0


def totality():
    """TB: sweep greedy rules (tier-order x FWD/REV) for stuck rate at scale."""
    import json
    import itertools
    step("TB-00", "greedy totality sweep: rule x direction x scale")
    rules = [["E1", "E4", "K", "T"], ["E1", "E4", "T", "K"],
             ["K", "E1", "E4", "T"], ["K", "E4", "E1", "T"],
             ["E4", "E1", "K", "T"], ["T", "E1", "E4", "K"]]
    rows = []
    for tiers in rules:
        for rev in (False, True):
            e = s = 0
            kills = 0
            for sh in range(40):
                n, T0, H = gen_walk(1000 + sh)
                v = eval_hist(n, T0, H, tiers, rev)
                if v is None:
                    continue
                e += 1
                if v[0] == "KILL":
                    kills += 1
                elif v[0] == "STUCK":
                    s += v[1]
            rows.append({"tiers": tiers, "rev": rev, "evals": e, "stuckbev": s, "kills": kills,
                         "rate": (s / e if e else None)})
            step("TB-R", "%s rev=%s evals=%d stuckbev=%d kills=%d" % (tiers, rev, e, s, kills))
    rows.sort(key=lambda r: (r["stuckbev"], str(r["tiers"])))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "totality.json").write_text(
        json.dumps({"rows": rows,
                    "best": rows[0] if rows else None,
                    "note": "never-stick rule = constructive 8AC matcher candidate"}, indent=1, default=str),
        encoding="utf-8")
    step("TB-01", "best=%s" % (rows[0] if rows else None))


if __name__ == "__main__":
    sys.exit(main())
