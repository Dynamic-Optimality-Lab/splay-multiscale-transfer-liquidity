# G01_TYPED_GRAPH_SPEC.md — Phase B (Gates G01-04/G01-07)

Vertices: O (valid iff U_O) + M (valid iff U_M). Edges: OO (low, w in -4..4,
9 realized); OM (high, w = 6-q); MO (w = 0 only); MM FALSE (no transition).
Provenance: E_low/E_sm/E_mt from the certified product (S03 free-var audits
re-verified here); q range audited (G01_Q_WEIGHT_RANGE_RESULTS.json):
only w=-4 proved UNSAT; w=-3 UNKNOWN (timeout, recorded obstruction);
w in {-2..1} SAT or UNKNOWN (kept, never silently dropped); w in 2..6 from
marked q 0..4 (genuine domain correspondence, proved separately from the
relation's structural allowance). MM absence is by WQ design (no midpoint
binders link m to m).
