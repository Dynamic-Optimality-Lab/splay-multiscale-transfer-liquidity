# DLSS cyclic interval proof (L1), baseline (L2-baseline), debt bound (L2)

## Interval identities (L1)

I_j = accesses after preceding KEEP through current KEEP (cyclic; seam by
closure). Each access lies in exactly one I_j (KEEPs are the cut points;
DELETEs belong to the following KEEP's interval). Hence ΣH=A, Σq=Q_B,
Σc=C_K, Σw=Q_B−2C_K, ΣR=2(A−C_K) by summation (verified on IN 55/36/16).

## A-root-change baseline (L2a)

H_j≥c_j: c=0 trivial. If c=1 with H=0, all accesses have a=0 (current-root
hits; root splays are structural no-ops), so the root never leaves x_{j-1}
(placed by the preceding KEEP splay) and the terminal KEEP targets x_{j-1},
contradicting x_j≠x_{j-1}. Thus c=1⇒H≥1. So R_j=2(H_j−c_j)≥0. No-ops and
arbitrary DELETEs allowed; seam covered (first interval wraps by closure).

## Nine-core debt bound (L2b, arbitrary ambient trees)

Marked core = ∪ root→marked-key paths (ancestor-closed by definition); every
such path lies inside the core. H1: |core|=9 at every state. Genuine KEEP
keys are marked ⇒ each root path has ≤9 nodes ⇒ ≤8 edges ⇒ d_B≤8 ⇒ q≤4
(corpus max dB=6, q=3; no nine-node-global assumption used).
c=0 ⇒ x_j=x_{j-1}: B rooted there by preceding KEEP, frozen by intervening
DELETEs (I_j holds no other KEEP) ⇒ d_B=0 ⇒ q=0 ⇒ w=0 (0 violations on
corpus). Hence w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}. No Q≤2C_K premise.
