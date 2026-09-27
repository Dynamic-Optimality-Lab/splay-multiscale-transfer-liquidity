import yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
led = yaml.safe_load((ROOT / "planning" / "CONTRACT_CLOSURE_LEDGER.yaml").read_text(encoding="utf-8"))
d = yaml.safe_load((ROOT / "planning" / "V04_TO_V041_SEMANTIC_DIFF.yaml").read_text(encoding="utf-8"))
dmap = {r["cc"]: r for r in d["changes"]}
L = ["# SPLAY-AM-MST-LIQ-v0.4.1 CONTRACT-CLOSURE Amendment", "",
     "Historical spec: historical/IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt (SHA-256 0E2C166E1B721DFC8A7E5327ED33AF29A1B4AC539CB71849F3C7231B32A8055B).",
     "This amendment + IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md are operative; v0.4 prose bows to them on conflict.", "",
     "## Per-finding repairs", ""]
for f in led["findings"]:
    L.append("### %s [%s] -> %s" % (f["id"], f["severity"], dmap[f["id"]]["class"]))
    L.append("Finding: %s" % f["original_finding"])
    L.append("Repair: %s" % f["normative_repair"])
    L.append("Artifacts: %s" % ", ".join(f["new_or_modified_artifacts"]))
    L.append("Backward compat: %s" % f["backward_compatibility_effect"])
    L.append("Status: %s" % f["status"])
    L.append("")
(ROOT / "amendments" / "SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md").write_text("\n".join(L), encoding="utf-8")
print("amendment lines:", len(L))
