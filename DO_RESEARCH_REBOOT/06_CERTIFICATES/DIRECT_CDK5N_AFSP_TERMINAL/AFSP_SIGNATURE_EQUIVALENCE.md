# Signature-equivalence quotient theorem (§11) — proved conditional; classes uncomputed

## Theorem

Let ~ be edge-guard equivalence: σ~τ iff ∀Γ_T∈G: Γ_T(σ)⟺Γ_T(τ) (including
high-cost feasibility guards). Then the σ-fixed and τ-fixed symbolic
products have identical state/edge relations under natural relabeling
(same masks/shadows/B-states; edges enabled identically by definition of
~); hence identical weights, identical negative-cycle status, and any
exact potential transfers verbatim (same inequalities). PROOF: definitional
unfolding (edge sets equal by ~; weights σ-independent given the edge;
potential inequalities identical). ∎

## Status: CONDITIONAL (theorem proved; premise uncomputed)

Equivalence CLASSES over 267^10 were not computed (no MDD implementation
within budget; enumeration impossible). No signatures merged (correctly:
nothing merged at all). The quotient is available as proof architecture
for future work; this campaign does not claim any class computation.
Consequence: signature-dependent potential (STEP 16) and uniform gate
(STEP 15/§19) NOT ATTEMPTED (blocked upstream: no symbolic product to
quotient). Recorded as open obligations, not failures of the quotient
theorem itself.
