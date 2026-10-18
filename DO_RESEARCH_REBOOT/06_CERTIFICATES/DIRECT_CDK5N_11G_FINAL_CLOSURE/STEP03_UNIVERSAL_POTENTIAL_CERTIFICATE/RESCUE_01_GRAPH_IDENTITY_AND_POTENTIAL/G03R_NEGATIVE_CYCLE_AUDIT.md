# G03R Negative-Cycle Audit

Independent Bellman-Ford (super-source, exact ints) + Tarjan SCC on: (1)
historical prefix-keyed graph, (2) corrected 9-edge-equivalent, (3) expanded
40-edge full-state graph: all `has_negative_cycle = False`; 76 singleton SCCs;
4 negative edges all cross-SCC (`G03R_CYCLE_RESULTS.json`, `G03R_SCC_RESULTS.json`).
(4) Contracted-high subgraph: no concrete-endpoint edges in the full-state
ledger (tier-2 SAT evidence referenced, never forged) — obligation retained.
Controls: BF verified on +/- synthetic graphs with exact cycle closure+total.
Scope: finite witnessed subgraph only. No universal claim.
