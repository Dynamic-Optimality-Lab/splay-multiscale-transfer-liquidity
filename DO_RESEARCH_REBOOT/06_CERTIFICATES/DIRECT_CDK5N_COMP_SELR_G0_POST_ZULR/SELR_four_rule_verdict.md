# DIRECT-CDK5N-COMP-SELR-G0 four-rule verdict (independent Gate-0)

## R1 — STRICTLY SMALLER: PASS

W_IN (8cd970c7, n=31, A=53, Q=36, C_K=16) in S_SELR cap R*: strict member
(E={4}, t_e=0, U={0,4}, donor p=0 H=18/q=3/R=34; others strict K/P) and
outside C24* (744 rotation-domain decisions EXCLUDED from true starts;
primitive 31/31 recursive negative, 0 indeterminates; independent verifier
PASS). W_OUT (c3a55f13, n=30, A=52, Q=36, C_K=16, E={4,12}) in R* minus
S_SELR (H2 fails with two bare exceptions; 720 decisions EXCLUDED; 30/30
primitive recursive negative). Hence empty != (S_SELR cap R*) proper-subset
R*. Evidence: SELR_proper_subclass_certificate.md, SELR_rotation
matrices, SELR_IN/OUT_negative_certificate.json,
SELR_negative_verification.json (PASS, 22 checks).

## R2 — SOLVABILITY: PASS

L1–L9 (SELR_L1_L9_universal_payment.md) proves Q<=2A over H1–H5: partition,
H>=c baseline, core-nine w in {1,2}, exception untyped via H=1 (K needs
H>=2, P needs a>=1 both), joint w_e+w_p=2<=R_p with q_p=3/H_p>=2 donor
(including sharp H=2 equality 2=2; q=4 donors correctly excluded),
predicates-first strict K/P elsewhere, disjoint pair+singletons,
telescoping (IN 4<=74). H3 relay classifies only. No aggregate premise, no
circularity. Evidence: L-doc + sharp-case audit + adversarial 36–55.

## R3 — ONE PROMPT: PASS

One theorem (SHA a36eccac… pinned before screening), one mechanism
(w_e+w_p<=R_p pair), one IN, seven seeds, one DELETE-only grammar, one
canonical order, one budget (60k/seed, 300k total, coded + untriggered),
one bank24, one Gate-0, one OUT (first-eligible: selr-in d1 rm18, 8
registered/8 screened/0 beyond-OUT, 0 indeterminate, 0 truncated, no L2).
Streaming generate->register->screen->decide verified by ordering fault
injection (log ops == generator prefix). No mutation/discovery/resume.
Evidence: SELR_search.py, screened log (8 entries), counters, distance-zero
audit (7/7 SHA, IN + 6 banked), adversarial 74–85.

## R4 — UPWARD PROGRESS: PASS

W_IN outside C24* (24 = 3+9+12 incl. MSINK/DLSS/UESINK/ZULR at every level;
SELR excluded): 744 direct + full recursive closure + 19-case oracle +
384-word regression (378+6, 0 residual) + 90-audit. BEFORE (IN residual) /
RESULT (universal paired payment, IN member) / AFTER (IN covered, OUT
residual-outside-SELR) per advancement audit. Mechanism independently
specified; H=2 sharpness symbolic only (no witnessed family claimed).

## Verdict

R1 PASS, R2 PASS, R3 PASS, R4 PASS.

**CDK5NSELR-G0-A — FOUR-RULE GATE 0 APPROVED (Gate 0 only; no promotion).**
Complement, K>=6, universal Coarse-Double, Dynamic Optimality remain OPEN.
