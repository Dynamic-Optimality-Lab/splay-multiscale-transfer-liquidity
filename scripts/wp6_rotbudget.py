"""WP-6 STEP RB-00: rotation-budget ratios (descent to coupled semigroup).

Measure on hostile + pump-heavy histories:
  r1 = R^B / (6*S_A)      (want <=1: the alive auxiliary R^B<=6*S_A)
  r2 = E_B / (3*S_A)      (want <=1: E_B<=3*S_A + D2-sum => stock in 2 lines)
  r3 = sumneed / R^B      (L1 tightness: ~1 means L1 tight, <<1 means slack)
  r4 = sumneed / (2*E_B)  (D2-sum tightness)
Any r1>1 kills the R^B-route (NOT stock); any r2>1 kills the E_B-route.
r3<<1 would mean needs are a small fraction of B-work (alignment rarity).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP RB-00: rotation-budget ratios.
    step("RB-00", "Rotation-budget ratio measurement")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"rb|%s|%d" % (self.s, self.c)).digest()

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

    w1 = w2 = 0.0
    ex1 = ex2 = None
    sum_r3 = sum_r4 = 0.0
    cnt_r3 = cnt_r4 = 0
    n_hist = 0
    for t in range(600):
        rng = DRBG(("rb%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 5 == 4:
                # pump bias: DELETE far keys (A-churn, B frozen), then KEEP x
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("RB-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        # B-rotations per B-StepEv class: ZIG 1, doubles 2 (structural)
        RB = 0
        EB = 0
        for acc in pre:
            if acc["mode"] == "KEEP":
                for (cls, lo, hi) in acc["Bev"]:
                    EB += 1
                    RB += 1 if cls == "ZIG" else 2
        SA = sum(1 for acc in pre for z in acc["sites"] if z)
        SN = sum(k["need"] for k in res["keeps"])
        if SA > 0:
            if RB / (6 * SA) > w1:
                w1, ex1 = RB / (6 * SA), (t, RB, SA)
            if EB / (3 * SA) > w2:
                w2, ex2 = EB / (3 * SA), (t, EB, SA)
        if RB > 0:
            sum_r3 += SN / RB
            cnt_r3 += 1
        if EB > 0:
            sum_r4 += SN / (2 * EB)
            cnt_r4 += 1
        n_hist += 1
    step("RB-01", "hist=%d worst R^B/6SA=%0.4f %s (want<=1)" % (n_hist, w1, ex1))
    step("RB-01", "worst E_B/3SA=%0.4f %s (want<=1)" % (w2, ex2))
    step("RB-01", "mean sumneed/R^B=%0.4f (L1 tightness)" % (sum_r3 / max(1, cnt_r3)))
    step("RB-01", "mean sumneed/2E_B=%0.4f (D2-sum tightness)" % (sum_r4 / max(1, cnt_r4)))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "rotbudget.json").write_text(
        json.dumps({"histories": n_hist, "worst_RB": w1, "RB_ex": ex1,
                    "worst_EB": w2, "EB_ex": ex2,
                    "mean_need_RB": sum_r3 / max(1, cnt_r3),
                    "mean_need_2EB": sum_r4 / max(1, cnt_r4)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
