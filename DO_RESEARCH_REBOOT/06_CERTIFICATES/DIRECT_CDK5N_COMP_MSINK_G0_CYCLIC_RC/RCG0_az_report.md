# RCG0 AZ report

- Entry `3332362` verified (branch/remote/hashes/status); prior dirs intact.
- Frozen witnesses replayed fresh (pointer+tuple lockstep): IN-new 64/36/16,
  OUT 55/36/16; SHAs gated; normal + -O runs PASS.
- Strict MSINK: IN member (E=[4,12], t=(0,2), sinks=[0], strict-P other);
  OUT nonmember (mixed [2,2]).
- 20-mechanism battery: IN/OUT all-negative; NP/S1/S2/VR/MR depth-0 exact;
  RT2/CDK4/CDK5L/AJ-AS positive paths verified.
- Recursive C*: old-IN covered depth≤1, CONCAT covered, IN-new + OUT uncovered
  (complete DAGs, 0 budget hits, termination by length decrease).
- Oracle 19/19 (incl. mandatory depth-two nested case).
- L1–L7 reconstructed + computationally verified on IN-new.
- 50 adversarial attacks all PASS; R1–R4 PASS; OUTCOME A (Gate-0 only).
- No promotion, no mutation, no search, no successor. Remaining frontier OPEN.
