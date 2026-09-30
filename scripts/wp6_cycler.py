"""WP-6 CYCLER: cap-exhaustion cycle killer — the purified residual (C59).

8S/8T/8U leave exactly one recipe open: MANY A-trivial micro-bursts on one x with
K capped (few past x-imprints ×3) and transients avoided, each cycle re-deepened by
minimal pushers. If cycles self-fund (setup+pusher supply >= burst/3), wall = contention-only.
Cycle = [pushers (KEEP z near x, k=0..3)] + [DELETE x (A-root)] + [KEEP x burst].
Objective: shortfall>0 -> hallkill exit 2; else min cycle-margin (3*newAnchored - dem).
Artifact: cycler.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from solver import encode as E
from wp6_eventflow_abl import build_tagged


def step(sid, msg):
    print("[WP-6][CYCLER %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def cycle_margins(n, T0, H):
    """Per (DELETE x, KEEP x-burst) cycle: (dem, newAnchoredCount, margin)."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    pre2 = g["pre"]
    # map acc -> e_B, and count sited Aevs per acc (new anchored supply units)
    from collections import defaultdict
    accB = defaultdict(int)
    for j in range(len(Bevs)):
        accB[Bevs[j][0]] += 1
    accA = defaultdict(int)
    for idx, acc in enumerate(pre2):
        accA[idx] = sum(1 for z in acc["sites"] if z)
    worst = None
    ncyc = 0
    for idx in range(1, len(pre2)):
        a0, a1 = pre2[idx - 1], pre2[idx]
        if a0["mode"] == "DELETE" and a1["mode"] == "KEEP" and a0["x"] == a1["x"]:
            dem = accB.get(idx, 0)
            new = accA[idx - 1] + accA[idx]
            m = 3 * new - dem
            ncyc += 1
            if worst is None or m < worst[0]:
                worst = (m, dem, new, idx, a1["x"])
    return (ncyc, worst)


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
    cm = cycle_margins(n, T0, H)
    if cm is None:
        return None
    return ("OK", nb, gap, cm)


def gen_seed(s, tag):
    rng = Rng(("cy%d" % s).encode(), tag)
    r = rng(0)
    n = [16, 32, 64, 128][r % 4]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % (n - 2)
    H = []
    ncyc = 3 + (r >> 24) % 5
    for c in range(ncyc):
        rr = Rng(("cy%d" % s).encode(), tag + b"c%d" % c)
        q = rr(7)
        npush = (q >> 3) % 4
        for p in range(npush):
            z = min(n, max(1, xc + [-3, -2, -1, 1, 2, 3][(q >> (5 + 2 * p)) % 6]))
            H.append(["KEEP", z])
        H.append(["DELETE", xc])
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("CY-00", "cap-exhaustion cycle killer")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "cycler.json"
    bestm = None
    evals = 0
    holders = []
    BUDGET = 10000
    for s in range(300):
        n, T0, H = gen_seed(s, b"cy")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("CY-KILL", "HALL seed %d n=%d shortfall=%d" % (s, n, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("CY-KILL", "GC seed %d" % s)
            return 2
        _, nb, gap, (ncyc, worst) = v
        holders.append((T0, H, n))
        if worst is not None and (bestm is None or worst[0] < bestm[0]):
            bestm = worst
            step("CY-NEW", "seed %d n=%d margin=%d dem=%d new=%d acc=%d x=%d" % (s, n, *worst[:5]))
            TP.write_text(json.dumps({"evals": evals, "bestmargin": bestm}, indent=1, default=str), encoding="utf-8")
    holders = holders[-16:]
    step("CY-01", "seeds evals=%d bestmargin=%s" % (evals, bestm))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"cym|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 80:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("CY-KILL", "HALL it=%d n=%d shortfall=%d H=%s" % (it, n, v[1], H2))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("CY-KILL", "GC it=%d" % it)
            return 2
        _, nb, gap, (ncyc, worst) = v
        if worst is not None and (bestm is None or worst[0] < bestm[0]):
            bestm = worst
            step("CY-NEW", "it=%d n=%d margin=%d dem=%d new=%d acc=%d x=%d" % (it, n, *worst[:5]))
            TP.write_text(json.dumps({"evals": evals, "bestmargin": bestm}, indent=1, default=str), encoding="utf-8")
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 2500 == 0:
            step("CY-02", "it=%d evals=%d bestmargin=%s" % (it, evals, bestm))
    step("CY-03", "evals=%d bestmargin=%s NO KILL" % (evals, bestm))
    TP.write_text(json.dumps({"evals": evals, "bestmargin": bestm, "nokill": True}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
