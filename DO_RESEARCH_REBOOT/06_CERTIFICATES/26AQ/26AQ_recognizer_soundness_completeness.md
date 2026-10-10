# Mixed recognizer: soundness, completeness, invariance, complexity

## Soundness

An emitted certificate is re-validated by `verify_cert`: every Direct piece
satisfies banked 26AP-P hypotheses (unit run, leader/KEEP r, a≥p,
nonpositive return) hence sums ≤0 by 26AP-P; every Bridge piece satisfies
AQ-P1–P7 (p≥3, genuine shallow bridge z≠r, interveners avoid r, return a≥p)
hence sums ≤0 by 26AQ-P; singletons are nonpositive by DP guard; pieces are
pairwise disjoint and jointly exhaustive by consumption check. So Σδ≤0.

## Completeness for C_AQmix

A valid cyclic partition has a piece boundary at some cut; enumerating all m
cuts aligns one linearization with it. Along that linearization the DP
succeeds: singletons transition directly; each Direct/Bridge piece matches
`valid_direct`/`valid_bridge` (maximal runs in the certificate are maximal
consecutive +1 runs in the linearization — a piece-internal run cannot extend
past its return/singleton boundary since those are nonpositive). Memoized
existence + fixed-priority reconstruction yields the certificate.

## Rotation invariance / termination / complexity

Cuts are over cyclic positions — relabeling the display permutes cut order
only; acceptance is existential over cuts. Finite m cuts × O(m) DP states ×
O(m) run scans = O(m³) packet tests, polynomial; terminates trivially.

## Preservation

`valid_direct` implements banked 26AP-P P1–P6 verbatim ⇒ every 26AP-accepted
decomposition is a valid all-Direct certificate ⇒ C_26AP ⊆ C_AQmix,
executed on the banked 26AP witness (Direct p=3 ACCEPT).
