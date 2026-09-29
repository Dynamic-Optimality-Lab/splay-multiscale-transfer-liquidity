"""WP-6 STEP GD-00: G_DEL on one-DELETE histories (SEC0 verification).

Pair-access history: DELETE x, then W all marked KEEP.
  A_D = sited A-StepEvs on DELETE (= c(T,x) if sited),
  A_K = sited A-StepEvs on KEEPs (= C(W,S_xT) sited),
  E_B = B-StepEvs (= C(W,T) since B untouched by DELETE).
  G_DEL = E_B - A_K - 3*A_D  (want<=0; >0 kills batch E_B<=A_K+3*A_D).
If SOD damage(T,x,W)>0 replays to G_DEL>0 here, batch is FALSE and the
earlier G_DEL hunt (returning 0) simply missed one-DELETE shapes.
Also record unsited counts (equivalence needs sitedness) + present-domain.
Hillclimb on G_DEL: rekey/extend/swap W, swap x, chirality, shapes.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def gdel_of(n, T0, x, W):
    H = [["DELETE", x]] + [["KEEP", w] for w in W]
    try:
        pre = E.precompute(n, T0, H)
    except ValueError:
        return None
    AK = AD = EB = 0
    uns = 0
    for acc in pre:
        eA = sum(1 for z in acc["sites"] if z)
        uns += len(acc["Aev"]) - eA
        if acc["mode"] == "KEEP":
            EB += len(acc["Bev"])
            AK += eA
        else:
            AD += eA
    return EB - AK - 3 * AD, (EB, AK, AD, uns)


def main() -> int:
    # WP-6 STEP GD-00: one-DELETE G_DEL hunt.
    step("GD-00", "G_DEL on one-DELETE histories")
    import hashlib
    import random
    import copy

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"gd|%s|%d" % (tag, c)).digest(), "big")

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
    ex = None
    evals = 0
    pool = []
    for s in range(200):
        r = R(("s%d" % s).encode(), 0)
        n = [16, 32, 64][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0) if r % 2 else shuf(n, 3000 + s)
        x = 1 + (r >> 16) % n
        L = 6 + (r >> 24) % 30
        pat = (r >> 30) % 3
        if pat == 0:
            W = [1, n] * (L // 2 + 1)
            W = W[:L]
        elif pat == 1:
            a = 1 + (r >> 33) % n
            W = [a] * L
        else:
            W = [1 + (R(("s%d" % s).encode(), 900 + i) % n) for i in range(L)]
        v = gdel_of(n, T0, x, W)
        evals += 1
        if v is not None:
            pool.append((T0, x, W, n))
            if v[0] > best:
                best, ex = v[0], (n, x, L, v[1])
    step("GD-01", "seeds: evals=%d best G_DEL=%d %s" % (evals, best, ex))
    scored = []
    for (T0, x, W, n) in pool:
        v = gdel_of(n, T0, x, W)
        if v is not None:
            scored.append((v[0], T0, x, W, n))
    scored.sort(key=lambda z: -z[0])
    holders = [(T0, x, W, n) for (_, T0, x, W, n) in scored[:8]]
    it = 0
    while evals < 5000 and it < 4000:
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
        v = gdel_of(n, copy.deepcopy(T0), x, W2)
        evals += 1
        if v is not None and v[0] > best:
            best, ex = v[0], (n, x, len(W2), v[1])
            holders.append((copy.deepcopy(T0), x, W2, n))
            holders = holders[-12:]
            if best > 0:
                break
    step("GD-02", "evals=%d best G_DEL=%d %s (EB,AK,AD,uns=%s)" % (evals, best, ex[0] if ex else None, ex[1] if ex else None))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gdel_one.json").write_text(
        json.dumps({"evals": evals, "best": best, "ex": ex,
                    "verdict": "BATCH FALSE" if best > 0 else "one-DELETE holds (batch alive here)"},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
