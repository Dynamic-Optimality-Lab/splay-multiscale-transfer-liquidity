"""WP-2 STEP 46: T5_{P,rho} bounded iteration + eligibleLatentCount gating.

Contract: v0.4.1 spec #3 + CC-007/008/009. P_all fires always (P_keep/case-restricted
arrive via the closed predicate family; predicate table frozen in WP-3 grammar lock).
"""
from __future__ import annotations

LATENT, ACTIVE, SPENT = "LATENT", "ACTIVE", "SPENT"


def predicate_fires(predicate: str, mode: str, ev) -> bool:
    """WP-2 STEP 46: predicate gate on (mode, normalized class) ONLY."""
    from .multiplicity import normalize
    if predicate == "P_all":
        return True
    if predicate == "P_keep":
        return mode == "KEEP"
    if predicate.startswith("P_case:"):
        allow = set(predicate.split(":", 1)[1].split(","))
        cls = normalize(ev["case"] if isinstance(ev, dict) else ev[0])
        return cls in allow
    raise ValueError("unknown predicate: %r" % (predicate,))


def eligible_indices(ledger, predicate: str, mode: str, ev):
    """WP-2 STEP 47: eligibleLatentCount positions (LATENT + predicate fires), ledger order."""
    if not predicate_fires(predicate, mode, ev):
        return []
    return [i for i, c in enumerate(ledger) if c[0] == LATENT]


def t5_one(ledger, predicate: str, mode: str, ev):
    """Inherited single activation primitive with explicit (P, mode, ev) binding."""
    # WP-2 STEP 48: T5_{P,1}; FLAT(1)/P_all instance is the WP-1-verified primitive.
    idx = eligible_indices(ledger, predicate, mode, ev)
    if not idx:
        return ledger
    i = idx[0]
    out = [list(c) for c in ledger]
    out[i][0] = ACTIVE
    return out


def t5_rho(ledger, predicate: str, profile, mode: str, ev):
    """WP-2 STEP 49: T5_{P,rho} = bounded iteration of T5_{P,1}, cap = profile.capacity(ev).

    Partial activation: fewer eligible than cap activates all available, creates nothing.
    """
    cap = profile.capacity(ev)
    out = [list(c) for c in ledger]
    for _ in range(cap):
        new = t5_one(out, predicate, mode, ev)
        if new == out:
            break
        out = new
    return out


def pools(ledger):
    lat = sum(1 for c in ledger if c[0] == LATENT)
    act = sum(1 for c in ledger if c[0] == ACTIVE)
    return lat, act


def energy(ledger):
    """E = #LATENT + #ACTIVE (Branch A unsigned)."""
    lat, act = pools(ledger)
    return lat + act


def support_multiset(ledger):
    return sorted((c[1], c[2], c[3]) for c in ledger)
