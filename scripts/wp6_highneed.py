"""PIVOT-25R-HN §2: high-need access generation (need>=3 + remaining double).

Families: vine A-rooted/B-deep (x=1 and x=n mirror, n=9..16 + spot 32);
A-shallow twin (x=9, n=9..12); random n=10..12 pairs filtered (w>=2,q>=2);
mirrors (key reflection) of selected cases. All replay-validated.
Saves dual_mine/highneed_bank.json with full harvest records.
"""
from __future__ import annotations
import sys
import copy
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_trcollect import harvest


def step(sid, msg):
    print("[HNG %s] %s" % (sid, msg), flush=True)


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


def valid(t, n, tag):
    assert inorder(t) == list(range(1, n + 1)), tag
    return t


def mirror(t, n):
    if t is None:
        return None
    return [n + 1 - t[0], mirror(t[2], n), mirror(t[1], n)]


def main():
    import wp6_cycle_ratio as O
    recs = []

    def add(n, A, B, x, mo, tag):
        valid(A, n, tag + "-A")
        valid(B, n, tag + "-B")
        ev = []
        harvest(A, B, x, mo, tag, ev)
        rep = V.replay(A, B, [(mo, x)])
        acc = rep["accesses"][0]
        if mo != "K" or not ev:
            return
        p0, _, t0, d0 = ev[0]["pat"], None, None, None
        p, sz, t, d = ev[0]["pat"], None, ev[0]["twinDrop"], ev[0]["DbDrop"]
        first_pay = t + d
        w = acc["eps"]
        need = w - first_pay
        rem = len(ev) - 1
        rec = {"n": n, "A": A, "B": B, "x": x, "mo": mo, "tag": tag,
               "a": acc["a"], "q": acc["q"], "w": w, "need": need,
               "rem": rem, "first": [p, first_pay], "ev": ev}
        recs.append(rec)
        step("E", "%s n=%d x=%d a=%d q=%d w=%d need=%d rem=%d" %
             (tag, n, x, acc["a"], acc["q"], w, need, rem))

    for n in (9, 10, 11, 12, 13, 14, 15, 16):
        add(n, [1, None, vr(range(2, n + 1))], vl(range(1, n + 1)), 1,
            "K", "V1-%d" % n)
    for n in (11, 16, 32):
        add(n, [n, vl(range(1, n)), None], vr(range(1, n + 1)), n,
            "K", "V1m-%d" % n)
    for n in (9, 10, 11, 12):
        A = [1, None, [8, [7, vr(range(2, 7)), None], vr(range(9, n + 1))]]
        add(n, A, vr(range(1, n + 1)), 7, "K", "TW-%d" % n)
    # random search n=10..12
    rng = random.Random(31)
    for n in (10, 11, 12):
        Sh = O.shapes_of(list(range(1, n + 1)))
        tried = 0
        for _ in range(6000):
            ia = rng.randrange(len(Sh))
            ib = rng.randrange(len(Sh))
            x = rng.randint(1, n)
            rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
            acc = rep["accesses"][0]
            if acc["q"] < 2 or acc["eps"] < 2:
                continue
            tried += 1
            add(n, Sh[ia], Sh[ib], x, "K", "R%d-%d" % (n, tried))
            if tried >= 40:
                break
        step("R", "n=%d scanned kept=%d" % (n, tried))
    # mirrors of first few high-need finds (decided post-hoc below: mirror
    # the vine family representatives + any need>=3 random finds)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "highneed_bank.json").write_text(
        json.dumps(recs, indent=0, default=str), encoding="utf-8")
    hn = [r for r in recs if r["need"] >= 3 and r["rem"] >= 1]
    step("S", "total=%d high-need+remainder=%d" % (len(recs), len(hn)))
    step("S", "needs=%s" %
         sorted(set(r["need"] for r in hn)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
