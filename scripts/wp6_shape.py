"""PIVOT-15: hunt the minimal-deficient shape.

Shape: starved (q>=2, SHARED setup with a tight non-starved (q'=2a'+1)),
setup a_s small, all creators starved/empty. Then charge + classify.
Also: generic tight-pool scan (pools with demand == capacity +1).
"""
from __future__ import annotations
import sys
import random
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
import wp6_breed as B
from wp6_ovf_anal import vine


def shape_scan(rep, L):
    """Find shared setups (starved-KEEP + tight-nonst) + zero-creator flags."""
    legs = rep["accesses"][L:]
    accs = {a["idx"]: a for a in rep["accesses"]}
    cr = V.creators(rep)
    crm = {}
    for d in cr:
        if d["acc"] >= L:
            crm.setdefault(d["acc"], []).append(d)
    nam = defaultdict(list)
    for a in legs:
        st = a.get("setup")
        if st is None or a["m"] != "K" or a["q"] < 1:
            continue
        nam[st].append(a)
    hits = []
    for st, ns in nam.items():
        sk = [a for a in ns if a["a"] == 0]
        nk = [a for a in ns if a["a"] >= 1 and a["q"] == 2 * a["a"] + 1]
        if sk and nk:
            # zero-creator check: all doubles of sk+nk have starved/None creators
            zc = True
            for a in sk + nk:
                for d in crm.get(a["idx"], []):
                    c = d["creator"]
                    if c is not None and accs[c]["a"] >= 1:
                        zc = False
            sa = accs[st]
            hits.append({"setup": st, "a_s": sa["a"],
                         "starved": [(a["x"], a["q"]) for a in sk],
                         "tight": [(a["x"], a["a"], a["q"]) for a in nk],
                         "zero_creators": zc})
    return hits


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 151
    rng = random.Random(seed)
    V.step("M-0", "shape hunt seed=%d" % seed)
    nshape = nfull = ntot = 0
    fails = []
    for n in (6, 7, 8):
        T0 = vine(n)
        tries = 0
        ncyc = 0
        while ncyc < 60 and tries < 6000:
            tries += 1
            r = B.sample(n, T0, T0, rng, 60)
            if not r:
                continue
            cyc, sA, sB = r
            rep = V.replay(sA, sB, cyc + cyc)
            L = len(cyc)
            legs = rep["accesses"][L:]
            if max(a["eps"] for a in legs) <= 0:
                continue
            ncyc += 1
            ntot += 1
            hits = shape_scan(rep, L)
            if hits:
                nshape += 1
            rr = S.cyclic_test(sA, sB, cyc)
            if rr["lap2full"]:
                nfull += 1
            else:
                A = sum(a["a"] for a in legs)
                Q = sum(a["q"] for a in legs)
                fails.append({"n": n, "w": cyc, "A": A, "Q": Q,
                              "WQ": Q - 2 * A, "hits": hits,
                              "hall": rr.get("hall")})
                V.step("M-1", "FAIL n=%d A=%d Q=%d WQ=%d hits=%s" %
                       (n, A, Q, Q - 2 * A, hits))
    V.step("M-2", "tested=%d full=%d shape-hits=%d fails=%d" %
           (ntot, nfull, nshape, len(fails)))
    V.save("shapehunt.json", {"tested": ntot, "full": nfull,
                              "shape_hits": nshape, "fails": fails})
    return 0


if __name__ == "__main__":
    sys.exit(main())
