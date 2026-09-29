"""WP-6 STEP OC-00: per-key B-triple occupancy contiguity probe.

For each KEEP access (splay of x, B-events b_1..b_m with triples T_i):
  for each non-x key z: occupancy = [i : z in T_i]; assert CONTIGUOUS (no gaps).
  Record max occupancy run per key; violations with full context (step kinds?).
Rationale: node (=x) rises monotonically (1-2 levels/StepEv, never down), so a
fixed ancestor z is p/g over a contiguous step-block. Contiguity lifts ML-W-BLOCKS
(sketch) to PROVED (each S-key <=1 block; |S|<=3 blocks per member-splay).
Uses exact replayed triples (pushes[k] | {x} as builders) + step kinds.
NEW artifact: occupancy.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class Rng:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag

    def __call__(self, c):
        return int.from_bytes(_h.sha256(self.tag + b"|%s|%d" % (self.s, c)).digest(), "big")


def gen(t, tag):
    rng = Rng(("s%d" % t).encode(), tag)
    r = rng(0)
    n = [16, 32, 64][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 10 + (r >> 16) % 20
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = Rng(("s%d" % t).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-16, -8, 8, 16][q % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if q % 3 else "DELETE", x])
        x = min(n, max(1, x + [-8, -4, -1, 1, 4, 8][(q >> 9) % 6]))
    return n, T0, H


def main() -> int:
    step("OC-00", "Per-key occupancy contiguity probe")
    import json
    from collections import Counter
    nkeys = 0
    viol = 0
    violex = []
    run_hist = Counter()
    maxrun = 0
    nsplay = 0
    for t in range(200):
        tag = b"oc" if t % 2 == 0 else b"oc2"
        n, T0, H = gen(t, tag)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("OC-KILL", "present kill t=%d" % t)
            return 2
        B = to_ptr(T0)
        A = to_ptr(T0)
        for idx, acc in enumerate(pre):
            mode, xx = acc["mode"], acc["x"]
            A, _ = splay_A(A, xx)
            if mode != "KEEP":
                continue
            B, pushes = splay_B_push(B, xx)
            nb = len(acc["Bev"])
            if nb == 0:
                continue
            nsplay += 1
            tris = []
            for k in range(nb):
                P = pushes[k] if k < len(pushes) else set()
                tris.append(set(P) | {xx})
            # per non-x key occupancy
            keys = set()
            for T in tris:
                keys |= T
            keys.discard(xx)
            for z in keys:
                occ = [i for i, T in enumerate(tris) if z in T]
                nkeys += 1
                run = 1
                best = 1
                gaps = 0
                for a, b in zip(occ, occ[1:]):
                    if b == a + 1:
                        run += 1
                        best = max(best, run)
                    else:
                        gaps += 1
                        run = 1
                run_hist[best] += 1
                maxrun = max(maxrun, best)
                if gaps:
                    viol += 1
                    if len(violex) < 8:
                        violex.append({"t": t, "acc": idx, "x": xx, "z": z,
                                       "occ": occ, "m": nb})
    step("OC-01", "splays=%d keys=%d viol=%d maxrun=%d runhist=%s" % (
        nsplay, nkeys, viol, maxrun, dict(run_hist)))
    for v in violex:
        step("OC-EX", "%s" % v)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "occupancy.json").write_text(
        json.dumps({"splays": nsplay, "keys": nkeys, "viol": viol,
                    "maxrun": maxrun, "run_hist": dict(run_hist),
                    "viol_ex": violex}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
