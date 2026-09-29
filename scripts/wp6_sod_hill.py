"""WP-6 STEP SD2-00: SOD hillclimb (max damage, damage/d, scaling).

Fitness: raw damage = E(W,T)-E(W,S_xT)-3d AND ratio (E(W,T)-E(W,S_xT))/d.
Mutations: rekey W, extend/shorten W, swap x, vine chirality, reshuffle shape.
Scaling: damage vs |W| (linear => c*=inf, single hopeless) and vs n.
Also G_DEL direct: (E_B-A_K)/A_D and G_DEL=E_B-A_K-3*A_D on pair-access
histories + ratio-hunt (batch === E_B<=A_K+3*A_D, stronger than E_B-link).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def execc(t, W):
    c = 0
    cur = t
    for x in W:
        cur, evs = PE.splay_trace(cur, x)
        c += len(evs)
    return c


def damage_of(T0, x, W):
    T = to_ptr(T0)
    Tp, evx = PE.splay_trace(to_ptr(T0), x)
    d = len(evx)
    cL = execc(to_ptr(T0), W)
    cR = execc(Tp, W)
    return cL - cR - 3 * d, (cL - cR, d)


def main() -> int:
    # WP-6 STEP SD2-00: SOD hillclimb + G_DEL direct.
    step("SD2-00", "SOD hillclimb + G_DEL direct")
    import hashlib
    import random
    import copy

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"sd2|%s|%d" % (tag, c)).digest(), "big")

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    def shuf(n, seed):
        r = random.Random(seed)
        ks = list(range(1, n + 1))
        r.shuffle(ks)
        t = None

        def ins(t, k):
            if t is None:
                return [k, None, None]
            if k < t[0]:
                t[1] = ins(t[1], k)
            else:
                t[2] = ins(t[2], k)
            return t

        for k in ks:
            t = ins(t, k)
        return t

    best = -10**18
    bestr = -1.0
    ex = exr = None
    evals = 0
    # seeds
    pool = []
    for s in range(150):
        r = R(("s%d" % s).encode(), 0)
        n = [16, 32, 64][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0) if r % 2 else shuf(n, 9000 + s)
        x = 1 + (r >> 16) % n
        L = 6 + (r >> 24) % 30
        W = [1 + (R(("s%d" % s).encode(), 500 + i) % n) for i in range(L)]
        if W and W[0] == x:
            W[0] = 1 if x != 1 else n
        pool.append((T0, x, W, n))
        dg, (fut, d) = damage_of(T0, x, W)
        evals += 1
        if dg > best:
            best, ex = dg, (n, x, L, fut, d)
        if d > 0 and fut / d > bestr:
            bestr, exr = fut / d, (n, x, L, fut, d)
    step("SD2-01", "seeds: evals=%d best damage=%d %s best ratio=%.2f %s"
         % (evals, best, ex, bestr, exr))
    scored = []
    for (T0, x, W, n) in pool:
        dg, _ = damage_of(T0, x, W)
        scored.append((dg, T0, x, W, n))
    scored.sort(key=lambda z: -z[0])
    holders = [(T0, x, W, n) for (_, T0, x, W, n) in scored[:6]]
    it = 0
    while evals < 4000 and it < 3000:
        it += 1
        r = R(b"mut", it)
        T0, x, W, n = holders[(r >> 2) % len(holders)]
        W2 = list(W)
        op = r % 4
        if op == 0 and W2:
            W2[(r >> 5) % len(W2)] = 1 + (r >> 11) % n
        elif op == 1 and len(W2) < 60:
            W2.insert((r >> 5) % (len(W2) + 1), 1 + (r >> 11) % n)
        elif op == 2 and len(W2) > 2:
            del W2[(r >> 5) % len(W2)]
        else:
            x = 1 + (r >> 11) % n
            if W2 and W2[0] == x:
                W2[0] = 1 if x != 1 else n
        T02 = copy.deepcopy(T0)
        dg, (fut, d) = damage_of(T02, x, W2)
        evals += 1
        if dg > best:
            best, ex = dg, (n, x, len(W2), fut, d)
            holders.append((T02, x, W2, n))
            holders = holders[-10:]
        if d > 0 and fut / d > bestr:
            bestr, exr = fut / d, (n, x, len(W2), fut, d)
    step("SD2-02", "evals=%d best damage=%d %s best fut/d=%.2f %s"
         % (evals, best, ex, bestr, exr))
    # G_DEL direct on pair-access histories
    wG = -10**18
    exG = None
    wJ = 0.0
    exJ = None
    for t in range(400):
        rng_r = R(("g%d" % t).encode(), 0)
        n = [16, 32, 64, 128][rng_r % 4]
        T0 = vine(n, (rng_r >> 8) % 2 == 0)
        L = 4 + (rng_r >> 16) % 20
        x = 1 + (rng_r >> 24) % n
        H = []
        for i in range(L):
            r = R(("g%d" % t).encode(), 700 + i)
            if i % 5 == 4:
                y = min(n, max(1, x + [-32, -16, 16, 32][(r >> 5) % 4]))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append(["KEEP" if r % 3 else "DELETE", x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("SD2-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        EB = AK = AD = 0
        for acc in pre:
            eA = sum(1 for z in acc["sites"] if z)
            if acc["mode"] == "KEEP":
                EB += len(acc["Bev"])
                AK += eA
            else:
                AD += eA
        G = EB - AK - 3 * AD
        if G > wG:
            wG, exG = G, (t, EB, AK, AD)
        if AD > 0 and (EB - AK) / AD > wJ:
            wJ, exJ = (EB - AK) / AD, (t, EB, AK, AD)
    step("SD2-03", "G_DEL worst=%d %s (want<=0); J_DEL worst=%.3f %s (want<=3)"
         % (wG, exG, wJ, exJ))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "sod_hill.json").write_text(
        json.dumps({"evals": evals, "best_damage": best, "damage_ex": ex,
                    "best_ratio": bestr, "ratio_ex": exr,
                    "G_DEL": wG, "G_ex": exG, "J_DEL": wJ, "J_ex": exJ},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
