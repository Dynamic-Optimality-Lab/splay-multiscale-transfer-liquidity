# DIRECT-CDK5N-COMP-ZULR-PROOF four-rule verdict (proof stage, independent)

## R1 — STRICTLY SMALLER: PASS

W_IN (593b3f3a, n=32, A=56, Q=36, C_K=16) in S_ZULR cap R*: strict member
(E=[], U={0} with H_0=18>=2, positives {0,4,8,12} others strict-K/P) and
outside C23* (23/23 rotation-domain negatives over 32 rotations = 736
EXCLUDED; primitive 32/32 recursive negative; 0 indeterminates; two engines
agree). W_OUT (8cd970c7, n=31, A=53, Q=36, C_K=16, E=[4]) in R* minus S_ZULR
(H2 fails; 23/23 negatives over 31 rotations = 713 EXCLUDED; 31/31 primitive).
Hence empty != (S_ZULR cap R*) proper-subset R*. Evidence:
ZULRP_proper_subclass_proof.md, ZULRP_strict_novelty_proof.md,
ZULRP_rotation_matrices.json, ZULRP_IN/OUT_negative_recursive_certificate.json,
ZULRP_negative_certificate_verification.json (PASS), adversarial-90 attacks
20-22, 26, 61, 65-66.

## R2 — SOLVABILITY: PASS

L1-L9 (ZULRP_L1_L9_universal_proof.md) proves Q<=2A for every H1-H5 walk:
partition identities; H>=c baseline; core-nine q<=4 so w>0 implies w in {1,2};
E-empty classification with explicit q=4/H=1 caveat; unique payer
R_p=2(H_p-1)>=2>=w_p including sharp q=4/H=2 equality 2=2; strict-K/P others
via predicates-first H>=2; per-interval payment (no sink, no transfer, no
double-spend); telescoping. No aggregate premise, no circularity (L8/L9
audits). Evidence: L1-L9 doc + supporting notes (cyclic_interval,
A_root_baseline, nine_core_debt_bound, exception_payer_strictKP,
strict_type_K_P, no_double_spend, recursive_soundness/completeness);
adversarial-90 attacks 36-55; IN corroboration 4<=80.

## R3 — ONE PROMPT: PASS

One theorem (H1-H6 frozen, SHA e39e8447...), one mechanism (unique local
self-payer), one IN, one OUT, one bank23, one provenance audit, one
certification campaign, one conditional promotion. No discovery/mutation/
successor: OUT = frozen rm7 residual (441 raw -> 425 distinct, first-five
rm0/rm1/rm2/rm5/rm7 decided non-closed/non-closed/NP-banked/ZULR-member/
OUT-HOPEFUL, first-eligible idx4). Deviations adjudicated without operative
effect: pre-generated parent list = identity registration, not screening
(erratum B); SHA-dedup reproduces exact-canonical order byte-identically
(erratum C); budget guards untriggered/0 hits (erratum D); manifest prose
count corrected 441/425 (erratum B). Evidence: ZULRP_provenance_audit.json,
ZULRP_provenance_reverification.json, ZULRP_search_provenance_audit.md,
ZULRP_gate0_metadata_errata.md (B/C/D), adversarial-90 attacks 74-85.

## R4 — UPWARD PROGRESS: PASS

W_IN outside C23* (bank23 = 3+8+12 = 23, UESINK included, ZULR excluded):
complete rotation matrices (736 IN + 713 OUT = 1449 EXCLUDED), full recursive
closure with every legitimate rotation/proper pair-closed segment/nested
partition from actual reachable starts, exact (start,canon) memoization,
budget/INDETERMINATE paths exercised with 0 hits, 18/18 cross-validation,
19/19 oracle, 384-word corpus regression (378 direct + 6 cyclic, 0 residual,
0 indeterminate). Evidence: ZULRP_independent_recursive_checker.py,
ZULRP_negative_certs.py, rotation/all_rotations scripts + matrices JSONs,
cross_validation (.py/.json), recursive_oracle.json (= Gate-0 battery),
corpus_regress (.py/.json), adversarial-90 attacks 56-73 + fault injection
(budget-forced-indeterminate, rotation-start-corrupt, negcert-corrupt).

## Verdict

R1 PASS, R2 PASS, R3 PASS, R4 PASS — promotion of CDK5NZULR-A authorized.
Complement, K>=6, universal Coarse-Double, Dynamic Optimality remain OPEN.
