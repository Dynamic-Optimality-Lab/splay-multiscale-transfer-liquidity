"""WP-6 STAGE 3b: size-capped mass screen.

C(v) = min(max(0, |IB(v)|-2*|IA(v)|), CAP), M = sum. Rotations change O(1)
interval records (Lemma A) -> creation budget 3*CAP per StepEv TESTABLE.
B-conservation (want<=0) and KEEP-consume (want gap<=0) measured; B-leak and
bystander mechanisms expected to fail both.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_quotient import to_ptr, intervals
from liquidity import legacy_embedding as PE
from solver import encode as E

CAP = 2


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def capped(iA, iB):
    s = 0
    for k in iA:
        sa = iA[k][1] - iA[k][0] + 1
        sb = iB[k][1] - iB[k][0] + 1
        d = sb - 2 * sa
        s += min(max(0, d), CAP)
    return s


def main() -> int:
    # WP-6 STAGE 3b: size-capped mass screen.
    step("S3b-00", "Size-capped (CAP=2) mass screen")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"s3b|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    def do_rot(node):
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
        else:
            PE._rot_right(p)
            PE._rot_left(g)

    worstA = -10**18
    worstB = -10**18
    worstK = -10**18
    exA = exB = exK = None
    for t in range(250):
        rng = DRBG(("s3b%d" % t).encode())
        n = 32
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 10)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("S3b-KILL", "present kill t=%d" % t)
            return 2
        kps = iter(res["keeps"])
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            _, path = PE._depth_to(A, xx)
            node = path[-1]
            while node["p"] is not None:
                m0 = capped(intervals(A), intervals(B))
                do_rot(node)
                dd = capped(intervals(A), intervals(B)) - m0
                if dd > worstA:
                    worstA, exA = dd, (t, mode, xx)
            if mode == "KEEP":
                kp = next(kps)
                M0 = capped(intervals(A), intervals(B))
                _, path = PE._depth_to(B, xx)
                node = path[-1]
                while node["p"] is not None:
                    m0 = capped(intervals(A), intervals(B))
                    do_rot(node)
                    dd = capped(intervals(A), intervals(B)) - m0
                    if dd > worstB:
                        worstB, exB = dd, (t, xx)
                gap = kp["need"] - (M0 - capped(intervals(A), intervals(B)))
                if gap > worstK:
                    worstK, exK = gap, (t, xx, kp["need"])
    step("S3b-01", "size-capped worst A-create=%d %s (budget %d)"
         % (worstA, exA, 3 * CAP))
    step("S3b-01", "size-capped worst B-increase=%d %s (want<=0)" % (worstB, exB))
    step("S3b-01", "size-capped worst KEEP gap=%d %s (want<=0)" % (worstK, exK))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "mass_capped_size.json").write_text(
        json.dumps({"CAP": CAP, "A_create": worstA, "A_ex": exA,
                    "B_increase": worstB, "B_ex": exB,
                    "KEEP_gap": worstK, "K_ex": exK}, indent=1,
                   sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
