# SELR-PROOF Gate-0 errata A–F (append-only; Gate-0 bytes untouched)

## Erratum A — IN arithmetic (CONFIRMED, documentation-only)

Frozen IN: A=53, Q=36, C_K=16. Hence Σw=36−2·16=4; ΣR=2(53−16)=74;
4≤74 telescopes to 36−32≤106−32, i.e. 36≤106. Gate-0 IN worksheet and
adversarial text writing 36≤104 for the IN are wrong (104=2·52 is the
OUT's 2A). Inconsistency only; the universal inequality never depended on
it. Corrected accounting used throughout this stage.

## Erratum B — verifier count + per-entry gap (CONFIRMED, repaired here)

SELR_negative_verification.json contains 19 named checks (all PASS), not
22 as the Gate-0 AZ report states. Moreover it checks matrix sizes/summary
flags without re-verifying each stored disposition. This stage's
SELRP_negative_verifier recomputes all 1,464 decisions entry-by-entry
(24 keys/row, true starts, closure, disposition/flag agreement) with
explicit -O-safe checks; ≥22 substantive proof-stage obligations.

## Erratum C — rotation omission in cover24 base (CONFIRMED, repaired here)

Gate-0 SELR_recursive.cover24 tests bank24 only at the input orientation
before recursing; C24* requires Rot(B24) base coverage at every level.
Gate-0 rotation audits covered only the frozen roots. New proof-stage
checker SELRP_recursive_checker implements rotation-aware base cases at
every recursive subproblem with true boundary starts. Witness impact:
none — both frozen witnesses are primitive, so recursion reduces to the
root rotation census (already all-negative); independently re-established
here. Gate-0 engine preserved unmodified.

## Erratum D — weak incomplete-recognizer injection (CONFIRMED, repaired)

Gate-0 adversarial checked isinstance(dict/None), which an incomplete
result can satisfy. Proof-stage: SELRP wrappers convert unknown-predicate
outcomes (missing recognizer, exception, malformed value) to
INDETERMINATE on the actual recursive path; fault injections demonstrate
COVERED→INDETERMINATE transitions (never silent EXCLUDED/UNCOVERED/PASS).

## Erratum E — assert reliance (ADDRESSED)

Proof-stage verifiers/checkers use explicit conditional checks raising
errors or returning failure dispositions; no assert controls a verdict.
Critical paths run under both normal Python and python -O with identical
rejection behavior.

## Erratum F — summary-only negative evidence (ADDRESSED)

Proof-stage negative certificates store: canonical word, SHA, initial
state, auditable boundary pair-state census, closure evidence, full
rotation census with per-domain dispositions, proper-closed-segment
census, recursive result, cap counters, verifier verdict — connected by
the primitivity+rotation-exclusion completeness argument (recursive
definition doc). No bare covered:false accepted.
