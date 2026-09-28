"""WP-4 STEP 112: exact evaluator driver (count-faithful ledger simulation).

Splay mechanics come from the frozen WP-1 pointer engine; traces are precomputed
once per episode (tree evolution is config-independent). The ledger is simulated
as exact integer pools: T7 injects k per A-event with nonempty sites; T5 moves
min(eligible,cap) LATENT->ACTIVE under closed-predicate gating; T6 discharges
min(ACTIVE,need) with need=max(y-C*a,0). Violation = legal KEEP with paid<need.

Count-simulation is proven equal to list-simulation on the fidelity corpus (SYN-01).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from liquidity import multiplicity as MU
from solver import predicates as CP
from solver import legality as LG

FLAT1 = (1, 1)
LADDER = [(r, r) for r in range(1, 7)] + [(r, 2 * r) for r in range(1, 7)]
LADDER_NAMES = ["FLAT(%d)" % r for r in range(1, 7)] + ["ROT(%d)" % r for r in range(1, 7)]
K_GRID = [0, 1, 2, 3, 4, 5, 6]
C_GRID = [2, 3, 4, 6, 8, 12, 16, 24, 32, 64]


def _sites_nonempty(lo: int, hi: int, x: int, n: int) -> bool:
    """WP-4 STEP 112: T7 site existence (same predicate as the frozen _sites)."""
    for i in range(lo, max(lo, hi)):
        if 1 <= i < n and i + 1 <= hi:
            return True
    return False


def _to_pointer(t):
    if t is None:
        return None
    nd = PE.mknode(t[0], _to_pointer(t[1]), _to_pointer(t[2]))
    if nd["l"] is not None:
        nd["l"]["p"] = nd
    if nd["r"] is not None:
        nd["r"]["p"] = nd
    return nd


def precompute(n: int, T0, H):
    """WP-4 STEP 112: config-independent splay precompute. Returns access records.

    Each record: (mode, x, a, y, A_events[(cls,lo,hi)], B_events[(cls,lo,hi)],
    A_sites[bool per A-event]). B_events empty for DELETE. Mirrors exec_hist order.
    """
    LG.check(n, T0, H)
    A, B = _to_pointer(T0), _to_pointer(T0)
    out = []
    for mode, x in H:
        a = PE.splay_cost(A, x)
        A2, evsA = PE.splay_trace(A, x)
        Aev = [(ev["case"], ev["lo"], ev["hi"]) for ev in evsA]
        sites = [_sites_nonempty(lo, hi, x, n) for (_, lo, hi) in Aev]
        if mode == "KEEP":
            y = PE.splay_cost(B, x)
            B2, evsB = PE.splay_trace(B, x)
            Bev = [(ev["case"], ev["lo"], ev["hi"]) for ev in evsB]
            A, B = A2, B2
        else:
            y, Bev = 0, []
            A = A2
        out.append({"mode": mode, "x": x, "a": a, "y": y,
                    "Aev": Aev, "Bev": Bev, "sites": sites})
    return out


def _cap(rho, cls: str) -> int:
    # WP-4 STEP 112: capacity from local class only (ROOT/no-event -> 0).
    z, d = rho
    if cls == "ROOT":
        return 0
    if cls == "ZIG":
        return z
    return d


def exec_counts(pre, pred: str, k: int, C: int, rho) -> dict:
    """WP-4 STEP 112: exact integer-pool execution. Returns keeps + violation info."""
    lat = act = spent = injected = 0
    cursor = 0
    keeps = []
    viol = 0
    first_viol = None
    for idx, acc in enumerate(pre):
        mode = acc["mode"]
        for (cls, lo, hi), sn in zip(acc["Aev"], acc["sites"]):
            cls_n = MU.normalize(cls)
            if sn:
                lat += k
                injected += k
                cursor += k
            if CP.fires(pred, mode, cls_n):
                mv = lat if lat < _cap(rho, cls_n) else _cap(rho, cls_n)
                lat -= mv
                act += mv
        if mode == "KEEP":
            act_pre_B = act
            for (cls, lo, hi) in acc["Bev"]:
                cls_n = MU.normalize(cls)
                if CP.fires(pred, "KEEP", cls_n):
                    mv = lat if lat < _cap(rho, cls_n) else _cap(rho, cls_n)
                    lat -= mv
                    act += mv
            need = acc["y"] - C * acc["a"]
            need = need if need > 0 else 0
            paid = act if act < need else need
            act -= paid
            spent += paid
            margin = act + paid - need
            keeps.append({"idx": idx, "need": need, "paid": paid, "margin": margin,
                          "act_pre_B": act_pre_B, "B_events": len(acc["Bev"])})
            if paid < need:
                viol += 1
                if first_viol is None:
                    first_viol = idx
        if lat + act + spent != injected:
            raise AssertionError("energy conservation violated")
    return {"keeps": keeps, "violations": viol, "first_violation": first_viol,
            "injected": injected}


def exec_full(n: int, T0, H, pred: str, k: int, C: int, rho) -> dict:
    """WP-4 STEP 112: precompute + count execution (convenience entry)."""
    return exec_counts(precompute(n, T0, H), pred, k, C, rho)


def residual_summary(res: dict) -> tuple:
    """WP-4 STEP 112: exact-residual dominance key (violations, worst shortfall)."""
    short = 0
    for kp in res["keeps"]:
        d = kp["need"] - kp["paid"]
        if d > short:
            short = d
    return (res["violations"], short)
