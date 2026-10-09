"""PIVOT-22 exact n=7 max-mean W_Q cycle via Howard policy iteration.

Prover: Howard (max mean-weight cycle + bias). Verifier: independent exact
integer check of dual inequalities + cleanroom replay of witness cycle.
Prover bugs cannot fake YES (verifier is exact + independent).
"""
from __future__ import annotations
import sys
import copy
import json
import pickle
import random
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[HOW %s] %s" % (sid, msg), flush=True)


def load(n):
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                         "0909c74a" / ("trans%d.pkl" % n)), "rb"))
    nS, Atrans, Btrans, Sh = D["nS"], D["Atrans"], D["Btrans"], D["Sh"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    dA, dB = {}, {}
    for ia in range(nS):
        dd = V.depths_of(ptrs[ia])
        for x in range(1, n + 1):
            dA[(ia, x)] = dd.get(x, 0)
            dB[(ia, x)] = dd.get(x, 0)
    return n, nS, Sh, Atrans, Btrans, dA, dB


def nbr(n, nS, Atrans, Btrans, dA, dB, u, k):
    """Edge k (0..2n-1: D1..Dn,K1..Kn) from u -> (to, w=q-2a)."""
    ia, ib = u // nS, u % nS
    if k < n:
        x = k + 1
        ia2, a = Atrans[(ia, x)]
        return ia2 * nS + ib, -2 * a
    x = k - n + 1
    ia2, a = Atrans[(ia, x)]
    ib2, _ = Btrans[(ib, x)]
    return ia2 * nS + ib2, dB[(ib, x)] // 2 - 2 * a


def find_cycles(n, nS, Atrans, Btrans, dA, dB, Vcount, pi):
    """All directed cycles of functional graph pi. O(V). Returns list."""
    state = [0] * Vcount
    cycles = []  # list of lists of (u, to, w)
    for s in range(Vcount):
        if state[s] == 2:
            continue
        pos = {}
        trail = []
        u = s
        while True:
            if u in pos:
                cyc = []
                v = u
                while True:
                    to, w = nbr(n, nS, Atrans, Btrans, dA, dB, v, pi[v])
                    cyc.append((v, to, w))
                    v = to
                    if v == u:
                        break
                cycles.append(cyc)
                break
            if state[u] == 2:
                break
            pos[u] = len(trail)
            trail.append(u)
            u, _ = nbr(n, nS, Atrans, Btrans, dA, dB, u, pi[u])
        for v in trail:
            state[v] = 2
    return cycles


def howard(n, nS, Atrans, Btrans, dA, dB, Vcount, maxit=300, seed=0):
    rng = random.Random(seed)
    N = 2 * n
    # init policy: greedy max immediate weight (deterministic-ish)
    pi = [0] * Vcount
    for u in range(Vcount):
        best, bk = None, 0
        for k in range(N):
            _, w = nbr(n, nS, Atrans, Btrans, dA, dB, u, k)
            if best is None or w > best:
                best, bk = w, k
        pi[u] = bk
    mu_num, mu_den = None, None
    h = [None] * Vcount
    for it in range(maxit):
        # --- evaluate: cycles + global max mean (exact cross-mult)
        cycles = find_cycles(n, nS, Atrans, Btrans, dA, dB, Vcount, pi)
        mu_num, mu_den = None, None
        for cyc in cycles:
            tot = sum(w for _, _, w in cyc)
            L = len(cyc)
            if mu_num is None or tot * mu_den > mu_num * L:
                mu_num, mu_den = tot, L
        # --- values: backward from max-mean cycles
        h = [None] * Vcount
        rev = [[] for _ in range(Vcount)]
        for u in range(Vcount):
            to, _ = nbr(n, nS, Atrans, Btrans, dA, dB, u, pi[u])
            rev[to].append(u)
        from collections import deque
        dq = deque()
        for cyc in cycles:
            tot = sum(w for _, _, w in cyc)
            L = len(cyc)
            if tot * mu_den == mu_num * L:
                rep = min(v for v, _, _ in cyc)
                if h[rep] is None:
                    h[rep] = Fraction(0)
                    dq.append(rep)
        while dq:
            v = dq.popleft()
            for u in rev[v]:
                if h[u] is None:
                    to, w = nbr(n, nS, Atrans, Btrans, dA, dB, u, pi[u])
                    assert to == v
                    h[u] = Fraction(w) - Fraction(mu_num, mu_den) + h[v]
                    dq.append(u)
        # --- improve
        switches = 0
        for u in range(Vcount):
            cur = None if h[u] is None else Fraction(mu_num, mu_den) + h[u]
            best, bk = cur, pi[u]
            for k in range(N):
                to, w = nbr(n, nS, Atrans, Btrans, dA, dB, u, k)
                if h[to] is None:
                    continue
                val = Fraction(w) + h[to]
                if best is None or val > best:
                    best, bk = val, k
            if bk != pi[u]:
                pi[u] = bk
                switches += 1
        step("IT-%d" % it, "mu=%s/%s switches=%d" % (mu_num, mu_den, switches))
        if switches == 0:
            break
    return (mu_num, mu_den), pi, h


def main():
    n = 7
    n, nS, Sh, Atrans, Btrans, dA, dB = load(n)
    Vcount = nS * nS
    step("H-0", "V=%d E=%d" % (Vcount, Vcount * 2 * n))
    (mu_num, mu_den), pi, h = howard(n, nS, Atrans, Btrans, dA, dB, Vcount)
    step("H-1", "max-mean mu=%s/%s = %.6f" % (mu_num, mu_den, mu_num / mu_den))
    out = {"mu_num": mu_num, "mu_den": mu_den}
    import json as J
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "howard7.json").write_text(J.dumps(out, indent=1), encoding="utf-8")
    # save policy + bias for verifier/witness extraction
    pickle.dump({"pi": pi,
                 "h": [(x.numerator, x.denominator) if x is not None else None
                       for x in h],
                 "mu": (mu_num, mu_den)},
                open(ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "howard7.pkl", "wb"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
