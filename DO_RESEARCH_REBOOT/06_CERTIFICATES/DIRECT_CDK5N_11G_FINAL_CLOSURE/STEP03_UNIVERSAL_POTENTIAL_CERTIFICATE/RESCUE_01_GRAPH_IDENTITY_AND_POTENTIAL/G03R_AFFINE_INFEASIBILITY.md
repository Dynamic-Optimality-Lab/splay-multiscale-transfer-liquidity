# G03R Affine Infeasibility (exact diagnosis)

Feature-difference matrices over 40 full-state ledger edges and the 38-edge
Step-03 seed corpus (16 features): rank 11/15, nullity 4, constant columns
`{sig_sum, sig_nonempty, b_rank_root}` (grounded samples carry zero saturated
signature). Rational feasibility (exact Z3 Reals): SAT on BOTH corpora —
NO Farkas family-contradiction exists for these 78 edges. Integer feasibility:
SAT (unbounded; refit max |coef| 924). E3 classification: NOT a
family-contradiction, NOT integer-only; it is bounded-box strain
(coefficients 1s -> 900s across refits) + generalization failure (final
refit-38: 15/60 fresh violations) + template incompleteness (killers:
rank_sum +2 @ w=1; shadow-marked +2 @ w=0; deep-chain cluster dmax 8->7).
No feature circulation is presented as a graph cycle: finite witnessed graph
has zero closed walks. (`G03R_DUAL_CERTIFICATE_RESULTS.json`.)
