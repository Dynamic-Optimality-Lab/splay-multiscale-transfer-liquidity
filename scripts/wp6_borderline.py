"""WP-6 STEP BL2-00: borderline-crossing hunt (decides N-FIRST shape).

Margin m(y) = c_B(y) - 3*c_A(y) (exact StepEv costs, pointer clones).
Borderline: m == 0 exactly (non-hazardous, zero margin).
Crossing: symdiff-push (B-rotated, A-rigid) with post margin > 0.
Parity gate: even-depth pushes add a StepEv, odd-depth absorbed by doubles.
500+ cashes over hostile histories; every borderline bystander tracked.
FOUND => N-FIRST needs borderline allowance term (exact shape recorded).
NEVER (500+ cashes, exact steps) => margin-absorption structurally sound
(parity+position conspire); N-FIRST formalization proceeds.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_cashchain import to_ptr, clone, evc, splay_sets
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def depths_keys(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    out = {}

    def rec(u, d):
        if u is None:
            return
        out[u["k"]] = d
        rec(u["l"], d + 1)
        rec(u["r"], d + 1)

    rec(r, 0)
    return out


def main() -> int:
    # WP-6 STEP BL2-00.
    step("BL2-00", "Borderline-crossing hunt")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"bl|%s|%d" % (self.s, self.c)).digest()

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

    n_borderline = 0
    n_cross = 0
    ex_cross = None
    n_cash = 0
    parity = {"even_push": 0, "odd_push": 0}
    for t in range(200):
        rng = DRBG(("bl%d" % t).encode())
        n = rng.ch([32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("BL2-KILL", "present kill t=%d" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            if mode == "KEEP":
                eA = sum(1 for z in acc["sites"] if z)
                eB = len(acc["Bev"])
                if eB - 3 * eA <= 0:
                    A, _ = PE.splay_trace(A, xx)
                    B, _ = PE.splay_trace(B, xx)
                    continue
                n_cash += 1
                dB0 = depths_keys(B)
                _, Arot, _ = splay_sets(clone(A), xx)
                _, _, Bpush = splay_sets(clone(B), xx)
                RA = set()
                for S in Arot:
                    RA |= S
                # pre margins + parity, post margins for symdiff-pushed
                pre_m = {}
                for y in range(1, n + 1):
                    if y == xx:
                        continue
                    pre_m[y] = evc(B, y) - 3 * evc(A, y)
                A, _ = PE.splay_trace(A, xx)
                B, _ = PE.splay_trace(B, xx)
                for y in range(1, n + 1):
                    if y == xx:
                        continue
                    inB = any(y in P for P in Bpush)
                    inA = y in RA
                    if inB and not inA and pre_m[y] == 0:
                        n_borderline += 1
                        post = evc(B, y) - 3 * evc(A, y)
                        if dB0[y] % 2 == 0:
                            parity["even_push"] += 1
                        else:
                            parity["odd_push"] += 1
                        if post > 0:
                            n_cross += 1
                            if ex_cross is None:
                                ex_cross = (t, xx, y, dB0[y], post)
            else:
                A, _ = PE.splay_trace(A, xx)
    step("BL2-01", "cashes=%d borderline-symdiff=%d crossed=%d %s parity=%s" %
         (n_cash, n_borderline, n_cross, ex_cross, parity))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "borderline.json").write_text(
        json.dumps({"cashes": n_cash, "borderline": n_borderline,
                    "crossed": n_cross, "ex": ex_cross, "parity": parity},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
