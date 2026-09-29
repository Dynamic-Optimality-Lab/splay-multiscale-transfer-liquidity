"""WP-6 STAGE 4: senary discharge verification (pool accounting).

Direct pool simulation: income 6 per A-StepEv into a global pool; each KEEP
pays need from the pool (greedy, in order). Measure worst deficit
(paid-shortfall) and worst need-to-income ratio over hostile histories.
A systematic deficit with a mechanism = the pool route fails as stated;
the RAW inequality (sum need <= 6*S_A) is tested separately in Stage 7
(a discharge deficit is NOT a refutation by itself).
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
    # WP-6 STAGE 4: senary discharge accounting.
    step("S4-00", "Greedy 6-per-A-event pool discharge simulation")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"s4|%s|%d" % (self.s, self.c)).digest()

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

    worst_short = 0
    worst_ratio = 0.0
    exS = exR = None
    tot_need = tot_inc = 0
    for t in range(600):
        rng = DRBG(("s4%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 16)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("S4-KILL", "present kill t=%d" % t)
            return 2
        pool = 0
        kps = list(res["keeps"])
        ki = 0
        for acc in pre:
            pool += 6 * len(acc["Aev"])
            tot_inc += 6 * len(acc["Aev"])
            if acc["mode"] == "KEEP":
                nd = kps[ki]["need"]
                tot_need += nd
                ki += 1
                if pool >= nd:
                    pool -= nd
                else:
                    short = nd - pool
                    if short > worst_short:
                        worst_short, exS = short, (t, acc["x"], nd)
                    pool = 0
        sa = sum(len(a["Aev"]) for a in pre)
        sn = sum(k["need"] for k in kps)
        if sa > 0 and sn / (6 * sa) > worst_ratio:
            worst_ratio, exR = sn / (6 * sa), (t, sn, sa)
    step("S4-01", "worst greedy shortfall=%d %s; global need/income=%0.4f; worst-history ratio=%0.4f %s"
         % (worst_short, exS, tot_need / max(1, tot_inc), worst_ratio, exR))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "discharge_greedy.json").write_text(
        json.dumps({"worst_shortfall": worst_short, "short_ex": exS,
                    "global_ratio": tot_need / max(1, tot_inc),
                    "worst_history_ratio": worst_ratio, "ratio_ex": exR},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
