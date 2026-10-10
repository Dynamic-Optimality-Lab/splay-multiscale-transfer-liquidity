# VRP historical errata record (append-only; Gate 0 untouched)

## ERR-VR-1 — K5 A-depth: RESOLVED, mission statement CORRECT

Authoritative replay (both engines agree): K5 (access idx 9) has d_A=2, a=1.
An earlier Gate-0 novelty note wrote d_A=1. Costs identical either way
(a=1 both); Type K fails under both (needs d_A≥3); exception/eligibility and
all downstream conclusions unchanged. Corrected value d_A=2 used everywhere
here. No hypothesis affected.

## ERR-VR-2 — CTL-B description: CLARIFIED

SHA-pinned CTL-B (ff156d94, 17 accesses) is the S1 inclusion word (successor
H=2), not a doubled two-exception control. Committed SHA/word/length/closure
and its VR-exclusion reason (successor H≥2) are authoritative. Clarification
only; frozen control unmutated.

## ERR-VR-3 — K9 interval: USE CORRECTED VALUES

Non-relay K9 row is H=6/R=10 (authoritative IV sums ΣH=31, ΣR=46 confirm).
Never the draft H=3/R=4. Used consistently; not a counterexample to anything.

## Policy

Discrepancies above change no frozen hypothesis, cost, eligibility, or novelty
verdict (each verified cost-neutral or conservative). If any future discrepancy
did, STOP would apply. Gate-0 files preserved byte-identical.
