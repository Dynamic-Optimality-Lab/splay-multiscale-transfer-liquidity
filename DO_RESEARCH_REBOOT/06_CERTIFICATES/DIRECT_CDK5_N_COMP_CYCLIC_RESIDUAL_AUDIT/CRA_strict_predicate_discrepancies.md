# Strict-predicate discrepancy report (task H / CRA-E)

Compared per word over all 384: old screening-MSINK (min-first sink,
H≥2-proxy K, any-in-interval-DELETE P) vs new strict-MSINK (existential
sinks, d_A≥3 K, immediately-preceding-DELETE P with a≥1 both).

## Result: ZERO discrepancies.

Every old-MSINK-True word is strict-True; every old-MSINK-False word is
strict-False (`msink_discrepancy: 0/384`). The historical proxies never
diverged from the frozen predicates on this corpus. No counterexample, no
reclassification attributable to predicate strictness. CRA-E: no defect
found (reported as a negative result, not a skipped check).

Note: the old/new implementations agree because corpus positives either
carry d_A≥3 KEEPs or preceding-DELETE P structures wherever the proxies
fired; the IN-finalization narrow-H5 verification (strict-P on both
residual singletons) is consistent with this corpus-wide finding.
