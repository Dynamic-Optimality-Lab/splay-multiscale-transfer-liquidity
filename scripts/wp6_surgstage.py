"""WP-6 STEP AS-01: surgical sterile-run falsifier (M1-guided).

Ops on state (n,T0,H) with victim key x:
  DEEPEN(x): append KEEP z (z!=x) with B-depth(x) strictly up, A-depth(x) same
             (M1 push in B, undisplaced in A) -> B-heavy pressure, E1 thin.
  STERILIZE(x): append access minimizing new-E3 for x (no fresh overlap).
  STRIKE(x): append KEEP x (demand at A-shallow/B-deep).
  SETUP(x): append DELETE x (E4 supply / reposition).
  GENERIC: mode/key/len mutate (AS-00 style).
Objective: max_b min-load-before (canonical least-loaded). Kill >=3
(starve.json + exit 2). Diagnostics: max sterile-run (consecutive B-events with
no fresh-0 entry), max frozen-core drain length.
NEW artifact: surgstage.json (+starve.json ONLY on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


def adepth(A, x):
    d, path = PE._depth_to(A, x)
    if not path or path[-1]["k"] != x:
        return None
    return d


def replay_AB(n, T0, H):
    A, B = to_ptr(T0), to_ptr(T0)
    for (m, x) in H:
        A, _ = splay_A(A, x)
        if m == "KEEP":
            B, _ = splay_B_push(B, x)
    return A, B


def maxminload(n, T0, H):
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return -2, None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    best = -1
    best_at = None
    for j in range(len(Bevs)):
        e = elig[j]
        cands = sorted((load.get(i, 0), i) for k in e for i in e[k] if Aevs[i][1])
        if not cands:
            continue
        if cands[0][0] > best:
            best, best_at = cands[0][0], j
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
        else:
            return 99, j
    return best, best_at


def sterile_run_info(n, T0, H):
    """Max consecutive B-events with no fresh-0 entry + max frozen-core drain."""
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    prevN = None
    run = 0
    maxrun = 0
    for j in range(len(Bevs)):
        e = elig[j]
        N = set(i for k in e for i in e[k] if Aevs[i][1])
        fresh0 = False
        if prevN is not None:
            for i in N - prevN:
                if load.get(i, 0) == 0:
                    fresh0 = True
                    break
        else:
            fresh0 = True
        if fresh0:
            run = 0
        else:
            run += 1
            maxrun = max(maxrun, run)
        prevN = N
        cands = sorted((load.get(i, 0), i) for i in N)
        if cands and cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
    return maxrun


def pick_victim(n, T0, H, r):
    """Choose victim: key with max (B-depth - A-depth) right now (B-heavy profile)."""
    A, B = replay_AB(n, T0, H)
    best = None
    bestd = -10 ** 9
    for x in range(1, n + 1):
        da, db = adepth(A, x), adepth(B, x)
        if da is None or db is None:
            continue
        if db - da > bestd:
            bestd, best = db - da, x
    if best is None:
        best = 1 + (r >> 7) % n
    return best


def op_deepen(n, T0, H, x, r):
    A, B = replay_AB(n, T0, H)
    da0, db0 = adepth(A, x), adepth(B, x)
    cands = []
    for z in range(1, n + 1):
        if z == x:
            continue
        import copy as _c
        A2 = _c.deepcopy(A)
        B2 = _c.deepcopy(B)
        A2, _ = splay_A(A2, z)
        B2, _ = splay_B_push(B2, z)
        da1, db1 = adepth(A2, x), adepth(B2, x)
        if da1 == da0 and db1 is not None and db0 is not None and db1 > db0:
            cands.append((db1 - db0, z))
    if not cands:
        return None
    cands.sort(reverse=True)
    return ["KEEP", cands[(r >> 3) % min(3, len(cands))][1]]


def op_sterilize(n, T0, H, x, r):
    """Access minimizing new A-rotated overlap with x's current B-triples."""
    from wp6_eventflow2 import build2
    A, B = replay_AB(n, T0, H)
    # current B-triples for x: simulate KEEP x B-part triples
    import copy as _c
    B2 = _c.deepcopy(B)
    B2, pushes = splay_B_push(B2, x)
    tri = set()
    for P in pushes:
        tri |= set(P)
    tri.add(x)
    best = None
    bestv = None
    keys = list(range(1, n + 1))
    start = (r >> 3) % n
    tried = 0
    for k in range(n):
        z = keys[(start + k) % n]
        if z == x or tried >= 12:
            continue
        tried += 1
        A2 = _c.deepcopy(A)
        A2, invs = splay_A(A2, z)
        ov = 0
        for S in invs:
            if set(S) & tri:
                ov += 1
        m = "DELETE" if (r >> (5 + k)) % 2 else "KEEP"
        if bestv is None or ov < bestv:
            bestv, best = ov, [m, z]
            if ov == 0:
                break
    return best


