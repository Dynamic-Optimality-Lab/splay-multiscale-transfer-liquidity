"""PIVOT-17: hunt direct Hall-violation shapes.

Shape R (per-access room): an access t (KEEP) with q_t > named-room(t),
named-room = 2a_t (local) + 2a_setup (if setup) + sum 2a_creator (fat only).
If found: X = t-doubles is Hall-deficient among named pools (charge must
fail on it unless other pools... charge uses exactly these pools, so charge
MUST fail) -> classify Q-2A ((a) mechanism vs (b) theorem).
Shape S (sharing over-tight): a pool with incident demand > capacity where
incident demands have no alternative (all alternatives saturated/empty).
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


def room_check(rep, L):
    """Per access: q vs named-room. Returns violations [(acc, q, room)]."""
    legs = rep["accesses"][L:]
    accs = {a["idx"]: a for a in rep["accesses"]}
    cr = V.creators(rep)
    crm = {}
    for d in cr:
        if d["acc"] >= L:
            crm.setdefault(d["acc"], []).append(d)
    viol = []
    for a in legs:
        if a["m"] != "K" or a["q"] < 1:
            continue
        room = 2 * a["a"]
        st = a.get("setup")
        if st is not None:
            room += 2 * accs[st]["a"]
        for d in crm.get(a["idx"], []):
            c = d["creator"]
            if c is not None and accs[c]["a"] >= 1:
                pass  # counted once below
        seen_c = set()
        for d in crm.get(a["idx"], []):
            c = d["creator"]
            if c is not None and c not in seen_c and accs[c]["a"] >= 1:
                seen_c.add(c)
                room += 2 * accs[c]["a"]
        if a["q"] > room:
            viol.append({"acc": a["idx"], "x": a["x"], "a": a["a"],
                         "q": a["q"], "room": room, "setup": st,
                         "fat_creators": sorted(seen_c)})
    return viol


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 171
    rng = random.Random(seed)
    V.step("R-0", "room hunt seed=%d" % seed)
    ntot = nfull = 0
    nviol = 0
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
            vv = room_check(rep, L)
            if vv:
                nviol += 1
            rr = S.cyclic_test(sA, sB, cyc)
            if rr["lap2full"]:
                nfull += 1
            else:
                A = sum(a["a"] for a in legs)
                Q = sum(a["q"] for a in legs)
                fails.append({"n": n, "w": cyc, "A": A, "Q": Q,
                              "WQ": Q - 2 * A, "viol": vv,
                              "hall": rr.get("hall")})
                V.step("R-1", "FAIL n=%d A=%d Q=%d WQ=%d viol=%s" %
                       (n, A, Q, Q - 2 * A, vv))
    V.step("R-2", "tested=%d full=%d room-viol-cycles=%d fails=%d" %
           (ntot, nfull, nviol, len(fails)))
    V.save("roomhunt.json", {"tested": ntot, "full": nfull,
                             "room_viol": nviol, "fails": fails})
    return 0


if __name__ == "__main__":
    sys.exit(main())
