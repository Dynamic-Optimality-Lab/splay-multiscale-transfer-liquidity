"""PIVOT-22 NO-hunt: W_Q hillclimb on CLOSED words (n>=10).

Mutate closed words (splice-preserving-closedness + BFS-close), maximize
W_Q exactly. Any W_Q>0 => replay-verify => NO certificate.
"""
from __future__ import annotations
import sys
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
import wp6_breed as B
from wp6_ovf_anal import vine


def wq_of(T0A, T0B, w):
    rep = V.replay(T0A, T0B, w)
    A = sum(a["a"] for a in rep["accesses"])
    Q = sum(a["q"] for a in rep["accesses"])
    return Q - 2 * A, rep


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 231
    ntrials = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    rng = random.Random(seed)
    V.step("N-0", "WQ-hillclimb seed=%d trials=%d" % (seed, ntrials))
    best = (None, None)
    for n in (10, 11, 12):
        T0 = vine(n)
        for t in range(ntrials):
            # start: bred closed cycle via shared-state walk
            r = B.sample(n, T0, T0, rng, 60)
            if not r:
                continue
            cyc, sA, sB = r
            cur = list(cyc)
            curW, _ = wq_of(sA, sB, cur + cur)
            curW //= 2
            # hillclimb: mutate + splice, keep closed + keep/improve W_Q
            for _ in range(25):
                # mutate: change/insert/delete events, then re-close by
                # splicing at shared states is complex; simpler: random
                # closed neighbor via short BFS-detour (skip: use splice
                # of two pool cycles (closed by construction))
                r2 = B.sample(n, T0, T0, rng, 40)
                if not r2:
                    continue
                cyc2, _, _ = r2
                # splice at shared state if any, else skip
                tr1 = B.trace(n, sA, sB, cur)
                tr2 = B.trace(n, T0, T0, cyc2)
                s1 = set(tr1[:-1])
                shared = [st for st in tr2[:-1] if st in s1]
                if not shared:
                    continue
                st = rng.choice(shared)
                p1 = tr1.index(st)
                p2 = tr2.index(st)
                wnew = cur[p1:] + cur[:p1] + cyc2[p2:] + cyc2[:p2]
                sAA = B.dec_shape(st[0])
                sBB = B.dec_shape(st[1])
                if B.trace(n, sAA, sBB, wnew)[-1] != st:
                    continue
                nw, _ = wq_of(sAA, sBB, wnew)
                # W over single lap:
                rep1 = V.replay(sAA, sBB, wnew)
                w1 = sum(a["q"] for a in rep1["accesses"]) - 2 * sum(
                    a["a"] for a in rep1["accesses"])
                if w1 >= curW:
                    cur, sA, sB, curW = wnew, sAA, sBB, w1
                    if curW > 0:
                        V.step("N-1", "POSITIVE n=%d WQ=%d len=%d" %
                               (n, curW, len(cur)))
                        V.save("nofail.json", {"n": n, "w": cur,
                                               "WQ": curW})
                        return 0
            if best[0] is None or curW > best[0]:
                best = (curW, (n, len(cur)))
    V.step("N-2", "done best W_Q=%s at %s (all <=0)" % (best[0], best[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
