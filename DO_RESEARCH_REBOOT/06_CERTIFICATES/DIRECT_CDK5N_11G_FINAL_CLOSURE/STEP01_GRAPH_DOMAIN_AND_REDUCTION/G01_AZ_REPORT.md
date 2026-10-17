# G01_AZ_REPORT.md — anti-fabrication record

- OM verdicts are per-weight measured (SAT/UNSAT/timeout), not uniform: w=-4
  UNSAT-certified; w=-3 UNKNOWN (recorded obstruction, not PASS-by-absence);
  w in {-2..1} SAT (retained, never silently dropped); w in 2..6 SAT with marked q.
  Timeouts vary run to run (resource fact, reported both runs).
- Contraction code found a harness bug (cross-DAG id use) before any claim; fixed
  and re-evidenced. Insignificant-looking None-verdicts (Tier-1 open formulas)
  are recorded as procedure-deferrals with the exact decision path named.
- No sampled nonnegativity: G_star = full graph; sectors partition without
  excluding. No terminal inequality claimed. Reproduction: the six Step-01
  runners from repo root (~25 min, ~2.5 GiB, fixed seeds).
