"""WP-5 STEP 133: clean-room evaluator (share-nothing re-derivation).

Authored SOLELY from math/theorems/* + artifacts/v04/cleanroom/contract/* + input
histories. Ordinary bottom-up splay (cost depth+1); KEEP/DELETE pair dynamics;
(T7, T5_{P,rho}, T6) ledger with frozen candidate params; weaker-domain
LegalPairInstance; absent-key empty-trace path. Stdlib only. NEVER imports
liquidity/solver/adversary/holdout/independent (audited by FRSH-02).
Outputs per-KEEP (need, paid, margin) + ledger diagnostics.
"""
from __future__ import annotations

LATENT, ACTIVE, SPENT = "LATENT", "ACTIVE", "SPENT"

# WP-5 STEP 133: closed predicate transcription (mode-sets x class-sets).
_MA = ("KEEP", "DELETE")
_CA = ("ZIG", "LL", "RR", "LR", "RL")
_DB = ("LL", "RR", "LR", "RL")
_PTAB = {
    "P_all": (_MA, _CA), "P_keep": (("KEEP",), _CA),
    "P_keep_all": (("KEEP",), _CA), "P_keep_doubles": (("KEEP",), _DB),
    "P_keep_zig": (("KEEP",), ("ZIG",)), "P_keep_zigzag": (("KEEP",), ("LR", "RL")),
    "P_keep_zigzig": (("KEEP",), ("LL", "RR")),
    "P_both_doubles": (_MA, _DB), "P_both_zig": (_MA, ("ZIG",)),
    "P_both_zigzag": (_MA, ("LR", "RL")), "P_both_zigzig": (_MA, ("LL", "RR")),
    "P_delete_all": (("DELETE",), _CA), "P_delete_doubles": (("DELETE",), _DB),
    "P_delete_zig": (("DELETE",), ("ZIG",)),
    "P_delete_zigzag": (("DELETE",), ("LR", "RL")),
    "P_delete_zigzig": (("DELETE",), ("LL", "RR")),
}


def _norm(case: str) -> str:
    if case in ("ZIG", "ZIG-L", "ZIG-R"):
        return "ZIG"
    if case in _DB:
        return case
    if case in ("ROOT", "NONE", "NO-EVENT"):
        return "ROOT"
    raise ValueError("unknown event class: %r" % (case,))


def _fires(pred: str, mode: str, cls: str) -> bool:
    modes, classes = _PTAB[pred]
    return mode in modes and cls in classes


def _cap(rho, cls: str) -> int:
    z, d = rho
    if cls == "ROOT":
        return 0
    return z if cls == "ZIG" else d


def _node(k, l=None, r=None, p=None):
    return {"k": k, "l": l, "r": r, "p": p}


def _from_nested(t):
    if t is None:
        return None
    nd = _node(t[0], _from_nested(t[1]), _from_nested(t[2]))
    if nd["l"] is not None:
        nd["l"]["p"] = nd
    if nd["r"] is not None:
        nd["r"]["p"] = nd
    return nd


def _clone(t):
    if t is None:
        return None
    nd = _node(t["k"], _clone(t["l"]), _clone(t["r"]))
    if nd["l"] is not None:
        nd["l"]["p"] = nd
    if nd["r"] is not None:
        nd["r"]["p"] = nd
    return nd


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


def _depth_cost(t, x) -> int:
    d, cur = 0, t
    while cur is not None:
        if x == cur["k"]:
            return d + 1
        cur = cur["l"] if x < cur["k"] else cur["r"]
        d += 1
    return d + 1


