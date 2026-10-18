# G03R Graph-Chaining Theorem (finite witnessed scope)

Let `K(s)` be the repaired 147-field canonical key. For ssertify-certified
single-KEEP edges `e1=(A,B,M,x)->(A1,B1)`, `e2=(A1,B1,M,y)->(A2,B2)` replayed
through identical concrete post-state serials, `K(t(e1)) = K(s(e2))`
(`T-A7` PASS; 11/11 empirical joins). Hence repaired-key chaining is sound:
joined vertices denote abstract-state equality, and any closed walk found in
the witnessed multigraph is a genuine abstract closed walk with exact signed
total. Converse: absence of closed walks in the 40-edge sample (0 joined
vertices; `G03R_RETURN_PATH_RESULTS.json: all_closed_walks_len_le4 = []`)
is evidence ONLY for the finite sample, never promoted to `NonNegCycles(G*)`.
Parallel edges with distinct weights/provenance preserved; 4 negative edges
(all cross-SCC) retained with full endpoint states.
