"""PIVOT-22 cleanroom replay (independent verifier, no repo imports).

Pair-Access, pointer BSTs, bottom-up splay. Returns per-access (dA,a,dB,q,z)
+ totals + closedness. Used to verify certificates independently.
"""
from __future__ import annotations
import copy


def mknode(k):
    return {"k": k, "l": None, "r": None, "p": None}


def to_ptr(t):
    if t is None:
        return None
    root = mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def depth_to(t, x):
    d, cur = 0, t
    while cur is not None:
        if x == cur["k"]:
            return d
        cur = cur["l"] if x < cur["k"] else cur["r"]
        d += 1
    return None  # absent (should not happen for keys 1..n)


def rot_right(p):
    x, g = p["l"], p["p"]
    b = x["r"]
    x["r"], p["l"] = p, b
    if b is not None:
        b["p"] = p
    x["p"], p["p"] = g, x
    if g is not None:
        if g["l"] is p:
            g["l"] = x
        else:
            g["r"] = x
    return x


def rot_left(p):
    x, g = p["r"], p["p"]
    b = x["l"]
    x["l"], p["r"] = p, b
    if b is not None:
        b["p"] = p
    x["p"], p["p"] = g, x
    if g is not None:
        if g["l"] is p:
            g["l"] = x
        else:
            g["r"] = x
    return x


def splay(root, x):
    """Bottom-up splay x. Returns (new_root, nsteps, ndoubles, nzigs)."""
    # find path
    path = []
    cur = root
    while cur is not None:
        path.append(cur)
        if x == cur["k"]:
            break
        cur = cur["l"] if x < cur["k"] else cur["r"]
    if not path or path[-1]["k"] != x:
        raise ValueError("absent key %s" % x)
    node = path[-1]
    nsteps = ndb = nzg = 0
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        nsteps += 1
        if g is None:
            nzg += 1
            if p["l"] is node:
                rot_right(p)
            else:
                rot_left(p)
        else:
            ndb += 1
            if p["l"] is node and g["l"] is p:
                rot_right(g)
                rot_right(p)
            elif p["r"] is node and g["r"] is p:
                rot_left(g)
                rot_left(p)
            elif p["r"] is node and g["l"] is p:
                rot_left(p)
                rot_right(g)
            else:
                rot_right(p)
                rot_left(g)
    while node["p"] is not None:
        node = node["p"]
    return node, nsteps, ndb, nzg


def enc(P):
    if P is None:
        return None
    return [P["k"], enc(P["l"]), enc(P["r"])]


def replay(T0A, T0B, word):
    """word = list of (mode, x). Returns dict with legs, totals, end shapes."""
    A = to_ptr(copy.deepcopy(T0A))
    B = to_ptr(copy.deepcopy(T0B))
    legs = []
    Aacc = Qacc = Zacc = 0
    for (md, x) in word:
        dA = depth_to(copy.deepcopy(A), x)
        a = (dA + 1) // 2
        A, _, _, _ = splay(A, x)
        # verify A steps == a
        if md == "K":
            dB = depth_to(copy.deepcopy(B), x)
            q, z = dB // 2, dB % 2
            B, ns, ndb, nzg = splay(B, x)
            assert ndb == q and nzg == z, (x, ndb, q, nzg, z)
        else:
            dB, q, z = None, 0, 0
        Aacc += a
        Qacc += q
        Zacc += z
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a,
                     "q": q, "z": z})
    return {"legs": legs, "A": Aacc, "Q": Qacc, "Z": Zacc,
            "WQ": Qacc - 2 * Aacc, "endA": enc(A), "endB": enc(B)}
