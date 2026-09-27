"""WP-2 STEP 40: event multiplicity mu(ev) + ZIG normalization map.

Contract: v0.4.1 spec #2 + CC-056/057. Total function; orientation retained by callers.
"""
from __future__ import annotations

CLASSES = ("ROOT", "ZIG", "LL", "RR", "LR", "RL")
DOUBLES = ("LL", "RR", "LR", "RL")


def normalize(case: str) -> str:
    """WP-2 STEP 40: map oriented/raw case labels to the canonical class.

    ZIG-L/ZIG-R (oriented trace labels) -> ZIG; orientation stays in the event record.
    """
    if case in ("ZIG-L", "ZIG-R", "ZIG"):
        return "ZIG"
    if case in DOUBLES:
        return case
    if case in ("ROOT", "NONE", "NO-EVENT"):
        return "ROOT"
    raise ValueError("unknown event class: %r" % (case,))


def mu(ev) -> int:
    """WP-2 STEP 41: primitive-rotation count. ROOT/no-event -> 0 (total)."""
    cls = normalize(ev["case"] if isinstance(ev, dict) else ev[0])
    if cls == "ROOT":
        return 0
    if cls == "ZIG":
        return 1
    return 2


def trace_sum(evs) -> int:
    """Sum of mu over a compressed StepEv trace."""
    # WP-2 STEP 42: LIQ0-02 computational content for present-key accesses.
    return sum(mu(ev) for ev in evs)
