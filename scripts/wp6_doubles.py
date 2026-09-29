"""WP-6 STEP DB-00: B-doubles vs S_A (zig/doubles split of E_B).

E_B = D_B (doubles) + Z_B (zigs, <=1/splay). With #cash<=S_A and
#noncash<=S_A (setup/nonearning arguments), Z_B <= 2*S_A, so E_B<=3*S_A
follows from D_B <= S_A. Measure worst D_B/S_A + cash/setup counts.
D_B/S_A > 1 kills this split (record). Also verify #cash<=S_A empirically
and setup-distinctness (each cash has a prior earning setup access).
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
    # WP-6 STEP DB-00: doubles split.
    step("DB-00", "B-doubles vs S_A + cash accounting")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"db|%s|%d" % (self.s, self.c)).digest()

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

    wDB = 0.0
    exDB = None
    wCash = 0  # max over histories of #cash - S_A (want <=0)
    exCash = None
    n_hist = 0
    for t in range(500):
        rng = DRBG(("db%d" % t).encode())
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
            step("DB-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        DB = 0
        SA = 0
        ncash = 0
        for acc in pre:
            eA = sum(1 for z in acc["sites"] if z)
            SA += eA
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                DB += sum(1 for (c, l, h) in acc["Bev"] if c != "ZIG")
                if eA == 0 and eB > 0:
                    ncash += 1
        if SA > 0 and DB / SA > wDB:
            wDB, exDB = DB / SA, (t, DB, SA)
        if ncash - SA > wCash:
            wCash, exCash = ncash - SA, (t, ncash, SA)
        n_hist += 1
    step("DB-01", "hist=%d worst D_B/S_A=%0.4f %s (want<=1)" % (n_hist, wDB, exDB))
    step("DB-01", "worst #cash-S_A=%d %s (want<=0)" % (wCash, exCash))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "doubles.json").write_text(
        json.dumps({"histories": n_hist, "worst_DB_SA": wDB, "DB_ex": exDB,
                    "worst_cash_SA": wCash, "cash_ex": exCash},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
