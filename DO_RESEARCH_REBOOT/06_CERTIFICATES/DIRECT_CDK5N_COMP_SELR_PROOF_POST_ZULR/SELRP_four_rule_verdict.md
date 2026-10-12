# DIRECT-CDK5N-COMP-SELR-PROOF final four-rule verdict (independent)

## R1 — STRICTLY SMALLER: PASS

W_IN 8cd970c7 ∈ S_SELR ∩ R_5,9^(24): source-valid, five keys, core-nine,
closed, E={4}, relay t=0, U={0,4}, donor p=0 (H=18,q=3), others strict
K/P; outside C24* (744 rotation exclusions from true starts; primitive
31/31 UNCOVERED by two independent rotation-aware engines; 0 unknowns).
W_OUT c3a55f13 ∈ R_5,9^(24) ∖ S_SELR: valid backbone (five keys,
core-nine, closure, 30/30 primitive); E={4,12} fails H2; 720 exclusions;
UNCOVERED. First-eligible rm18 provenance reconstructed. Hence
∅ ≠ (S_SELR ∩ R_5,9^(24)) ⊊ R_5,9^(24). Evidence: replay JSONs, primitivity
certs, rotation matrices, rich negative certs, 22-check verifier PASS,
cross-validation 15/15, adversarial A/B/D/E classes.

## R2 — SOLVABILITY: PASS

L1–L10 fixture-independent proof over H1–H5: partition; H≥c baseline;
core-nine w∈{1,2}; exception untyped via H=1; joint w_e+w_p=2≤R_p with
q=3/H≥2 donor (sharp H=2 equality 2=2; q=4/H=2 correctly excluded since
3>2); predicates-first strict K/P elsewhere; disjoint pair+singletons
(overlap counted once; relay pays nothing); telescoping with corrected IN
accounting 4≤74 ⇒ 36≤106; L10 scope/redundancy/noncircularity audit. No
aggregate premise, no finite witness as premise, no generalization.
Evidence: L-doc, sharp content, adversarial C-class (20).

## R3 — ONE PROMPT: PASS

Unchanged theorem (SHA a36eccac…), mechanism, IN, OUT; historical search
audited not rerun (7 seeds SHA-verified; first-eight reconstructed:
non-closed/non-closed/S1-banked/AMG+UESINK-banked/SELR-member/
non-closed/non-closed/rm18-OUT; 8/8/8/8, 0 INDET, 0 truncated, no L2,
single run, ordering fault-verified); no mutation/resume/successor;
deviations: none found (Gate-0 streaming complied). Evidence: provenance
audit, log, counters, sensitivity record, adversarial E-class.

## R4 — UPWARD PROGRESS: PASS

W_IN outside C24* (24 = 3+9+12 incl. MSINK/DLSS/UESINK/ZULR at every
level; SELR excluded): 1,464 per-entry-verified rotation decisions;
primitive UNCOVERED by repaired rotation-aware checker + independent DFS
checker (15/15 agree); unknown/cap paths proven INDETERMINATE (forced
injections); corpus 384 unchanged (378+6, 0 residual); 27-case oracle.
BEFORE/RESULT/AFTER advancement holds (paired unit-debt class removed
from residual; H=2 symbolic only). No witness-status change from the
rotation repair (old-vs-new agreement experiment).

## Verdict

R1 PASS, R2 PASS, R3 PASS, R4 PASS — promotion of CDK5NSELR-A authorized.
Complement, K≥6, universal Coarse-Double, Dynamic Optimality remain OPEN.
