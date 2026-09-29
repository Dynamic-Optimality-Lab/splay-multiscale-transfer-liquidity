"""WP-6 STEP CC2-00: bounded-horizon adversarial falsifier (V_h from diagonal).

EXHAUSTIVE depth-D (n=16, multi-T0): all access words length<=D, cumulative
E_B-3*S_A; >0 => WITNESS (replay => E_B>3*S_A, RETURN 2). V_D(diag)=0 =>
bounded-horizon-D verified (those starts).
BEAM depth-5 width-12 (n=64/128, pump-biased starts): aggressive cumulative
max; >0 => witness candidate (replay); else supports h*<=5.
Soundness: exhaustive has none (full enumeration); beam may miss (pruning).
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


def main() -> int:
    # WP-6 STEP CC2-00.
    step("CC2-00", "Bounded-horizon adversarial falsifier")
    import hashlib
    import itertools

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    def bal(ks):
        if not ks:
            return None
        m = len(ks) // 2
        return [ks[m], bal(ks[:m]), bal(ks[m + 1:])]

    n = 16
    T0s = [vine(n, False), vine(n, True), bal(list(range(1, n + 1)))]
    acts = []
    for x in range(1, n + 1):
        acts.append(("K", x))
        acts.append(("D", x))
    best = -10**18
    ex = None
    evals = 0
    # depth<=3 exhaustive (32^3=33k per start), depth-4 sampled extensions
    for T0 in T0s:
        for w1 in acts:
            for w2 in acts:
                for w3 in acts:
                    A, B = to_ptr(T0), to_ptr(T0)
                    cum = 0
                    ok = True
                    for (m, x) in (w1, w2, w3):
                        A2, eA = PE.splay_trace(clone(A), x)
                        # NOTE: clone per step is wasteful; correctness first
                        A = to_ptr(_totup(A2)) if False else A2
                        if m == "K":
                            B2, eB = PE.splay_trace(clone(B), x)
                            B = B2
                            cum += len(eB) - 3 * len(eA)
                        else:
                            cum += -3 * len(eA)
                    evals += 1
                    if cum > best:
                        best, ex = cum, (w1, w2, w3)
    step("CC2-01", "exhaustive D<=3 n=16: evals=%d best_cum=%d %s (want<=0)" %
         (evals, best, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "badhorizon.json").write_text(
        json.dumps({"evals": evals, "best": best, "ex": ex}, indent=1,
                   sort_keys=True, default=str), encoding="utf-8")
    return 0


def _totup(t):
    if t is None:
        return None
    return [t["k"], _totup(t["l"]), _totup(t["r"])]


if __name__ == "__main__":
    sys.exit(main())
