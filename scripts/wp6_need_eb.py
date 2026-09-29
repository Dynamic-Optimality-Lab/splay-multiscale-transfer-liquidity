"""WP-6 STEP DE-00: needs vs B-StepEvs (D <= E_B screen for the weaker door).

If D <= E_B (global + prefix) held: stock follows from R^B<=6*S_A (alive L2:
E_B <= R^B since >=1 rotation/StepEv). Two weaker links (D/E_B~0.40 measured
mean) instead of one tight (E_B<=3*S_A). Measure worst D/E_B + prefix gaps.
Violation kills this door (record); survival descends to L2 assault + D<=E_B.
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
    # WP-6 STEP DE-00: D vs E_B.
    step("DE-00", "Needs vs B-StepEvs")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"de|%s|%d" % (self.s, self.c)).digest()

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

    wR = 0.0
    exR = None
    wPX = -10**18
    exPX = None
    n_hist = 0
    for t in range(500):
        rng = DRBG(("de%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 5 == 4:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("DE-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        D = EB = 0
        ki = 0
        kps = list(res["keeps"])
        for acc in pre:
            if acc["mode"] == "KEEP":
                D += kps[ki]["need"]
                ki += 1
                EB += len(acc["Bev"])
            if EB > 0 and D / EB > wR:
                wR, exR = D / EB, (t, D, EB)
            gap = D - EB
            if gap > wPX:
                wPX, exPX = gap, (t, D, EB)
        n_hist += 1
    step("DE-01", "hist=%d worst D/E_B=%0.4f %s (want<=1)" % (n_hist, wR, exR))
    step("DE-01", "worst prefix D-E_B gap=%d %s (want<=0)" % (wPX, exPX))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "need_eb.json").write_text(
        json.dumps({"histories": n_hist, "worst_ratio": wR, "ratio_ex": exR,
                    "worst_prefix_gap": wPX, "px_ex": exPX},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
