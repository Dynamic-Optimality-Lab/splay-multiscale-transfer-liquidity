# AFSP_STATE_RELATION.md + AFSP_LOW/HIGH_TRANSITION_RELATION.md + AFSP_PRODUCT_COMPLETENESS.md (condensed)

States v=(μ,b,α,σ): 126 masks; B rank-shapes (4,862; per-mask reachable
tabulated, 17,920 depth-8 edges all-mask); A canonical shadows (order-type
endpoints; S-ranks exact; anonymous canonical); σ∈{0..266}^10 saturated
(not enumerated: 267^10). Root-sync enforced; BST feasibility via AF-2.
Low edges: H≤2 grammar ([K],[D,K],[D,D,K0]) simulated on representative
concretions (AF-1/AF-3 sound); weight exact 2H−q; guard = AF-2 feasibility.
High edges: H≥3, exact B successor, root, signature preserved, any
compatible A' shadow, weight 6−q ≤ 2H−q; compressed group fanout with
proved max-equivalence (M(μ,b',v,σ)=max Φ; constraint ⟺ conjunction).
Completeness C1/C2/C4/C5/C8-C10: proved for completed scopes (9-key:
4.26M-state closed graph; correspondence per-walk via Stage 10).
C3/C6/C7/C11-C13 BLOCKED universally (fringe completions/state bounds;
high-cost fanout explosion measured: 5.5M states then killed; analytic
612k mids × ~700 dstates ≫ caps). Lazy-incompleteness noted (unreached
true states gap soundness; upfront-full infeasible 5.5B UB).
