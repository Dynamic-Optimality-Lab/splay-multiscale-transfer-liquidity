"""WP-6 STAGE 3: capped-sum mass screen + M3-creation case-analysis evidence.

Capped mass C(v) = min(max(0, dB(v)-2*dA(v)), CAP), M = sum_v C(v).
Per-record cap bounds per-record gain (<=CAP per changed record, <=3 records
per StepEv by Lemma A) -> creation <= 3*CAP per StepEv is TESTABLE (not assumed).
Measure: A-create worst, B-transport worst (want <=0, expect leak), KEEP drop vs
need. Also M3-creation distribution (per-A-StepEv max-div increase histogram)
as evidence for the micro-lemma case analysis.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_quotient import to_ptr, intervals, depths
from liquidity import legacy_embedding as PE
from solver import encode as E

CAP = 2


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def capped(dA, dB):
    return sum(min(max(0, dB[k] - 2 * dA[k]), CAP) for k in dA)


def m3(dA, dB):
    return max([0] + [dB[k] - 2 * dA[k] for k in dA])


def snap(A, B):
    return (depths(A), depths(B))


def main() -> int:
    # WP-6 STAGE 3: capped-sum transport screen + M3 creation histogram.
    step("S3-00", "Capped-sum (CAP=2) mass-transport screen")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"s3|%s|%d" % (self.s, self.c)).digest()

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
    histA = {}
    nA = 0
    for t in range(250):
        rng = DRBG(("s3%d" % t).encode())
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
            step("S3-KILL", "present kill t=%d" % t)
            return 2
        kps = iter(res["keeps"])
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            _, path = PE._depth_to(A, xx)
            node = path[-1]
            while node["p"] is not None:
                dA0, dB0 = snap(A, B)
                m0, q0 = capped(dA0, dB0), m3(dA0, dB0)
                do_rot(node)
                dA1, dB1 = snap(A, B)
                dd = capped(dA1, dB1) - m0
                if dd > worstA:
                    worstA, exA = dd, (t, mode, xx)
                dq = m3(dA1, dB1) - q0
                histA[dq] = histA.get(dq, 0) + 1
                nA += 1
            if mode == "KEEP":
                kp = next(kps)
                dA0, dB0 = snap(A, B)
                M0 = capped(dA0, dB0)
                _, path = PE._depth_to(B, xx)
                node = path[-1]
                while node["p"] is not None:
                    dA0, dB0 = snap(A, B)
                    m0 = capped(dA0, dB0)
                    do_rot(node)
                    dA1, dB1 = snap(A, B)
                    dd = capped(dA1, dB1) - m0
                    if dd > worstB:
                        worstB, exB = dd, (t, xx)
                dA1, dB1 = snap(A, B)
                gap = kp["need"] - (M0 - capped(dA1, dB1))
                if gap > worstK:
                    worstK, exK = gap, (t, xx, kp["need"])
    step("S3-01", "capped-sum worst A-create=%d %s (budget 3*CAP=%d)"
         % (worstA, exA, 3 * CAP))
    step("S3-01", "capped-sum worst B-increase=%d %s (want<=0)" % (worstB, exB))
    step("S3-01", "capped-sum worst KEEP gap=%d %s (want<=0)" % (worstK, exK))
    step("S3-02", "M3 per-A-StepEv increase histogram n=%d: %s"
         % (nA, dict(sorted(histA.items()))))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "mass_capped.json").write_text(
        json.dumps({"CAP": CAP, "A_create": worstA, "A_ex": exA,
                    "B_increase": worstB, "B_ex": exB,
                    "KEEP_gap": worstK, "K_ex": exK,
                    "M3_hist": histA, "n_A_events": nA,
                    "verdict": ("B-CONSERVATION FAILS" if worstB > 0 else "holds") + " / " +
                               ("KEEP-CONSUME FAILS" if worstK > 0 else "holds")},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
