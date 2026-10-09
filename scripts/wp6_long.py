"""PIVOT-18: multi-splice long overflow-dense cycles (5-10 segments, len 100-300)
+ per-access room + charge + Q-2A classify. Gaussian-tail territory for era."""
from __future__ import annotations
import sys
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
import wp6_breed as B
import wp6_room as RM
from wp6_ovf_anal import vine


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 181
    nbreed = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    nseg = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    rng = random.Random(seed)
    n = 6
    T0 = vine(n)
    V.step("L-0", "long-splice n=%d breeds=%d segs=%d" % (n, nbreed, nseg))
    # pool with traces + start shapes
    pool = []
    tries = 0
    while len(pool) < 100 and tries < 6000:
        tries += 1
        r = B.sample(n, T0, T0, rng, 40)
        if not r:
            continue
        cyc, sA, sB = r
        rep = V.replay(sA, sB, cyc)
        if max(a["eps"] for a in rep["accesses"]) <= 0:
            continue
        tr = B.trace(n, sA, sB, cyc)
        pool.append((cyc, tr))
    V.step("L-1", "pool=%d" % len(pool))
    idx = {}
    for ci, (cyc, tr) in enumerate(pool):
        for pos, st in enumerate(tr[:-1]):
            idx.setdefault(st, []).append((ci, pos))
    shared = {st: v for st, v in idx.items()
              if len(set(c for c, _ in v)) > 1}
    V.step("L-1", "shared=%d" % len(shared))
    if not shared:
        return 0
    tested = full = 0
    roomviol = 0
    fails = []
    maxlen = 0
    for b in range(nbreed):
        # chain nseg segments through shared states
        st = rng.choice(list(shared.keys()))
        w = []
        ok = True
        for _ in range(nseg):
            cands = [x for x in shared[st] if True]
            ci, pos = rng.choice(shared[st])
            cyc = pool[ci][0]
            w += cyc[pos:] + cyc[:pos]
            # next shared state: end state = st (closed segs) -> pick new
            # (segments are closed loops from st; chain stays at st)
        # w is closed (concatenation of closed loops at st)
        sA = B.dec_shape(st[0])
        sB = B.dec_shape(st[1])
        tr = B.trace(n, sA, sB, w)
        if tr[0] != tr[-1]:
            continue
        rep = V.replay(sA, sB, w + w)
        L = len(w)
        no = sum(1 for a in rep["accesses"][L:] if a["eps"] > 0)
        if no == 0:
            continue
        tested += 1
        maxlen = max(maxlen, L)
        vv = RM.room_check(rep, L)
        if vv:
            roomviol += 1
        r = S.cyclic_test(sA, sB, w)
        if r["lap2full"]:
            full += 1
        else:
            A = sum(a["a"] for a in rep["accesses"][L:])
            Q = sum(a["q"] for a in rep["accesses"][L:])
            fails.append({"len": L, "A": A, "Q": Q, "WQ": Q - 2 * A,
                          "viol": vv, "hall": r.get("hall")})
            V.step("L-2", "FAIL len=%d A=%d Q=%d WQ=%d viol=%s" %
                   (L, A, Q, Q - 2 * A, vv))
    V.step("L-3", "tested=%d full=%d roomviol=%d maxlen=%d fails=%d" %
           (tested, full, roomviol, maxlen, len(fails)))
    V.save("longsplice.json", {"tested": tested, "full": full,
                               "roomviol": roomviol, "fails": fails})
    return 0


if __name__ == "__main__":
    sys.exit(main())
