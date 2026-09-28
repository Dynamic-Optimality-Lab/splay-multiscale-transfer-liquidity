"""FIXED_KEY_PAIR_ACCESS_CLOSURE tests (new-route domain law).

Proves from the frozen rotation code + hostile present-only histories that:
1. every rotation preserves the key set (unit);
2. keys(A_i) = keys(B_i) = K along any present-only Pair Access run;
3. every requested key is present in both trees at its occurrence;
4. occurrence mask (index-based) differs from value-set mask under duplicates.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE

PRESENT_SET = frozenset(range(1, 33))


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


def keys_of(p):
    if p is None:
        return set()
    r = p
    while r["p"] is not None:
        r = r["p"]
    out = set()

    def rec(u):
        if u is None:
            return
        out.add(u["k"])
        rec(u["l"])
        rec(u["r"])

    rec(r)
    return out


def vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


def test_closure_single_rotation_preserves_keys():
    import random
    rnd = random.Random(7)
    for _ in range(300):
        n = rnd.randint(2, 12)
        T0 = vine(n)
        A = to_ptr(T0)
        x = rnd.randint(1, n)
        before = keys_of(A)
        A, evs = PE.splay_trace(A, x)
        assert keys_of(A) == before == set(range(1, n + 1))
        assert len(evs) > 0 or x == 1


def test_closure_pair_access_run():
    import random
    for t in range(200):
        rnd = random.Random(t)
        n = rnd.randint(2, 16)
        T0 = vine(n)
        K = set(range(1, n + 1))
        A, B = to_ptr(T0), to_ptr(T0)
        for _ in range(rnd.randint(1, 12)):
            x = rnd.randint(1, n)
            assert x in keys_of(A) and x in keys_of(B)
            A, _ = PE.splay_trace(A, x)
            if rnd.below(2) if hasattr(rnd, "below") else rnd.randint(0, 1):
                B, _ = PE.splay_trace(B, x)
            assert keys_of(A) == K and keys_of(B) == K


def test_closure_occurrence_mask_not_value_set():
    X = [5, 5, 5]
    A_mask = [True, False, True]  # keep occurrences 0 and 2
    Y_by_occurrence = [x for x, keep in zip(X, A_mask) if keep]
    Y_by_valueset = [x for x in X if x in set(Y_by_occurrence)]
    assert Y_by_occurrence == [5, 5]  # two retained occurrence copies
    assert Y_by_valueset == [5, 5, 5]  # value-set test wrongly restores all three
    assert Y_by_occurrence != Y_by_valueset
    assert len(Y_by_occurrence) == sum(A_mask)
