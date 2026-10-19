# CL-02A CPU Overlap Analysis

Duplicate OUTPUT FILES (base == S802 bytes) are not duplicate RUNS: one
seed-802 pairing execution, two filenames (copy). Counted once (49.1s).
S801 vs FULL: two executions of the same seed (30.9 + 33.0) — disjoint
process CPU, both counted (reruns consume afresh; no deduction). Builder
run 1 vs run 2: distinct seeds/runs, both counted (700 + 351.5). No
evidence of concurrent/overlapping wall-time double-counting within a
single cpu_s figure (each is one process's process-time). Verifier runs:
multiple (failed-path debugging + final) — small, estimated in aggregate.
CONCLUSION: measured CL-02 total ~1205s of DISJOINT process CPU (no
duplicate-run inflation beyond the documented copy).
