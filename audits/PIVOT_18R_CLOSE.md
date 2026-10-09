# PIVOT-18R closes: forced-pool lemma + final wall map + verdict

## Forced-pool lemma (new, proved)

Zero-fat E0-overfull ⟹ GENUINE Hall failure (not canonical artifact):
starved demands are FORCED to setup (no locals (a=0); creators empty
(zero-fat)); nonst residuals forced to setup iff locals full + creators
empty; setup overfull (`q_t+r' > 2a_s`) ⟹ pigeonhole with NO reorder
escape (starved have no alternatives; nonst alternatives (locals
full / creators empty) exhausted) ⟹ unmatched demands ⟹ Hall-deficient.
Hence **U4 ⟹ no zero-fat E0-overfull** (necessary condition, banked).

## Why this doesn't close U4 (the wall, final map)

E0-overfull SUFFICES for failure; minimal-X NECESSITY (every minimal
deficiency contains E0-overfull dance) is what's missing — and it fails
because deficiency can distribute (gap=1 spread as tightness across
many cells + sharing-excess, no single overfull cell). Cell-decomposition
attempted: overlapping cells make gap-accounting artifact-prone
(double-counted shared pools); global gap is exact but needs global
bounds. Ten independent formulations (access/cell/pool/demand/residual/
canonical/augmenting-builder-tree/dual/fat-lift/peeling) all terminate
at the SAME wall: sharing-multiplicity vs headroom with independent
A/B-discrepancy quantities. No formulation dominates another; the
missing piece is invariant across framings.

## E0 integer realizability (why refutation also fails)

`(0,2)+(1,3)+a_s=1+zero-fat`: every conjunct OBSERVED ((0,2)×4,
(1,3)×8-closed, a_s=1 common, single-starved-builder 50/51, sharing
6/66). Only their JOINT exact co-occurrence (E0=1 + order + closure)
is unobserved (0/900+). Integers always work; dynamics coherent via
temporal root-moving; marginal-lucky conjunction unruled-out. Neither
proof nor refutation available — wall is joint-coherence itself.

## Verdict (unchanged, now exhaustive)

E0/U4/`overflow≤slack`/COARSE-DOUBLE: OPEN (compositions ready).
`Q_B≤2A` unrefuted on ~900 tests; §26/§38/§44 never fired.
ONE missing: E0-dance unrealizability (joint form).
DO conditional (C.ZIG-V1V3 + PIVOT-2-excision mechanical).
Lean U1 green; block+E0 gap stands.
Zero kills across PIVOT-13→18R.
