# G01_SOURCE_COVERAGE_THEOREM.md — G_star freeze + coverage (Phase G/G01-18)

FREEZE: G_star = G_AF (full certified two-sort graph; safe default per spec).
Coverage is then trivially complete: C_11F ⊆ C_star since every Stage 11F image
edge is a G_AF edge by construction (U1-U16 simulation builds abstract vertices
and edges of G_AF directly; the composed 2-chain demo exhibits chained
containment). Reachability restriction: NONE used (no fixture-initial-state
filter), so no reachability-coverage proof is owed. Any future smaller region
requires a new coverage proof and is not authorized here (no reactive narrowing
after Step 01). Spurious-cycle taxonomy (A-D) preserved for Step 02; TYPE B/C/D
cycles never refute the original theorem, and a negative cycle inside G_star
would refute only the Step-04 premise (to be proved), never silently dismissed.
