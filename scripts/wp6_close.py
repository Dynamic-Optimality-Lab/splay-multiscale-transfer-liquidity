"""U4-core: BFS-close extremal open words at n=7 via on-demand pair-graph BFS
(trans tables only, no full adj), then cyclic charge + classify."""
from __future__ import annotations
import sys
import json
import copy
import random
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
import wp6_cycle_ratio as O
from wp6_ovf_anal import vine


def build_trans(n):
    import wp6_cycle_ratio as C
    Sh = C.shapes_of(list(range(1, n + 1)))
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]

    def shape_of(P):
        return idx[json.dumps(list(O.enc_ptr(P)), sort_keys=True)]

    Atrans, Btrans = {}, {}
    for ia in range(len(Sh)):
        for x in range(1, n + 1):
            A2 = copy.deepcopy(ptrs[ia])
            A2, iv = V.splay_cap(A2, x, 0, [])
            Atrans[(ia, x)] = (shape_of(A2), len(iv))
            B2 = copy.deepcopy(ptrs[ia])
            B2, p = V.splay_cap(B2, x, 0, [])
            Btrans[(ia, x)] = (shape_of(B2), len(p))
    return Sh, Atrans, Btrans


def nbrs(nS, Atrans, Btrans, u, n):
    ia, ib = u // nS, u % nS
    out = []
    for x in range(1, n + 1):
        ia2, a = Atrans[(ia, x)]
        out.append((ia2 * nS + ib, "D", x))
        ib2, b = Btrans[(ib, x)]
        out.append((ia2 * nS + ib2, "K", x))
    return out


def bfs_close(nS, Atrans, Btrans, u_end, u_start, n, cap=400000):
    prev = {u_end: None}
    dq = deque([u_end])
    while dq and len(prev) < cap:
        u = dq.popleft()
        if u == u_start:
            break
        for (to, md, x) in nbrs(nS, Atrans, Btrans, u, n):
            if to not in prev:
                prev[to] = (u, md, x)
                dq.append(to)
    if u_start not in prev:
        return None
    path = []
    u = u_start
    while prev[u] is not None:
        pu, md, x = prev[u]
        path.append((md, x))
        u = pu
    path.reverse()
    return path


def state_of_word(nS, Atrans, Btrans, u0, w):
    u = u0
    for (md, x) in w:
        ia, ib = u // nS, u % nS
        if md == "D":
            ia2, _ = Atrans[(ia, x)]
            u = ia2 * nS + ib
        else:
            ia2, _ = Atrans[(ia, x)]
            ib2, _ = Btrans[(ib, x)]
            u = ia2 * nS + ib2
    return u


def main():
    n = 7
    T0 = vine(n)
    V.step("F-0", "building trans n=7")
    Sh, Atrans, Btrans = build_trans(n)
    nS = len(Sh)
    vj = json.dumps(T0, sort_keys=True)
    vi = next(i for i, s in enumerate(Sh) if json.dumps(s, sort_keys=True) == vj)
    u0 = vi * nS + vi
    V.step("F-0", "shapes=%d u0=%d" % (nS, u0))
    # regenerate extremal words (same seed => same words)
    import wp6_extremal  # noqa (ensures module present)
    rng = random.Random(81)
    closed = []
    tries = 0
    while len(closed) < 8 and tries < 400:
        tries += 1
        x = rng.randint(1, n)
        others = [k for k in range(1, n + 1) if k != x]
        w = []
        for _ in range(rng.randint(2, 5)):
            rng.shuffle(others)
            w += [("K", k) for k in others]
        w += [("D", x)]
        for _ in range(rng.randint(1, 2)):
            w += [("D", rng.choice(others))]
        w += [("K", x)]
        rep = V.replay(T0, T0, w)
        ext = [a for a in rep["accesses"]
               if a["m"] == "K" and ((a["a"] == 0 and a["q"] >= 3) or
                                    (a["a"] >= 1 and a["eps"] >= 1))]
        if not ext:
            continue
        u_end = state_of_word(nS, Atrans, Btrans, u0, w)
        closer = bfs_close(nS, Atrans, Btrans, u_end, u0, n)
        if closer is None:
            V.step("F-1", "no close (cap)")
            continue
        wc = w + closer
        r = S.cyclic_test(T0, T0, wc)
        rep2 = V.replay(T0, T0, wc + wc)
        L = len(wc)
        no = sum(1 for a in rep2["accesses"][L:] if a["eps"] > 0)
        deep = [(a["x"], a["a"], a["q"], a["eps"]) for a in rep2["accesses"][L:]
                if a["m"] == "K" and ((a["a"] == 0 and a["q"] >= 3) or
                                     (a["a"] >= 1 and a["eps"] >= 1))]
        closed.append({"len": len(wc), "lap2full": r["lap2full"],
                       "A": r["A"], "Q": r["Q"],
                       "WQ": r["WQ"], "novf": no, "deep": deep,
                       "hall": r.get("hall")})
        V.step("F-1", "closed len=%d lap2full=%s A=%d Q=%d WQ=%d novf=%d deep=%s" %
               (len(wc), r["lap2full"], r["A"], r["Q"], r["WQ"], no, deep))
    V.save("extremal_closed.json", closed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
