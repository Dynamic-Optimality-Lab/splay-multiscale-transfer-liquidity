"""H5 firewall automaton: dedicated state machine, independent from H4L history.

Lifecycle: EMPTY -> GENERATOR_FROZEN -> BANK_GENERATED_SECRET ->
COMMITMENT_PUBLISHED -> CANDIDATE_SET_BOUND -> REVEALED_ONCE -> CONSUMED.
Secret bytes readable only at/after REVEALED_ONCE. Unlock max 1.
State file: artifacts/v04/h5/firewall_state.json (never touches H4L state).
Secret dir: $H5_SECRET (outside the repo).
"""
from __future__ import annotations
import json
import os
from pathlib import Path

STATES = ["EMPTY", "GENERATOR_FROZEN", "BANK_GENERATED_SECRET", "COMMITMENT_PUBLISHED",
          "CANDIDATE_SET_BOUND", "REVEALED_ONCE", "CONSUMED"]
STATE_FILE = Path(__file__).resolve().parents[2] / "artifacts" / "v04" / "h5" / "firewall_state.json"
UNLOCK_MAX = 1


class FirewallError(Exception):
    pass


def _default_secret() -> Path:
    return Path(os.environ.get("H5_SECRET", r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\h5-secret"))


def read_state() -> dict:
    if not STATE_FILE.exists():
        return {"state": "EMPTY", "unlocks": 0, "log": []}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _write(st: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, indent=2, sort_keys=True), encoding="utf-8")


def transition(to: str, note: str = "") -> dict:
    st = read_state()
    order = {s: i for i, s in enumerate(STATES)}
    if to not in order or order[to] != order[st["state"]] + 1:
        raise FirewallError("illegal H5 firewall transition %s -> %s" % (st["state"], to))
    if to == "REVEALED_ONCE":
        if st["unlocks"] >= UNLOCK_MAX:
            raise FirewallError("second H5 unlock forbidden")
        st["unlocks"] = 1
    st["state"] = to
    st["log"].append({"to": to, "note": note})
    _write(st)
    print("[H5] Firewall -> %s (%s)" % (to, note))
    return st


def guard_bank_read() -> Path:
    st = read_state()
    if STATES.index(st["state"]) < STATES.index("REVEALED_ONCE"):
        raise FirewallError("H5 bank read before reveal (state=%s)" % st["state"])
    return _default_secret()


def reveal() -> Path:
    st = read_state()
    if st["state"] != "CANDIDATE_SET_BOUND":
        raise FirewallError("H5 reveal legal only from CANDIDATE_SET_BOUND (state=%s)" % st["state"])
    transition("REVEALED_ONCE", "one-shot H5 reveal")
    return _default_secret()
