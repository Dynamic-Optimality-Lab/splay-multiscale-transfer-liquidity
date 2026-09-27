import hashlib
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "v03" / "history"
rows = []
for p in sorted(base.rglob("*")):
    if p.is_file():
        rel = p.relative_to(base).as_posix()
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        rows.append({"path": rel, "sha256": h, "bytes": p.stat().st_size})
man = {"tree_commit": "895889169772087e391e84c33228648c84684e1e",
       "role": "architecture_navigation_commit tree (HEAD; closure/seal commits verified present in clone)",
       "files": len(rows), "total_bytes": sum(r["bytes"] for r in rows),
       "entries": rows}
with open(ROOT / "v03" / "byte_manifest.sha256.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(man, f, sort_keys=False)
print("WP-0 STEP manifest: files=%d bytes=%d" % (len(rows), man["total_bytes"]))
key = {}
for rel in ["prereg/transfer_grammar_v0.3.yaml", "prereg/event_ontology_v0.3.yaml"]:
    key[rel] = hashlib.sha256((base / rel).read_bytes()).hexdigest()
print("WP-0 STEP key hashes done")
with open(ROOT / "v03" / "key_content_hashes.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(key, f, sort_keys=False)
