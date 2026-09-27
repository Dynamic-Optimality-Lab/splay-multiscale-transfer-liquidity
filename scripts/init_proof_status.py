"""WP-0 STEP 09 helper: initialize math/proof_status.json (27 theorems, all UNPROVED/NO_WITNESS)."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ids = sorted(p.stem for p in (ROOT / "math" / "theorems").glob("*.md"))
assert len(ids) == 27, ids
st = {tid: {"truth": "UNPROVED", "prove_track": "UNPROVED", "refute_track": "NO_WITNESS",
            "theorem_hash": None, "proof_hash": None, "review_hash": None} for tid in ids}
(ROOT / "math" / "proof_status.json").write_text(json.dumps(st, indent=2, sort_keys=True), encoding="utf-8")
print("[WP-0][STEP 09] proof_status initialized: %d rows, all UNPROVED/NO_WITNESS" % len(st))