def _splay(t, x):
    """WP-5 STEP 133: bottom-up splay; absent key -> (t, []) with defined cost."""
    d, cur, path = 0, t, []
    while cur is not None:
        path.append(cur)
        if x == cur["k"]:
            break
        cur = cur["l"] if x < cur["k"] else cur["r"]
        d += 1
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
                evs.append(("ZIG", min(node["k"], p["k"]), max(node["k"], p["k"])))
            else:
                _rot_left(p)
                evs.append(("ZIG", min(node["k"], p["k"]), max(node["k"], p["k"])))
        elif p["l"] is node and g["l"] is p:
            _rot_right(g)
            _rot_right(p)
            evs.append(("LL", min(node["k"], p["k"], g["k"]), max(node["k"], p["k"], g["k"])))
        elif p["r"] is node and g["r"] is p:
            _rot_left(g)
            _rot_left(p)
            evs.append(("RR", min(node["k"], p["k"], g["k"]), max(node["k"], p["k"], g["k"])))
        elif p["r"] is node and g["l"] is p:
            _rot_left(p)
            _rot_right(g)
            evs.append(("LR", min(node["k"], p["k"], g["k"]), max(node["k"], p["k"], g["k"])))
        else:
            _rot_right(p)
            _rot_left(g)
            evs.append(("RL", min(node["k"], p["k"], g["k"]), max(node["k"], p["k"], g["k"])))
    while node["p"] is not None:
        node = node["p"]
    return node, evs


def _sites(lo, hi, x, n):
    out = []
    for i in range(lo, max(lo, hi)):
        if 1 <= i < n and i + 1 <= hi:
            out.append(i)
    return out


def _check(n, T0, H) -> None:
    # WP-5 STEP 133: weaker-domain legality (keys(T0) subset [n], keys in [n]).
    def keys(t):
        return [] if t is None else keys(t[1]) + [t[0]] + keys(t[2])

    def bst(t, lo=0, hi=10 ** 9):
        return True if t is None else (
            lo < t[0] < hi and bst(t[1], lo, t[0]) and bst(t[2], t[0], hi))

    if not bst(T0) or any(not (1 <= k <= n) for k in keys(T0)):
        raise ValueError("illegal T0")
    for m, x in H:
        if m not in ("KEEP", "DELETE") or not (1 <= x <= n):
            raise ValueError("illegal access %r" % ((m, x),))


def execute(n, T0, H, pred: str, k: int, C: int, rho) -> dict:
    """WP-5 STEP 133: full exact execution; returns per-KEEP (need, paid, margin)."""
    _check(n, T0, H)
    A, B = _clone(_from_nested(T0)), _clone(_from_nested(T0))
    ledger, cursor = [], 0
    keeps = []
    for mode, x in H:
        a = _depth_cost(A, x)
        A, evsA = _splay(A, x)
        for case, lo, hi in evsA:
            cls = _norm(case)
            if _sites(lo, hi, x, n):
                ledger = ledger + [[LATENT] for _ in range(k)]
                cursor += k
            if _fires(pred, mode, cls):
                for _ in range(_cap(rho, cls)):
                    for i, c in enumerate(ledger):
                        if c[0] == LATENT:
                            ledger[i][0] = ACTIVE
                            break
                    else:
                        break
        if mode == "KEEP":
            y = _depth_cost(B, x)
            B, evsB = _splay(B, x)
            for case, lo, hi in evsB:
                cls = _norm(case)
                if _fires(pred, "KEEP", cls):
                    for _ in range(_cap(rho, cls)):
                        for i, c in enumerate(ledger):
                            if c[0] == LATENT:
                                ledger[i][0] = ACTIVE
                                break
                        else:
                            break
            need = y - C * a
            need = need if need > 0 else 0
            paid, rem = 0, need
            for c in ledger:
                if rem > 0 and c[0] == ACTIVE:
                    c[0] = SPENT
                    paid += 1
                    rem -= 1
            keeps.append({"need": need, "paid": paid,
                          "margin": sum(1 for c in ledger if c[0] == ACTIVE) + paid - need})
    return {"keeps": keeps,
            "violations": sum(1 for kp in keeps if kp["paid"] < kp["need"])}
