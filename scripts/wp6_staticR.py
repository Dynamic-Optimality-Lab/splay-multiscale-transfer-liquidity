"""PIVOT-25R-COMP §1: static R_T(x) evaluator (fold, NO rotations).

R_T(x) = q(x) - (B-depth dividend of splaying x), computed by backward
coefficient fold over the reversed double word from the terminal form
(zero if even depth, zig-form with side from key order if odd),
evaluated on X_0 fringe. Validated against replay-measured R_B.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[SRT %s] %s" % (sid, msg), flush=True)


def path_nodes(t, y):
    p, nd = [], t
    while nd is not None and nd[0] != y:
        p.append(nd)
        nd = nd[1] if y < nd[0] else nd[2]
    if nd is None:
        return None
    p.append(nd)
    return p


def sz(nd):
    if nd is None:
        return 0
    return 1 + sz(nd[1]) + sz(nd[2])


def depths_list(t):
    out = {}

    def go(nd, d):
        if nd is None:
            return
        out[nd[0]] = d
        go(nd[1], d + 1)
        go(nd[2], d + 1)
    go(t, 0)
    return out


def Tmap(pat, st):
    aL, aR, f, c = st
    f = list(f)
    if pat == "LL":
        return (aL - 2, aR - 1, [1 + aR, 2 + aR] + f, c + 1 + 2 * aR)
    if pat == "RR":
        return (aL - 1, aR - 2, [1 + aL, 2 + aL] + f, c + 1 + 2 * aL)
    if pat == "LR":
        return (aL - 1, aR - 1, [aL, 1 + aR] + f, c + aL + aR)
    if pat == "RL":
        return (aL - 1, aR - 1, [aR, 1 + aL] + f, c + aL + aR)
    raise AssertionError(pat)


def R_static(T, x):
    """Exact B-fringe demand R = q - (B-depth dividend), no rotations."""
    P = path_nodes(T, x)
    d = len(P) - 1
    if d == 0:
        return 0
    dd = depths_list(T)
    q = dd[x] // 2
    # double words bottom-up: pairs of turns from x side
    pats = []
    for i in range(d, 1, -2):
        gnd, pnd, xnd = P[i - 2], P[i - 1], P[i]
        sp = 0 if gnd[1] is pnd else 1
        sx = 0 if pnd[1] is xnd else 1
        pats.append({(0, 0): "LL", (1, 1): "RR", (0, 1): "LR",
                     (1, 0): "RL"}[(sp, sx)])
    # fringe masses m_k (k=0-based FROM X upward): off-path mass at the
    # ancestorSdk level: ancestor at depth d-1-k has off-child mass m_k.
    m = []
    for k in range(d):
        par = P[d - 1 - k]
        ch = P[d - k]
        off = par[2] if par[1] is ch else par[1]
        m.append(sz(off))
    # x children sizes
    xn = P[d]
    L, R = sz(xn[1]), sz(xn[2])
    if d % 2 == 0:
        st = (0, 0, [], 0)
    else:
        # zig terminal: side from key order vs ORIGINAL root (root
        # unchanged until zig since no double touched it: doubles need
        # g=root i.e. depth 2, but d is odd so last double ended depth 1)
        r0 = P[0][0]
        st = (-1, 0, [1], 0) if x < r0 else (0, -1, [1], 0)
    # backward fold: terminal first, i.e. LAST double first.
    for pat in reversed(pats):
        st = Tmap(pat, st)
    aL, aR, f, c = st
    R = c + aL * L + aR * R
    for j, fj in enumerate(f):
        R += fj * (m[j] if j < len(m) else 0)
    return R


def main():
    import random
    import wp6_cycle_ratio as O
    rng = random.Random(15)
    bad = 0
    for trial in range(300):
        n = rng.choice([6, 7, 8])
        Sh = O.shapes_of(list(range(1, n + 1)))
        T = copy.deepcopy(Sh[rng.randrange(len(Sh))])
        x = rng.randint(1, n)
        Rs = R_static(T, x)
        pT = V.to_ptr(copy.deepcopy(T))
        dd = V.depths_of(pT)
        q = dd.get(x, 0) // 2
        pT, _ = V.splay_cap(pT, x, 0, [])
        # depths post: recompute from ptr (now rooted at x)
        r = pT
        while r["p"] is not None:
            r = r["p"]
        dd2 = V.depths_of(r)
        # pre total depth: need fresh ptr (pT mutated)
        pT0 = V.to_ptr(copy.deepcopy(T))
        RB = sum(V.depths_of(pT0).values()) - sum(dd2.values())
        if Rs != q - RB:
            bad += 1
            if bad <= 3:
                step("MM", "trial %d n=%d x=%d Rstatic=%s q-RB=%s" %
                     (trial, n, x, Rs, q - RB))
    step("S", "R_static validation: %d/300 mismatches" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
