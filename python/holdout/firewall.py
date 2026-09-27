"""WP-3 STEP 86: firewall automaton. States EMPTY -> GENERATOR_FROZEN -> BANK_GENERATED_SECRET
-> COMMITMENT_PUBLISHED -> CANDIDATE_SET_FROZEN -> REVEALED_ONCE -> CONSUMED.
Secret bytes readable only at/after REVEALED_ONCE. Unlock count immutable, max 1.
"""
from __future__ import annotations
import json
import os
from pathlib import Path

STATES = ["EMPTY", "GENERATOR_FROZEN", "BANK_GENERATED_SECRET", "COMMITMENT_PUBLISHED",
          "CANDIDATE_SET_FROZEN", "REVEALED_ONCE", "CONSUMED"]
STATE_FILE = Path(__file__).resolve().parents[2] / "artifacts" / "v04" / "holdouts" / "firewall_state.json"


class FirewallError(Exception):
    pass


def _default_secret() -> Path:
    return Path(os.environ.get("H4L_SECRET", r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\h4l-secret"))


def read_state() -> dict:
    # WP-3 STEP 86: missing state file means EMPTY (fail-closed default).
    if not STATE_FILE.exists():
        return {"state": "EMPTY", "unlocks": 0, "log": []}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _write(st: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, indent=2, sort_keys=True), encoding="utf-8")


def transition(to: str, note: str = "") -> dict:
    """WP-3 STEP 87: legal transitions only; unlocks immutable increment on REVEALED_ONCE."""
    st = read_state()
    order = {s: i for i, s in enumerate(STATES)}
    if to not in order or order[to] != order[st["state"]] + 1:
        raise FirewallError("illegal firewall transition %s -> %s" % (st["state"], to))
    if to == "REVEALED_ONCE":
        if st["unlocks"] >= 1:
            raise FirewallError("second unlock forbidden")
        st["unlocks"] = 1
    st["state"] = to
    st["log"].append({"to": to, "note": note})
    _write(st)
    print("[WP-3][STEP 87] Firewall -> %s (%s)" % (to, note))
    return st


def guard_bank_read() -> Path:
    """WP-3 STEP 88: secret bank bytes readable only at/after REVEALED_ONCE."""
    st = read_state()
    if STATES.index(st["state"]) < STATES.index("REVEALED_ONCE"):
        raise FirewallError("bank read before reveal (state=%s)" % st["state"])
    return _default_secret()


def reveal() -> Path:
    """WP-3 STEP 89: one-shot reveal, legal only from CANDIDATE_SET_FROZEN."""
    st = read_state()
    if st["state"] != "CANDIDATE_SET_FROZEN":
        raise FirewallError("reveal legal only from CANDIDATE_SET_FROZEN (state=%s)" % st["state"])
    transition("REVEALED_ONCE", "one-shot reveal")
    return _default_secret()
