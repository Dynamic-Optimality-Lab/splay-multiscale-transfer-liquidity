"""WP-2 STEP 50: per-KEEP liquidity diagnostics (sealed-compatible + capacity books).

Q (flat activation pressure) is diagnostic-only, never a theorem premise.
Output conforms to schemas/keep_record.schema.json (13 required fields).
"""
from __future__ import annotations

from .activation import pools
from .multiplicity import trace_sum


def flat_pressure(need: int, active_pre: int, opportunities: int):
    """WP-2 STEP 50: Q = 0 if need covered; ceil((need-active)/N); +inf if N=0 and short."""
    if need <= active_pre:
        return 0
    if opportunities <= 0:
        return float("inf")
    return -(-(need - active_pre) // opportunities)


def keep_record(lat_bA, act_bA, capA, actA, lat_bB, act_bB, capB, actB, need, paid,
                stock_pre, unused_cap):
    """WP-2 STEP 51: build the 13-field KEEP record (schema-locked field set)."""
    return {"latent_before_A": lat_bA, "active_before_A": act_bA,
            "A_capacity": capA, "A_actual": actA,
            "latent_before_B": lat_bB, "active_before_B": act_bB,
            "B_capacity": capB, "B_actual": actB,
            "need": need, "paid": paid,
            "liquidity_slack": paid - need, "stock_before_discharge": stock_pre,
            "unused_capacity": unused_cap}
