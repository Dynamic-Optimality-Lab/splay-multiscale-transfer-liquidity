"""WP-6 PHIDRAIN: cumulative-Phi drain hillclimb (C158).

8AC-PREFIX reduces Hall to prefix counts: Phi(t) = 3*SA(<=t) - EB(<=t) >= 0.
A negative Phi REFUTES prefix-GC, hence (by the equivalence) HALL and
GC-STATIC. This hillclimbs cumulative drain directly (bypassing all
matching subtlety): reward per-access (e_B - 3*e_A) [B-splashes, A-triviality]
+ B-depth building, with key migration for fresh supply-free states.
Operations: KEEP/DELETE on migrated/neighbor keys, DELETE-then-KEEP
repeat-pushers (E2-hole supply-free pattern), far-key avoidance.
Tracks min Phi + stall anatomy ( WHY the drain stops, if it does: no-ops?
repeats stall? migration dries up? A-banking forced?). Artifact:
phidrain.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][PHIDRAIN %s] %s" % (sid, msg), flush=True)


def depths_of(T):
    dd = {}
    stack = [(T, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        dd[nd["k"]] = d
        stack.append((nd["l"], d + 1))
        stack.append((nd["r"], d + 1))
    return dd


def eval_hist(n, T0, H):
    """Returns (minPhi, diagnosed) with per-access instant drain + depths."""
    try:
        pre = E.precompute(n, T0, H)
        bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
    except Exception:
        return None
    if bad:
        return None
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    minphi = 0
    worst = None
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        eA = len(invs)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            eB = len(pushes)
        else:
            eB = 0
        SA += eA
        EB += eB
        phi = 3 * SA - EB
        if phi < minphi:
            minphi = phi
            worst = (idx, acc["mode"], acc["x"], eA, eB)
    return (minphi, worst)


def root_key(T):
    return T["k"] if T is not None else None


def hillclimb(s):
    rng = Rng(("pd%d" % s).encode(), b"pd")
    r = rng(0)
    n = [64, 128, 256][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % (n - 2)
    H = []
    best = 0
    bestH = None
    # greedy build: each step try candidate ops, keep max instant drain
    L = 80
    for i in range(L):
        # current roots (A-root KEEP = guaranteed A-trivial splash attempt)
        pre = E.precompute(n, T0, H)
        A2, B2 = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            A2, _ = splay_A(A2, acc["x"])
            if acc["mode"] == "KEEP":
                B2, _ = splay_B_push(B2, acc["x"])
        cands = []
        # neighbor keys + migrated far keys + repeat-pushers
        jumps = [-16, -8, -4, -2, -1, 1, 2, 4, 8, 16]
        rr = Rng(("pd%d" % s).encode(), b"pd" + bytes([i % 200]))
        q = rr(7000 + i)
        base = [min(n, max(1, xc + j)) for j in jumps]
        if (q >> 3) % 3 == 0:
            base.append(1 + (q >> 7) % n)
        for z in base:
            cands.append(["KEEP", z])
            cands.append(["DELETE", z])
        # repeat-pusher pairs
        cands.append(["DELETE", xc])
        cands.append(["KEEP", xc])
        # A-root KEEP (A-trivial by construction: supply-free splash if B-deep)
        if A2 is not None:
            cands.append(["KEEP", A2["k"]])
        bestop = None
        bestdrain = -10 ** 9
        for op in cands:
            HH = H + [op]
            v = eval_hist(n, T0, HH)
            if v is None:
                continue
            # instant drain of last op + depth bonus
            pre = E.precompute(n, T0, HH)
            A2, B2 = to_ptr(T0), to_ptr(T0)
            for acc in pre[:-1]:
                A2, _ = splay_A(A2, acc["x"])
                if acc["mode"] == "KEEP":
                    B2, _ = splay_B_push(B2, acc["x"])
            A2, invs = splay_A(A2, pre[-1]["x"])
            eA = len(invs)
            if pre[-1]["mode"] == "KEEP":
                B2, pushes = splay_B_push(B2, pre[-1]["x"])
                eB = len(pushes)
            else:
                eB = 0
            drain = eB - 3 * eA
            if drain > bestdrain:
                bestdrain = drain
                bestop = op
        if bestop is None:
            break
        H.append(bestop)
        if bestop[0] == "KEEP":
            xc = bestop[1]
        v = eval_hist(n, T0, H)
        if v is not None and v[0] < best:
            best = v[0]
            bestH = (list(H), v[1])
        if best < 0:
            break
    return best, bestH, n


def main() -> int:
    step("PD-00", "cumulative-Phi drain hillclimb (refute prefix-GC)")
    best = 0
    bestex = None
    for s in range(150):
        b, bex, n = hillclimb(s)
        if b < best:
            best = b
            bestex = (s, n, bex)
            step("PD-NEW", "minPhi=%d seed=%d" % (best, s))
        if best < 0:
            step("PD-KILL", "NEGATIVE PHI (prefix-GC REFUTED, hence HALL)")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "phikill.json").write_text(
                json.dumps({"kill": True, "minPhi": best, "ex": bestex}, indent=1, default=str),
                encoding="utf-8")
            return 2
    out = {"evals": 150, "minPhi": best, "bestex": bestex}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "phidrain.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("PD-01", json.dumps(out, sort_keys=True, default=str)[:800])
    return 0


if __name__ == "__main__":
    sys.exit(main())
