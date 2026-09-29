"""WP-6 STEP ML-00: mass-law screen for pure-function candidates.

For each candidate mass M(A,B) (pure state function), measure over hostile
histories, per single StepEv (A-side vs B-side):
  max increase on A-events  (want <= 6 for creation law)
  max increase on B-events  (want <= 0 for conservation)
and per KEEP: drop = M_before - M_after vs need (want drop >= need).
A candidate surviving all three becomes a Stage-4 case-analysis target.
Any failure is recorded with its mechanism (no fitting: functions fixed here).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_quotient import to_ptr, intervals, depths
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def mass(name, dA, dB, iA, iB):
    ks = dA.keys()
    if name == "M1":
        return sum(max(0, (iB[k][1] - iB[k][0] + 1) - 2 * (iA[k][1] - iA[k][0] + 1))
                   for k in ks)
    if name == "M2":
        return sum(max(0, dB[k] - 2 * dA[k]) for k in ks)
    if name == "M3":
        return max([0] + [dB[k] - 2 * dA[k] for k in ks])
    if name == "M5":
        return sum(max(0, (iB[k][1] - iB[k][0] + 1) - (iA[k][1] - iA[k][0] + 1))
                   for k in ks)
    raise ValueError(name)


NAMES = ["M1", "M2", "M3", "M5"]


def snap(A, B):
    return (intervals(A), intervals(B), depths(A), depths(B))


def Mof(name, s):
    iA, iB, dA, dB = s
    return mass(name, dA, dB, iA, iB)


def main() -> int:
    # WP-6 STEP ML-00: mass-law screen.
    step("ML-00", "Screening pure-function mass candidates")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ml|%s|%d" % (self.s, self.c)).digest()

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

    # per-event granularity: replicate splay_trace loop to attribute deltas
    worstA = {nm: (-10 ** 18, None) for nm in NAMES}
    worstB = {nm: (-10 ** 18, None) for nm in NAMES}
    worstK = {nm: (-10 ** 18, None) for nm in NAMES}
    for t in range(250):
        rng = DRBG(("ml%d" % t).encode())
        n = 32
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 10)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ML-KILL", "present kill t=%d" % t)
            return 2
        kps = iter(res["keeps"])
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            # A-side events one by one (mirror splay_trace loop manually)
            d, path = PE._depth_to(A, xx)
            if path and path[-1]["k"] == xx:
                node = path[-1]
                while node["p"] is not None:
                    p = node["p"]
                    g = p["p"]
                    s0 = snap(A, B)
                    if g is None:
                        if p["l"] is node:
                            PE._rot_right(p)
                        else:
                            PE._rot_left(p)
                    elif p["l"] is node and g["l"] is p:
                        PE._rot_right(g)
                        PE._rot_right(p)
                    elif p["r"] is node and g["r"] is p:
                        PE._rot_left(g)
                        PE._rot_left(p)
                    elif p["r"] is node and g["l"] is p:
                        PE._rot_left(p)
                        PE._rot_right(g)
                    else:
                        PE._rot_right(p)
                        PE._rot_left(g)
                    s1 = snap(A, B)
                    for nm in NAMES:
                        dd = Mof(nm, s1) - Mof(nm, s0)
                        if dd > worstA[nm][0]:
                            worstA[nm] = (dd, (t, mode, xx))
            else:
                # absent cannot occur (present route); guard anyway
                pass
            if mode == "KEEP":
                kp = next(kps)
                # B-side events one by one; KEEP drop measured over full access
                sB0 = snap(A, B)
                d, path = PE._depth_to(B, xx)
                node = path[-1]
                while node["p"] is not None:
                    p = node["p"]
                    g = p["p"]
                    s0 = snap(A, B)
                    if g is None:
                        if p["l"] is node:
                            PE._rot_right(p)
                        else:
                            PE._rot_left(p)
                    elif p["l"] is node and g["l"] is p:
                        PE._rot_right(g)
                        PE._rot_right(p)
                    elif p["r"] is node and g["r"] is p:
                        PE._rot_left(g)
                        PE._rot_left(p)
                    elif p["r"] is node and g["l"] is p:
                        PE._rot_left(p)
                        PE._rot_right(g)
                    else:
                        PE._rot_right(p)
                        PE._rot_left(g)
                    s1 = snap(A, B)
                    for nm in NAMES:
                        dd = Mof(nm, s1) - Mof(nm, s0)
                        if dd > worstB[nm][0]:
                            worstB[nm] = (dd, (t, xx))
                sB1 = snap(A, B)
                for nm in NAMES:
                    drop = Mof(nm, sB0) - Mof(nm, sB1)
                    gap = kp["need"] - drop
                    if gap > worstK[nm][0]:
                        worstK[nm] = (gap, (t, xx, kp["need"]))
    step("ML-01", "worst A-increase: %s" % {k: v[0] for k, v in worstA.items()})
    step("ML-01", "worst B-increase: %s" % {k: v[0] for k, v in worstB.items()})
    step("ML-01", "worst KEEP need-drop gap: %s" % {k: v[0] for k, v in worstK.items()})
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "mass_screen.json").write_text(
        json.dumps({"A_increase": {k: v[0] for k, v in worstA.items()},
                    "B_increase": {k: v[0] for k, v in worstB.items()},
                    "KEEP_gap": {k: v[0] for k, v in worstK.items()},
                    "A_ex": {k: v[1] for k, v in worstA.items()},
                    "B_ex": {k: v[1] for k, v in worstB.items()},
                    "K_ex": {k: v[1] for k, v in worstK.items()}},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
