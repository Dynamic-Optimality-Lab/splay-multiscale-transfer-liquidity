"""WP-6 STEP FS-00: freshness split (fresh/genesis exactness + stale fraction).

Fresh access = key at BOTH roots pre-splay (e_A=e_B=0, contributes nothing).
Genesis-region access = A_t==B_t as trees (same splay => e_A==e_B exactly).
Measure: fresh fraction, genesis-region fraction, stale E_B/S_A split,
genesis E_B/E_A equality violations (want 0: same-tree same-splay).
Validates freshness-exactness; quantifies the stale (sharing) remainder.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


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


def canon(t):
    if t is None:
        return "."
    r = t
    while r["p"] is not None:
        r = r["p"]
    return PE.canonical(r)


def main() -> int:
    # WP-6 STEP FS-00: freshness split.
    step("FS-00", "Freshness split")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"fs|%s|%d" % (self.s, self.c)).digest()

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

    n_fresh = n_gen = n_acc = 0
    stale_EB = stale_SA = 0
    gen_viol = 0
    n_hist = 0
    for t in range(300):
        rng = DRBG(("fs%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 18)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("FS-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            n_acc += 1
            eA = sum(1 for z in acc["sites"] if z)
            dA, pa = PE._depth_to(A, xx)
            fresh = (dA == 0)
            if mode == "KEEP":
                dB, pb = PE._depth_to(B, xx)
                fresh = fresh and (dB == 0)
            if fresh:
                n_fresh += 1
                if eA != 0 or (mode == "KEEP" and len(acc["Bev"]) != 0):
                    step("FS-FAIL", "fresh access did work t=%d" % t)
                    return 2
            gen = (canon(A) == canon(B))
            if gen:
                n_gen += 1
                if mode == "KEEP" and len(acc["Bev"]) != len(acc["Aev"]):
                    gen_viol += 1
            else:
                stale_EB += len(acc["Bev"]) if mode == "KEEP" else 0
                stale_SA += eA
            A, _ = PE.splay_trace(A, xx)
            if mode == "KEEP":
                B, _ = PE.splay_trace(B, xx)
        n_hist += 1
    step("FS-01", "hist=%d acc=%d fresh=%0.3f genesis=%0.3f gen-viol=%d"
         % (n_hist, n_acc, n_fresh / n_acc, n_gen / n_acc, gen_viol))
    step("FS-01", "stale EB=%d SA=%d ratio=%0.4f" % (stale_EB, stale_SA, stale_EB / max(1, stale_SA)))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "freshness.json").write_text(
        json.dumps({"histories": n_hist, "accesses": n_acc,
                    "fresh_frac": n_fresh / n_acc, "genesis_frac": n_gen / n_acc,
                    "gen_viol": gen_viol, "stale_EB": stale_EB,
                    "stale_SA": stale_SA,
                    "stale_ratio": stale_EB / max(1, stale_SA)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
