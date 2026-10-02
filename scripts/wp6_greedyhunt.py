"""WP-6 GREEDYHUNT: kill-or-crown the 8AC-greedy rule (C99).

Objective per history: min over all 24 FWD tier-perms of greedy-shortfall.
RULE-KILL = min > 0 (every FWD tier order sticks somewhere) AND maxflow == 0
(true matching needed; greedy path dead, honestly).
Hillclimb seeds: triple-style + steer-style + random; mutations as killshot2.
Artifact: greedyhunt.json (+hallkill on Hall kill). Sealed files untouched.
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
    print("[WP-6][GREEDYHUNT %s] %s" % (sid, msg), flush=True)


import hashlib as _h
import itertools


TIERS = [list(p) for p in itertools.permutations(["E1", "E4", "K", "T"])]


def eval_hist(n, T0, H):
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
    seq = sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j))
    mins = None
    for tord in TIERS:
        s = greedy_with(n, T0, H, G, Arot, acc_of, seq, tord)
        if mins is None or s < mins:
            mins = s
    return ("OK", mins, nb)


def gen_seed(s, tag):
    rng = Rng(("gh%d" % s).encode(), tag)
    r = rng(0)
    n = [16, 32, 64, 128][r % 4]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % (n - 2)
    H = []
    L = 14 + (r >> 24) % 16
    for i in range(L):
        rr = Rng(("gh%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 10
        if op < 4:
            H.append(["DELETE", xc])
        elif op < 7:
            z = min(n, max(1, xc + [-2, -1, 1, 2][(q >> 9) % 4]))
            H.append(["KEEP", z])
        else:
            H.append(["KEEP", xc])
    for _ in range(1 + (r >> 20) % 3):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("GH-00", "greedy-killer hunt (min over 24 FWD perms)")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "greedyhunt.json"
    best = -1
    bestex = None
    evals = 0
    holders = []
    BUDGET = 8000
    for s in range(250):
        n, T0, H = gen_seed(s, b"gh")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("GH-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, mins, nb = v
        holders.append((T0, H, n))
        if mins > best:
            best = mins
            bestex = (s, n, nb)
            step("GH-NEW", "seed %d n=%d minshort=%d nb=%d" % (s, n, mins, nb))
            if mins > 0:
                step("GH-RULEKILL", "rule dead at seed %d" % s)
                TP.write_text(json.dumps({"rulekill": True, "seed": s, "n": n, "H": H},
                                         indent=1, default=str), encoding="utf-8")
                return 3
    holders = holders[-16:]
    step("GH-01", "seeds evals=%d bestmin=%d" % (evals, best))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"ghm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 70:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif op == 3 and H2:
            xs = [a[1] for a in H2 if a[0] == "KEEP"][-3:]
            if xs:
                H2.append(["KEEP", xs[(r >> 5) % len(xs)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("GH-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, mins, nb = v
        if mins > best:
            best = mins
            bestex = (it, n, nb)
            step("GH-NEW", "it=%d n=%d minshort=%d nb=%d" % (it, n, mins, nb))
            holders.append((T0, H2, n))
            holders = holders[-16:]
            if mins > 0:
                step("GH-RULEKILL", "rule dead at it=%d" % it)
                TP.write_text(json.dumps({"rulekill": True, "it": it, "n": n, "H": H2},
                                         indent=1, default=str), encoding="utf-8")
                return 3
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 2000 == 0:
            step("GH-02", "it=%d evals=%d bestmin=%d" % (it, evals, best))
    step("GH-03", "evals=%d bestmin=%d best=%s NO RULEKILL" % (evals, best, bestex))
    TP.write_text(json.dumps({"evals": evals, "bestmin": best, "bestex": bestex,
                              "norulekill": True}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
