"""Property tests for D1/D2 local present mechanics.

D1: present + need>0 ==> B trace nonempty; Aev=Bev=0 ==> need=0.
D2: ceil((y-1)/2) <= len(Bev) <= y-1; 2*len(Bev) >= need.
Present-only enforced (keys drawn from keys(T0)).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def bst(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], bst(keys[:m]), bst(keys[m + 1:])]


def histories():
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"pm|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    out = []
    for t in range(400):
        rng = DRBG(("pm%d" % t).encode())
        n = rng.ch([8, 16, 32, 64])
        ks = list(range(1, n + 1))
        T0 = bst(ks)
        L = rng.ir(2, 12)
        H = [[rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)] for _ in range(L)]
        out.append((n, T0, H))
    return out


def test_d1_need_implies_b_work():
    for (n, T0, H) in histories():
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        for acc, kp in zip([a for a in pre if a["mode"] == "KEEP"], res["keeps"]):
            if kp["need"] > 0:
                assert len(acc["Bev"]) > 0, "D1 violated"
            if not acc["Aev"] and not acc["Bev"]:
                assert kp["need"] == 0, "D1 corollary violated"


def test_d2_event_count_bounds():
    import math
    for (n, T0, H) in histories():
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        for acc, kp in zip([a for a in pre if a["mode"] == "KEEP"], res["keeps"]):
            d = acc["y"] - 1
            e = len(acc["Bev"])
            assert math.ceil(d / 2) <= e <= max(d, 0) or (d == 0 and e == 0)
            assert 2 * e >= kp["need"], "raw bandwidth violated"


def test_d2_a_empty_forces_b_work():
    for (n, T0, H) in histories():
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        for acc, kp in zip([a for a in pre if a["mode"] == "KEEP"], res["keeps"]):
            if not acc["Aev"] and kp["need"] > 0:
                assert acc["a"] == 1 and acc["y"] >= 3 and len(acc["Bev"]) > 0
