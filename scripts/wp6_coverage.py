"""WP-6 STEP CV-00: prefix coverage invariant (Vm+F >= Vp?).

Vm = sum max(0,3*e_A-e_B) (anti), F = 1.5*sum_DEL d_A (DELETE-Q),
Vp = sum max(0,e_B-3*e_A) (excess). Coverage C(t) = Vm+F-Vp per prefix.
C>=0 everywhere + F<=3*S_A^del (termwise d_A<=2*e_A) => E_B<=3*S_A (algebra).
Measure prefix-min C + excess/C-slack ratio (tight or loose?).
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
    # WP-6 STEP CV-00: prefix coverage.
    step("CV-00", "Prefix coverage invariant")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"cv|%s|%d" % (self.s, self.c)).digest()

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

    minC = 10**18
    exC = None
    worst_tight = -1.0
    exT = None
    n_hist = 0
    for t in range(400):
        rng = DRBG(("cv%d" % t).encode())
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
            step("CV-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        Vm = F = Vp = 0.0
        for idx, acc in enumerate(pre):
            eA = sum(1 for z in acc["sites"] if z)
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                if eB - 3 * eA > 0:
                    X = eB - 3 * eA
                    Cbefore = Vm + F - Vp
                    if Cbefore > 0 and X / Cbefore > worst_tight:
                        worst_tight, exT = X / Cbefore, (t, idx, X, Cbefore)
                    Vp += X
                else:
                    Vm += 3 * eA - eB
            else:
                F += 1.5 * (acc["a"] - 1)
            C = Vm + F - Vp
            if C < minC:
                minC, exC = C, (t, idx, acc["mode"], Vm, F, Vp)
        n_hist += 1
    step("CV-01", "hist=%d prefix-min coverage=%0.2f %s (want>=0)" % (n_hist, minC, exC))
    step("CV-01", "worst excess/C-slack=%0.4f %s" % (worst_tight, exT))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "coverage.json").write_text(
        json.dumps({"histories": n_hist, "min_coverage": minC, "cov_ex": exC,
                    "worst_tight": worst_tight, "tight_ex": exT},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
