"""WP-4 STEP 111: weaker-domain LegalPairInstance gate (spec #2, CC-004/005).

keys(T0) subset of [n]; valid BST; modes KEEP/DELETE; access keys in [n]
(presence NOT required); A/B start equal T0 (checked by caller construction).
"""
from __future__ import annotations


def keys_of(t) -> list:
    if t is None:
        return []
    k, l, r = t
    return keys_of(l) + [k] + keys_of(r)


def valid_bst(t, lo=0, hi=10 ** 9) -> bool:
    if t is None:
        return True
    k, l, r = t
    return lo < k < hi and valid_bst(l, lo, k) and valid_bst(r, k, hi)


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
