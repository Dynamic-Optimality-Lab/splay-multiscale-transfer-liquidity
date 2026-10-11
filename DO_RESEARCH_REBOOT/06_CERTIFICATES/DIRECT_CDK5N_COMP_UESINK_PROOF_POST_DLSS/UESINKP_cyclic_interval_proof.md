# Cyclic interval proof + A-root baseline + nine-core debt (L1/L2 lemmas)

## Partition (L1)

KEEP occurrences cut the cyclic access sequence; I_j = accesses strictly
after K_{j-1} through K_j (wraparound for j=0 by closure). Every access has
exactly one KEEP at-or-after it, so membership is unique and exhaustive.
Summation gives ΣH=A, Σq=Q, Σc=C_K, hence Σw=Q−2C_K, ΣR=2(A−C_K). Verified
on IN (55→56? no: IN A=56: ΣH=56, Σq=36, Σc=16 — recomputed in replay).

## Baseline H≥c (L2a)

c=0: H≥0=c trivially. c=1 with H=0: all a_t=0 in I_j, i.e., every access
hits the current A-root; splaying the root restructures nothing, so the
root remains x_{j-1} (placed by the preceding KEEP splay) through the
interval, and the terminal KEEP targets x_{j-1}, contradicting x_j≠x_{j-1}.
Hence c=1 ⇒ H≥1=c. So R=2(H−c)≥0. Arbitrary DELETE counts, any seam.

## Debt bound (L2b)

Marked core: ancestor-closed union of root→marked-key paths, nine nodes at
every state (H1). Genuine KEEP keys are marked ⇒ their root paths lie in
the core ⇒ ≤9 nodes ⇒ ≤8 edges ⇒ d_B≤8 ⇒ q≤4 (ambient size unrestricted;
paths never leave the core). c=0 ⇒ x_j=x_{j-1}: B was rooted there by the
preceding KEEP and frozen by intervening DELETEs (I_j holds no other KEEP)
⇒ d_B=0 ⇒ q=0 ⇒ w=0. Thus w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}. No Q≤2C_K premise.
