"""WP-2 STEP 43: rho profiles over (rho_ZIG, rho_DOUBLE), 0..12; FLAT/ROT subfamilies.

Contract: v0.4.1 spec #3 + prereg/liquidity_axis.yaml. Static allowlist: a profile
may inspect ONLY the normalized local event class. Constructor rejects everything else.
"""
from __future__ import annotations

from .multiplicity import normalize

RMAX = 12
FORBIDDEN = ("n", "tree_identity", "state_id", "cycle_id", "history_index", "future_key",
             "candidate_residual", "bellman_value", "holdout_membership", "support_id",
             "required_amount", "would_otherwise_fail")


class RhoProfile:
    """Frozen (rho_ZIG, rho_DOUBLE) profile. Immutable after construction."""

    def __init__(self, rho_zig: int, rho_double: int, name: str):
        # WP-2 STEP 43: bounds + ROOT totalization live here, nowhere else.
        if not (0 <= rho_zig <= RMAX and 0 <= rho_double <= RMAX):
            raise ValueError("rho out of admissible 0..12")
        for f in FORBIDDEN:
            if f in name:
                raise ValueError("profile name carries forbidden dependency: %s" % f)
        self._z = rho_zig
        self._d = rho_double
        self.name = name

    def capacity(self, ev) -> int:
        """WP-2 STEP 44: per-event capacity from LOCAL CLASS ONLY.

        Any caller passing residual/need/tree-derived data has no reader here:
        the signature exposes exactly (normalized class). ROOT/no-event -> 0.
        """
        cls = normalize(ev["case"] if isinstance(ev, dict) else ev[0])
        if cls == "ROOT":
            return 0
        if cls == "ZIG":
            return self._z
        return self._d

    def as_pair(self):
        return (self._z, self._d)


def FLAT(r: int) -> RhoProfile:
    if not 1 <= r <= 6:
        raise ValueError("ladder FLAT r out of 1..6")
    return RhoProfile(r, r, "FLAT(%d)" % r)


def ROT(r: int) -> RhoProfile:
    if not 1 <= r <= 6:
        raise ValueError("ladder ROT r out of 1..6")
    return RhoProfile(r, 2 * r, "ROT(%d)" % r)


def LADDER():
    """WP-2 STEP 45: the frozen 12-profile discovery ladder (exact set)."""
    return [FLAT(r) for r in range(1, 7)] + [ROT(r) for r in range(1, 7)]
