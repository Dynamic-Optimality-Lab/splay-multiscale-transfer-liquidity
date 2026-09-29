"""WP-6 STEP SD3-00: damage tail anatomy + mass (why does batch survive?).

Single SOD-3 dead (c*=12). Batch G_DEL<=0 holds. Resolution must be
tail-mass: bad removals (damage_future>2d) rare/small vs good removals.
Measure: distribution of damage_future/d (d-weighted!); tail-d-fraction
(sum d over bad / sum d total); anatomy of bad tail (pump/setup/genesis/
tenure-shaped? exclusive or shared funding?); nearby-access counts.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE


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


def main() -> int:
    # WP-6 STEP SD3-00: tail anatomy.
    step("SD3-00", "Damage tail anatomy + mass")
    import hashlib
    import random

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"sd3|%s|%d" % (tag, c)).digest(), "big")

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

    import statistics
    ratios = []
    tail_d = 0
    total_d = 0
    tail_cases = []
    n_cases = 0
    for t in range(500):
        r = R(("s%d" % t).encode(), 0)
        n = [16, 32, 64][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0) if r % 2 else shuf(n, 7000 + t)
        x = 1 + (r >> 16) % n
        L = 6 + (r >> 24) % 30
        W = [1 + (R(("s%d" % t).encode(), 300 + i) % n) for i in range(L)]
        if W and W[0] == x:
            W[0] = 1 if x != 1 else n
        Tp, evx = PE.splay_trace(to_ptr(T0), x)
        d = len(evx)
        if d == 0:
            continue
        cL = execc(to_ptr(T0), W)
        cR = execc(Tp, W)
        fut = cL - cR
        ratios.append(fut / d)
        total_d += d
        n_cases += 1
        if fut > 2 * d:
            tail_d += d
            if len(tail_cases) < 15:
                tail_cases.append((t, n, x, L, fut, d, round(fut / d, 2)))
    ratios.sort()
    step("SD3-01", "cases=%d fut/d: min=%.2f med=%.2f p90=%.2f max=%.2f" %
         (n_cases, ratios[0], statistics.median(ratios),
          ratios[int(0.9 * len(ratios))], ratios[-1]))
    step("SD3-01", "tail-d-fraction (fut>2d d-weight/total-d) = %.4f" % (tail_d / total_d))
    step("SD3-01", "tail cases (t,n,x,L,fut,d,ratio): %s" % tail_cases[:10])
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "sod_tail.json").write_text(
        json.dumps({"cases": n_cases, "min": ratios[0], "med": statistics.median(ratios),
                    "p90": ratios[int(0.9 * len(ratios))], "max": ratios[-1],
                    "tail_frac": tail_d / total_d, "tail": tail_cases},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
