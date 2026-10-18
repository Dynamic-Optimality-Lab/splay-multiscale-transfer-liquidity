# G02_AZ_REPORT.md — anti-fabrication record

- OM verdicts re-measured fresh (not copied): w=-4 UNSAT twice; w=-3 UNKNOWN at
  60/120/240s (documented obstruction, never claimed absent); SAT weights
  re-verified with witness extraction. Flaky boundary verdicts reported as such.
- A Step-04 file was briefly touched then restored byte-identical (verified via
  git status); a Step-02-boundary edit attempt was reverted in favor of the
  additive Step-03 file. No history modified.
- The cycle search is bounded and says so: k=1 theorem, k=2 exhaustive, BFS
  truncated=>UNKNOWN, 80 survivors all replay-verified. Zero candidates were
  upgraded to verdicts without verification.
- No potential candidate endorsed; no universal claim made; one N5-style
  over-strong negative was caught and replaced during construction (documented
  in Step-03 AZ; same discipline applied here).
- Reproduction: six Step-02 runners from repo root (~25 min, ~2.5 GiB).
