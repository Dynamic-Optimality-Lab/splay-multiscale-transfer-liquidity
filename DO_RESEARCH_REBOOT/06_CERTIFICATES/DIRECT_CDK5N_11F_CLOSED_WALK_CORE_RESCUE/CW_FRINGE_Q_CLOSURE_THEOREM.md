# CW_FRINGE_Q_CLOSURE_THEOREM.md — Gate E (q exact via walk-stable core; S-relabeling)

## Core identification (no new observable)
Per admissible closed walk, S := C_M(B_0) (stable 9-set by Gate C; contains M=G(W)).
S-indices 0..8 label sorted C_M members (order-faithful; circuit-agnostic relabeling at the
concretize mapping only — no circuit change, no new coordinate, no new observable).
Masks = genuine positions within sorted C_M (126 possibilities). Gaps = between consecutive C_M
members; fringe = complement. All order/cost machinery transfers verbatim.

## q equality (representative = original)
For marked x: Path_{B}(root,x) ⊆ S (all ancestors in C_M by definition) ⟹ concrete d_B(x) =
S-induced depth ⟹ `q_original = floor(d_{B|S}/2)` = skeleton depth with nearest-C_M links =
B-controller computation under S-relabeling (paths verified, depths asserted equal, mismatches
openly skipped). |S|=9 ⟹ depths ≤8 ⟹ q ∈ 0..4. Fringe members of S (if any) are ordinary
S-indexed nodes with exact depths — no special-casing, no approximation.

## Why the previous gap is closed (not worked around)
Previous OPEN lemma: representative q (fixed-identity core) vs concrete q (fringe ancestors).
Resolution: the "fixed identities" were fixture coordinates, not the theoretical core. The
theoretical core IS C_M (walk-stable, possibly fringe-including); under S-relabeling the
representative and the original compute q on the SAME induced tree. The fringe-ancestor
"ambiguity" was a coordinate artifact. No all-core-ancestor restriction remains (it is not
assumed; paths are in S by definition, whatever S contains).

## T=266 re-audit vs strengthened invariant
E1-E8/L1-L8 machinery is S-parametric (takes Sset): re-audited items with S := C_M —
(1) nine S identities = C_M members; (2) five marked = G; (3) B-core = C_M-induced topology;
(4) marked depth induced-exact; (5) q exact (above); (6-13) unchanged (prefix/ports/atoms/word/
rotations/H/shadows/signature all S-relative via ranks). Per-edge representatives may differ;
boundaries map consistently (mu/B-core/alpha/sig canonical under relabeling). No globally fixed
2669-key set claimed (§11 distinction kept).

## Gates E (SC10-class obligations): PASS. Fringe-q correspondence CLOSED.
