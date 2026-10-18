# SR-01 Credit-Law Falsification Record

Method: exact arithmetic on stored grounded edges (no sampling, no solver).
F1 (w=−1 low, 3 ledger + seeds): PASS. F2 (E4 w=−2 seed0 + ledger): PASS.
F3 (rank-jump seed13): PASS (C5-branch: 0 ≤ 1). F4 (shadow-mark seed21):
PASS. F5 (root-targeted, 1 stored violation): PASS. F6 (deep-targeted, 2
stored): PASS. F7 (zero-cost seeds): PASS. F8 (positive edges): PASS. F9
(source-realizable high): CONDITIONAL — no abstract (s,t) witness data
stored (contracted checks kept verdicts only). F10 (anomalous high):
CONDITIONAL (incl. −3 UNKNOWN). Refuted alternatives on the same rig:
C1(5), C5-alone(2×E4), C2-alone(2 killers), scalings, Q/parity/D/marked/
occupancy families, min(C2,C5) branch-switch (2×E4), joint-LP piecewise
(12/40). (`SR01_TARGETED_CASE_RESULTS.json`.)
