# CC_B_CORE_PROOF.md — fixed nine-node B-core reduction (STEP 02)

## Claim

For marked KEEP transitions: C_M(B_next) ⊆ C_M(B_current) (fringe never
enters the core). DELETE: B unchanged ⇒ core unchanged. For exactly closed
B walks with core-nine throughout: C_M(B_t) = C_M(B_0) for all t (finite
monotone + equal cardinality 9). Projection π_S (contract fringe subtrees
to opaque leaves) commutes with marked splays; marked B-depths, q-costs,
successor shapes preserved; fringe blocks keep internal structure and
rank-gap identity.

## Proof

Rotation pivots lie on the splayed marked key's search path; every node on
that path is an ancestor of a marked key, hence core (DELETE: vacuous).
A rotation reattaches whole subtrees rigidly at on-path nodes: a fringe
node (in no marked path) stays inside its side subtree and never becomes
an ancestor of a marked key (marked keys never move below off-path nodes:
attachment points are always on-path). Thus no fringe label enters C_M:
monotonicity. Closed walk + |C_M|=9 at every state ⇒ constancy (finite
A_0⊇A_1…⊇A_m=A_0 with |·|=9 forces equality). Fringe never on marked paths
⇒ marked paths in B and π_S(B) identical ⇒ same rotation sequence ⇒
commutation; marked depths equal (ancestors all core); q preserved; fringe
blocks move rigidly (internal structure kept); inorder preserved ⇒ fixed
rank-gap identity. ∎

## Verification (CC_step02.py)

2,144 B-steps monotone (incl. DELETE-equal); 62/62 closed walks
constant-9; projection/splay commutation on all sampled KEEPs; marked
depths equal. PASS.

## B-controller conventions (STEP 03 record)

Full controller: 4,862 shapes × 126 masks = 612,612 states; 5 marked
transitions each (engine-checked). Odd-mask full: 24,310 triples =
24,310 pairs (no multi-key collisions — distinct targets give distinct
roots), 3,584 self-loops, 2,108 SCCs, 128 depth-8 edges (all in
nontrivial SCCs). Reachable-from-T0 odd-mask: 2,252 states (every state
marked-rooted: exactly 1 self-loop each), 11,260 triples = pairs, 152
SCCs (all nontrivial), 68 depth-8 edges. Historical reports (826 states,
2,824/2,786 edges, 292/290 SCCs, 24/16 depth-8) use a narrower filter
that is not recoverable from the stated conventions (reachable/cyclic/
genuine-only/self-loop variants computed above match none of them:
2252/11260/152 vs 826/2824/292). Discrepancy RECORDED as documentation
convention gap, NOT a mathematical blocker: the full controller is a
verified SUPERSET — every original B trajectory projects onto a
controller path (STEP-02 commutation) — so product-certificate soundness
does not depend on reproducing the historical counts. The 38-edge
(2824−2786) and 2-SCC (292−290) gaps are consistent with
triple-vs-pair labeling and self-loop filtering, but the 826-state base
remains unexplained (possibly A-shadow or product-level counts
mislabeled as B-states).
