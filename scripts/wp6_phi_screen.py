"""WP-6 STEP: potential-candidate tester (discovery only).

For candidate potentials Phi(A,B), checks the per-access telescoping
inequality need_j <= 6*s_j + Phi_before - Phi_after on hostile histories
(DELETE: need_j = 0). Reports worst violation per Phi. A survivor earns a
local case-table proof attempt; a violator is discarded with its witness.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from liquidity import legacy_embedding as PE


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def depths(t):
    out = {}

    def rec(u, d):
        if u is None:
            return
        out[u[0]] = d
        rec(u[1], d + 1)
        rec(u[2], d + 1)

    rec(t, 0)
    return out


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def to_nested(p):
    # pointer -> nested via iterative traversal using structure
    if p is None:
        return None
    # find root
    r = p
    while r["p"] is not None:
        r = r["p"]
    # iterative deep copy to nested
    def conv(u):
        if u is None:
            return None
        return [u["k"], conv(u["l"]), conv(u["r"])]
    sys.setrecursionlimit(10000)
    try:
        return conv(r)
    finally:
        sys.setrecursionlimit(1000)


def PHI(name, dA, dB):
    if name == "2IPL_A-IPL_B":
        return 2 * sum(dA.values()) - sum(dB.values())
    if name == "IPL_B-2IPL_A":
        return sum(dB.values()) - 2 * sum(dA.values())
    if name == "IPL_A":
        return sum(dA.values())
    if name == "IPL_B":
        return sum(dB.values())
    raise ValueError(name)


def main() -> int:
    # WP-6 STEP PT-00: build hostile history corpus with live-tree tracking.
    step("PT-00", "Building corpus + live A/B trees")
    import hashlib as _h

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0
        def b(self):
            self.c += 1
            return _h.sha256(b"phi|%s|%d" % (self.s, self.c)).digest()
        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n
        def ir(self, a, b): return a + self.below(b - a + 1)
        def ch(self, s): return s[self.below(len(s))]

    def vine(n):
        t = None
        for k in range(n, 0, -1):
            t = [k, None, t]
        return t

    names = ["2IPL_A-IPL_B", "IPL_B-2IPL_A", "IPL_A", "IPL_B"]
    worst = {nm: [0, None] for nm in names}  # [worst_excess, case]
    n_hist = 0
    for t in range(1500):
        rng = DRBG(("p%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n)
        A, B = to_ptr(T0), to_ptr(T0)
        L = rng.ir(2, 12)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        # live simulation with sited counts via exec parity: use E.precompute
        # on full history for sited/a/y/need, and live trees for depths.
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        kps = iter(res["keeps"])
        A2, B2 = to_ptr(T0), to_ptr(T0)
        sited_cum = 0
        for acc in pre:
            mode = acc["mode"]
            xx = acc["x"]
            sited_cum += sum(1 for s in acc["sites"] if s)
            s_j = sum(1 for s in acc["sites"] if s)
            dA0, dB0 = depths(to_nested(A2)), depths(to_nested(B2))
            a = PE.splay_cost(A2, xx)
            A2, _ = PE.splay_trace(A2, xx)
            if mode == "KEEP":
                kp = next(kps)
                y = PE.splay_cost(B2, xx)
                B2, _ = PE.splay_trace(B2, xx)
                need = kp["need"]
            else:
                y, need = 0, 0
            dA1, dB1 = depths(to_nested(A2)), depths(to_nested(B2))
            for nm in names:
                excess = need - 6 * s_j - (PHI(nm, dA0, dB0) - PHI(nm, dA1, dB1))
                if excess > worst[nm][0]:
                    worst[nm] = [excess, {"t": t, "mode": mode, "x": xx, "a": a,
                                          "y": y, "need": need, "s": s_j}]
        n_hist += 1
    # WP-6 STEP PT-01: report per-potential worst excess (must be <= 0 to survive).
    step("PT-01", "Per-potential worst excess over %d histories" % n_hist)
    for nm, (w, c) in worst.items():
        print("[WP-6][STEP PT-01] Phi=%s worst_excess=%d case=%s" % (nm, w, c), flush=True)
    Path(ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "phi_screen.json").write_text(
        json.dumps({nm: {"worst_excess": w, "case": c} for nm, (w, c) in worst.items()},
                   indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
