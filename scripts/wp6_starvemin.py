"""WP-6 STEP MZ-00: starvation-witness minimizer + anatomy (Stage-B kill banking).

Loads starve.json H (n=128 assumed from keys; tries both vines, keeps the one
that starves). Greedy access-removal fixpoint: drop each access while starvation
persists (minload>=3 somewhere) and present-legality holds. Then anatomy of the
starving event: access/key/e_A/e_B/fresh-f/K-0/classes/ages/ladder histories of
the 5 blockers; E1-CAP zone check (starving access MUST be B-heavy, else the
E1-CAP proof is wrong); margin; synchrony.
Writes: starve_min.json (n, T0left, Hmin, starve_at, anatomy). Sealed files
untouched (starve.json itself is C36+ unsealed output; do NOT overwrite route
ledgers here -- banking commit follows after review).
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_spread import vine
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def starve_info(n, T0, H):
    """None if illegal; else (best_minload, first_starve or None, B)."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    best = -1
    first = None
    for j in range(len(Bevs)):
        e = elig[j]
        N = set(i for k in e for i in e[k] if Aevs[i][1])
        cands = sorted((load.get(i, 0), i) for i in N)
        if not cands:
            continue
        best = max(best, cands[0][0])
        if cands[0][0] >= 3 and first is None:
            first = j
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
    return best, first, len(Bevs)


def main() -> int:
    step("MZ-00", "Starvation-witness minimizer + anatomy")
    import json
    d = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json"))
    H = d["H"]
    n = 128
    T0 = None
    for left in (True, False):
        T = vine(n, left)
        r = starve_info(n, T, H)
        if r is not None and r[1] is not None:
            T0 = T
            T0left = left
            break
    if T0 is None:
        step("MZ-FAIL", "could not reproduce starvation")
        return 2
    step("MZ-01", "reproduced left=%s best=%s first=%s B=%s" % (T0left, r[0], r[1], r[2]))
    Hmin = copy.deepcopy(H)
    changed = True
    while changed:
        changed = False
        for i in range(len(Hmin)):
            H2 = Hmin[:i] + Hmin[i + 1:]
            if not H2:
                continue
            r2 = starve_info(n, T0, H2)
            if r2 is not None and r2[1] is not None:
                Hmin = H2
                changed = True
                break
    r = starve_info(n, T0, Hmin)
    step("MZ-02", "minimized lenH %d -> %d best=%s first=%s B=%s" % (len(H), len(Hmin), r[0], r[1], r[2]))
    # anatomy of first starving event
    g = build_tagged(n, T0, Hmin)
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
    load = {}
    firstinfo = None
    for j in range(len(Bevs)):
        acc = Bevs[j][0]
        xx = pre2[acc]["x"]
        e = elig[j]
        E1s = set(i for i in e["E1"] if Aevs[i][1])
        E3s = set(i for i in e["E3"] if Aevs[i][1])
        K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
        W = E3s - K - E1s
        E2s = set(i for i in e["E2"] if Aevs[i][1])
        E4s = set(i for i in e["E4"] if Aevs[i][1])
        N = E1s | E3s | E2s | E4s
        cands = sorted((load.get(i, 0), i) for i in N)
        if cands and cands[0][0] >= 3 and firstinfo is None:
            eA = sum(1 for z in pre2[acc]["sites"] if z)
            eB = sum(1 for jj in range(len(Bevs)) if Bevs[jj][0] == acc)
            firstinfo = {"bev": j, "acc": acc, "x": xx, "eA": eA, "eB": eB,
                         "nanc": len(N),
                         "E1": sorted(E1s), "E2": sorted(E2s), "E4": sorted(E4s),
                         "K": sorted(K), "W": sorted(W),
                         "loads": sorted(load.get(i, 0) for i in N),
                         "ages": {i: acc - acc_of.get(i, acc) for i in N}}
        if cands and cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
    step("MZ-03", "anatomy: %s" % json.dumps(firstinfo, default=str))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json").write_text(
        json.dumps({"n": n, "T0left": T0left, "Hmin": Hmin, "lenH": len(Hmin),
                    "best": r[0], "first": r[1], "B": r[2], "anatomy": firstinfo},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
