"""PIVOT-14 breeder: splice overflow cycles at shared states into long
overflow-dense closed cycles; cyclic-test the charging mechanism."""
from __future__ import annotations
import sys
import json
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
from wp6_ovf_anal import vine


def sample(n, T0A, T0B, rng, maxlen):
    """Random walk with full trace; returns (cycle, startA, startB) with
    start shapes = the cycle's true entry state, or None."""
    import copy
    A = V.to_ptr(copy.deepcopy(T0A))
    B = V.to_ptr(copy.deepcopy(T0B))
    seen = {}
    s0 = (S.enc_shape(A), S.enc_shape(B))
    seen[s0] = (0, s0[0], s0[1])
    hist = []
    for i in range(maxlen):
        md = rng.choice(["K", "K", "D"])
        x = rng.randint(1, n)
        A, _ = V.splay_cap(A, x, i, [])
        if md == "K":
            B, _ = V.splay_cap(B, x, i, [])
        hist.append((md, x))
        st = (S.enc_shape(A), S.enc_shape(B))
        if st in seen:
            j = seen[st][0]
            cyc = hist[j:]
            if len(cyc) >= 2:
                return cyc, dec_shape(seen[st][1]), dec_shape(seen[st][2])
            return None
        seen[st] = (len(hist), st[0], st[1])
    return None


def dec_shape(e):
    if e is None:
        return None
    return [e[0], dec_shape(e[1]), dec_shape(e[2])]


def trace(n, T0A, T0B, w):
    A = V.to_ptr(copy.deepcopy(T0A))
    B = V.to_ptr(copy.deepcopy(T0B))
    tr = [(S.enc_shape(A), S.enc_shape(B))]
    for i, (md, x) in enumerate(w):
        A, _ = V.splay_cap(A, x, i, [])
        if md == "K":
            B, _ = V.splay_cap(B, x, i, [])
        tr.append((S.enc_shape(A), S.enc_shape(B)))
    return tr


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    npool = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    nbreed = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    rng = random.Random(seed)
    T0 = vine(n)
    V.step("B-0", "breed n=%d pool=%d breeds=%d" % (n, npool, nbreed))
    # pool of overflow cycles with traces
    pool = []
    tries = 0
    while len(pool) < npool and tries < npool * 40:
        tries += 1
        r = sample(n, T0, T0, rng, 40)
        if not r:
            continue
        cyc, sA, sB = r
        rep = V.replay(sA, sB, cyc)
        if max(a["eps"] for a in rep["accesses"]) <= 0:
            continue
        tr = trace(n, sA, sB, cyc)
        assert tr[0] == tr[-1]
        pool.append((cyc, tr, sA, sB))
    V.step("B-1", "pool=%d" % len(pool))
    # index states
    idx = {}
    for ci, (cyc, tr, sA, sB) in enumerate(pool):
        for pos, st in enumerate(tr[:-1]):
            idx.setdefault(st, []).append((ci, pos))
    shared = {st: v for st, v in idx.items() if len(set(c for c, _ in v)) > 1}
    V.step("B-1", "shared states=%d" % len(shared))
    if not shared:
        V.step("B-1", "no shared states; done")
        return 0
    # breed
    tested = full = 0
    tot_ovf = 0
    fails = []
    maxlen = 0
    for b in range(nbreed):
        st = rng.choice(list(shared.keys()))
        members = shared[st]
        (c1, p1), (c2, p2) = rng.sample(members, 2)
        w1, w2 = pool[c1][0], pool[c2][0]
        r1 = w1[p1:] + w1[:p1]
        r2 = w2[p2:] + w2[:p2]
        w = r1 + r2
        # start shapes: decode shared state st
        sA = dec_shape(st[0])
        sB = dec_shape(st[1])
        # verify closed by trace
        tr = trace(n, sA, sB, w)
        if tr[0] != tr[-1]:
            continue
        r = S.cyclic_test(sA, sB, w)
        rep = V.replay(sA, sB, w + w)
        L = len(w)
        no = sum(1 for a in rep["accesses"][L:] if a["eps"] > 0)
        tot_ovf += no
        maxlen = max(maxlen, L)
        tested += 1
        if r["lap2full"]:
            full += 1
        else:
            fails.append({"w": w, "r": r})
    V.step("B-2", "bred=%d full=%d meanOvf=%.2f maxlen=%d fails=%d" %
           (tested, full, tot_ovf / max(1, tested), maxlen, len(fails)))
    V.save("breed_n%d.json" % n, {"seed": seed, "tested": tested,
                                  "full": full, "fails": fails})
    return 0


if __name__ == "__main__":
    sys.exit(main())
