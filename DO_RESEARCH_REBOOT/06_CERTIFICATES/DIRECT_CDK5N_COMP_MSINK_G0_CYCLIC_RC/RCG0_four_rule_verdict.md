# RCG0 four-rule verdict — CDK5NCMS-RCG0-A APPROVED (Gate-0 only)

## R1 STRICTLY SMALLER: PASS

W_IN (`788b459d…efd6d0a`, 64/36/16) ∈ S_MSINK ∩ R_5^*: strict member
(E=[4,12], t=(0,2), unique joint sink p=0 H=13, other-positive strict-P),
20/20 direct negatives, recursive C* negative (complete DAG, 19 subproblems,
budgets untouched). W_OUT (`b8b02be7…bedab3`, 55/36/16) ∈ R_5^* ∖ S_MSINK:
H3 mixed-fail t=(2,2), 20/20 negatives, primitive ⇒ no recursive partition.
∅ ≠ (S_MSINK ∩ R_5^*) ⊊ R_5^*. Proper-subclass certificate present.

## R2 SOLVABILITY: PASS

Reconstructed L1–L7 holds on H1–H6 (identities, baseline, q≤4, exceptions,
joint sink over full q_p range, strict others, disjointness, telescoping;
verified computationally on IN-new: Σw=4≤96=ΣR). No aggregate premise,
no new mechanism, no circularity. Mechanism certification for Gate-0 only.

## R3 ONE-PROMPT SCOPE: PASS

One theorem, one H1–H6, one mechanism, fixed IN/OUT, one recursive criterion,
one attempt, one outcome. No discovery/mutants/candidates/mutation/promotion/
successor. Prior dirs, ledger, deps, 02_PROVED untouched.

## R4 UPWARD PROGRESS: PASS

IN outside C_*: not direct-banked (20/20 negative incl. pointer-push AS),
not one-level-cyclic-covered (DP-exhaustive), not nested-covered (full
recursion, 19 subproblems, complete negative DAG). Old anchored-only evidence
superseded by construction, not by assumption.

## Terminal

**CDK5NCMS-RCG0-A — FOUR-RULE RECURSIVE CYCLIC GATE 0 APPROVED.**
Gate-0 approval only. No theorem promotion. No MSINK-PROOF launch.
