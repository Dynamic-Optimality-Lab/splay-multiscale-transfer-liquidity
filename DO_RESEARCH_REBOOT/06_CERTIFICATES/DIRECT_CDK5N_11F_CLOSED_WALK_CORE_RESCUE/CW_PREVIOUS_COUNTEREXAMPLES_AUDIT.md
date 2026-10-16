# CW_PREVIOUS_COUNTEREXAMPLES_AUDIT.md — Gate D (no deletion, full classification)

## D1. Unrestricted-monotonicity witness: B=10(1,20), M={20}, KEEP(1)
Growth {10,20} -> {1,10,20} replay-verified (both engines). Status: CORRECT refutation of the
UNRESTRICTED lemma (arbitrary external M), RETAINED as such. Not a counterexample to the
exact-domain statement, for two independent reasons:
(a) Word-incomplete: a single operation is not an exactly closed word (no closure to test).
(b) Wrong marked set: KEEP(1) changes B, so 1 ∈ G of any word containing it; the exact-domain
marked set is M=G(W)∋1, under which C_M before = {1,10,20} = after (no growth — consistent with
marked-splay monotonicity since 1 is marked). The growth was an artifact of externally imposing
M={20} ≠ G. Prior certificate stands unmodified; this reclassification is additive.

## D2. Fringe-ancestor boundary (root 5, designated M={2,5,9,10,11}, marked 9 ancestors [12,7])
Questions: (i) Is designated M the genuine set of an extendable closed word? (ii) Does fringe
break the new theory?
(i) Extendability: bounded attempt (2000 random continuations from the boundary seeking exact
pair-closure with genuine set exactly designated M): 0 found. Absence is NOT exclusion (search
space unbounded; closure with exact genuine control is rare). Recorded UNKNOWN per mandate.
(ii) Compatibility: even if extendable with G = designated M, stable fringe in C_M is COMPATIBLE
with the rescued theory (constancy allows stable members; q via S-induced tree exact with S=C_M;
no fringe-free claim made or needed). The witness refuted only the old all-core-ancestor filter
(an implementation filter, since replaced by S-relabeled exactness), not any current theorem.
If a future closed word exhibits it with G confirmed, the theory covers it (fringe stably in S,
depths induced-exact).

## Completion criterion
Both prior examples explained without deleting negative evidence: D1 = wrong-M artifact (+word
incomplete); D2 = compatible-or-unknown (extendability undecided, theory fringe-tolerant).
Neither contradicts the exact-domain statements (Gates A-C). Gate D: PASS.
