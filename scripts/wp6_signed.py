"""PIVOT-19/20: signed-builder beam search for era violation.

Classify each builder KEEP y by signed effect on x: (sgn dBx, sgn dAx).
Beam-search sequences accumulating B-depth while canceling A-depth.
Either finds era violation (q > a_s) or reveals sign-correlation.
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


def sgn(v):
    return (v > 0) - (v < 0)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 201
    rng = random.Random(seed)
    n = 7
    T0 = vine(n)
    V.step("S-0", "signed-beam seed=%d" % seed)
    # Phase 1: sign census -- joint distribution of (sgn dB, sgn dA)
    from collections import Counter
    SC = Counter()
    for t in range(300):
        x = rng.randint(1, n)
        others = [k for k in range(1, n + 1) if k != x]
        A = V.to_ptr(copy.deepcopy(T0))
        B = V.to_ptr(copy.deepcopy(T0))
        # random prefix (5-10 steps) for shape diversity
        for _ in range(rng.randint(5, 10)):
            k = rng.randint(1, n)
            md = rng.choice(["K", "K", "D"])
            A, _ = V.splay_cap(A, k, 0, [])
            if md == "K":
                B, _ = V.splay_cap(B, k, 0, [])
        y = rng.choice(others)
        b0 = V.depths_of(copy.deepcopy(B)).get(x, 0)
        a0 = V.depths_of(copy.deepcopy(A)).get(x, 0)
        A2 = copy.deepcopy(A)
        B2 = copy.deepcopy(B)
        A2, _ = V.splay_cap(A2, y, 0, [])
        B2, _ = V.splay_cap(B2, y, 0, [])
        b1 = V.depths_of(copy.deepcopy(B2)).get(x, 0)
        a1 = V.depths_of(copy.deepcopy(A2)).get(x, 0)
        SC[(sgn(b1 - b0), sgn(a1 - a0))] += 1
    V.step("S-1", "sign joint (dB,dA): %s" % dict(SC))
    # Phase 2: beam search (B accum + A cancel) from vine
    x = 3
    others = [k for k in range(1, n + 1) if k != x]
    beam = [([], V.to_ptr(copy.deepcopy(T0)), V.to_ptr(copy.deepcopy(T0)))]
    for r in range(15):
        cand = []
        for w, A, B in beam:
            for y in others:
                A2 = copy.deepcopy(A)
                B2 = copy.deepcopy(B)
                A2, _ = V.splay_cap(A2, y, 0, [])
                B2, _ = V.splay_cap(B2, y, 0, [])
                dB = V.depths_of(copy.deepcopy(B2)).get(x, 0)
                dA = V.depths_of(copy.deepcopy(A2)).get(x, 0)
                # objective: B deep + A shallow (discrepancy), cap A<=3
                score = dB - 3 * max(0, dA - 2)
                cand.append((score, w + [("K", y)], A2, B2))
        cand.sort(key=lambda z: -z[0])
        beam = [(w, A, B) for _, w, A, B in cand[:30]]
        V.step("S-2", "round %d best=%s" % (r, cand[0][0]))
    # Phase 3: finish best with setup+dethrone+consume, check era
    V.step("S-3", "finishing top beams:")
    for _, w, A, B in [(c[0], c[1], c[2], c[3]) for c in cand[:5]]:
        A = copy.deepcopy(A)
        B = copy.deepcopy(B)
        w = list(w)
        w.append(("D", x))
        A, _ = V.splay_cap(A, x, 0, [])
        dS = V.depths_of(copy.deepcopy(A)).get(x, 0)
        if dS == 0:
            continue
        a_s = (dS + 1) // 2
        y = rng.choice(others)
        w.append(("D", y))
        A, _ = V.splay_cap(A, y, 0, [])
        w.append(("K", x))
        dA = V.depths_of(copy.deepcopy(A)).get(x, 0)
        dB = V.depths_of(copy.deepcopy(B)).get(x, 0)
        A, _ = V.splay_cap(A, x, 0, [])
        B, _ = V.splay_cap(B, x, 0, [])
        a, q = (dA + 1) // 2, dB // 2
        V.step("S-3", "x=%d dSetup=%d a_s=%d dA=%d dB=%d (a,q)=(%d,%d) "
               "q-a_s=%d" % (x, dS, a_s, dA, dB, a, q, q - a_s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
