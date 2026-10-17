# S03_RESOURCE_RECONCILIATION.md — Gate G03 ledger erratum (additive, history preserved)

## Discrepancy
Campaign ledger Step-02 entries: 0.10 + 0.50 + 0.20 + 0.07 = 0.87 h, but
`used_step02` reads 0.4 h.

## Finding
The four entries are overlapping phase estimates (implementation-probes wall time
overlaps entry-audit, evidence-runs, and verification windows; all single-threaded
wall ≈ CPU). The 0.4 value is not derivable from the parts. Primary logs
(S02_SOLVER_PROFILING.json solver CPU + per-case cpu_s + runner wall times) support
measured execution ≈ 0.2-0.3 h; the 0.87 sum is a valid conservative UPPER bound.

## Resolution (conservative, no allocation expansion)
Carry Step-02 actual as 0.87 h (component sum). Cumulative: 1.0 (Step 01) + 0.87
(Step 02) = 1.87 h against the 12 h cap. Remaining: Steps 03 (1.5) + 04 (0.7) +
reserve (1.8) = 4.0 h; total accounted 5.87 h ≤ 12 h. No budget increase; the
historical ledger file is preserved unmodified (correction appended additively
in the campaign ledger by this step).
