"""Read-only research inventory; write only inside this new audit directory.

The inventory is not a proof verification. Hashing, lexical indexing, semantic
reading, and independent witness replay are deliberately separate activities.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCAN = Path("\\\\?\\" + str(ROOT)) if os.name == "nt" else ROOT
EXCLUDED = {".git", ".lake", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}
DOC_EXT = {".md", ".rst", ".tex"}
CODE_EXT = {".py", ".lean", ".sh", ".ps1", ".js", ".ts"}
STATUS = re.compile(r"(?i)\b(proved|unproved|open|refuted|conditional|blocked|verdict|theorem|conclusion|not established|not proved|does not prove|remains)\b")
ROUTES = {
    "pair_access": re.compile(r"(?i)pair.access|MSTL?[- _]?(?:14|15|16|17|18|19|20)\b|8AC|keep.repayment"),
    "coarse_double": re.compile(r"(?i)coarse.double|universal.?CD|CD\([56]\)|CD[56]|internal.double|internal.neutral|neutral.double"),
    "final_reduction": re.compile(r"(?i)dynamic.optimal|eventual.monotonic|approximate.monotonic|Theorem.?4\.3|Levy.Tarjan"),
    "uniform_bridge": re.compile(r"(?i)uniform|source.fund|source.work|regeneration|inheritance|nested.path|packet|restoration"),
}


def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    inventory, documents, errors = [], [], []
    top_counts, top_bytes, extensions = Counter(), Counter(), Counter()
    branches = {}
    for directory, dirs, files in os.walk(SCAN):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and Path(directory, d) != Path("\\\\?\\" + str(HERE)))
        for name in sorted(files):
            path = Path(directory, name)
            relative = path.relative_to(SCAN).as_posix()
            try:
                stat = path.stat()
                digest = None
                hash_selected = path.suffix.lower() in DOC_EXT or path.suffix.lower() == ".sha256" or (
                    path.suffix.lower() in CODE_EXT and relative.startswith(("python/", "lean/", "scripts/"))
                )
                if hash_selected:
                    digest = hashlib.sha256()
                    with path.open("rb") as stream:
                        for data in iter(lambda: stream.read(4 * 1024 * 1024), b""):
                            digest.update(data)
                item = {"path": relative, "bytes": stat.st_size, "sha256": digest.hexdigest() if digest else None, "mtime_ns": stat.st_mtime_ns,
                        "hash_scope": "current_read" if digest else "metadata_only_raw_artifact_not_reread"}
                inventory.append(item)
                top = relative.split("/")[0] if "/" in relative else "(root)"
                top_counts[top] += 1
                top_bytes[top] += stat.st_size
                extensions[path.suffix.lower()] += 1
                if path.suffix.lower() not in DOC_EXT:
                    continue
                body = path.read_text(encoding="utf-8-sig", errors="replace")
                lines = body.splitlines()
                headings = [{"line": i, "text": line[:350]} for i, line in enumerate(lines, 1) if re.match(r"^#{1,6} ", line)]
                hits = [{"line": i, "text": line[:650]} for i, line in enumerate(lines, 1) if STATUS.search(line)]
                tags = [label for label, pattern in ROUTES.items() if pattern.search(body)]
                doc = {**item, "words": len(body.split()), "headings": headings, "status_mentions": hits, "route_tags": tags}
                documents.append(doc)
                parts = relative.split("/")
                branch = "/".join(parts[:2]) if len(parts) > 2 else parts[0]
                branch_item = branches.setdefault(branch, {"documents": [], "words": 0, "tags": Counter()})
                branch_item["documents"].append(relative)
                branch_item["words"] += doc["words"]
                branch_item["tags"].update(tags)
            except OSError as exc:
                errors.append({"path": relative, "error": str(exc)})
    for name, rows in [("corpus_inventory.jsonl", inventory), ("document_index.jsonl", documents)]:
        with (HERE / name).open("w", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    write_json("branch_index.json", branches)
    summary = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "root": str(ROOT),
        "excluded_directory_names": sorted(EXCLUDED), "excluded_audit_directory": str(HERE),
        "files_inventoried": len(inventory), "bytes_inventoried": sum(x["bytes"] for x in inventory),
        "files_sha256_hashed": sum(x["sha256"] is not None for x in inventory),
        "bytes_sha256_hashed": sum(x["bytes"] for x in inventory if x["sha256"] is not None),
        "hash_policy": "Hash all Markdown/rst/tex, .sha256 files and core source code under python/, lean/ and scripts/. Other artifacts receive metadata inventory only; selected additional semantic sources have separate agent-recorded hashes. Existing seals are indexed, not automatically revalidated.",
        "documents_lexically_indexed": len(documents), "document_words": sum(x["words"] for x in documents),
        "extensions": dict(extensions.most_common()),
        "top_directories": [{"path": k, "files": n, "bytes": top_bytes[k]} for k, n in top_counts.most_common()],
        "errors": errors,
        "coverage_caveat": "SHA256 inventory and lexical status mentions do not establish truth, currentness, proof dependencies, or independent witness verification. Generated data are not unpickled or executed. Canonical semantic reads are recorded separately."
    }
    write_json("inventory_summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in {"extensions", "top_directories"}}, indent=2))


if __name__ == "__main__":
    main()
