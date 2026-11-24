"""Build a navigation graph, never an automatically certified proof DAG.

Document nodes and folder edges cover the full Markdown index. Semantic
claim edges come only from the separately recorded route-source reviews.
Core-code AST edges are software structure, not mathematical implications.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

# Graphify initializes its AST cache at import time. Set the audit-local cwd
# before importing it so regeneration never writes a cache into the old tree.
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "graphify-out"
os.chdir(HERE)

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.benchmark import print_benchmark, run_benchmark
from graphify.build import build_from_json
from graphify.cache import save_semantic_cache
from graphify.cluster import cluster, score_all
from graphify.detect import save_manifest
from graphify.export import to_html, to_json
from graphify.extract import extract
from graphify.report import generate

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def identity(prefix, value):
    return prefix + hashlib.sha256(value.encode()).hexdigest()[:18]


def main():
    os.chdir(HERE)
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(exist_ok=True)
    nodes, edges, hyperedges = {}, [], []
    documents = [json.loads(line) for line in (HERE / "document_index.jsonl").read_text(encoding="utf-8").splitlines()]
    for doc in documents:
        path = doc["path"]
        node_id = identity("doc_", path)
        title = doc["headings"][0]["text"].lstrip("# ") if doc["headings"] else Path(path).stem
        nodes[node_id] = {"id": node_id, "label": title[:110], "file_type": "document", "source_file": path,
                          "source_location": "L1", "review_level": "lexical_index_only_unless_listed_in_findings", "words": doc["words"]}
        parts = path.split("/")
        branch = "/".join(parts[:2]) if len(parts) > 2 else parts[0] if len(parts) > 1 else "(root)"
        parent_id = identity("branch_", branch)
        nodes.setdefault(parent_id, {"id": parent_id, "label": branch.split("/")[-1], "file_type": "document",
                                     "source_file": branch, "source_location": None, "review_level": "directory_structure"})
        edges.append({"source": parent_id, "target": node_id, "relation": "contains_document", "confidence": "EXTRACTED",
                      "confidence_score": 1.0, "source_file": path, "source_location": "filesystem path", "weight": 1.0})

    semantic_files = sorted(f for f in HERE.glob("*_graph.json") if f.name != "route_graph.json")
    semantic_names = []
    for file in semantic_files:
        fragment = read_json(file)
        semantic_names.append(file.name)
        id_map = {n["id"]: file.stem + "::" + n["id"] for n in fragment.get("nodes", [])}
        for node in fragment.get("nodes", []):
            node = {**node, "id": id_map[node["id"]]}
            if node["id"] in nodes and nodes[node["id"]] != node:
                raise ValueError("Conflicting semantic node identity: " + node["id"])
            nodes[node["id"]] = node
            source = node.get("source_file", "").replace("\\", "/")
            document_id = identity("doc_", source)
            if document_id in nodes:
                edges.append({"source": document_id, "target": node["id"], "relation": "documents_concept",
                              "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": source,
                              "source_location": node.get("source_location"), "weight": 1.0})
        edges.extend({**edge, "source": id_map[edge["source"]], "target": id_map[edge["target"]]} for edge in fragment.get("edges", []))
        hyperedges.extend({**h, "id": file.stem + "::" + h["id"], "nodes": [id_map[n] for n in h["nodes"]]} for h in fragment.get("hyperedges", []))

    # Deliberately limited AST selection; the 3,495-source-file inventory is not
    # advertised as a complete software-semantic or Lean proof audit.
    core = [ROOT / p for p in ["python/independent/splay.py", "python/independent/pair.py",
                               "python/liquidity/legacy_embedding.py", "lean/WP6/SplayRotate.lean",
                               "lean/WP6/GCStaticKeep2Step.lean"]]
    ast = extract(core)
    for node in ast.get("nodes", []):
        node["review_level"] = "core_ast_only_not_formal_certification"
        nodes.setdefault(node["id"], node)
    for edge in ast.get("edges", []):
        if edge.get("confidence") == "EXTRACTED":
            edge["confidence_score"] = 1.0
        edges.append(edge)
    for edge in edges:
        if "confidence_score" not in edge:
            raise ValueError("Missing provenance score")
        if edge.get("confidence") == "EXTRACTED" and edge["confidence_score"] != 1.0:
            raise ValueError("Extracted edge must have score 1")
        if edge["source"] not in nodes or edge["target"] not in nodes:
            raise ValueError("Dangling graph endpoint")
    extraction = {"nodes": list(nodes.values()), "edges": edges, "hyperedges": hyperedges,
                  "input_tokens": 0, "output_tokens": 0,
                  "token_accounting": "Unavailable; zeros are schema placeholders, not measured cost."}
    (HERE / "route_graph.json").write_text(json.dumps(extraction, ensure_ascii=False, indent=2), encoding="utf-8")
    graph = build_from_json(extraction)
    communities = cluster(graph)
    cohesion = score_all(graph, communities)
    labels = {}
    for cid, members in communities.items():
        labels_in_group = [str(graph.nodes[n].get("source_file", "")) for n in members]
        counts = Counter()
        for source in labels_in_group:
            parts = source.replace("\\", "/").split("/")
            counts[parts[1] if len(parts) > 1 and parts[0] == "DO_RESEARCH_REBOOT" else parts[0]] += 1
        prominent = counts.most_common(1)[0][0] if counts else "Proof route"
        # Short names stay descriptive rather than presenting generic centrality
        # as proof importance.
        mapping = {"06_CERTIFICATES": "Historical scoped certificates", "EXP04_UNIVERSAL_RESIDUAL_CONSERVATION": "Current residual conservation",
                   "M3_XFER21": "Frozen graph conservation", "CD5_BASE01": "Five support base",
                   "SE03_STEP2_CD6_FINAL_ASSEMBLY_14": "Six support assembly", "audits": "Original route audits",
                   "v03": "Original Pair Access", "math": "Registered proof obligations"}
        if prominent in mapping:
            label = mapping[prominent]
        elif prominent.startswith("M3_XFER"):
            label = "Frozen graph transfer " + prominent.removeprefix("M3_XFER")
        elif prominent.startswith("M3_"):
            label = "Frozen graph source studies"
        elif prominent.startswith("SE03_"):
            label = "Source funding and closure"
        elif prominent.startswith("EXP"):
            label = "Physical residual discovery"
        elif prominent.startswith(("PARALLEL", "ROUTE")):
            label = "Alternative aggregate routes"
        elif prominent.startswith("SHARP"):
            label = "Sharp coefficient conservation"
        elif prominent in {"scripts", "python", "lean"}:
            label = "Core mechanics and arithmetic"
        elif prominent.startswith("0"):
            label = "Historical proof route records"
        else:
            label = "Research sources and dependencies"
        labels[cid] = label
    gods = god_nodes(graph)
    surprises = surprising_connections(graph, communities)
    questions = suggest_questions(graph, communities, labels)
    detection = read_json(HERE / ".graphify_detect_full.json")
    tokens = {"input": 0, "output": 0}
    report = generate(graph, communities, cohesion, labels, gods, surprises, detection, tokens, str(ROOT), suggested_questions=questions)
    caution = (
        "# Navigation scope and verification limits\n\n"
        "This is a repository navigation graph, not a certified proof DAG. All Markdown files receive lexical document nodes; "
        "folder membership is exact filesystem structure. Semantic edges are limited to the listed source reviews. "
        "EXTRACTED means explicitly documented, not independently proved. AST edges describe five selected core sources. "
        "Raw witness files were inventoried, not replayed. Community centrality and suggested connections do not establish mathematical dependencies.\n\n"
        "Token cost: unavailable; numeric zero fields are schema placeholders. No cost or compression measurement of this agent session is claimed.\n\n"
        "Semantic fragments: " + ", ".join(semantic_names) + ".\n\n"
    )
    confidence_counts = Counter(data.get("confidence", "UNSPECIFIED") for _, _, data in graph.edges(data=True))
    caution += "Exact edge provenance counts: " + ", ".join(f"{key}={count}" for key, count in sorted(confidence_counts.items())) + ". Percentages below are rounded.\n\n"
    (OUT / "GRAPH_REPORT.md").write_text(caution + report, encoding="utf-8")
    to_json(graph, communities, str(OUT / "graph.json"))
    if graph.number_of_nodes() <= 5000:
        to_html(graph, communities, str(OUT / "graph.html"), community_labels=labels)
    else:
        print("WARNING: graph exceeds 5,000 nodes; full HTML not generated.")
    analysis = {"communities": {str(k): v for k, v in communities.items()}, "cohesion": cohesion, "labels": labels,
                "god_nodes": gods, "surprising_connections": surprises, "suggested_questions": questions,
                "semantic_fragments": semantic_names}
    (OUT / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    # Cache into this audit directory only, keeping all old research read-only.
    sem_nodes = [n for f in semantic_files for n in read_json(f).get("nodes", [])]
    sem_edges = [e for f in semantic_files for e in read_json(f).get("edges", [])]
    sem_hypers = [h for f in semantic_files for h in read_json(f).get("hyperedges", [])]
    for row in sem_nodes + sem_edges + sem_hypers:
        source = row.get("source_file", "")
        if source and not Path(source).is_absolute():
            original = ROOT / source
            row["source_file"] = "\\\\?\\" + str(original) if os.name == "nt" else str(original)
    save_semantic_cache(sem_nodes, sem_edges, sem_hypers, root=HERE)
    save_manifest(detection["files"], manifest_path=str(OUT / "manifest.json"))
    (OUT / "cost.json").write_text(json.dumps({"input_tokens": None, "output_tokens": None, "reason": "Agent token measurements unavailable"}), encoding="utf-8")
    print(json.dumps({"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(), "communities": len(communities),
                      "semantic_fragments": semantic_names, "html": graph.number_of_nodes() <= 5000}))
    benchmark = run_benchmark(str(OUT / "graph.json"), corpus_words=sum(d["words"] for d in documents), questions=[
        "relaxed Universal Coarse Double Dynamic Optimality",
        "CD(6) uniform support transfer",
        "MSTL-14 integrability Pair Access",
        "internal neutral first-hit collision",
        "PF PM residual original A work",
    ])
    benchmark["interpretation"] = "Estimated graph-navigation footprint only; not actual agent token cost, proof completeness, or answer-quality measurement."
    (OUT / "navigation_benchmark.json").write_text(json.dumps(benchmark, indent=2), encoding="utf-8")
    print_benchmark(benchmark)


if __name__ == "__main__":
    main()
