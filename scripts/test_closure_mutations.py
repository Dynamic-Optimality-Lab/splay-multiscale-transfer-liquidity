"""False-closure attacks: each mutation must make check_contract_closure.py fail."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
CHECK = [PY, str(ROOT / "scripts" / "check_contract_closure.py")]

def run():
    r = subprocess.run(CHECK, capture_output=True, text=True, cwd=str(ROOT))
    return r.returncode

MUTS = {
    "drop-CC-mapping": ("amendments/SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md", "CC-033", "CC-XXX"),
    "alter-parent-SHA": ("planning/PARENT_PROVENANCE_MATRIX.yaml", ARCH_C := "9859e654b76ba92c1d0e0809f62a7ffe1cac3b98", "0" * 40),
    "alter-legal-domain": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "presence NOT required", "presence required"),
    "open-P-space": ("prereg/predicate_family_v0.4.1.yaml", "closed: true", "closed: false"),
    "remove-replay-order": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "T7 \u2192 T5_{P,rho}", "T7 then something"),
    "rho-inspects-need": ("prereg/liquidity_axis.yaml", "would_otherwise_fail", "need_amount"),
    "expose-H4L-seed": ("prereg/h4l_holdout.yaml", "NEVER committed pre-reveal", "committed to git-lfs pre-reveal"),
    "drop-theorem-node": ("prereg/theorem_gate_matrix.yaml", "MST0-21", "MST0-2X"),
    "drop-control": ("planning/PARENT_CONTROL_DISPOSITION.yaml", "INV-070", "INV-07X"),
    "reject-is-refuted": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "REJECT (package rejected, truth stays UNPROVED) != REFUTED", "REJECT means REFUTED"),
    "mutate-C-same-ID": ("schemas/candidate.schema.json", "rule_family_id", "rule_family_xx"),
    "dirty-tree": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "porcelain", "porcelax"),
    "omit-bridge": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "BLOCKED_BY_SOURCE", "BLOCKED_BY_SOURCX"),
    "remove-shard-rule": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "per-shard", "per-shaXD"),
    "inplace-axis": ("IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md", "backward embedding", "backward embezzling"),
    "drop-theorem-file": ("MATHFILE:math/theorems/MSTL-09.md", None, None),
}

fails = []
base = run()
print("baseline returncode:", base)
assert base == 0, "baseline must PASS before mutation attacks"
for name, (rel, old, new) in MUTS.items():
    if rel.startswith("MATHFILE:"):
        p = ROOT / rel.split(":", 1)[1]
        backup = p.read_bytes()
        p.unlink()
        restore = lambda p=p, backup=backup: p.write_bytes(backup)
    else:
        p = ROOT / rel
        backup = p.read_bytes()
        data = backup.decode("utf-8")
        assert old in data, (name, "pattern missing")
        p.write_text(data.replace(old, new, 1), encoding="utf-8")
        restore = lambda p=p, backup=backup: p.write_bytes(backup)
    try:
        rc = run()
        ok = rc != 0
        print(("KILLED " if ok else "SURVIVED ") + name)
        if not ok:
            fails.append(name)
    finally:
        restore()
final = run()
print("restored returncode:", final)
if fails or final != 0:
    print("MUTATION_RESULT = FAIL", fails)
    sys.exit(1)
print("MUTATION_RESULT = ALL_16_KILLED")
