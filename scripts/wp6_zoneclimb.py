"""WP-6 ZONECLIMB: mindeg>=4 violator-zone Delta climb (C118b).

Mode-A 8AC-ZONE falsifier with CONTINUOUS objective (not binary shortfall):
maximize Delta(Q) over candidate Qs with mindeg(N(Q))>=4 (8B signature).
KILL tiers: Delta>=1 -> hallkill.json + exit 2 (Hall kill = GC-STATIC REFUTED).
Thinning: Delta>=-7 (beats K2B max -8 at 12k vine-only) -> record + continue.
Candidates/history: full-B + access slices + min-cut sides + biased randoms.
Generators: vine/balanced/random-BST T0, n=8..128, L=12..40, B-heavy bias +
repeat bias + pressure recipe (DELETE-x-root + KEEP-burst) + pusher cycles.
Hillclimb 15k evals on best holders. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, degrees, cands_from_cut
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from wp6_killshot3 import balanced, random_bst


def step(sid, msg):
    print("[WP-6][ZONECLIMB %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def zone_best(n, T0, H, seed=None):
    """Returns kill-tuple or ("OK", best_zone, nb). Scans cut/access/full slices
    + 20 deterministic random subsets (seeded); tracks max Delta with mindeg>=4."""
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    best = None
    seen = set()
    cands = cands_from_cut(G, lv) + [("all", list(range(len(G["Bevs"]))))]
    if seed is not None and len(G["Bevs"]) > 0:
        for t in range(20):
            r1 = int.from_bytes(_h.sha256(b"zcr|%d|%d" % (seed, t)).digest(), "big")
            k = 1 + r1 % min(len(G["Bevs"]), 30)
            Q = sorted((r1 >> (11 * (i + 1))) % len(G["Bevs"]) for i in range(k))
            cands.append(("rand%d" % t, Q))
    for name, Q in cands:
        if not Q:
            continue
        t = tuple(sorted(Q))
        if t in seen:
            continue
        seen.add(t)
        Qs = set(Q)
        deg = degrees(G, Qs)
        if not deg:
            continue
        if min(deg.values()) >= 4:
            d, N = delta_of(G, Qs)
            if d > 0:
                return ("QKILL", d, (name, len(Qs), len(N)))
            if best is None or d > best[0]:
                best = (d, name, len(Qs), len(N))
    return ("OK", best, nb)


def gen_seed(s, tag):
    rng = Rng(("zc%d" % s).encode(), tag)
    r = rng(0)
    n = [8, 12, 16, 24, 32, 48, 64, 96, 128][r % 9]
    fam = (r >> 5) % 3
    if fam == 0:
        T0 = vine(n, (r >> 8) % 2 == 0)
    elif fam == 1:
        T0 = balanced(n)
    else:
        T0 = random_bst(n, rng, s)
    xc = 2 + (r >> 16) % max(1, n - 2)
    H = []
    L = 12 + (r >> 24) % 20
    for i in range(L):
        rr = Rng(("zc%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 10
        if op < 3:
            H.append(["DELETE", xc])
        elif op < 5:
            H.append(["KEEP", xc])
        elif op < 7:
            z = min(n, max(1, xc + [-3, -2, -1, 1, 2, 3][(q >> 9) % 6]))
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        else:
            H.append(["KEEP" if (q >> 5) % 3 else "DELETE", 1 + (q >> 11) % n])
    for _ in range(1 + (r >> 20) % 2):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("ZC-00", "mindeg>=4 zone-Delta climb (8AC-ZONE falsifier)")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "zoneclimb.json"
    best = -10 ** 9
    bestex = None
    thin = False
    evals = 0
    holders = []
    BUDGET = 15000
    for s in range(300):
        n, T0, H = gen_seed(s, b"zc")
        v = zone_best(n, T0, H, s)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("ZC-KILL", "HALL seed %d shortfall=%d nb=%d (GC-STATIC REFUTED)" % (s, v[1], v[2]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "QKILL":
            step("ZC-KILL", "ZONE-Q seed %d Delta=%d %s (GC-STATIC REFUTED)" % (s, v[1], v[2]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H, "Q": v[2]}, indent=1, default=str),
                encoding="utf-8")
            return 2
        _, b, nb = v
        holders.append((T0, H, n))
        if b is not None and b[0] > best:
            best = b[0]
            bestex = (s, n, nb, b)
            step("ZC-NEW", "seed %d n=%d zoneDelta=%d %s Q=%d N=%d" % (s, n, b[0], b[1], b[2], b[3]))
            TP.write_text(json.dumps({"evals": evals, "best": best, "bestex": str(bestex)},
                                     indent=1, default=str), encoding="utf-8")
            if best >= -7 and not thin:
                thin = True
                step("ZC-THIN", "wall-thinning vs K2B (-8): zoneDelta=%d" % best)
    holders = holders[-16:]
    step("ZC-01", "seeds evals=%d bestzone=%s" % (evals, best))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"zcm|%d" % it).digest(), "big")
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
        v = zone_best(n, T0, H2, 100000 + it)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("ZC-KILL", "HALL it=%d shortfall=%d (GC-STATIC REFUTED)" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "QKILL":
            step("ZC-KILL", "ZONE-Q it=%d Delta=%d (GC-STATIC REFUTED)" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2, "Q": v[2]}, indent=1, default=str),
                encoding="utf-8")
            return 2
        _, b, nb = v
        if b is not None and b[0] > best:
            best = b[0]
            bestex = (it, n, nb, b)
            step("ZC-NEW", "it=%d n=%d zoneDelta=%d %s Q=%d N=%d" % (it, n, b[0], b[1], b[2], b[3]))
            TP.write_text(json.dumps({"evals": evals, "best": best, "bestex": str(bestex)},
                                     indent=1, default=str), encoding="utf-8")
            holders.append((T0, H2, n))
            holders = holders[-16:]
            if best >= -7 and not thin:
                thin = True
                step("ZC-THIN", "wall-thinning vs K2B (-8): zoneDelta=%d" % best)
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 2500 == 0:
            step("ZC-02", "it=%d evals=%d bestzone=%d" % (it, evals, best))
    step("ZC-03", "evals=%d bestzone=%d thin=%s NO KILL" % (evals, best, thin))
    import json as _j
    try:
        _prev = _j.loads(TP.read_text(encoding="utf-8"))
    except Exception:
        _prev = {}
    _prev["evals"] = evals
    _prev["best"] = best
    _prev["thin"] = thin
    _prev["nokill"] = True
    TP.write_text(_j.dumps(_prev, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
