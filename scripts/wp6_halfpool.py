"""PIVOT-15: greedy-steered falsification of half-pool (q <= a_s).

At each build step, choose KEEP y maximizing (B-deepening of x minus
A-motion of x) to engineer cancellation (B accumulates, A cancels).
Then DELETE-setup + DELETE-dethrone + KEEP x; check q > a_s.
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
from wp6_ovf_anal import vine


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 161
    ntrials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)
    n = 7
    T0 = vine(n)
    V.step("H-0", "halfpool-steer seed=%d trials=%d" % (seed, ntrials))
    best = (0, None)
    viol = []
    for t in range(ntrials):
        x = rng.randint(1, n)
        others = [k for k in range(1, n + 1) if k != x]
        A = V.to_ptr(copy.deepcopy(T0))
        B = V.to_ptr(copy.deepcopy(T0))
        w = []
        # greedy build: 25 steps maximizing deepB(x)-moveA(x)
        for _ in range(25):
            dAx0 = V.depths_of(copy.deepcopy(A)).get(x, 0)
            dBx0 = V.depths_of(copy.deepcopy(B)).get(x, 0)
            scored = []
            for y in others:
                A2 = copy.deepcopy(A)
                B2 = copy.deepcopy(B)
                A2, _ = V.splay_cap(A2, y, 0, [])
                B2, _ = V.splay_cap(B2, y, 0, [])
                dAx1 = V.depths_of(copy.deepcopy(A2)).get(x, 0)
                dBx1 = V.depths_of(copy.deepcopy(B2)).get(x, 0)
                gain = (dBx1 - dBx0) - abs(dAx1 - dAx0)
                scored.append((gain, y))
            scored.sort(reverse=True)
            # epsilon-greedy (sometimes random to diversify)
            y = scored[0][1] if rng.random() < 0.8 else rng.choice(others)
            w.append(("K", y))
            A, _ = V.splay_cap(A, y, 0, [])
            B, _ = V.splay_cap(B, y, 0, [])
        # setup + dethrone + consume
        w.append(("D", x))
        A, _ = V.splay_cap(A, x, 0, [])
        dSetup = V.depths_of(copy.deepcopy(A)).get(x, 0)
        # NOTE dSetup is pre-setup depth; setup needs dA>0
        if dSetup == 0:
            continue
        a_s = (dSetup + 1) // 2
        y = rng.choice(others)
        w.append(("D", y))
        A, _ = V.splay_cap(A, y, 0, [])
        w.append(("K", x))
        dA = V.depths_of(copy.deepcopy(A)).get(x, 0)
        dB = V.depths_of(copy.deepcopy(B)).get(x, 0)
        A, _ = V.splay_cap(A, x, 0, [])
        B, _ = V.splay_cap(B, x, 0, [])
        a, q = (dA + 1) // 2, dB // 2
        if a == 0 and q >= 1 and q > best[0]:
            best = (q, (x, dSetup, a_s, dA, dB, a, q, q - a_s))
            V.step("H-1", "starved x=%d dSetup=%d a_s=%d dA=%d dB=%d "
                   "(a,q)=(%d,%d) q-a_s=%d" %
                   (x, dSetup, a_s, dA, dB, a, q, q - a_s))
            if q > a_s:
                viol.append((w, x, dSetup, a_s, dA, dB, a, q))
    V.step("H-2", "best q=%s violations=%d" % (best[0], len(viol)))
    V.save("halfpool.json", {"best": best[0], "viol": viol[:5]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
