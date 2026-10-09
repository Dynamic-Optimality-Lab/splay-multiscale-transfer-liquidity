"""PIVOT-14 siege: adversarial falsification of the charging mechanism.

Cyclic protocol: closed word w -> replay w+w -> match SECOND copy
(context = first copy = same cycle mod m). Any second-copy failure is a
mechanism failure (classify Q-2A per PIVOT-14 S26).

Batteries: long walks (n=6,7,8), overload cannon (one starved builder +
many starved consumers sharing one setup), DELETE-poor (all-KEEP),
crossing-epoch dense.
"""
from __future__ import annotations
import sys
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_walk as W
from wp6_ovf_anal import vine


def cyclic_test(T0A, T0B, w):
    rep = V.replay(T0A, T0B, w + w)
    L = len(w)
    A = sum(a["a"] for a in rep["accesses"][L:])
    Q = sum(a["q"] for a in rep["accesses"][L:])
    cr = V.creators(rep)
    lap2 = [d for d in cr if d["acc"] >= L]
    sub = V.charge(rep, lap2)
    return {"len": L, "A": A, "Q": Q, "WQ": Q - 2 * A,
            "Qlap2": len(lap2), "lap2full": sub["full"],
            "hall": sub.get("hall_detail"),
            "mix": (sub.get("n_local"), sub.get("n_creator"),
                    sub.get("n_setup"))}


def enc_shape(P):
    if P is None:
        return None
    return (P["k"], enc_shape(P["l"]), enc_shape(P["r"]))


def closed_walk(n, T0A, T0B, rng, maxlen, keep_only=False):
    import copy
    A = V.to_ptr(copy.deepcopy(T0A))
    B = V.to_ptr(copy.deepcopy(T0B))
    seen = {(enc_shape(A), enc_shape(B)): 0}
    hist = []
    for i in range(maxlen):
        md = "K" if keep_only else rng.choice(["K", "K", "D"])
        x = rng.randint(1, n)
        A, _ = V.splay_cap(A, x, i, [])
        if md == "K":
            B, _ = V.splay_cap(B, x, i, [])
        hist.append((md, x))
        st = (enc_shape(A), enc_shape(B))
        if st in seen:
            cyc = hist[seen[st]:]
            if len(cyc) >= 2:
                return cyc
            return None
        seen[st] = len(hist)
    return None


def overload_cannon(n, rng):
    """Dy,Ky(builder) then Dx_j,Kx_j for many j. Tune: builder deep."""
    y = rng.randint(1, n)
    others = [k for k in range(1, n + 1) if k != y]
    rng.shuffle(others)
    # build phase: deep KEEPs to give y B-depth (sweep y from far keys)
    w = [("K", k) for k in others[:max(1, len(others) // 2)]]
    w += [("D", y), ("K", y)]
    for j in others:
        w += [("D", j), ("K", j)]
    return w


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    rng = random.Random(seed)
    fails = []
    stats = {}
    V.step("S-0", "siege seed=%d" % seed)
    # battery 1: long walks n=6,7,8
    for n, cnt, ml in ((6, 40, 150), (7, 30, 120), (8, 20, 100)):
        T0 = vine(n)
        tested = full = 0
        tries = 0
        while tested < cnt and tries < cnt * 60:
            tries += 1
            cyc = closed_walk(n, T0, T0, rng, ml)
            if not cyc:
                continue
            r = cyclic_test(T0, T0, cyc)
            tested += 1
            if r["lap2full"]:
                full += 1
            else:
                fails.append({"bat": "long-n%d" % n, "w": cyc, "r": r})
        stats["long-n%d" % n] = (full, tested)
        V.step("S-1", "long n=%d: %d/%d" % (n, full, tested))
    # battery 2: overload cannon n=6,8 (closed? cannon is OPEN word;
    # close it by appending return path: replay to find end state then BFS?
    # simpler: run cannon twice (2-lap) as finite history; failure here is
    # still mechanism-relevant (transient+steady mix).)
    for n in (6, 8):
        T0 = vine(n)
        tested = full = 0
        for t in range(30):
            w = overload_cannon(n, rng)
            rep = V.replay(T0, T0, w)
            cr = V.creators(rep)
            r = V.charge(rep, cr)
            tested += 1
            if r["full"]:
                full += 1
            else:
                A = sum(a["a"] for a in rep["accesses"])
                Q = sum(a["q"] for a in rep["accesses"])
                fails.append({"bat": "cannon-n%d" % n, "w": w,
                              "r": {"A": A, "Q": Q, "WQ": Q - 2 * A,
                                    "hall": r.get("hall_detail")}})
        stats["cannon-n%d" % n] = (full, tested)
        V.step("S-1", "cannon n=%d: %d/%d" % (n, full, tested))
    # battery 3: DELETE-poor (all-KEEP closed walks) n=6,7
    for n, cnt in ((6, 40), (7, 25)):
        T0 = vine(n)
        tested = full = 0
        tries = 0
        while tested < cnt and tries < cnt * 60:
            tries += 1
            cyc = closed_walk(n, T0, T0, rng, 80, keep_only=True)
            if not cyc:
                continue
            r = cyclic_test(T0, T0, cyc)
            tested += 1
            if r["lap2full"]:
                full += 1
            else:
                fails.append({"bat": "keep-n%d" % n, "w": cyc, "r": r})
        stats["keep-n%d" % n] = (full, tested)
        V.step("S-1", "keep-only n=%d: %d/%d" % (n, full, tested))
    # battery 4: crossing-epoch dense (alternate 2 keys + drift) n=6
    T0 = vine(6)
    tested = full = 0
    tries = 0
    while tested < 40 and tries < 2400:
        tries += 1
        a, b = rng.sample(range(1, 7), 2)
        w = []
        for _ in range(rng.randint(2, 6)):
            w += [("K", a), ("D", rng.randint(1, 6)), ("K", b),
                  ("D", rng.randint(1, 6))]
        # close: check closed, else skip (finite test anyway on 2-lap)
        rep = V.replay(T0, T0, w + w)
        L = len(w)
        cr = V.creators(rep)
        lap2 = [d for d in cr if d["acc"] >= L]
        sub = V.charge(rep, lap2)
        tested += 1
        if sub["full"]:
            full += 1
        else:
            A = sum(x["a"] for x in rep["accesses"][L:])
            Q = sum(x["q"] for x in rep["accesses"][L:])
            fails.append({"bat": "cross", "w": w,
                          "r": {"A": A, "Q": Q, "WQ": Q - 2 * A,
                                "hall": sub.get("hall_detail")}})
    stats["cross"] = (full, tested)
    V.step("S-1", "cross: %d/%d" % (full, tested))
    V.step("S-2", "stats=%s fails=%d" % (stats, len(fails)))
    V.save("siege.json", {"seed": seed, "stats": stats, "fails": fails})
    return 0


if __name__ == "__main__":
    sys.exit(main())
