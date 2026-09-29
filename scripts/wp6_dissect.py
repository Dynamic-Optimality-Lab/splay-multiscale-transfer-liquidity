"""WP-6 STEP DX-00: saturation dissection (read the witnesses, don't theorize).

Dissect: (a) J1/J2 argmax shape (rebuilt: n=128 vine + pump-biased seed that
hit E_B/S_A=1.57, R/Q=1.58); (b) high-excess single accesses (e_B>>3*e_A);
(c) per-access (d_A,d_B,e_A,e_B,slack-before,excess,pumps-since,backing).
Goal: exhibit EXPLICITLY what funds each excess (pump-backing? DELETE-Q?
anti-volume?) and identify the saturation invariant.
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
    # WP-6 STEP DX-00: dissection.
    step("DX-00", "Saturation dissection")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"dx|%s|%d" % (self.s, self.c)).digest()

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

    # rebuild a saturation-shape history: n=128, pump-heavy, then scan ALL
    # prefixes/accesses for top excess + print their full context
    top = []
    for t in range(300):
        rng = DRBG(("dx%d" % t).encode())
        n = 128
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(10, 30)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("DX-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        eb = sa = 0
        R = Q = 0
        for idx, acc in enumerate(pre):
            eA = sum(1 for z in acc["sites"] if z)
            dA = acc["a"] - 1
            Q += dA
            sa += eA
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                dB = acc["y"] - 1
                X = eB - 3 * eA
                slack_before = 3 * sa - eb
                if X > 8:
                    top.append((X, t, idx, acc["x"], eA, eB, dA, dB,
                                slack_before, sa, eb, R, Q))
                eb += eB
                R += dB
    top.sort(reverse=True)
    step("DX-01", "top-excess accesses (X,t,idx,x,eA,eB,dA,dB,slack,SA,EB,R,Q):")
    for row in top[:12]:
        step("DX-01", str(row))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "dissect.json").write_text(
        json.dumps({"top": top[:40]}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
