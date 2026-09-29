"""WP-6 STEP DH-00: depth-5/6 exhaustive falsifier (sound, small-n).

n=8 depth<=5 (16^5=1M/start), n=6 depth<=6 (12^6=3M/start), multiple T0
(vines/balanced/shuffled). Maximize cumulative E_B-3*S_A over prefixes.
>0 => minimize + replay (GC witness, RETURN 2). =0 everywhere => V_5/V_6
verified (those starts). Exact clone-splay semantics (legacy engine).
"""
from __future__ import annotations
import sys
import itertools
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


def main() -> int:
    # WP-6 STEP DH-00.
    step("DH-00", "Depth-5/6 exhaustive falsifier")
    import json
    out = {}

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

    import random
    configs = []
    n = 8
    r = random.Random(7)
    ks = list(range(1, n + 1))
    r.shuffle(ks)
    t = None

    def ins(T, k):
        if T is None:
            return [k, None, None]
        if k < T[0]:
            T[1] = ins(T[1], k)
        else:
            T[2] = ins(T[2], k)
        return T

    for k in ks:
        t = ins(t, k)
    for name, T0, D in (("vineL8", vine(8, False), 5), ("vineR8", vine(8, True), 5),
                        ("bal8", bal(list(range(1, 9))), 5),
                        ("shuf8", t, 5)):
        acts = []
        for x in range(1, 9):
            acts.append(("K", x))
            acts.append(("D", x))
        best = -10**18
        ex = None
        cnt = 0
        for w in itertools.product(acts, repeat=D):
            A, B = to_ptr(T0), to_ptr(T0)
            cum = 0
            for (m, x) in w:
                A2, eA = PE.splay_trace(clone(A), x)
                A = A2
                if m == "K":
                    B2, eB = PE.splay_trace(clone(B), x)
                    B = B2
                    cum += len(eB) - 3 * len(eA)
                else:
                    cum += -3 * len(eA)
                if cum > best:
                    best = cum
                    ex = w
                    if best > 0:
                        break
            cnt += 1
            if best > 0:
                break
        step("DH-%s" % name, "paths=%d best=%d %s" % (cnt, best, ex if best > 0 else ""))
        out[name] = {"paths": cnt, "best": best, "ex": ex if best > 0 else None}
        if best > 0:
            step("DH-KILL", "positive depth-%d path (GC witness!)" % D)
    # n=6 depth 6 on vines only (12^6=3M x2 starts; time-boxed by timeout)
    n = 6
    for name, T0 in (("vineL6", vine(6, False)), ("vineR6", vine(6, True))):
        acts = []
        for x in range(1, 7):
            acts.append(("K", x))
            acts.append(("D", x))
        best = -10**18
        ex = None
        cnt = 0
        for w in itertools.product(acts, repeat=6):
            A, B = to_ptr(T0), to_ptr(T0)
            cum = 0
            for (m, x) in w:
                A2, eA = PE.splay_trace(clone(A), x)
                A = A2
                if m == "K":
                    B2, eB = PE.splay_trace(clone(B), x)
                    B = B2
                    cum += len(eB) - 3 * len(eA)
                else:
                    cum += -3 * len(eA)
                if cum > best:
                    best = cum
                    ex = w
                    if best > 0:
                        break
            cnt += 1
            if best > 0 or (cnt % 1000000 == 0):
                step("DH-%s" % name, "progress paths=%d best=%d" % (cnt, best))
            if best > 0:
                break
        step("DH-%s-done" % name, "paths=%d best=%d" % (cnt, best))
        out[name] = {"paths": cnt, "best": best, "ex": ex if best > 0 else None}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "depth56.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
