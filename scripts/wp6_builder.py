"""PIVOT-16: starved-deep-builder construction (case-(a) probe).

Engineer: prev-x-KEEP (reset) + mild dethrone + Dx (shallow setup a_s=1)
+ starved-deep-y (A-rooted + B-deep, prepared with fat setup-y) building
x deep (x A-frozen-rooted) + KEEP x (starved deep). Expect: 1-hop charge
FAILS with deficit, Q-2A <= 0 (case a). Then 2-hop repair.
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


def depths(P):
    return V.depths_of(copy.deepcopy(P))


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 181
    rng = random.Random(seed)
    n = 8
    T0 = vine(n)
    V.step("K-0", "builder-construction seed=%d" % seed)
    best = None
    for t in range(300):
        x = rng.randint(1, n)
        others = [k for k in range(1, n + 1) if k != x]
        A = V.to_ptr(copy.deepcopy(T0))
        B = V.to_ptr(copy.deepcopy(T0))
        w = []
        # 1. reset x (root both)
        w.append(("K", x))
        A, _ = V.splay_cap(A, x, 0, [])
        B, _ = V.splay_cap(B, x, 0, [])
        # 2. prepare starved-deep y: pick y, build y B-deep via others
        y = rng.choice(others)
        yo = [k for k in range(1, n + 1) if k != y]
        for _ in range(rng.randint(3, 8)):
            rng.shuffle(yo)
            for k in yo[:rng.randint(2, n - 1)]:
                w.append(("K", k))
                A, _ = V.splay_cap(A, k, 0, [])
                B, _ = V.splay_cap(B, k, 0, [])
        # Dy re-root y (setup-y); want y B-deep preserved
        w.append(("D", y))
        A, _ = V.splay_cap(A, y, 0, [])
        dBy = depths(B).get(y, 0)
        dAy_pre = depths(A).get(y, 0)
        # NOTE Dy already applied above for A; B untouched by construction
        if dBy < 6:
            continue
        # 3. mild dethrone x + Dx shallow setup (x must be mildly dethroned)
        # x A-state now: whatever builds left; force mild via... just Dx
        # if dA small else skip (need a_s small)
        dAx = depths(A).get(x, 0)
        if dAx > 2 or dAx == 0:
            continue
        w.append(("D", x))
        A, _ = V.splay_cap(A, x, 0, [])
        a_s = (dAx + 1) // 2
        # 4. y builds x: Ky (y must be A-rooted now? y rooted by Dy above?
        # Dy rooted y (A). Between Dy and now: Dx (DELETE x: moves y? y was
        # root (A-root): Dx dethrones y!). Check y rooted:
        if depths(A).get(y, 0) != 0:
            continue
        dBx0 = depths(B).get(x, 0)
        w.append(("K", y))
        A, _ = V.splay_cap(A, y, 0, [])
        B, _ = V.splay_cap(B, y, 0, [])
        dBx1 = depths(B).get(x, 0)
        # 5. KEEP x (want starved deep)
        dAx2 = depths(A).get(x, 0)
        if dAx2 != 0:
            continue
        w.append(("K", x))
        A, _ = V.splay_cap(A, x, 0, [])
        B, _ = V.splay_cap(B, x, 0, [])
        a, q = 0, dBx1 // 2
        if q >= 3 and q > best[0] if best else True:
            if best is None or q > best[0]:
                best = (q, (x, y, a_s, dBx1, list(w)))
                V.step("K-1", "BUILT x=%d y=%d a_s=%d dBx=%d q=%d" %
                       (x, y, a_s, dBx1, q))
    V.step("K-2", "best=%s" % (best[0] if best else None,))
    if best:
        V.save("builder.json", {"best": best[0], "info": best[1]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
