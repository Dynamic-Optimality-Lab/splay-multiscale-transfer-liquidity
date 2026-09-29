"""WP-6 STEP RQ-00: reset-depth ratio R vs Q (B-reset-depth vs A-reset-depth).

R = sum_KEEPS d_B(pre-splay); Q = sum_ALL d_A(pre-splay).
Chain (all termwise-safe except the middle link):
  E_B <= R (e_B<=d_B) ; R <=? 1.5*Q ; Q <= 2*S_A (d_A<=2*e_A)
=> E_B <= 3*S_A (with D2 => stock). Measure full-history R/Q and PREFIX
R-1.5*Q gaps. Prefix violation kills this link (record). KEEP-only histories
should show R-1.5Q<=0 (no divergence source) -- verify as control.
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
    # WP-6 STEP RQ-00: reset-depth ratios.
    step("RQ-00", "Reset-depth ratio R vs Q")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"rq|%s|%d" % (self.s, self.c)).digest()

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

    wRQ = 0.0
    exRQ = None
    wPX = -10**18
    exPX = None
    keep_only_bad = 0
    n_hist = 0
    for t in range(500):
        rng = DRBG(("rq%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 24)
        x = rng.ir(1, n)
        keep_only = (t % 5 == 0)
        H = []
        for i in range(L):
            if keep_only:
                H.append(["KEEP", x])
            elif i % 5 == 4:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("RQ-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        R = Q = 0
        for idx, acc in enumerate(pre):
            dA = acc["a"] - 1
            Q += dA
            if acc["mode"] == "KEEP":
                R += acc["y"] - 1
            gap = R - 1.5 * Q
            if gap > wPX:
                wPX, exPX = gap, (t, idx, R, Q)
        if Q > 0 and R / Q > wRQ:
            wRQ, exRQ = R / Q, (t, R, Q)
        if keep_only and R - 1.5 * Q > 0:
            keep_only_bad += 1
        n_hist += 1
    step("RQ-01", "hist=%d worst R/Q=%0.4f %s (want<=1.5)" % (n_hist, wRQ, exRQ))
    step("RQ-01", "worst prefix R-1.5Q gap=%0.2f %s (want<=0)" % (wPX, exPX))
    step("RQ-01", "KEEP-only violations=%d (want 0)" % keep_only_bad)
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "resetdepth.json").write_text(
        json.dumps({"histories": n_hist, "worst_RQ": wRQ, "RQ_ex": exRQ,
                    "worst_prefix_gap": wPX, "PX_ex": exPX,
                    "keep_only_bad": keep_only_bad},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
