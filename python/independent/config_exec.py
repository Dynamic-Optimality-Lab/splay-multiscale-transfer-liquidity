"""WP-4 STEP 115: share-nothing independent violation replay with (P,k,C,rho).

Re-derives closed-predicate gating, k-injection, C-need, and rho-caps from the
frozen prereg semantics using ONLY independent siblings (.splay/.pair tuple
engine + local ledger ops). Never imports liquidity/solver/holdout/adversary.
"""
from __future__ import annotations

from .splay import cost, trace

LAT, ACT, SP = "LATENT", "ACTIVE", "SPENT"

# WP-4 STEP 115: independent transcription of the closed predicate family
# (mode-sets x class-sets; cross-checked against prereg by SYN-03/SYN-05).
_MODES_ALL = ("KEEP", "DELETE")
_CLS_ALL = ("ZIG", "LL", "RR", "LR", "RL")
_CLS_DBL = ("LL", "RR", "LR", "RL")
_PTAB = {
    "P_all": (_MODES_ALL, _CLS_ALL), "P_keep": (("KEEP",), _CLS_ALL),
    "P_keep_all": (("KEEP",), _CLS_ALL), "P_keep_doubles": (("KEEP",), _CLS_DBL),
    "P_keep_zig": (("KEEP",), ("ZIG",)), "P_keep_zigzag": (("KEEP",), ("LR", "RL")),
    "P_keep_zigzig": (("KEEP",), ("LL", "RR")),
    "P_both_doubles": (_MODES_ALL, _CLS_DBL), "P_both_zig": (_MODES_ALL, ("ZIG",)),
    "P_both_zigzag": (_MODES_ALL, ("LR", "RL")),
    "P_both_zigzig": (_MODES_ALL, ("LL", "RR")),
    "P_delete_all": (("DELETE",), _CLS_ALL), "P_delete_doubles": (("DELETE",), _CLS_DBL),
    "P_delete_zig": (("DELETE",), ("ZIG",)),
    "P_delete_zigzag": (("DELETE",), ("LR", "RL")),
    "P_delete_zigzig": (("DELETE",), ("LL", "RR")),
}


def _norm(case: str) -> str:
    if case in ("ZIG", "ZIG-L", "ZIG-R"):
        return "ZIG"
    if case in _CLS_DBL:
        return case
    if case in ("ROOT", "NONE", "NO-EVENT"):
        return "ROOT"
    raise ValueError("unknown class %r" % (case,))


def _fires(pred: str, mode: str, cls: str) -> bool:
    modes, classes = _PTAB[pred]
    return mode in modes and cls in classes


def _cap(rho, cls: str) -> int:
    z, d = rho
    if cls == "ROOT":
        return 0
    return z if cls == "ZIG" else d


def _sites(lo, hi, x, n):
    out = []
    for i in range(lo, max(lo, hi)):
        if 1 <= i < n and i + 1 <= hi:
            out.append((i, i + 1))
    return out


def _to_tuple(t):
    # WP-4 STEP 115 (+ WP-5 iterative robustness): nested-list T0 -> independent
    # tuple tree, post-order explicit stack (no shared bytes, no recursion limit).
    from .splay import node, LEAF
    if t is None:
        return LEAF
    out = {}
    stack = [(t, False)]
    while stack:
        src, done = stack.pop()
        if src is None:
            continue
        if done:
            l = out[id(src[1])] if src[1] is not None else LEAF
            r = out[id(src[2])] if src[2] is not None else LEAF
            out[id(src)] = node(src[0], l, r)
        else:
            stack.append((src, True))
            stack.append((src[1], False))
            stack.append((src[2], False))
    return out[id(t)]


def _clone(t):
    # WP-5 robustness: iterative deep copy of tuple trees.
    from .splay import node, LEAF
    if t[0] == "leaf":
        return LEAF
    out = {}
    stack = [(t, False)]
    while stack:
        src, done = stack.pop()
        if src[0] == "leaf":
            out[id(src)] = LEAF
            continue
        if done:
            out[id(src)] = node(src[1], out[id(src[2])], out[id(src[3])])
        else:
            stack.append((src, True))
            stack.append((src[2], False))
            stack.append((src[3], False))
    return out[id(t)]


def replay(n, T0, H, pred: str, k: int, C: int, rho) -> dict:
    """WP-4 STEP 115: independent full execution; returns per-KEEP (need, paid)."""
    A, B = _clone(_to_tuple(T0)), _clone(_to_tuple(T0))
    led, cur = [], 0
    keeps = []
    for mode, x in H:
        a = cost(A, x)
        A2, evsA = trace(A, x)
        for ev in evsA:
            cls = _norm(ev[0])
            if _sites(ev[1], ev[2], x, n):
                led = led + [(LAT,)] * k
                cur += k
            if _fires(pred, mode, cls):
                for _ in range(_cap(rho, cls)):
                    for i, c in enumerate(led):
                        if c[0] == LAT:
                            led = led[:i] + [(ACT,)] + led[i + 1:]
                            break
                    else:
                        break
        A = A2
        if mode == "KEEP":
            y = cost(B, x)
            B2, evsB = trace(B, x)
            for ev in evsB:
                cls = _norm(ev[0])
                if _fires(pred, "KEEP", cls):
                    for _ in range(_cap(rho, cls)):
                        for i, c in enumerate(led):
                            if c[0] == LAT:
                                led = led[:i] + [(ACT,)] + led[i + 1:]
                                break
                        else:
                            break
            need = y - C * a
            need = need if need > 0 else 0
            paid, rem = 0, need
            out = []
            for c in led:
                if rem > 0 and c[0] == ACT:
                    out.append((SP,))
                    paid += 1
                    rem -= 1
                else:
                    out.append(c)
            led = out
            keeps.append({"need": need, "paid": paid})
            B = B2
    return {"keeps": keeps,
            "violations": sum(1 for kp in keeps if kp["paid"] < kp["need"])}