def main() -> int:
    step("AS-01", "Surgical sterile-run falsifier")
    import json
    best = -1
    evals = 0
    holders = []
    try:
        w = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json"))["witness"]
        holders.append((w["T0"], w["H"], w["n"], 2))
        step("AS01-W", "seeded M2 witness")
    except Exception as ex:
        step("AS01-W", "no M2 seed (%s)" % ex)
    for s in range(40):
        r = int.from_bytes(_h.sha256(b"as1|%d" % s).digest(), "big")
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        x0 = 1 + (r >> 24) % n
        H = [["DELETE", x0]]
        v, at = maxminload(n, T0, H)
        evals += 1
        holders.append((T0, H, n, v))
    holders.sort(key=lambda z: z[3], reverse=True)
    holders = holders[:12]
    maxster = 0
    it = 0
    ops = ["deepen", "sterilize", "strike", "setup", "generic"]
    while evals < 12000:
        it += 1
        r = int.from_bytes(_h.sha256(b"as1m|%d" % it).digest(), "big")
        T0, H, n, _ = holders[(r >> 2) % len(holders)]
        x = pick_victim(n, T0, H, r)
        op = ops[(r >> 5) % len(ops)]
        H2 = copy.deepcopy(H)
        if op == "deepen":
            a = op_deepen(n, T0, H2, x, r)
            H2.append(a if a else ["KEEP", 1 + (r >> 11) % n])
        elif op == "sterilize":
            a = op_sterilize(n, T0, H2, x, r)
            H2.append(a if a else ["DELETE", 1 + (r >> 11) % n])
        elif op == "strike":
            H2.append(["KEEP", x])
        elif op == "setup":
            H2.append(["DELETE", x])
        else:
            q = (r >> 9) % 3
            if q == 0 and H2:
                i = (r >> 11) % len(H2)
                H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
            elif q == 1 and H2:
                i = (r >> 11) % len(H2)
                H2[i][1] = 1 + (r >> 15) % n
            elif len(H2) < 70:
                H2.insert((r >> 11) % (len(H2) + 1), ["KEEP", 1 + (r >> 15) % n])
        if len(H2) > 70:
            H2 = H2[-70:]
        v, at = maxminload(n, T0, H2)
        evals += 1
        if v == -2:
            step("AS01-KILL", "present kill it=%d" % it)
            return 2
        if v == 99:
            step("AS01-KILL", "STARVATION it=%d bev=%s H=%s" % (it, at, H2))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "where": at, "H": H2}, indent=1, default=str),
                encoding="utf-8")
            return 2
        if v > best:
            best = v
            holders.append((T0, H2, n, v))
            holders.sort(key=lambda z: z[3], reverse=True)
            holders = holders[:12]
        else:
            if (r >> 6) % 4 == 0:
                holders.append((T0, H2, n, v))
                holders.sort(key=lambda z: z[3], reverse=True)
                holders = holders[:12]
        if it % 10 == 0:
            ms = sterile_run_info(n, T0, H2)
            if ms > maxster:
                maxster = ms
        if it % 1500 == 0:
            step("AS01-02", "it=%d evals=%d best=%d maxster=%d" % (it, evals, best, maxster))
    step("AS01-03", "evals=%d best=%d maxster=%d" % (evals, best, maxster))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "surgstage.json").write_text(
        json.dumps({"evals": evals, "best": best, "max_sterile_run": maxster},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
