# PIVOT-26AM gate: two-splay signed repayment — OUTCOME B

- A. Mechanism: 26AM-L1 is a direct corollary of 26AL-L1 (apply twice); no new
  displacement mechanism beyond 26AL. G/S are four-slot generalizations of 26AL-G/S.
- B. Generalization hierarchy: C_S ⊆ C_G proved; both subsume single-slot 26AL
  walks with r at i+1/i+2 as degenerate cases (no new coverage claimed from this).
- C. Strict novelty: GENUINE new coverage requires a walk whose ONLY positive is
  the S-quad (excluded from 26AJ/26AK/26AL-G by single-positive + r-at-i+3) —
  NOT found.
- D. Disjointness: proved for m≥4; m<4 vacuous (distinctness hypothesis
  unsatisfiable ⟹ sum ≤ 0 trivially). No J4/ROW/J-SELF/DTQ/UG used.
- E. Hunt: one script, 3758 histories (≤100000), 12 quad-BFS, 0 closures — negative.
- F. Non-refutation: hunt failure does not refute the walk form (§22).
- G. Realizability: algebraic ✓; joint local-state plausible unproved; closure ✗.
- H. Rule-4 promotion: NO — no certified witness, no strict-coverage argument.
- I. Multi-splay delays / deficits beyond capacity / indirect repayment: still OPEN.
- J. Budget compliance: single search script + no verifier-needed; histories within cap.
- K. Files: `02_PROVED/26AM_two_splay_signed_repayment.md` (G/S/L1 theorems only);
  `06_CERTIFICATES/26AM_two_splay_displacement_audit.md`; hunt script + log in
  `06_CERTIFICATES/26AM/`.
- L. VERDICT — **OUTCOME B**: 26AM-G AND 26AM-S PROVED as universal theorems;
  NO NEW closed-walk coverage; RULE 4: NO. Do NOT launch 26AN automatically.
