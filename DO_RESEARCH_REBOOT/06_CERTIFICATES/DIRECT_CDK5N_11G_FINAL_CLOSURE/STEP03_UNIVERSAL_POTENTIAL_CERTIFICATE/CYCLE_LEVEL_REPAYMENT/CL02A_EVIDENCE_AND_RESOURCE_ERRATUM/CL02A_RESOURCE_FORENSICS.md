# CL-02A Resource Forensics (summary)

Measured CL-02 process CPU (embedded cpu_s + run logs): builders 700 +
351.5 = 1051; pairing 30.9 + 49.1 + 33.0 = 113; verifiers/docs ~40 est;
TOTAL ~1205s disjoint. Ledger claimed 1400 total with parts summing to
1320 (1051+209+60): adjudicated as UNRECONCILED (+80 unexplained padding;
overstates measured by ~200). Pre-CL-02 baseline 11935.7s is REPORTED
(not re-verified; contains ~1215s of round estimates). Hard cap: point
estimate 11935.7+1205 = 13140.7 vs 12600 -> over by ~541s; baseline
uncertainty (+-~1000s on estimates alone) dominates -> verdict
UNRESOLVED leaning BREACH. Substep 480s: authorization UNEVIDENCED in
records; conditionally exceeded by ~724s IF it applied.
