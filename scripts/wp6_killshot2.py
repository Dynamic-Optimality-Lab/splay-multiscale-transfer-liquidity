"""WP-6 KILLSHOT2: one-access-Delta + violator-zone (mindeg>=4) climb (C57b).

KS-00 (12k, n=6..32): NO KILL, bestslack 2 (degenerate singleton — wrong objective).
This script climbs the RIGHT objectives:
  A) one-access Delta: max over accesses acc of (|Q_acc|-3|N_acc|). >0 = Hall kill
     (one-access violator IS global violator). Direct E3-union minimizer.
  B) violator-zone: max Delta over Qs with mindeg(N(Q))>=4 (8B signature).
     M2 4-core Delta=-183; climb toward 0 then over.
Generator: repeat-trivial-A bursts (E1=empty: x root in A, deep in B) + zone-separated
B-paths (E3-union small) + E2/E4/K thin. n=6..64, L=16..60.
Kill: either objective >0 -> hallkill.json exit 2.
Artifact: killshot2.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, degrees
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng


def step(sid, msg):
    print("[WP-6][KILLSHOT2 %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def objectives(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    if gap > 0:
        return ("GCKILL", gap, nb)
    A = {"best": None}  # one-access Delta
    byacc = defaultdict(list)
    for j in range(len(G["Bevs"])):
        byacc[G["Bevs"][j][0]].append(j)
    for acc, js in byacc.items():
        d, N = delta_of(G, js)
        if A["best"] is None or d > A["best"][0]:
            A["best"] = (d, acc, len(js), len(N))
    # B) violator-zone: candidate Qs = full + access slices + min-cut sides;
    # filter mindeg>=4, max Delta
    from wp6_hallcore import cands_from_cut
    B = {"best": None}
    seen = set()
    cands = cands_from_cut(G, lv) + [("all", list(range(len(G["Bevs"]))))]
    for name, Q in cands:
        if not Q:
            continue
        t = tuple(sorted(Q))
        if t in seen:
            continue
        seen.add(t)
        deg = degrees(G, set(Q))
        if not deg:
            continue
        if min(deg.values()) >= 4:
            d, N = delta_of(G, set(Q))
            if B["best"] is None or d > B["best"][0]:
                B["best"] = (d, name, len(Q), len(N))
    return ("OK", A["best"], B["best"], nb, gap)


def gen_seed(s, tag):
    rng = Rng(("k2%d" % s).encode(), tag)
    r = rng(0)
    n = [6, 8, 12, 16, 24, 32, 48, 64][r % 8]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % max(1, n - 2)
    H = []
    # setup: bring xc to root in A only (decouple), keep B stale deep:
    # alternate DELETE-far (A moves) with no B change, then hammer xc KEEPs
    L = 16 + (r >> 24) % 20
    for i in range(L):
        rr = Rng(("k2%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 10
        if op < 4:
            # pin xc at A-root: touch xc via DELETE (A-only, no B demand, banks E4/K?)
            H.append(["DELETE", xc])
        elif op < 7:
            # B-pushers near xc (both trees move; try to deepen B chain)
            z = min(n, max(1, xc + [-2, -1, 1, 2][(q >> 9) % 4]))
            H.append(["KEEP", z])
        else:
            # burst xc (if A-rooted: E1 empty, E3-union only + E2/E4/K)
            H.append(["KEEP", xc])
    for _ in range(2 + (r >> 20) % 4):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("K2-00", "one-access-Delta + violator-zone climb")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "killshot2.json"
    bestA = None  # max one-access Delta (want >0)
    bestB = None  # max violator-zone Delta (want >0)
    evals = 0
    holders = []
    BUDGET = 12000
    for s in range(400):
        n, T0, H = gen_seed(s, b"k2")
        v = objectives(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("K2-KILL", "HALL seed %d n=%d shortfall=%d" % (s, n, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "seed": s, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("K2-KILL", "GC seed %d gap=%d" % (s, v[1]))
            return 2
        _, a, b, nb, gap = v
        holders.append((T0, H, n, a, b))
        if a is not None and (bestA is None or a[0] > bestA[0]):
            bestA = a
            step("K2-NEWA", "seed %d n=%d oneAccDelta=%d acc=%s Q=%d N=%d" % (s, n, a[0], a[1], a[2], a[3]))
        if b is not None and (bestB is None or b[0] > bestB[0]):
            bestB = b
            step("K2-NEWB", "seed %d n=%d zoneDelta=%d %s Q=%d N=%d" % (s, n, b[0], b[1], b[2], b[3]))
    holders = sorted(holders, key=lambda t: ((t[3][0] if t[3] else -10**9), (t[4][0] if t[4] else -10**9)))[-20:]
    step("K2-01", "seeds evals=%d bestA=%s bestB=%s" % (evals, bestA, bestB))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"k2m|%d" % it).digest(), "big")
        T0, H, n, _, _ = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 6
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
                for _ in range(1 + (r >> 7) % 3):
                    H2.append(["KEEP", xs[(r >> 5) % len(xs)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif op == 4 and H2:
            i = (r >> 5) % len(H2)
            H2.insert(i + 1, [H2[i][0], H2[i][1]])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = objectives(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("K2-KILL", "HALL it=%d n=%d shortfall=%d H=%s" % (it, n, v[1], H2))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "it": it, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("K2-KILL", "GC it=%d gap=%d" % (it, v[1]))
            return 2
        _, a, b, nb, gap = v
        improved = False
        if a is not None and (bestA is None or a[0] > bestA[0]):
            bestA = a
            improved = True
            step("K2-NEWA", "it=%d n=%d oneAccDelta=%d acc=%s Q=%d N=%d" % (it, n, a[0], a[1], a[2], a[3]))
            TP.write_text(json.dumps({"evals": evals, "bestA": bestA, "bestB": bestB}, indent=1, default=str), encoding="utf-8")
        if b is not None and (bestB is None or b[0] > bestB[0]):
            bestB = b
            improved = True
            step("K2-NEWB", "it=%d n=%d zoneDelta=%d %s Q=%d N=%d" % (it, n, b[0], b[1], b[2], b[3]))
            TP.write_text(json.dumps({"evals": evals, "bestA": bestA, "bestB": bestB}, indent=1, default=str), encoding="utf-8")
        if improved:
            holders.append((T0, H2, n, a, b))
            holders = sorted(holders, key=lambda t: ((t[3][0] if t[3] else -10**9), (t[4][0] if t[4] else -10**9)))[-20:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n, a, b))
            holders = sorted(holders, key=lambda t: ((t[3][0] if t[3] else -10**9), (t[4][0] if t[4] else -10**9)))[-20:]
        if it % 2500 == 0:
            step("K2-02", "it=%d evals=%d bestA=%s bestB=%s" % (it, evals, bestA, bestB))
    step("K2-03", "evals=%d bestA=%s bestB=%s NO KILL" % (evals, bestA, bestB))
    TP.write_text(json.dumps({"evals": evals, "bestA": bestA, "bestB": bestB, "nokill": True}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
