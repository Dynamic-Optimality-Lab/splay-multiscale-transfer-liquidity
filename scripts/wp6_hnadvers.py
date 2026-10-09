"""PIVOT-25R-HN adversarial + held-out prediction test.

Builds: RL-comb (alternating suffix), delayed-twin pair (odd/even depth),
unbalanced fringe, mirrors of bank finds. Then predicts on HELD-OUT
doubles (supply, next L/R/fringe/twin/pat) from X-state via recurrence
rules; reports exact mismatches.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_hnrec import state_of, do_double, reroot, find
from wp6_trcollect import harvest


def step(sid, msg):
    print("[HNA %s] %s" % (sid, msg), flush=True)


def inorder(t):
    return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])


def vr(keys):
    t = None
    for k in reversed(list(keys)):
        t = [k, None, t]
    return t


def vl(keys):
    t = None
    for k in list(keys):
        t = [k, t, None]
    return t


def mirror(t, n):
    if t is None:
        return None
    return [n + 1 - t[0], mirror(t[2], n), mirror(t[1], n)]


def valid(t, n, tag):
    assert inorder(t) == list(range(1, n + 1)), tag
    return t


def predict_next(X):
    """Recurrence prediction of post-double (L,R,fringe,twin,pat-next inputs).
    Returns predicted (L2,R2,fr2) + predicted twin' (needs remdepth)."""
    L, R, U, Vv, pat = X["L"], X["R"], X["U"], X["V"], X["pat"]
    if pat == "LL":
        L2, R2 = L, 2 + R + U + Vv
    elif pat == "RR":
        L2, R2 = 2 + L + U + Vv, R
    elif pat == "LR":
        L2, R2 = 1 + U + L, 1 + R + Vv
    else:
        # RL (NOT the mirror of LR: left absorbs gO, right absorbs pO)
        L2, R2 = 1 + L + Vv, 1 + R + U
    fr = X["fr"]
    # rem = depth-1. x roots the tree <=> pre-depth==2 <=> rem==1.
    # fringe': [new0] + old[3:] (length rem-1 = post depth); [] if rooted.
    if X["rem"] == 1:
        fr2 = []
    else:
        s2 = fr[2][0] if len(fr) > 2 else None
        o2 = fr[2][1] if len(fr) > 2 else 0
        s3 = fr[3][0] if len(fr) > 3 else None
        new0 = [s2, o2, (s3 + s2) if (s3 and s2) else None]
        rest = [list(f) for f in fr[3:]]
        fr2 = [new0] + rest
    tw2 = 1 if X["rem"] == 1 else X["tw"]
    return L2, R2, fr2, tw2


def main():
    cases = []

    def add(n, A, B, x, tag):
        valid(A, n, tag + "-A")
        valid(B, n, tag + "-B")
        ev = []
        harvest(A, B, x, "K", tag, ev)
        rep = V.replay(A, B, [("K", x)])
        acc = rep["accesses"][0]
        cases.append({"n": n, "A": A, "B": B, "x": x, "tag": tag,
                      "a": acc["a"], "q": acc["q"], "w": acc["eps"]})
        step("E", "%s n=%d x=%d a=%d q=%d w=%d ndb=%d" %
             (tag, n, x, acc["a"], acc["q"], acc["eps"], len(ev)))

    # RL-comb: x=9 depth 4 alternating (R,L,R,L), outer mass, A-rooted
    M = [6, [5, None, None], [7, None, None]]
    B = [4, [3, [2, [1, None, None], None], None],
            [12, [8, M, [10, [9, None, None], [11, None, None]]],
             [14, [13, None, None], [15, None, None]]]]
    A = [9, vl(range(1, 9)), vr(range(10, 16))]
    add(15, A, B, 9, "ADV-RLcomb")
    # delayed twin pair: odd depth (twin at zig) vs even (twin at double)
    add(12, [1, None, vr(range(2, 13))], vl(range(1, 13)), 1, "ADV-dly11")
    add(11, [1, None, vr(range(2, 12))], vl(range(1, 12)), 1, "ADV-evn10")
    # unbalanced fringe: huge top-off-path block + deep x elsewhere
    Bu = [6, vl([1, 2, 3, 4, 5]), vr(range(7, 13))]
    Au = [1, None, vr(range(2, 13))]
    add(12, Au, Bu, 1, "ADV-unbal")
    # mirrors of two bank finds (V1-9-ish vine + an RL random): mirror vines
    add(11, mirror([1, None, vr(range(2, 12))], 11),
        mirror(vl(range(1, 12)), 11), 11, "ADV-mir11")
    # PR904 + mirror (held-out: never in collision calibration)
    import wp6_cycle_ratio as O
    Sh9 = O.shapes_of(list(range(1, 10)))
    add(9, Sh9[3432], Sh9[0], 9, "ADV-PR904")
    add(9, mirror(Sh9[3432], 9), mirror(Sh9[0], 9), 1, "ADV-PR904m")
    # fresh random n=11 held-out (not in discovery randoms: new seed range)
    import random
    rng = random.Random(913)
    Sh11 = O.shapes_of(list(range(1, 12)))
    for t in range(12):
        ia = rng.randrange(len(Sh11))
        ib = rng.randrange(len(Sh11))
        x = rng.randint(1, 11)
        add(11, Sh11[ia], Sh11[ib], x, "ADV-rnd%d" % t)
    # prediction test on ALL held-out doubles
    tot = ok = 0
    bad = []
    for c in cases:
        A = V.to_ptr(copy.deepcopy(c["A"]))
        B = V.to_ptr(copy.deepcopy(c["B"]))
        x = c["x"]
        A, _ = V.splay_cap(A, x, 0, [])
        while True:
            nd = find(B, x)
            if nd["p"] is None or nd["p"]["p"] is None:
                break
            X = state_of(A, B, x)
            L2, R2, fr2, tw2 = predict_next(X)
            rA = reroot(A)["k"]
            tw0 = 1 if rA == reroot(B)["k"] else 0
            D0 = sum(V.depths_of(reroot(B)).values())
            B = do_double(B, x)
            tw1 = 1 if rA == reroot(B)["k"] else 0
            D1 = sum(V.depths_of(reroot(B)).values())
            s = 2 * (tw1 - tw0) + (D0 - D1)
            # predicted supply from formula+twin timing
            nd2 = find(B, x)
            if nd2["p"] is None or nd2["p"]["p"] is None:
                Xp = None
            else:
                Xp = state_of(A, B, x)
            tot += 1
            good = True
            # predicted supply: formula(sizes) + twin timing (rooted<=>d==2
            # pre-step; rA==x phase invariant gives twin post).
            from wp6_transport import dbdrop_formula
            pred_s = dbdrop_formula(X["pat"], X["L"], X["R"], X["U"],
                                    X["V"]) + 2 * (tw2 - tw0)
            if pred_s != s:
                good = False
            if Xp is not None:
                if (Xp["L"], Xp["R"]) != (L2, R2):
                    good = False
                frp = [list(f) for f in Xp["fr"]]
                if frp != fr2:
                    good = False
                if Xp["tw"] != tw2:
                    good = False
            if good:
                ok += 1
            elif len(bad) < 6:
                bad.append((c["tag"], X["pat"], (L2, R2),
                            (Xp["L"], Xp["R"]) if Xp else None))
    step("T", "held-out doubles=%d predicted=%d" % (tot, ok))
    for b in bad:
        step("B", str(b))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "hnadversarial.json").write_text(
        json.dumps({"cases": [
            {k: v for k, v in c.items() if k != "A" and k != "B"}
            for c in cases], "tot": tot, "ok": ok,
            "bad": bad}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
