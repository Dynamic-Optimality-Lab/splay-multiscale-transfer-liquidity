"""U4-core: trajectory-filtered extremal loops. Build specific key B-deep
(filter trajectories reaching dB>=6), DELETE-setup + DELETE-dethrone + KEEP
(extremal (1,3)), repeat word, find trajectory repeat -> closed cycle,
charge + classify."""
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
from wp6_ovf_anal import vine


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 141
    rng = random.Random(seed)
    n = 7
    T0 = vine(n)
    V.step("J-0", "extremal loop seed=%d" % seed)
    found = 0
    tries = 0
    while found < 5 and tries < 300:
        tries += 1
        x = rng.randint(1, n)
        others = [k for k in range(1, n + 1) if k != x]
        # phase 1: random builds until x B-deep (cap 60)
        A = V.to_ptr(copy.deepcopy(T0))
        B = V.to_ptr(copy.deepcopy(T0))
        w = []
        deep = False
        for _ in range(60):
            k = rng.choice(others)
            w.append(("K", k))
            A, _ = V.splay_cap(A, k, 0, [])
            B, _ = V.splay_cap(B, k, 0, [])
            if V.depths_of(copy.deepcopy(B)).get(x, 0) >= 6:
                deep = True
                break
        if not deep:
            continue
        # phase 2: DELETE-setup x, DELETE-dethrone, KEEP x
        w += [("D", x)]
        A, _ = V.splay_cap(A, x, 0, [])
        y = rng.choice(others)
        w += [("D", y)]
        A, _ = V.splay_cap(A, y, 0, [])
        w += [("K", x)]
        dA = V.depths_of(copy.deepcopy(A)).get(x, 0)
        dB = V.depths_of(copy.deepcopy(B)).get(x, 0)
        A, _ = V.splay_cap(A, x, 0, [])
        B, _ = V.splay_cap(B, x, 0, [])
        a, q = (dA + 1) // 2, dB // 2
        if not (a >= 1 and q - 2 * a >= 1):
            continue
        V.step("J-1", "extremal built x=%d dA=%d dB=%d (a,q)=(%d,%d)" %
               (x, dA, dB, a, q))
        # phase 3: repeat word, find trajectory repeat -> closed cycle
        AA = V.to_ptr(copy.deepcopy(T0))
        BB = V.to_ptr(copy.deepcopy(T0))
        seen = {}
        cyc = None
        for i in range(len(w) * 12):
            md, xk = w[i % len(w)]
            AA, _ = V.splay_cap(AA, xk, 0, [])
            if md == "K":
                BB, _ = V.splay_cap(BB, xk, 0, [])
            st = (S.enc_shape(AA), S.enc_shape(BB))
            if st in seen:
                cand = [w[(seen[st] + j) % len(w)]
                        for j in range(i + 1 - seen[st])]
                # verify cand is closed from its start state
                cyc = cand
                break
            seen[st] = i + 1
        if not cyc:
            continue
        # find start state of cyc: replay prefix
        AA = V.to_ptr(copy.deepcopy(T0))
        BB = V.to_ptr(copy.deepcopy(T0))
        # locate: rerun and record state at cycle entry = seen[st] steps
        # (simpler: cyclic_test needs T0 pair that closes; use trace to get
        # start shapes)
        trA, trB = V.to_ptr(copy.deepcopy(T0)), V.to_ptr(copy.deepcopy(T0))
        states = [(S.enc_shape(trA), S.enc_shape(trB))]
        for j, (md, xk) in enumerate(w * 12):
            trA, _ = V.splay_cap(trA, xk, 0, [])
            if md == "K":
                trB, _ = V.splay_cap(trB, xk, 0, [])
            states.append((S.enc_shape(trA), S.enc_shape(trB)))
        # cyc starts at states[seen[st]]; decode shapes
        import wp6_breed as BD
        sA = BD.dec_shape(states[0][0])
        # NOTE states[0] is vine; cycle entry state:
        # recompute: entry index = position where repeat started
        V.step("J-1", "trajectory repeat found, cyc len=%d" % len(cyc))
        # verify closure from decoded entry state by trace
        # (entry = state at step seen[st]; find via replay of prefix)
        # simplest: test cyclic_test from ALL rotations? just test from vine
        # with the rotated word (closed by construction at entry state):
        # decode entry state:
        # rebuild: walk w*12, record ptr snapshots is heavy; instead verify
        # closedness by checking trace from decoded shapes below.
        found += 1
        # decode entry: we know entry step index e0 = (position of first
        # occurrence). Redo carefully with index tracking:
        AA = V.to_ptr(copy.deepcopy(T0))
        BB = V.to_ptr(copy.deepcopy(T0))
        seen2 = {}
        e0 = None
        W2 = w * 12
        for i in range(len(W2)):
            st = (S.enc_shape(AA), S.enc_shape(BB))
            if st in seen2:
                e0 = seen2[st]
                cyc = W2[e0:i]
                # entry shapes = decode st
                sA = BD.dec_shape(st[0])
                sB = BD.dec_shape(st[1])
                break
            seen2[st] = i
            md, xk = W2[i]
            AA, _ = V.splay_cap(AA, xk, 0, [])
            if md == "K":
                BB, _ = V.splay_cap(BB, xk, 0, [])
        if e0 is None or not cyc:
            found -= 1
            continue
        r = S.cyclic_test(sA, sB, cyc)
        rep = V.replay(sA, sB, cyc + cyc)
        L = len(cyc)
        deep = [(aa["x"], aa["a"], aa["q"], aa["eps"])
                for aa in rep["accesses"][L:]
                if aa["m"] == "K" and ((aa["a"] == 0 and aa["q"] >= 3) or
                                      (aa["a"] >= 1 and aa["eps"] >= 1))]
        V.step("J-2", "CLOSED len=%d lap2full=%s A=%d Q=%d WQ=%d deep=%s" %
               (len(cyc), r["lap2full"], r["A"], r["Q"], r["WQ"], deep))
        if not r["lap2full"]:
            V.step("J-2", "  HALL=%s" % (r.get("hall"),))
    V.step("J-3", "done found=%d" % found)
    return 0


if __name__ == "__main__":
    sys.exit(main())
