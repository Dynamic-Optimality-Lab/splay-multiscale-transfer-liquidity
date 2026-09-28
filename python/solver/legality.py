"""WP-4 STEP 111: weaker-domain LegalPairInstance gate (spec #2, CC-004/005).

keys(T0) subset of [n]; valid BST; modes KEEP/DELETE; access keys in [n]
(presence NOT required); A/B start equal T0 (checked by caller construction).
"""
from __future__ import annotations


def keys_of(t) -> list:
    # WP-5 robustness: iterative traversal (recursion depth unsafe at large n).
    out, stack = [], [t]
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        out.append(cur[0])
        stack.append(cur[1])
        stack.append(cur[2])
    return out


def valid_bst(t, lo=0, hi=10 ** 9) -> bool:
    # WP-5 robustness: iterative bounds check (recursion depth unsafe at large n).
    stack = [(t, lo, hi)]
    while stack:
        cur, lo, hi = stack.pop()
        if cur is None:
            continue
        k, l, r = cur
        if not (lo < k < hi):
            return False
        stack.append((l, lo, k))
        stack.append((r, k, hi))
    return True


def check(n: int, T0, H) -> None:
    """WP-4 STEP 111: raises ValueError on any legality violation."""
    if not isinstance(n, int) or n < 1:
        raise ValueError("illegal n: %r" % (n,))
    if not valid_bst(T0):
        raise ValueError("T0 not a valid BST")
    if any(not (1 <= k <= n) for k in keys_of(T0)):
        raise ValueError("keys(T0) not subset of [n]")
    for step in H:
        m, x = step
        if m not in ("KEEP", "DELETE"):
            raise ValueError("illegal mode: %r" % (m,))
        if not (1 <= x <= n):
            raise ValueError("access key outside [n]: %r" % (x,))


def episode_id(n: int, T0, H) -> str:
    """WP-4 STEP 111: canonical episode ID (sorted JSON hash; dev/validation registries)."""
    import hashlib
    import json
    return hashlib.sha256(json.dumps({"n": n, "T0": T0, "H": H},
                                     sort_keys=True).encode()).hexdigest()
