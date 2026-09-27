"""WP-1 STEP 16c: independent ledger + replay (imports .splay/.pair only)."""
from __future__ import annotations

from .pair import required
from .splay import cost, trace

K = 6
LAT, ACT, SP = "LATENT", "ACTIVE", "SPENT"


def fires(mode, ev):
    return True


def boundary(lo, hi, x, n):
    out = []
    for i in range(lo, max(lo, hi)):
        if 1 <= i < n and i + 1 <= hi:
            out.append((i, i + 1, (i + 1) <= x))
    return out


def inject(st, is_a, lo, hi, x, n):
    led, cur = st
    if not is_a:
        return st
    ss = boundary(lo, hi, x, n)
    if not ss:
        return st
    add = [(LAT,) + ss[(cur + j) % len(ss)] for j in range(K)]
    return (led + add, cur + K)


def activate(st, mode, ev):
    # WP-1 STEP 19: single first-eligible activation primitive.
    led, cur = st
    if not fires(mode, ev):
        return st
    for i, c in enumerate(led):
        if c[0] == LAT:
            return (led[:i] + [(ACT,) + c[1:]] + led[i + 1:], cur)
    return st


def pools(led):
    return (sum(1 for c in led if c[0] == LAT), sum(1 for c in led if c[0] == ACT))


def spend(led, need):
    out, paid = [], 0
    rem = need
    for c in led:
        if rem > 0 and c[0] == ACT:
            out.append((SP,) + c[1:])
            paid += 1
            rem -= 1
        else:
            out.append(c)
    return out, paid


def do_A(st, A, mode, x, n):
    a = cost(A, x)
    A2, evs = trace(A, x)
    e, ra = st, 0
    for ev in evs:
        _, lo, hi, _ = (ev[0], ev[1], ev[2], ev[3])
        before = pools(e[0])[1]
        e = activate(inject(e, True, lo, hi, x, n), mode, ev)
        ra += pools(e[0])[1] - before
    return e, A2, a, ra, [tuple(ev) for ev in evs]


def do_B(st, B, x, a):
    y = cost(B, x)
    B2, evs = trace(B, x)
    e, rb = st, 0
    for ev in evs:
        before = pools(e[0])[1]
        e = activate(e, "KEEP", ev)
        rb += pools(e[0])[1] - before
    need = required(y, a)
    led, paid = spend(e[0], need)
    return (led, e[1]), B2, y, need, paid, rb, [tuple(ev) for ev in evs]


def run(T0, H, n):
    """WP-1 STEP 20: KEEP = full A replay, full B replay, then discharge; DELETE = A only."""
    for mode, x in H:
        if mode not in ("KEEP", "DELETE"):
            raise ValueError("illegal mode: %r" % (mode,))
        if not (1 <= x <= n):
            raise ValueError("access key outside [n]: %r" % (x,))
    A, B, st = T0, T0, ([], 0)
    sA = sB = 0
    recs = []
    for mode, x in H:
        if mode == "KEEP":
            L0, P0 = pools(st[0])
            S0pre = sum(1 for c in st[0] if c[0] == SP)
            st, A2, a, ra, evA = do_A(st, A, mode, x, n)
            L1, P1 = pools(st[0])
            st, B2, y, need, paid, rb, evB = do_B(st, B, x, a)
            L2, P2 = pools(st[0])
            sA, sB = sA + a, sB + y
            recs.append({"mode": mode, "x": x, "a": a, "y": y, "need": need, "paid": paid,
                         "margin": P2 + paid - need, "liq_slack": paid - need,
                         "dA": a - 1, "dB": y - 1,
                         "L0": L0, "P0": P0, "L1": L1, "P1": P1, "L2": L2, "P2": P2,
                         "rA": ra, "rB": rb, "actB_k": rb, "sA": sA, "sB": sB,
                         "events_A": evA, "events_B": evB,
                         "S0": S0pre})
            A, B = A2, B2
        else:
            L0, P0 = pools(st[0])
            S0pre = sum(1 for c in st[0] if c[0] == SP)
            st, A2, a, ra, evA = do_A(st, A, mode, x, n)
            L1, P1 = pools(st[0])
            sA += a
            recs.append({"mode": mode, "x": x, "a": a, "y": 0, "need": 0, "paid": 0,
                         "margin": None, "dA": a - 1, "dB": None,
                         "L0": L0, "P0": P0, "L1": L1, "P1": P1,
                         "rA": ra, "rB": 0, "sA": sA, "sB": sB, "events_A": evA,
                         "S0": S0pre})
            A = A2
    return recs, (st, A, B, sA, sB)


def rho_cap(pair, ev):
    """WP-2 STEP 52: independent capacity from LOCAL CLASS ONLY. pair=(z, d); ROOT->0."""
    cls = ev[0] if isinstance(ev, tuple) else ev.get("case", "ROOT")
    if cls in ("ROOT", "NONE", "NO-EVENT"):
        return 0
    if cls in ("ZIG", "ZIG-L", "ZIG-R"):
        return pair[0]
    if cls in ("LL", "RR", "LR", "RL"):
        return pair[1]
    raise ValueError("unknown event class: %r" % (cls,))


def activate_bounded(st, cap, mode, ev):
    """WP-2 STEP 53: bounded first-eligible activation (tuple style, no liquidity imports)."""
    led, cur = st
    for _ in range(cap):
        nxt = activate((led, cur), mode, ev)
        if nxt[0] == led:
            break
        led, cur = nxt
    return (led, cur)


def energy_of(ledger):
    lat, act = pools(ledger)
    return lat + act
