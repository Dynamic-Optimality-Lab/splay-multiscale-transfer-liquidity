# G03R Vertex-Identity Erratum

Confirmed defect: `canon_key` in `G03_GROUNDED_GRAPH_CHECK.py` sorted prefixed
names (`SLs_*` vs `SLt_*`), so equal abstract states under different namespaces
produced unequal vertex ids. Consequence: every edge ran source-vertex in the
`SLs_` namespace and destination in `SLt_`; no destination could ever equal a
source, so every directed cycle was unrepresentable and the old "no negative
cycle" verdict on 16V/9E was vacuous (bipartite by construction: 76 SCCs on the
same data under old keying, zero cross joins possible).

Repair (`G03R_CANONICAL_STATE.py`): 147-field namespace-free key derived from
`StateVars7` (`mu` + `BState` 115 + `alpha7` 21 + `sigma` 10); missing fields
raise; bools normalized; domains checked; `T-A1..T-A10` + validity all PASS
(`G03R_CANONICALIZATION_TESTS.json`). Rebuilt graph: 40 full-state edges, 76
vertices, 0 joined s-t vertices in the random sample (honest), 11/11 joins on
constructed 2-leg continuations (`G03R_CHAINED_WALKS.json`) — chaining works
iff endpoints genuinely coincide. Old verdict NOT overwritten; old graph
recomputed for comparison (`G03R_CYCLE_RESULTS.json`).
