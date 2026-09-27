"""WP-1 STEP 16a: independent splay core (tuple trees, recursive frames)."""
from __future__ import annotations

C = 2
K = 6
LAT, ACT, SP = "LATENT", "ACTIVE", "SPENT"
LEAF = ("leaf",)


def node(k, l, r):
    return ("node", k, l, r)


def vine(n):
    t = LEAF
    for k in range(n, 0, -1):
        t = node(k, LEAF, t)
    return t


def vine_left(n):
    """Mirror image left vine (mirror-variant corpus)."""
    # WP-1 STEP 24: mirror builder; BST-valid by construction.
    t = LEAF
    for k in range(1, n + 1):
        t = node(k, t, LEAF)
    return t


def balanced(keys):
    """BST over an arbitrary key subset (sparse-T0 corpus)."""
    # WP-1 STEP 26: median-recursive balanced builder; valid by construction.
    if not keys:
        return LEAF
    ks = sorted(keys)
    m = len(ks) // 2
    return node(ks[m], balanced(ks[:m]), balanced(ks[m + 1:]))


def inorder(t):
    if t[0] == "leaf":
        return []
    _, k, l, r = t
    return inorder(l) + [k] + inorder(r)


def is_valid(t):
    ks = inorder(t)
    return all(a < b for a, b in zip(ks, ks[1:]))


def lookup(t, x):
    """(found, depth): depth counts edges to x, or to the leaf where search ends."""
    d, cur = 0, t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return True, d
        cur = l if x < k else r
        d += 1
    return False, d


def cost(t, x):
    # WP-1 STEP 17: depth+1 cost total on absent keys.
    return lookup(t, x)[1] + 1


def _descend(t, x, frames):
    if t[0] == "leaf":
        return None
    _, k, l, r = t
    if x == k:
        return (t, frames)
    if x < k:
        return _descend(l, x, frames + [("L", k, r)])
    return _descend(r, x, frames + [("R", k, l)])


def _plug(frames, t):
    for tag, k, sib in reversed(frames):
        t = node(k, t, sib) if tag == "L" else node(k, sib, t)
    return t


def _rebuild(frames, sub):
    """Apply splay rotations bottom-up; frames outermost-first. Returns (tree, events)."""
    evs = []
    fr = list(frames)
    cur = sub
    while fr:
        if len(fr) >= 2 and fr[-1][0] == fr[-2][0] == "L":
            (_, kp, q), (_, kg, c) = fr[-1], fr[-2]
            x = cur[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            if cur[0] == "leaf":
                return _plug(fr, cur), evs
            _, _, t1, t2 = cur
            cur = node(x, t1, node(kp, t2, node(kg, q, c)))
            fr = fr[:-2]
            evs.append(("LL", lo, hi, "-"))
        elif len(fr) >= 2 and fr[-1][0] == fr[-2][0] == "R":
            (_, kp, q), (_, kg, c) = fr[-1], fr[-2]
            x = cur[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            if cur[0] == "leaf":
                return _plug(fr, cur), evs
            _, _, t1, t2 = cur
            cur = node(x, node(kp, node(kg, c, q), t1), t2)
            fr = fr[:-2]
            evs.append(("RR", lo, hi, "-"))
        elif len(fr) >= 2 and fr[-1][0] == "R" and fr[-2][0] == "L":
            (_, kp, q), (_, kg, d) = fr[-1], fr[-2]
            x = cur[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            if cur[0] == "leaf":
                return _plug(fr, cur), evs
            _, _, t1, t2 = cur
            cur = node(x, node(kp, q, t1), node(kg, t2, d))
            fr = fr[:-2]
            evs.append(("LR", lo, hi, "-"))
        elif len(fr) >= 2 and fr[-1][0] == "L" and fr[-2][0] == "R":
            (_, kp, q), (_, kg, a) = fr[-1], fr[-2]
            x = cur[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            if cur[0] == "leaf":
                return _plug(fr, cur), evs
            _, _, t1, t2 = cur
            cur = node(x, node(kg, a, t1), node(kp, t2, q))
            fr = fr[:-2]
            evs.append(("RL", lo, hi, "-"))
        else:
            tag, kp, q = fr[-1]
            if cur[0] == "leaf":
                return _plug(fr, cur), evs
            x = cur[1]
            _, _, t1, t2 = cur
            if tag == "L":
                cur = node(x, t1, node(kp, t2, q))
                o = "L"
            else:
                cur = node(x, node(kp, q, t1), t2)
                o = "R"
            fr = fr[:-1]
            evs.append(("ZIG", min(x, kp), max(x, kp), o))
    return _plug(fr, cur), evs


def trace(t, x):
    """WP-1 STEP 18: absent key -> unchanged tree, empty event list."""
    hit = _descend(t, x, [])
    if hit is None:
        return t, []
    sub, frames = hit
    return _rebuild(frames, sub)


def serial(t):
    if t[0] == "leaf":
        return "."
    _, k, l, r = t
    return "(%d%s%s)" % (k, serial(l), serial(r))


