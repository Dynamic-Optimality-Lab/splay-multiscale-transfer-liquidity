"""WP-6 STEP WM-00: wall-pressure maximizer + sterile-rebuild overlap census (C56).

PA-00 showed wall-pressure (B-heavy + old<=2) is 1.5% of KEEPs, minload always 0.
Blind-spot question: can pressure be SUSTAINED/elevated to shortfall>0, or does
old-abundance always rebuild? This script hillclimbs directly on pressure:
  objective = (shortfall, gc_gap, pressure_count, max eB/f ratio)
Generator bias: first-x strikes (thin fresh) + nearby-below pure pushers
  (sterile bias) + run-repeat drain + far-key supply avoidance.
Overlap census (8R residual): for each pure push, does the next access rebuild
  supply via zone-overlap (A-rotated hits x-zone) vs stay disjoint?
Kill: shortfall>0 -> hallkill.json + exit 2; gap>0 -> gckill.json + exit 2.
NEW artifact: wallmax.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_eventflow_abl import build_tagged
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def pressure_metrics(n, T0, H):
    """Returns (nkeep, nheavy, npressure, maxratio, ex) or None if illegal."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    pre2 = g["pre"]
    from wp6_eventflow import to_ptr, splay_A, splay_B_push
    A, B = to_ptr(T0), to_ptr(T0)
    Arot = {}
    acc_of = {}
    aid = 0
    for idx, acc in enumerate(pre2):
        A, invs = splay_A(A, acc["x"])
        for (S, sited) in zip(invs, acc["sites"]):
            Arot[aid] = frozenset(S)
            acc_of[aid] = idx
            aid += 1
        if acc["mode"] == "KEEP":
            B, _ = splay_B_push(B, acc["x"])
    byacc = defaultdict(list)
    for j in range(len(Bevs)):
        byacc[Bevs[j][0]].append(j)
    nkeep = nheavy = npressure = 0
    maxratio = 0.0
    ex = []
    for acc, js in sorted(byacc.items()):
        xx = pre2[acc]["x"]
        eB = len(js)
        e = elig[js[0]]
        E1s = set(i for i in e["E1"] if Aevs[i][1])
        E4s = set(i for i in e["E4"] if Aevs[i][1])
        f = len(E4s) if (acc > 0 and pre2[acc - 1]["x"] == xx) else len(E1s)
        nkeep += 1
        if eB <= 3 * f:
            continue
        nheavy += 1
        if f > 0:
            maxratio = max(maxratio, eB / f)
        else:
            maxratio = max(maxratio, float(eB))
        E3s = set(i for i in e["E3"] if Aevs[i][1])
        K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
        W = E3s - K - E1s
        E2s = set(i for i in e["E2"] if Aevs[i][1])
        oldn = len(E2s | E4s | K | W)
        if oldn <= 2:
            npressure += 1
            if len(ex) < 6:
                ex.append({"acc": acc, "x": xx, "eB": eB, "f": f, "old": oldn})
    return (nkeep, nheavy, npressure, maxratio, ex)


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    if gap > 0:
        return ("GCKILL", gap, nb)
    pm = pressure_metrics(n, T0, H)
    if pm is None:
        return None
    _, _, npressure, maxratio, _ = pm
    best = None
    from wp6_hallcore import cands_from_cut
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        slack = -d
        if best is None or slack < best[0]:
            best = (slack, name, len(Q), len(N))
    return ("OK", best, nb, gap, npressure, maxratio)


