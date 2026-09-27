"""WP-1 STEP 10: primary legacy engine (pointer-based) implementing T5_{P_all,FLAT(1)}.

Contract: v0.4.1 spec #3 + WP1_CONTRACT REQ-002/003/004.
Pointer nodes {k,l,r,p}; iterative bottom-up splay; oriented ZIG events.
Ledger: list-credits [ctype,lo,hi,oriented] + cycling cursor; exact ints.
"""
from __future__ import annotations

C_FROZEN = 2
K_FROZEN = 6
LATENT, ACTIVE, SPENT = "LATENT", "ACTIVE", "SPENT"


def mknode(k, l=None, r=None, p=None):
    return {"k": k, "l": l, "r": r, "p": p}


def vine_right(n):
    """Degenerate right vine over keys 1..n (sealed T0 shape)."""
    root = None
    for k in range(n, 0, -1):
        nd = mknode(k, None, root)
        if root is not None:
            root["p"] = nd
        root = nd
    return root


def vine_left(n):
    """Mirror image: degenerate left vine over keys 1..n (mirror-variant corpus)."""
    # WP-1 STEP 23: mirror builder; BST-valid by construction.
    root = None
    for k in range(1, n + 1):
        nd = mknode(k, root, None)
        if root is not None:
            root["p"] = nd
        root = nd
    return root


def keys_inorder(t):
    out = []
    stack, cur = [], t
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = cur["l"]
        cur = stack.pop()
        out.append(cur["k"])
        cur = cur["r"]
    return out


def valid(t):
    ks = keys_inorder(t)
    return all(a < b for a, b in zip(ks, ks[1:]))


def _depth_to(t, x):
    """(depth, path) where path lists nodes from root; depth counts edges to x or leaf."""
    d, cur, path = 0, t, []
    while cur is not None:
        path.append(cur)
        if x == cur["k"]:
            return d, path
        cur = cur["l"] if x < cur["k"] else cur["r"]
        d += 1
    return d, path


def splay_cost(t, x):
    # WP-1 STEP 11: depth+1 cost, defined also for absent keys (depth to leaf).
    d, _ = _depth_to(t, x)
    return d + 1


def _rot_right(p):
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


def _rot_left(p):
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


def splay_trace(t, x):
    """Bottom-up splay. Returns (new_root, events). Absent key: (t, [])."""
    # WP-1 STEP 12: absent-key path — cost defined, empty trace, tree unchanged.
    d, path = _depth_to(t, x)
    if not path or path[-1]["k"] != x:
        return t, []
    evs = []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                _rot_right(p)
                evs.append({"case": "ZIG", "lo": min(node["k"], p["k"]), "hi": max(node["k"], p["k"]), "orient": "L"})
            else:
                _rot_left(p)
                evs.append({"case": "ZIG", "lo": min(node["k"], p["k"]), "hi": max(node["k"], p["k"]), "orient": "R"})
        elif p["l"] is node and g["l"] is p:
            _rot_right(g)
            _rot_right(p)
            evs.append({"case": "LL", "lo": min(node["k"], p["k"], g["k"]), "hi": max(node["k"], p["k"], g["k"]), "orient": "-"})
        elif p["r"] is node and g["r"] is p:
            _rot_left(g)
            _rot_left(p)
            evs.append({"case": "RR", "lo": min(node["k"], p["k"], g["k"]), "hi": max(node["k"], p["k"], g["k"]), "orient": "-"})
        elif p["r"] is node and g["l"] is p:
            _rot_left(p)
            _rot_right(g)
            evs.append({"case": "LR", "lo": min(node["k"], p["k"], g["k"]), "hi": max(node["k"], p["k"], g["k"]), "orient": "-"})
        else:
            _rot_right(p)
            _rot_left(g)
            evs.append({"case": "RL", "lo": min(node["k"], p["k"], g["k"]), "hi": max(node["k"], p["k"], g["k"]), "orient": "-"})
    while node["p"] is not None:
        node = node["p"]
    return node, evs


def canonical(t):
    if t is None:
        return "."
    return "(%d%s%s)" % (t["k"], canonical(t["l"]), canonical(t["r"]))


def p_all(mode, ev):
    return True


def _sites(lo, hi, x, nkeys):
    out = []
    for i in range(lo, max(lo, hi)):
        if 1 <= i < nkeys and i + 1 <= hi:
            out.append((i, i + 1, (i + 1) <= x))
    return out


def t7inject(st, is_a, lo, hi, x, nkeys):
    ledger, cursor = st
    if not is_a:
        return st
    ss = _sites(lo, hi, x, nkeys)
    if not ss:
        return st
    picks = [ss[(cursor + j) % len(ss)] for j in range(K_FROZEN)]
    return (ledger + [[LATENT, a, b, o] for (a, b, o) in picks], cursor + K_FROZEN)


def t5_one(st, mode, ev):
    """Inherited single activation (first-eligible ledger order)."""
    # WP-1 STEP 13: T5_{P_all,1} primitive; rho=FLAT(1) iterates it exactly once.
    ledger, cursor = st
    if not p_all(mode, ev):
        return st
    for i, c in enumerate(ledger):
        if c[0] == LATENT:
            ledger[i][0] = ACTIVE
            return (ledger, cursor)
    return st


def t5_rho_flat1(st, mode, ev):
    return t5_one(st, mode, ev)


