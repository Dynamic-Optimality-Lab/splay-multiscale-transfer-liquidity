"""WP-5 STEP 135: reveal-once driver (single lawful transition to REVEALED_ONCE).

Guards: firewall must be CANDIDATE_SET_FROZEN with unlocks==0; commitment must
re-verify against the secret bank BEFORE the transition. Publishes seed + bank +
manifest to artifacts/v04/h4l_reveal/ (public reveal record). Never evaluates.
Refuses second reveal, regen, and any pre-freeze invocation. Single-shot.
"""
from __future__ import annotations
import datetime
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import firewall as FW
from holdout import h4l_verify as V


def main() -> int:
    print("[WP-5][STEP 135] Reveal-once driver", flush=True)
    st = FW.read_state()
    if st["state"] != "CANDIDATE_SET_FROZEN":
        print("[WP-5][STEP 135] Refuses: reveal legal only from CANDIDATE_SET_FROZEN "
              "(state=%s)" % st["state"], flush=True)
        return 2
    if st["unlocks"] != 0:
        print("[WP-5][STEP 135] Refuses: unlock counter nonzero", flush=True)
        return 2
    com_p = ROOT / "artifacts" / "v04" / "holdouts" / "h4l_commitment.json"
    if not com_p.exists():
        print("[WP-5][STEP 135] Refuses: no published commitment", flush=True)
        return 2
    secret = FW._default_secret()
    if not (secret / "seed.bin").exists():
        print("[WP-5][STEP 135] Refuses: secret bank absent", flush=True)
        return 2
    if not V.verify(secret, com_p):
        print("[WP-5][STEP 135] Refuses: commitment recompute failed", flush=True)
        return 2
    print("[WP-5][STEP 135] Commitment re-verified at reveal; publishing bank", flush=True)
    dest = ROOT / "artifacts" / "v04" / "h4l_reveal"
    if dest.exists():
        print("[WP-5][STEP 135] Refuses: reveal record already published", flush=True)
        return 2
    (dest / "bank").mkdir(parents=True)
    shutil.copy2(secret / "seed.bin", dest / "seed.bin")
    for sh in sorted((secret / "bank").glob("*.json.zst")):
        shutil.copy2(sh, dest / "bank" / sh.name)
    shutil.copy2(secret / "manifest.json", dest / "manifest.json")
    FW.transition("REVEALED_ONCE", "one-shot reveal after commitment re-verify")
    (dest / "reveal.json").write_text(json.dumps({
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "unlocks": 1, "state": "REVEALED_ONCE"}, indent=2, sort_keys=True), encoding="utf-8")
    print("[WP-5][STEP 135] Revealed once (unlocks=1)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
