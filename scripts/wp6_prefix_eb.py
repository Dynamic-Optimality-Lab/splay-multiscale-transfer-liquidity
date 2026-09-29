"""WP-6 STEP PX-00: prefix-closedness of E_B <= 3*S_A.

Stock needs PREFIX bounds (D(t)<=6*S_A(t) for EVERY prefix). Via D2-sum this
needs PREFIX E_B(t)<=3*S_A(t). Measure worst prefix gap E_B-3*S_A over hostile
histories. Positive gap => E_B-route NOT prefix-inductive (route dead as a
prefix lemma; full-history version unprovable by prefix induction).
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
    # WP-6 STEP PX-00: prefix gap screen.
    step("PX-00", "Prefix-closedness of E_B <= 3*S_A")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"px|%s|%d" % (self.s, self.c)).digest()

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

    worst = -10**18
    ex = None
    n_hist = 0
    for t in range(500):
        rng = DRBG(("px%d" % t).encode())
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
            step("PX-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        eb = sa = 0
        for idx, acc in enumerate(pre):
            if acc["mode"] == "KEEP":
                eb += len(acc["Bev"])
            sa += sum(1 for z in acc["sites"] if z)
            gap = eb - 3 * sa
            if gap > worst:
                worst, ex = gap, (t, idx, eb, sa)
        n_hist += 1
    step("PX-01", "hist=%d worst prefix E_B-3S_A gap=%d %s (want<=0)" % (n_hist, worst, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "prefix_eb.json").write_text(
        json.dumps({"histories": n_hist, "worst_prefix_gap": worst, "ex": ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