def active_pool(ledger):
    return sum(1 for c in ledger if c[0] == ACTIVE)


def latent_pool(ledger):
    return sum(1 for c in ledger if c[0] == LATENT)


def discharge(ledger, need):
    out, paid = [], 0
    rem = need
    for c in ledger:
        if rem > 0 and c[0] == ACTIVE:
            out.append([SPENT, c[1], c[2], c[3]])
            paid += 1
            rem -= 1
        else:
            out.append(c)
    return out, paid


def required(y, a):
    return max(y - C_FROZEN * a, 0)


def replay_step(st, is_a, mode, ev, x, n):
    # WP-1 STEP 14: frozen replay equations — A-side T7->T5 per StepEv.
    _, lo, hi = ev["case"], ev["lo"], ev["hi"]
    return t5_rho_flat1(t7inject(st, is_a, lo, hi, x, n), mode, ev)


def replay_A(st, A, mode, x, n):
    a = splay_cost(A, x)
    A2, evs = splay_trace(A, x)
    e = st
    ract = 0
    for ev in evs:
        before = active_pool(e[0])
        e = replay_step(e, True, mode, ev, x, n)
        ract += active_pool(e[0]) - before
    return e, A2, a, ract, [(ev["case"], ev["lo"], ev["hi"], ev["orient"]) for ev in evs]


def replay_B(st, B, x, a):
    y = splay_cost(B, x)
    B2, evs = splay_trace(B, x)
    e = st
    ract = 0
    for ev in evs:
        before = active_pool(e[0])
        e = t5_rho_flat1(e, "KEEP", ev)
        ract += active_pool(e[0]) - before
    need = required(y, a)
    ledger, paid = discharge(e[0], need)
    return (ledger, e[1]), B2, y, need, paid, ract, [(ev["case"], ev["lo"], ev["hi"], ev["orient"]) for ev in evs]


def clone_tree(t):
    """Deep copy: A and B begin equal as VALUES and must not alias (else A-splay corrupts B)."""
    # WP-1 STEP 15a: aliasing A/B is a semantic fault (caught by differential LEG-02).
    if t is None:
        return None
    l, r = clone_tree(t["l"]), clone_tree(t["r"])
    nd = mknode(t["k"], l, r)
    if l is not None:
        l["p"] = nd
    if r is not None:
        r["p"] = nd
    return nd


def balanced(keys):
    """BST over an arbitrary key subset (sparse-T0 corpus)."""
    # WP-1 STEP 25: median-recursive balanced builder; valid by construction.
    if not keys:
        return None
    ks = sorted(keys)
    m = len(ks) // 2
    nd = mknode(ks[m], balanced(ks[:m]), balanced(ks[m + 1:]))
    if nd["l"] is not None:
        nd["l"]["p"] = nd
    if nd["r"] is not None:
        nd["r"]["p"] = nd
    return nd


def exec_hist(T0, H, n):
    """Full execution with per-access diagnostics. Returns (records, final)."""
    # WP-1 STEP 15: KEEP discharge after complete B trace; DELETE A-only, no discharge.
    for mode, x in H:
        if mode not in ("KEEP", "DELETE"):
            raise ValueError("illegal mode: %r" % (mode,))
        if not (1 <= x <= n):
            raise ValueError("access key outside [n]: %r" % (x,))
    A, B, st = clone_tree(T0), clone_tree(T0), ([], 0)
    sA = sB = 0
    recs = []
    for mode, x in H:
        if mode == "KEEP":
            L0, P0 = latent_pool(st[0]), active_pool(st[0])
            S0pre = sum(1 for c in st[0] if c[0] == SPENT)
            st, A2, a, ra, evA = replay_A(st, A, mode, x, n)
            Lmid, Pmid = latent_pool(st[0]), active_pool(st[0])
            st, B2, y, need, paid, rb, evB = replay_B(st, B, x, a)
            L2, P2 = latent_pool(st[0]), active_pool(st[0])
            sA, sB = sA + a, sB + y
            recs.append({"mode": mode, "x": x, "a": a, "y": y, "need": need, "paid": paid,
                         "margin": P2 + paid - need, "liq_slack": paid - need,
                         "dA": a - 1, "dB": y - 1,
                         "L0": L0, "P0": P0, "L1": Lmid, "P1": Pmid, "L2": L2, "P2": P2,
                         "rA": ra, "rB": rb, "actB_k": rb, "sA": sA, "sB": sB,
                         "events_A": evA, "events_B": evB,
                         "S0": S0pre})
            A, B = A2, B2
        else:
            L0, P0 = latent_pool(st[0]), active_pool(st[0])
            S0pre = sum(1 for c in st[0] if c[0] == SPENT)
            st, A2, a, ra, evA = replay_A(st, A, mode, x, n)
            L1, P1 = latent_pool(st[0]), active_pool(st[0])
            sA += a
            recs.append({"mode": mode, "x": x, "a": a, "y": 0, "need": 0, "paid": 0,
                         "margin": None, "dA": a - 1, "dB": None,
                         "L0": L0, "P0": P0, "L1": L1, "P1": P1,
                         "rA": ra, "rB": 0, "sA": sA, "sB": sB, "events_A": evA,
                         "S0": S0pre})
            A = A2
    return recs, (st, A, B, sA, sB)
