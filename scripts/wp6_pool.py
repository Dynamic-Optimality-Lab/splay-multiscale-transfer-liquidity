"""WP-6 STEP PE-00: pool-deficit diagnostic hunt (pressure map, not a kill path).

Per history: overflow-sum = Σ over B-heavy accesses (e_B > 3f) of (e_B - 3f),
with f = |E1| (non-repeat) or pristine-|E4| (repeat/DELETE-run);
FRESH-UNION = disjoint fresh sets over demanding accesses (8H);
R_old = N(all-B) minus FRESH-UNION (old-exclusive union);
deficit = overflow-sum - 3*|R_old| (pressure: violator needs deficit>0... and
buffers/Delta accounting on top; deficit>0 does NOT imply Hall kill).
Objective: maximize deficit (pressure map); ALSO track shortfall (exact Hall
kill >0 -> hallkill + §24 path) and GC-gap (kill >0 -> gckill).
Holder selection by deficit (overflow-heavy regimes HH underweights).
INCREMENTAL persist on best-deficit. Sealed files untouched.
NEW artifact: pooldef.json (+hallkill/gckill ONLY on kills).
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_offline import gc_gap, H_walk, vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def pool_metrics(n, T0, H):
    """(deficit, overflow, R_old, fresh_n, nheavy, shortfall, gap) or None."""
    G = build_graph(n, T0, H)
    if G is None:
        return None
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre = G["pre"]
    f, nb, _ = maxflow_cap3(G)
    sf = nb - f
    gap, _ = gc_gap(n, T0, H)
    byacc = defaultdict(list)
    for j in range(len(Bevs)):
        byacc[Bevs[j][0]].append(j)
    fresh_ids = set()
    overflow = 0
    # exact fresh via tagged elig (reuse G)
    G2 = G
    elig = G2["elig"]
    for acc, js in byacc.items():
        xx = pre[acc]["x"]
        e0 = elig[js[0]]
        E1s = set(i for i in e0["E1"] if Aevs[i][1])
        E4s = set(i for i in e0["E4"] if Aevs[i][1])
        if acc > 0 and pre[acc - 1]["x"] == xx:
            F = set(E4s)
        else:
            F = set(E1s)
        fresh_ids |= F
        eB = len(js)
        if eB > 3 * len(F):
            overflow += eB - 3 * len(F)
    Nall = set()
    for j in range(len(Bevs)):
        Nall |= G["adj"][j]
    R_old = set(a for a in Nall if a not in fresh_ids)
    deficit = overflow - 3 * len(R_old)
    return deficit, overflow, len(R_old), len(fresh_ids), sf, gap, nb


def mutate(H, n, r):
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
        recent = [a[1] for a in H2][-6:]
        base = recent[(r >> 5) % len(recent)] if recent else 1 + (r >> 13) % n
        stepd = [-2, -1, -1, 0, 1, 1, 2][(r >> 9) % 7]
        H2.append(["KEEP" if r % 2 else "DELETE", min(n, max(1, base + stepd))])
    elif op == 4 and H2:
        recent = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
        if recent:
            H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
        else:
            H2.append(["KEEP", 1 + (r >> 13) % n])
    elif len(H2) > 4:
        del H2[(r >> 5) % len(H2)]
    return H2


def main() -> int:
    step("PE-00", "Pool-deficit diagnostic hunt")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pooldef.json"
    best = None
    best_rec = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    for s in range(100):
        rng = Rng(("s%d" % s).encode(), b"pe")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"peh")
        H = H_walk(rr, n, 12 + (r >> 16) % 22, 1 + (r >> 24) % n)
        v = pool_metrics(n, T0, H)
        evals += 1
        if v is None:
            continue
        deficit, overflow, rold, freshn, sf, gap, nb = v
        if sf > 0:
            step("PE-KILL", "HALL seed %d" % s)
            TP.write_text(_j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if gap > 0:
            step("PE-KILL", "GC seed %d" % s)
            return 2
        if best is None or deficit > best:
            best = deficit
            best_rec = {"deficit": deficit, "overflow": overflow, "R_old": rold,
                        "fresh": freshn, "B": nb}
            TP.write_text(_j.dumps({"evals": evals, "best": best_rec}, indent=1, sort_keys=True,
                                   default=str), encoding="utf-8")
            step("PE-NEW", "seeds deficit=%d overflow=%d R_old=%d" % (deficit, overflow, rold))
        holders.append((T0, H, n))
    holders = holders[:16]
    step("PE-01", "seeds evals=%d best_deficit=%s" % (evals, best))
    it = 0
    while evals < 12000:
        it += 1
        r = int.from_bytes(_h.sha256(b"pem|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = mutate(H, n, r)
        v = pool_metrics(n, T0, H2)
        evals += 1
        if v is None:
            continue
        deficit, overflow, rold, freshn, sf, gap, nb = v
        if sf > 0:
            step("PE-KILL", "HALL it=%d" % it)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if gap > 0:
            step("PE-KILL", "GC it=%d" % it)
            return 2
        if deficit > best:
            best = deficit
            best_rec = {"deficit": deficit, "overflow": overflow, "R_old": rold,
                        "fresh": freshn, "B": nb}
            TP.write_text(_j.dumps({"evals": evals, "best": best_rec}, indent=1, sort_keys=True,
                                   default=str), encoding="utf-8")
            step("PE-NEW", "it=%d deficit=%d overflow=%d R_old=%d" % (it, deficit, overflow, rold))
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("PE-02", "it=%d evals=%d best_deficit=%s" % (it, evals, best))
    step("PE-03", "evals=%d best_deficit=%s %s" % (evals, best, best_rec))
    TP.write_text(_j.dumps({"evals": evals, "best": best_rec}, indent=1, sort_keys=True, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
