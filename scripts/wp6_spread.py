"""WP-6 STEP SC-00: spread-3 + 2-blocker convergence hunt + dormancy census.

For each history/B-event (canonical least-loaded, causal builders):
  spread(b) = max-min load in N; blockers(b) = #{load>=3 in N};
  dormancy episodes: per source, gaps (eligible, absent, eligible) with load
  delta across gap (dormant-while-others-climb events).
Adversarial: maximize (blockers, spread) lexicographically; sustain-drain bias
(repeat-KEEP, B-heavy, long tenure). Kill: minload>=3 (starve.json + exit 2).
spread>=3 found => SAVE witness + CONTINUE (spread alone does not starve).
2-blockers found => SAVE (convergence pair!) + CONTINUE toward all-3.
NEW artifact: spread.json (+starve.json ONLY on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class Rng:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag

    def __call__(self, c):
        return int.from_bytes(_h.sha256(self.tag + b"|%s|%d" % (self.s, c)).digest(), "big")


def H_walk(rr, n, L, x0):
    H = []
    x = x0
    for i in range(L):
        r = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
    return H


def scan(n, T0, H):
    """(maxspread, spread_at, maxblock, block_at, minload_best, starve, dorm)."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    ms = -1
    ms_at = None
    mb = -1
    mb_at = None
    mlb = -1
    starve = None
    last_seen = {}
    prevN = None
    dorm = 0
    maxdorm_climb = 0
    for j in range(len(Bevs)):
        e = elig[j]
        N = set(i for k in e for i in e[k] if Aevs[i][1])
        if N:
            ls = [load.get(i, 0) for i in N]
            sp = max(ls) - min(ls)
            if sp > ms:
                ms, ms_at = sp, j
            nb = sum(1 for v in ls if v >= 3)
            if nb > mb:
                mb, mb_at = nb, j
        # dormancy: returning after a gap (absent >=1 consecutive B-event)
        for i in N:
            if i in last_seen and last_seen[i] < j - 1:
                dorm += 1
            last_seen[i] = j
        prevN = N
        cands = sorted((load.get(i, 0), i) for i in N)
        if not cands:
            continue
        mlb = max(mlb, cands[0][0])
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
        else:
            starve = j
    return ms, ms_at, mb, mb_at, mlb, starve, dorm


def main() -> int:
    step("SC-00", "Spread-3 + 2-blocker convergence hunt")
    import json
    best_sp = -1
    best_bl = -1
    spwit = None
    blwit = None
    evals = 0
    holders = []
    for s in range(100):
        rng = Rng(("s%d" % s).encode(), b"sc")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"sch")
        H = H_walk(rr, n, 14 + (r >> 16) % 24, 1 + (r >> 24) % n)
        v = scan(n, T0, H)
        evals += 1
        if v is None:
            step("SC-KILL", "present kill s=%d" % s)
            return 2
        ms, at, mb, bat, mlb, st, dorm = v
        if st is not None:
            step("SC-KILL", "STARVATION s=%d" % s)
            return 2
        if ms > best_sp:
            best_sp = ms
            if ms >= 3 and spwit is None:
                spwit = {"n": n, "H": copy.deepcopy(H), "at": at}
        if mb > best_bl:
            best_bl = mb
            if mb >= 2 and blwit is None:
                blwit = {"n": n, "H": copy.deepcopy(H), "at": bat}
        holders.append((T0, H, n, mb, ms))
    holders.sort(key=lambda z: (z[3], z[4]), reverse=True)
    holders = holders[:14]
    step("SC-01", "seeds evals=%d best_spread=%d best_blockers=%d" % (evals, best_sp, best_bl))
    it = 0
    while evals < 25000:
        it += 1
        r = int.from_bytes(_h.sha256(b"scm|%d" % it).digest(), "big")
        T0, H, n, _, _ = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 70:
            keeps = [a[1] for a in H2 if a[0] == "KEEP"][-5:]
            k = keeps[(r >> 5) % len(keeps)] if keeps else 1 + (r >> 13) % n
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", k])
        elif op == 3 and H2:
            keeps = [a[1] for a in H2 if a[0] == "KEEP"][-5:]
            if keeps:
                H2.append(["KEEP", keeps[(r >> 5) % len(keeps)]])
            else:
                H2.append(["KEEP", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = scan(n, T0, H2)
        evals += 1
        if v is None:
            continue
        ms, at, mb, bat, mlb, st, dorm = v
        if st is not None:
            step("SC-KILL", "STARVATION it=%d" % it)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if (mb, ms) > (best_bl, best_sp):
            best_bl, best_sp = mb, ms
            holders.append((T0, H2, n, mb, ms))
            holders.sort(key=lambda z: (z[3], z[4]), reverse=True)
            holders = holders[:14]
            if mb >= 2 and blwit is None:
                blwit = {"n": n, "H": copy.deepcopy(H2), "at": bat}
                step("SC-WIT", "2-BLOCKERS it=%d at=%s" % (it, bat))
            if ms >= 3 and spwit is None:
                spwit = {"n": n, "H": copy.deepcopy(H2), "at": at}
                step("SC-WIT", "SPREAD3 it=%d at=%s" % (it, at))
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n, mb, ms))
            holders.sort(key=lambda z: (z[3], z[4]), reverse=True)
            holders = holders[:14]
        if it % 5000 == 0:
            step("SC-02", "it=%d evals=%d spread=%d blockers=%d" % (it, evals, best_sp, best_bl))
    step("SC-03", "evals=%d spread=%d blockers=%d" % (evals, best_sp, best_bl))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "spread.json").write_text(
        json.dumps({"evals": evals, "best_spread": best_sp, "best_blockers": best_bl,
                    "spread_witness": spwit, "blocker_witness": blwit},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
