"""PIVOT-13 T3: walk-based closed-cycle sampler (any n) + hard-corpora tests.

Random walk on pair-shapes via direct replay (no full adj build); on state
repeat, extract the loop (closed cycle). 2-lap creator+setup matching.
Also: n=5 killer, BlockScan-violator pattern, 5/3 -- finite-history matches.
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


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


def enc_shape(P):
    if P is None:
        return None
    return (P["k"], enc_shape(P["l"]), enc_shape(P["r"]))


def sample_cycle(n, T0A, T0B, rng, maxlen=80, want_overflow=True):
    """Random walk until pair-state repeats; return closed-cycle word or None."""
    import copy
    A = V.to_ptr(copy.deepcopy(T0A))
    B = V.to_ptr(copy.deepcopy(T0B))
    seen = {(enc_shape(A), enc_shape(B)): 0}
    hist = []
    for i in range(maxlen):
        md = rng.choice(["K", "K", "D"])
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


def test_word(T0A, T0B, word, label):
    rep = V.replay(T0A, T0B, word + word)
    L = len(word)
    legs = rep["accesses"][:L]
    meps = max(a["eps"] for a in legs)
    cr = V.creators(rep)
    rfull = V.charge(rep, cr)
    lap2dbl = [d for d in cr if d["acc"] >= L]
    sub = V.charge(rep, lap2dbl)
    mix = ""
    if sub["full"]:
        mix = "loc=%d cre=%d set=%d" % (sub.get("n_local", 0),
                                        sub.get("n_creator", 0),
                                        sub.get("n_setup", 0))
    V.step("C-1", "%s len=%d maxeps=%d Qlap2=%d full=%s lap2=%s %s" %
           (label, L, meps, len(lap2dbl), rfull["full"], sub["full"], mix))
    return {"label": label, "len": L, "maxeps": meps,
            "Qlap2": len(lap2dbl), "full": rfull["full"],
            "lap2": sub["full"], "mix": mix,
            "hall": sub.get("hall_detail")}


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    ncyc = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    rng = random.Random(seed)
    T0A, T0B = vine(n), vine(n)
    V.step("C-0", "walk-sampler n=%d seed=%d target=%d" % (n, seed, ncyc))
    out = []
    # hard corpora first (n=6 shapes where needed)
    if n == 6:
        import wp6_cycle_ratio as O
        G = O.build(6)
        Sh = G["Sh"]
        out.append(test_word(Sh[1], Sh[5],
                             [("K", 3), ("K", 6), ("K", 3), ("K", 4),
                              ("K", 2), ("K", 1)], "53-cycle"))
        out.append(test_word(vine(5), vine(5),
                             [("K", 5), ("K", 1), ("K", 5), ("K", 3)],
                             "n5-killer-vineT0"))
    tested = 0
    tries = 0
    while tested < ncyc and tries < ncyc * 40:
        tries += 1
        cyc = sample_cycle(n, T0A, T0B, rng)
        if not cyc:
            continue
        rep0 = V.replay(T0A, T0B, cyc)
        if max(a["eps"] for a in rep0["accesses"]) <= 0:
            continue
        out.append(test_word(T0A, T0B, cyc, "walk-%d" % tested))
        tested += 1
        if tested % 10 == 0:
            V.step("C-1", "progress %d/%d" % (tested, ncyc))
    ok = sum(1 for e in out if e["lap2"])
    V.step("C-2", "n=%d entries=%d lap2-full=%d" % (n, len(out), ok))
    V.save("walk_n%d.json" % n, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
