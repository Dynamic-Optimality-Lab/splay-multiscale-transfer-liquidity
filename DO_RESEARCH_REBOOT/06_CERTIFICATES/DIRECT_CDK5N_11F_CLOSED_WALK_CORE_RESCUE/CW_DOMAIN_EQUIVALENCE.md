# CW_DOMAIN_EQUIVALENCE.md — Gate A verdict: DOMAIN-EQUIVALENT (M = G(W) definitionally)

## Authoritative sources
- GLOB_observables.md: "M = five genuine KEEP keys of the walk."
- GLOB_theorem_spec.md: W_5^9 = exactly closed pair-walks + exactly five distinct genuine KEEP keys
  + complete marked B-ancestor core nine at every cyclic state.
- GLOB_source_semantics.md: "Marked B-core = ancestor-closed union of B-root→genuine-KEEP-target
  paths"; KEEP splays A+B; DELETE splays A only, q=0; full labeled A/B pair-closure.
- Membership code: `genuine_keys(legs) = {x: KEEP(x) with chg}` (dynamic G(W), |G|=5 enforced);
  `core_of(ps, M=MSET)` with MSET={1,3,5,7,9} (fixed) for core-9 checks; SELR fixtures assert
  `genuine == [1,3,5,7,9]` (genuine coincides with MSET ON FIXTURES by construction).

## Verdict: DOMAIN-EQUIVALENT
The theorem's marked set M is exactly G(W) (the five genuine B-changing KEEP keys), by definition
in the authoritative spec (observables + theorem_spec + source_semantics agree: marked paths are
root→genuine-target paths). No equivalence to prove beyond reading: M=G(W) is definitional.

## MSET classification (entry-audit items)
- Theorem quantifies over: G(W) (dynamic, per-word genuine five-set).
- Test harness (fixtures) uses: MSET={1,3,5,7,9} as the genuine set OF FIXTURE WORDS (constructed
  so genuine coincides with odds; SELR_negative_verifier asserts this shape).
- Identical in general: NO (MSET fixed, G(W) dynamic).
- Source-derived normalization equating them: NONE (and none needed — theory is G(W)-native).
- Order-preserving relabeling to MSET: IMPOSSIBLE in general (order-automorphisms of {1..n} are
  identity; exact odd-position mapping requires |U|=9 with G at odds — not general). Hence MSET is
  fixture-only coordinate choice, not the marked set; no relabeling is required or performed.
- 126 masks: 5-subsets of abstract core positions 0..8 (mask = G's sorted positions within C_M);
  covers all ordered configurations (each walk matches its mask; no weaker domain).
- R1-T domain unchanged: (U arbitrary, M=G(W) five genuine, C_M nine-count, exact pair-closure).

## Gate A: PASS (DOMAIN-EQUIVALENT). Proceed to Gate B.
