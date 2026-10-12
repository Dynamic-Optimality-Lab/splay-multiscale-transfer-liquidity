# CC_LOW_COST_MACRO_GRAMMAR.md (STEP 08-09) + CC_HIGH_COST_SOUNDNESS.md (STEP 10)

## Low-cost macros (h=2, exact)

Per post-KEEP state (A-cone, B, root u, mask): effective words with H≤2,
≤h nontrivial accesses (cone corollary), interior DELETEs + terminal
KEEP(v∈mask), zero-cost root DELETEs normalized away. Patterns: [K(v)]
a≤2; [D(y),K(v)] ay≥1, total≤2; [D,D,K(v)] 1+1+0. Terminal A-root=v
required; B-transition exact via controller; weight w=2H−q exact.
Completeness: every H≤2 original interval's nonzero-access subsequence +
terminal is enumerated (targets within depth 2h by accessed-node bound;
patterns exhaustive by cost arithmetic) ⇒ maps to ≥1 macro with exact H,q
(verified: 0 uncovered on 6,800 intervals / 405 words: CC_CORRESPONDENCE).

## High-cost soundness (STEP 10)

H≥3 intervals: w_orig=2H−q ≥ 2(h+1)−q =: w_high (H≥h+1=3). Conservative
class: exact B-transition, root v preserved, inventory preserved, ANY
compatible A' shadow, charged w_high ≤ w_orig. Spurious transitions
allowed (permissive); never unsound in the sufficient-certificate
direction (more edges/paths can only add abstract cycles; a clean
abstract graph still certifies). Saturated weight is a lower bound, never
claimed as actual cost or independent theorem.

## Product + certificate (STEPS 11,13-14)

States (A,B) post-KEEP (concrete 9-key prototype; symbolic design
documented as open work). Edges: exact low-cost + compressed high-cost
(src→mid 6−q, mid→dst 0 over all compatible A'; weight-preserving).
Closed low BFS (233,600 states) + closed high-cost fixed point (388,096
states, 337 mids, 7.12M edges). Vectorized Bellman-Ford: STABLE in 6
iterations (0.4s) ⇒ potential Φ with w≥Φ(dst)−Φ(src) on all edges ⇒ all
abstract closed walks ≥0 ⇒ (via correspondence) all covered original
walks satisfy Q≤2A. Potential saved (CC_POTENTIAL.npy, 388,433 entries);
independent verifier: 1,081/1,081 low + 673/673 high max-constraints PASS.
No negative abstract cycles exist in the completed graph (§15: nothing to
classify). h=4 NOT warranted (criterion unmet: h=2 closed clean on its
domain; the gap is coverage/scale, not precision).
