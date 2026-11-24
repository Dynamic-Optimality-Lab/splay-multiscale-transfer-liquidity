# Dynamic Optimality route audit — technical index

The new strategic assessment is saved in [Notion](https://app.notion.com/p/41e6251839be81f7ad04c7bd9ae62f03). This directory holds its reproducible source indexes and review metadata, not a new universal proof.

- `inventory_summary.json` describes coverage and exclusions; `corpus_inventory.jsonl` inventories every research file. Larger raw artifacts have metadata coverage, not fresh hashes or replay.
- `document_index.jsonl`, `all_markdown_frontiers.jsonl`, and `branch_index.json` index all 3,351 Markdown manuscripts. Status-word matches are search aids, not truth classifications.
- Six `*_findings.json` files record the route reviews, exact evidence lines, full-versus-section reading, theorem scopes, corrections, and verification limits. The semantic assignments contain 134 distinct anchors plus additional recorded reads.
- Six `*_graph.json` fragments preserve explicit versus inferred source relationships. `route_graph.json` adds document/folder navigation and limited core-code AST structure.
- [Interactive source graph](graphify-out/graph.html), [graph report](graphify-out/GRAPH_REPORT.md), and `graphify-out/graph.json` provide navigation. Folder centrality and EXTRACTED provenance do not certify mathematical dependencies or theorem validity.
- `graphify-out/navigation_benchmark.json` estimates graph-retrieval footprint for five research questions. It does not measure this session's token cost, prove coverage, or validate answers. Actual agent token measurements are unavailable.
- `index_corpus.py` and `build_route_graph.py` regenerate the indexes within this directory. They are read-only with respect to original source files. Build/dependency caches and this audit directory are excluded from the source census.

No new splay-source experiments, solver campaigns, witness replays, or Lean proof builds were performed. The report distinguishes conditional reductions from open universal hypotheses. Existing research and tracked Git content were preserved.
