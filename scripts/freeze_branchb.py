import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = {"status": "DORMANT", "branch": "SIGNED_MULTISCALE", "rho_ladder": ["FLAT-1..6", "ROT-1..6"],
        "energy": "E_signed = sum(m) with proved lower bound MSTL-12 (unproved; use forbidden)",
        "note": "Dormant pre-reveal freeze (CC-020). No synthesis. Activation only on Branch-A dev/fresh rejection."}
for pid, pred in [("dormant_B01", "P_all"), ("dormant_B02", "P_keep")]:
    ident = dict(BASE)
    ident.update({"calculus_id": pid, "rule_family_id": "SIGNED_FAM_001", "predicate": pred,
                  "k": 6, "C": 2, "T7": "inherited", "T5_rho": "signed sign-preserving (spec #7)",
                  "T6": "inherited", "legal_domain": "weaker-domain hash at WP-5 freeze"})
    ident["identity_hash"] = hashlib.sha256(json.dumps(ident, sort_keys=True).encode()).hexdigest()
    (ROOT / "artifacts" / "v04" / "candidates" / "branchB" / ("%s.json" % pid)).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts" / "v04" / "candidates" / "branchB" / ("%s.json" % pid)).write_text(json.dumps(ident, indent=2, sort_keys=True), encoding="utf-8")
print("WP-3 STEP 92: 2 dormant Branch-B identities frozen")
