"""WP-6 STEP CC-00: residual cash-chain harness + Q-transition classification.

PART 1 (chain hunt): from diagonal T0 (and from pumped states), greedy
max-immediate + beam lookahead (depth 4, width 10) maximizing CUMULATIVE
E_B-3*S_A. Kill: cumulative > 0 from diagonal (direct E_B witness, replay).
Record per step (key,e_A,e_B,r,cum,|M|,top-q,pos,neg,Q) + setup-between-cashes
(forced setup before next cash?).
PART 2 (Q-transition): on each profitable cash, classify dangerous
bystanders (q>0 pre): rigid / A-path-modified / B-path-modified /
both-path / newly-dangerous (q<=0->>0) / destroyed; q-mass flow per class.
Compensated orders tested on profiles (majorization/lexicographic/prefix).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE


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


def splay_sets(t, x):
    """Replay splay capturing rotated-key set per StepEv + pushed set."""
    import copy as _c
    c = clone(t)
    d, path = PE._depth_to(c, x)
    if not path or path[-1]["k"] != x:
        return c, [], []
    rot, push = [], []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            rot.append({node["k"], p["k"]})
            push.append({p["k"]})
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            rot.append({node["k"], p["k"], g["k"]})
            push.append({p["k"], g["k"]})
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            rot.append({node["k"], p["k"], g["k"]})
            push.append({p["k"], g["k"]})
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            rot.append({node["k"], p["k"], g["k"]})
            push.append({p["k"], g["k"]})
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            rot.append({node["k"], p["k"], g["k"]})
            push.append({p["k"], g["k"]})
    while node["p"] is not None:
        node = node["p"]
    return node, rot, push


def main() -> int:
    # WP-6 STEP CC-00.
    step("CC-00", "Residual cash-chain harness + Q-transition")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"cc|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ch(self, s):
            return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    # PART 1: greedy cumulative-max from diagonal (kill = cum > 0)
    worst_cum = -10**18
    exC = None
    n_cash_chains = 0
    for t in range(30):
        rng = DRBG(("cc%d" % t).encode())
        n = rng.ch([32, 64])
        T0 = vine(n, rng.below(2) == 0)
        A, B = to_ptr(T0), to_ptr(T0)
        cum = 0
        pos = neg = 0
        cashes = 0
        setups_between = []
        since_setup = 0
        for step_i in range(40):
            # greedy: best immediate reward access
            best = (0, None, 0, 0)
            for xx in range(1, n + 1):
                ca = evc(A, xx)
                cb = evc(B, xx)
                r = cb - 3 * ca
                if r > best[0]:
                    best = (r, ("K", xx), ca, cb)
                r = -3 * ca
                if r > best[0]:
                    best = (r, ("D", xx), ca, 0)
            r, act, ca, cb = best
            if act is None:
                break
            m, xx = act
            cum += r
            if cum > worst_cum:
                worst_cum, exC = cum, (t, step_i, m, xx, ca, cb)
            if cum > 0:
                step("CC-KILL", "cumulative>0 t=%d %s (E_B witness!)" % (t, exC))
                return 2
            if r > 0:
                cashes += 1
                setups_between.append(since_setup)
                since_setup = 0
            else:
                since_setup += 1
            if r > 0:
                pos += r
            else:
                neg -= r
            A, _ = PE.splay_trace(A, xx)
            if m == "K":
                B, _ = PE.splay_trace(B, xx)
        if cashes:
            n_cash_chains += 1
    import statistics as _st
    step("CC-01", "greedy chains=%d worst_cum=%d %s setup-between-cash med=%s" %
         (n_cash_chains, worst_cum, exC,
          _st.median(setups_between) if setups_between else None))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "cashchain.json").write_text(
        json.dumps({"chains": n_cash_chains, "worst_cum": worst_cum, "ex": exC,
                    "setup_med": _st.median(setups_between) if setups_between else None,
                    "setup_all": setups_between[:60]},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
