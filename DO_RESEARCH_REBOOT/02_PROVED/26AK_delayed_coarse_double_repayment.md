# 26AK: delayed former-root repayment (PROVED restricted class)

**Status: PROVED** — universal opposite-branch displacement lemma + capacity-gated
three-block repayment + validated genuinely-delayed witness. No J4, ROW-DIAMETER,
J-SELF, DTQ, UG, potentials, LP, or compactness used.

## Theorem 26AK-T (opposite-branch delayed repayment)

Let γ be a finite reachable closed present-key Pair-Access walk with cyclic
A-root blocks as in 26AJ. Suppose every positive-deficit block B_i satisfies:

- **H1**: δ_i > 0, with key x_i and former B-root r_i ≠ x_i;
- **H2**: block i+1 performs a genuine B-changing KEEP of y_i with
  y_i ≠ x_i, y_i ≠ r_i (y_i ≠ x_i already forces B-change since B is rooted
  at x_i; leadership y_i ≠ A-root is automatic);
- **H3**: opposite-branch geometry (r_i−x_i)(y_i−x_i) < 0;
- **H4**: block i+2's leader accesses x_{i+2} = r_i;
- **H5**: δ_{i+1} ≤ 0;
- **H6**: with h_i = depth of r_i after block i (h_i ∈ {1,2} by 26AJ Lemma 2)
  and c_i = floor((h_i+2)/2) ∈ {1,2}: δ_i ≤ (2a_{i+1}−q_{i+1}) + (2a_{i+2}−c_i).

Then Q_B(γ) ≤ 2A(γ).

## Proof

26AK-L1 (companion displacement audit) gives `d'(r_i) = d'(x_i) + h_i` after the
intervening splay of `y_i`, where `d'(x_i) ≤ 2` by the former-root lemma applied
to that same splay (x_i was B's root before it). Hence `d'(r_i) ≤ h_i+2`. Hence block i+2's first B splay has q ≤ c_i, so
δ_{i+2} ≤ c_i − 2a_{i+2} ≤ 0 (as c_i ≤ 2 ≤ 2a). Then
δ_i+δ_{i+1}+δ_{i+2} ≤ δ_i + (H5) + (cap) ≤ 0 by H6.
Disjointness: triples of distinct positives are disjoint — a shared block k
with slot ≥1 in some triple is forced nonpositive by that triple, so k cannot
be positive; small-m self-overlap (m=1,2) makes positivity jointly inconsistent
(x_i=r_i contradicts nontrivial splay; H2 distinctness fails). Triple-less
blocks are nonpositive (else they'd own triples). Summing disjoint
nonpositive triples plus nonpositive leftovers: Σδ ≤ 0, i.e. Q_B ≤ 2A.
Frozen-detour variant (no B change in block i+1): stronger cap q ≤ 1 applies;
recorded as corollary, not needed for the theorem.

## Witness (genuinely new coverage)

n=7 (shape index 1, not a vine): prefix D6,D1; cycle
`K6,K7,K1,K3,K5,K4,D2,D6,K1,K2,K1` (11 blocks), closed exactly (both trees,
serial-compared, `replay()`-identical). Sole positive block (K6, δ=+1,
former root r from shape root); intervening KEEP y=7 is genuine B-changing,
opposite-branch ((r−6)(7−6)<0), B-root==6 verified at its start; delayed
KEEP r with h=2 (c=2); H5 (−2≤0); capacity 1 ≤ (2−0)+(4−2) = 4; total −25.
Repetition gives arbitrarily long covered walks. Outside zero-A, n≤6 closure,
bounded-depth charging; NOT 26AJ's immediate pattern (successor ≠ r).
Records: `06_CERTIFICATES/26AK/26AK_{witness,validated}.json`, `ak_close2.py`,
`ak_validate.py` (+ tuple/ptr engine agreement 400/400).

## Scope (exact)

Covers closed walks whose every positive block meets H1–H6. Does NOT cover:
positives without former-root-delayed successors, deficits beyond capacity,
multi-step/indirect repayment, unrestricted Coarse-Double. No J4/ROW claim.
