"""WP-6 STEP HT-00: hub/top vs deep/pump tier split (two-tier diversity check).

For each B-StepEv: TOP iff accessed-key B-depth pre-splay <= 4 (triple near
root zone); else DEEP. Measure top/deep B counts + same-access E1 cover
(e_A of own access) for top + pump-ancestry presence for deep.
Tests the two-tier hypothesis: top-B funded by fresh same-access/own slots,
deep-B funded by pump-ancestry (distinct backing events).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP HT-00.
    step("HT-00", "Hub/top vs deep/pump tier split")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ht|%s|%d" % (self.s, self.c)).digest()

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

    top_ct = deep_ct = 0
    top_e1cov = 0
    deep_pump = 0
    for t in range(60):
        rng = DRBG(("ht%d" % t).encode())
        n = rng.ch([32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(6, 16)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-16, -8, 8, 16])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("HT-KILL", "present kill t=%d" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        pumped = set()
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            if mode == "KEEP":
                d, _ = PE._depth_to(B, xx)
                eA = sum(1 for z in acc["sites"] if z)
                if d <= 4:
                    top_ct += len(acc["Bev"])
                    top_e1cov += min(len(acc["Bev"]), 3 * eA)
                else:
                    deep_ct += len(acc["Bev"])
                    if xx in pumped:
                        deep_pump += len(acc["Bev"])
                B, pushes = splay_B_push(B, xx)
                for P in pushes:
                    pumped |= P
            A, _ = splay_A(A, xx)
    step("HT-01", "top-B=%d (E1-covered %d) deep-B=%d (pump-touched %d)" %
         (top_ct, top_e1cov, deep_ct, deep_pump))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "tiers.json").write_text(
        json.dumps({"top": top_ct, "top_e1cov": top_e1cov, "deep": deep_ct,
                    "deep_pump": deep_pump}, indent=1, sort_keys=True,
                   default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
