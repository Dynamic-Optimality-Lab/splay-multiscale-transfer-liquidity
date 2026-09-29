"""WP-6 STEP ST-00: sterilization probe (CASE S vs R, single-reward + anatomy).

For each B-heavy KEEP (q=e_B-3*e_A>0) on hostile multi-divergent histories:
post-cash state (A',B'): max SINGLE immediate reward over all next accesses
(V_after>0 if any r>0). If >0: CASE R (residual mode!); anatomy of residual
keys (max-r key: genesis-depth (never pumped since last reset?) vs pumped?
A-shallow? B-deep? which?). If all <=0: consistent with S (multi-step open).
Also: pumped/residual split (genesis-E4-exclusive vs pumped-marginal?).
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


def clone(t):
    r = t
    while r["p"] is not None:
        r = r["p"]

    def rec(u, p):
        if u is None:
            return None
        nd = PE.mknode(u["k"])
        nd["p"] = p
        nd["l"] = rec(u["l"], nd)
        nd["r"] = rec(u["r"], nd)
        return nd

    return rec(r, None)


def evc(t, x):
    _, evs = PE.splay_trace(clone(t), x)
    return len(evs)


def main() -> int:
    # WP-6 STEP ST-00.
    step("ST-00", "Sterilization probe (post-cash single reward + anatomy)")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"st|%s|%d" % (self.s, self.c)).digest()

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

    nR = 0
    worst_resid = -10**18
    exR = None
    gen_count = pump_count = 0
    n_hist = 0
    for t in range(150):
        rng = DRBG(("st%d" % t).encode())
        n = rng.ch([32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ST-KILL", "present kill t=%d" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        # track pumps per key since last reset (for genesis flag)
        pumped = set()
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            if mode == "KEEP":
                eA = sum(1 for z in acc["sites"] if z)
                eB = len(acc["Bev"])
                if eB - 3 * eA > 0:
                    A, _ = PE.splay_trace(A, xx)
                    B, _ = PE.splay_trace(B, xx)
                    # post-cash: max single immediate reward + residual key
                    br = -10**18
                    bk = None
                    bea = beb = 0
                    for y in range(1, n + 1):
                        ca = evc(A, y)
                        cb = evc(B, y)
                        r = cb - 3 * ca
                        if r > br:
                            br, bk, bea, beb = r, y, ca, cb
                    if br > 0:
                        nR += 1
                        if br > worst_resid:
                            worst_resid, exR = br, (t, xx, eA, eB, bk, bea, beb)
                        if bk in pumped:
                            pump_count += 1
                        else:
                            gen_count += 1
                    pumped = set()  # cash resets x, but others persist; reset per-key below
                else:
                    A, _ = PE.splay_trace(A, xx)
                    B, _ = PE.splay_trace(B, xx)
            else:
                A, _ = PE.splay_trace(A, xx)
            # update pumped: keys B-pushed since their last KEEP (approx: all
            # B-rotated non-reset keys this access -- simplified: track via
            # B-depth increases is costly; APPROX: pumped |= keys on B-path
            # that are not xx. Skip precise; use empty (genesis-biased).
            # NOTE: simplification biases gen_count up; residual existence
            # (br>0) is exact regardless.
        n_hist += 1
    step("ST-01", "hist=%d post-cash single-positive=%d worst_resid=%s %s" %
         (n_hist, nR, worst_resid, exR))
    step("ST-01", "residual pumped=%d genesis-or-unknown=%d (pump tracking approx)" %
         (pump_count, gen_count))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "sterile.json").write_text(
        json.dumps({"histories": n_hist, "caseR": nR, "worst": worst_resid,
                    "ex": exR, "pump": pump_count, "gen": gen_count},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
