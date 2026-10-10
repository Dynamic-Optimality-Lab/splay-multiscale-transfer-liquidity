# ARmix recognizer: soundness, completeness, invariance, complexity

## Soundness

`verify_cert` re-checks every piece: Direct ⟹ banked 26AP-P hypotheses ⟹
packet ≤0; Bridge ⟹ 26AQ-P hypotheses ⟹ ≤0; Split ⟹ AR-P1–P10 (dA thresholds
from leader pre-depths, a_r,a_s<p, keeps-noninterference, r≠s) ⟹ ≤0 by 26AR-P
(cross-checks assert the derived δ bounds and joint sum). Singletons guarded
nonpositive; consumption exact-once; coverage exhaustive. So Σδ≤0.

## Completeness for C_ARmix

A valid cyclic partition has a piece boundary at some cut; all m cuts
enumerated. Along the aligned linearization, DP succeeds: singletons step
directly; each D/B/S piece matches its validator (Split tries all p≥3 within
the +1 run; maximal-run semantics preserved since piece returns/singletons
are nonpositive). Fixed-priority reconstruction is deterministic.

## Rotation invariance / no double credit / termination / complexity

Existential over cyclic cuts ⟹ display-independent. Consumption sets are
disjoint by construction + verifier-enforced. Finite cuts × O(m) states ×
O(m) run scans × O(1) checks = O(m⁴) worst case (m=37 trivial).

## Preservation

D/B validators are the banked 26AQ module functions themselves (imported, not
re-implemented) ⇒ every 26AQ certificate is an ARmix certificate with identical
pieces ⇒ C_AQmix ⊆ C_ARmix; executed on both banked witnesses.
