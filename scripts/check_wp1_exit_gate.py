"""WP-1 STEP 34: exit-gate checker — review existence, ACCEPT, hash binding, REVIEWED.

Fail closed (exit 2) on any mismatch. No verdicts created here.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> int:
    print("[WP-1][STEP 34] EXIT-GATE FAIL: %s" % msg)
    return 2


def main() -> int:
    print("[WP-1][STEP 34] Verifying WP-1 exit gate")
    rj_p = ROOT / "math" / "reviews" / "LIQ0-01.review.json"
    if not rj_p.exists():
        return fail("review record missing")
    rj = json.loads(rj_p.read_text(encoding="utf-8"))
    if rj.get("verdict") != "ACCEPT":
        return fail("verdict is %r, not ACCEPT" % rj.get("verdict"))
    thm = (ROOT / "math" / "theorems" / "LIQ0-01.md").read_bytes()
    prf = (ROOT / "math" / "proofs" / "LIQ0-01.md").read_bytes()
    pkg = (ROOT / "math" / "reviews" / "LIQ0-01.PACKAGE.md").read_bytes()
    if hashlib.sha256(thm).hexdigest() != rj.get("theorem_hash"):
        return fail("theorem hash drift")
    if hashlib.sha256(prf).hexdigest() != rj.get("evidence", {}).get("layerA"):
        return fail("proof hash drift")
    if hashlib.sha256(pkg).hexdigest() != rj.get("evidence", {}).get("package"):
        return fail("package hash drift")
    corpus = (ROOT / "artifacts" / "v04" / "parent_import" / "replay" / "corpus_report.json").read_bytes()
    if hashlib.sha256(corpus).hexdigest() != rj.get("evidence", {}).get("corpus_sha256"):
        return fail("corpus hash drift")
    st = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    row = st.get("LIQ0-01", {})
    if row.get("truth") != "REVIEWED":
        return fail("proof_status truth is %r" % row.get("truth"))
    if row.get("proof_hash") != hashlib.sha256(prf).hexdigest():
        return fail("proof_status proof_hash drift")
    print("[WP-1][STEP 34] EXIT-GATE PASS (ACCEPT + hashes bound + REVIEWED)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
