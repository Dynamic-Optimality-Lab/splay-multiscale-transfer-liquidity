# S04_DAG_CAP_RECONCILIATION.md — F04-04/F04-05 (Gate A1 erratum)

Step-03 S03_SYMBOLIC_BUILDS recorded minpre_gt.growth = 4,129,230 genuinely
allocated nodes on the live 1.6M-node production DAG (peak ~5.73M > 4M cap).
The S03 G23 resource PASS is SUPERSEDED for eager monolithic MinPre
normalization (this additive erratum; Step-03 files untouched). Repair (exact,
in-architecture): lazy per-weight Pre normalization (measured growth 0 per
weight, 11 weights; peak-live 1,603,171/4,000,000 — S04_DAG_PEAK_RESULTS.json).
Lazy == eager by alpha-equivalence of per-disjunct privatization + the proved
finite-weight procedure equivalence. Compliant fresh execution recorded. The cap
reading used throughout: max-live hash-consed nodes per build (Step-01/02/04
ledgers consistent with it).
