"""WP-6 STEP FD-00: funding-source decomposition (who funds excess?).

Excess volume V+ = sum_KEEPS max(0, e_B-3*e_A) (drains).
Anti volume V- = sum_KEEPS max(0, 3*e_A-e_B) (offsets).
DELETE funding F = 1.5 * sum_DELETES d_A.
Coverage: (V- + F) / V+ (want >= 1: anti+DELETEs fund excess).
Also: excess-KEEP count/volume vs anti-KEEP count/volume (frequency symmetry?),
pure-pump share, revelation share (Psi-jump vs push-built).
Determines whether DELETE-funding is a viable door.
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
    # WP-6 STEP FD-00: funding decomposition.
    step("FD-00", "Funding-source decomposition")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"fd|%s|%d" % (self.s, self.c)).digest()

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

    wCov = 10**18
    exCov = None
    totVp = totVm = totF = 0
    n_ex = n_an = 0
    n_hist = 0
    for t in range(400):
        rng = DRBG(("fd%d" % t).encode())
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
            step("FD-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        Vp = Vm = F = 0.0
        for acc in pre:
            eA = sum(1 for z in acc["sites"] if z)
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                if eB - 3 * eA > 0:
                    Vp += eB - 3 * eA
                    n_ex += 1
                else:
                    Vm += 3 * eA - eB
                    n_an += 1
            else:
                F += 1.5 * (acc["a"] - 1)
        totVp += Vp
        totVm += Vm
        totF += F
        if Vp > 0 and (Vm + F) / Vp < wCov:
            wCov, exCov = (Vm + F) / Vp, (t, Vp, Vm, F)
        n_hist += 1
    step("FD-01", "hist=%d excessVol=%0.1f antiVol=%0.1f DELfund=%0.1f n_ex=%d n_an=%d"
         % (n_hist, totVp, totVm, totF, n_ex, n_an))
    step("FD-01", "worst coverage (V-+F)/V+=%0.4f %s (want>=1)" % (wCov, exCov))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "funding.json").write_text(
        json.dumps({"histories": n_hist, "excessVol": totVp, "antiVol": totVm,
                    "DELfund": totF, "n_excess": n_ex, "n_anti": n_an,
                    "worst_coverage": wCov, "cov_ex": exCov},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
