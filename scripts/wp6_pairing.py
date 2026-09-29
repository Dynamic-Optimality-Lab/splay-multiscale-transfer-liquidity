"""WP-6 STEP PR-00: excess decomposition + cash/setup pairing.

Excess X = e_B - 3*e_A per KEEP (DELETEs contribute -3*e_A <= 0 always).
Q1: is all positive excess from CASHES (e_A=0)? (non-cash excess total <= 0?)
Q2: per cash+setup pair: e_B(cash)+e_B(setup) <= 3*e_A(setup)? (setup = last
    root-arrival strictly before cash, via A-root tracking; pairs disjoint.)
If Q1 (noncash-excess<=0) and Q2 (per-pair) both hold: E_B<=3*S_A PROVED
(sum pairs + noncash + DELETEs, all <=0). Falsifiable; minimized witness kept.
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


def root_key(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return r["k"]


def main() -> int:
    # WP-6 STEP PR-00: pairing screen.
    step("PR-00", "Excess decomposition + cash/setup pairing")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"pr|%s|%d" % (self.s, self.c)).digest()

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

    tot_pos_cash = 0
    tot_pos_noncash = 0
    worst_pair = -10**18
    ex_pair = None
    worst_noncash = -10**18
    ex_nc = None
    n_hist = 0
    for t in range(400):
        rng = DRBG(("pr%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 20)
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
            step("PR-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        A = to_ptr(T0)
        # A-root tracking + per-access e_A/e_B + setup per key (last root-arrival)
        setup = {}  # key -> access idx of last root-arrival (non-root-before)
        for idx, acc in enumerate(pre):
            mode, xx = acc["mode"], acc["x"]
            r_before = root_key(A)
            eA = sum(1 for z in acc["sites"] if z)
            nonroot_before = (r_before != xx)
            A, _ = PE.splay_trace(A, xx)
            # after: xx at root (if present; present domain always)
            if nonroot_before:
                setup[xx] = idx
            if mode == "KEEP":
                eB = len(acc["Bev"])
                X = eB - 3 * eA
                if eA == 0 and eB > 0:
                    if X > 0:
                        tot_pos_cash += X
                    # pair with setup
                    s = setup.get(xx, None)
                    if s is None:
                        # genesis-root (xx root since T0, never arrived): pair with nothing;
                        # e_B must be 0 (B-root too? xx B-position: genesis...). Check:
                        pgap = eB  # uncovered!
                        if pgap > worst_pair:
                            worst_pair, ex_pair = pgap, (t, xx, "GENESIS-ROOT", eB)
                    else:
                        seA = sum(1 for z in pre[s]["sites"] if z)
                        seB = len(pre[s]["Bev"]) if pre[s]["mode"] == "KEEP" else 0
                        pgap = eB + seB - 3 * seA
                        if pgap > worst_pair:
                            worst_pair, ex_pair = pgap, (t, xx, s, eB, seB, seA)
                else:
                    if X > worst_noncash:
                        worst_noncash, ex_nc = X, (t, xx, eB, eA)
                    if X > 0:
                        tot_pos_noncash += X
        n_hist += 1
    step("PR-01", "hist=%d total pos-cash-excess=%d total pos-noncash-excess=%d"
         % (n_hist, tot_pos_cash, tot_pos_noncash))
    step("PR-01", "worst pair-gap=%s %s (want<=0)" % (worst_pair, ex_pair))
    step("PR-01", "worst noncash single-gap=%s %s" % (worst_noncash, ex_nc))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pairing.json").write_text(
        json.dumps({"histories": n_hist, "pos_cash": tot_pos_cash,
                    "pos_noncash": tot_pos_noncash, "worst_pair": worst_pair,
                    "pair_ex": ex_pair, "worst_noncash": worst_noncash,
                    "nc_ex": ex_nc}, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
