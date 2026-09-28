"""WP-4 STEP 110: closed predicate family resolver (16 IDs -> (modes, classes)).

Semantics transcribed from prereg/predicate_family_v0.4.1.yaml (frozen); this module
adds no new predicates. Verified against the prereg file by SYN-03.
"""
from __future__ import annotations

MODES = ("KEEP", "DELETE")
CLASSES = ("ZIG", "LL", "RR", "LR", "RL")
DOUBLES = ("LL", "RR", "LR", "RL")

# WP-4 STEP 110: frozen (mode-set, class-set) per closed predicate ID.
TABLE = {
    "P_all": (MODES, CLASSES),
    "P_keep": (("KEEP",), CLASSES),
    "P_keep_all": (("KEEP",), CLASSES),
    "P_keep_doubles": (("KEEP",), DOUBLES),
    "P_keep_zig": (("KEEP",), ("ZIG",)),
    "P_keep_zigzag": (("KEEP",), ("LR", "RL")),
    "P_keep_zigzig": (("KEEP",), ("LL", "RR")),
    "P_both_doubles": (MODES, DOUBLES),
    "P_both_zig": (MODES, ("ZIG",)),
    "P_both_zigzag": (MODES, ("LR", "RL")),
    "P_both_zigzig": (MODES, ("LL", "RR")),
    "P_delete_all": (("DELETE",), CLASSES),
    "P_delete_doubles": (("DELETE",), DOUBLES),
    "P_delete_zig": (("DELETE",), ("ZIG",)),
    "P_delete_zigzag": (("DELETE",), ("LR", "RL")),
    "P_delete_zigzig": (("DELETE",), ("LL", "RR")),
}

CLOSED_IDS = tuple(sorted(TABLE))


def firing_pairs(pred: str) -> int:
    """WP-4 STEP 110: rule breadth (simpler-P ordering: fewer firing pairs first)."""
    modes, classes = TABLE[pred]
    return len(modes) * len(classes)


def fires(pred: str, mode: str, cls: str) -> bool:
    """WP-4 STEP 110: closed-predicate gate on (mode, normalized class) ONLY."""
    modes, classes = TABLE[pred]
    return mode in modes and cls in classes