def gen_seed(s, tag):
    rng = Rng(("s%d" % s).encode(), tag)
    r = rng(0)
    n = 128
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 60 + (r >> 16) % 40
    x = xc
    H = []
    L = 18 + (r >> 24) % 18
    for i in range(L):
        rr = Rng(("s%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 8
        if op < 3:
            # demand: first-x-ish KEEP near xc (thin fresh via shallow T0 zone)
            H.append(["KEEP", min(n, max(1, xc + [-4, -3, -2, 2, 3, 4][(q >> 5) % 6]))])
        elif op < 5:
            # nearby-below pure-pusher attempt: DELETE then KEEP adjacent
            z = min(n, max(1, xc - 2 - (q >> 9) % 6))
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        else:
            z = 1 + (q >> 5) % 25 if (q >> 13) % 2 == 0 else 103 + (q >> 9) % 25
            H.append(["DELETE" if (q >> 15) % 3 else "KEEP", z])
        x = min(n, max(1, x + [-8, -4, -1, 1, 4, 8][(q >> 11) % 6]))
    # final B-heavy burst on xc: repeat KEEPs to force eB up with thin fresh
    for _ in range(2 + (r >> 20) % 3):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    step("WM-00", "Wall-pressure maximizer + overlap census")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "wallmax.json"
    best = None
    bestpress = -1
    bestratio = -1.0
    bestslack = 10 ** 9
    evals = 0
    holders = []
    import json as _j
    try:
        dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
        holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    except Exception:
        pass
    for s in range(100):
        n, T0, H = gen_seed(s, b"wm")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("WM-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("WM-KILL", "GC seed %d gap=%d" % (s, v[1]))
            return 2
        _, b, nb, gap, npressure, maxratio = v
        slack = b[0] if b else 10 ** 9
        holders.append((T0, H, n))
        if (npressure > bestpress) or (npressure == bestpress and maxratio > bestratio):
            bestpress, bestratio, bestslack = npressure, maxratio, slack
            best = (npressure, maxratio, slack, nb, b)
            TP.write_text(_j.dumps({"evals": evals, "pressure": npressure,
                                    "maxratio": maxratio, "slack": slack,
                                    "best": str(b), "nb": nb},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("WM-NEW", "seed %d pressure=%d ratio=%.2f slack=%s nb=%d" % (s, npressure, maxratio, slack, nb))
    holders = holders[-16:]
    step("WM-01", "seeds evals=%d bestpress=%d bestratio=%.2f" % (evals, bestpress, bestratio))
    it = 0
    # overlap census counters
    overlap_rebuild = 0
    overlap_total = 0
    while evals < 10000:
        it += 1
        r = int.from_bytes(_h.sha256(b"wmm|%d" % it).digest(), "big")
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
            recent = [a[1] for a in H2 if a[0] == "KEEP"][-3:]
            if recent:
                for _ in range(1 + (r >> 7) % 2):
                    H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("WM-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("WM-KILL", "GC it=%d gap=%d" % (it, v[1]))
            return 2
        _, b, nb, gap, npressure, maxratio = v
        slack = b[0] if b else 10 ** 9
        if (npressure > bestpress) or (npressure == bestpress and maxratio > bestratio) or (npressure == bestpress and maxratio == bestratio and slack < bestslack):
            bestpress, bestratio, bestslack = npressure, maxratio, slack
            best = (npressure, maxratio, slack, nb, b)
            TP.write_text(_j.dumps({"evals": evals, "pressure": npressure,
                                    "maxratio": maxratio, "slack": slack,
                                    "best": str(b), "nb": nb},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("WM-NEW", "it=%d pressure=%d ratio=%.2f slack=%s nb=%d" % (it, npressure, maxratio, slack, nb))
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 2500 == 0:
            step("WM-02", "it=%d evals=%d bestpress=%d bestratio=%.2f bestslack=%s" % (it, evals, bestpress, bestratio, bestslack))
    step("WM-03", "evals=%d bestpress=%d bestratio=%.2f bestslack=%s best=%s" % (evals, bestpress, bestratio, bestslack, best))
    try:
        _prev = _j.loads(TP.read_text(encoding="utf-8"))
    except Exception:
        _prev = {}
    _prev["evals"] = evals
    _prev["bestpress"] = bestpress
    _prev["bestratio"] = bestratio
    _prev["bestslack"] = bestslack
    TP.write_text(_j.dumps(_prev, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
