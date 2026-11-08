# A source-uniform obstruction to a global geometric debt route

Status: PROVED refutation of the exact candidate class below, NOT C33,
Coarse-Double, or any frozen-owner architecture. No historical source or
successful owner is modified. This child eliminates a proposed global
geometry-only credit route, rather than repairing individual projections.

## Candidate source lemma being attacked

Let rot(A,B) be ordinary binary-rotation distance on the SAME finite ordered
physical keys. Let C(T) be the set of inorder key intervals of all nonempty
rooted subtrees (one per node), and let

    mis(A,B) = n - |C(A) intersect C(B)|.

A rotation replaces just one interval; both quantities are natural attempts
to turn A rotation work into comparison credit. Consider ANY debt function
depending only on `(n,r,rot(A,B),mis(A,B))`, with arbitrary dependence on
r and arbitrary nonlinear values. The candidate would assert the source
inequality `2H-Q+D(after)-D(before)>=0` on every natural packet.

That entire candidate class is false, even on original maximal-core
sources with r>=7. Additional full geometry or genuine chart information
is outside the refuted class.

## Uniform exact packet

Fix r>=7 and n=2r-1. Physical keys are1,...,n; genuine B KEEP keys are odd.
All extra gap trees may be empty; this is an allowed original-source case.
Write R_n for the right vine, L_[i,j] for the left vine on i,...,j. At a
synchronized key1 boundary take

    B0 = R_n,
    A0 = 1(empty, n(L_[2,n-1], empty)).

The packet is the ORIGINAL single KEEP n. In A its depth is1, so H=1.
In B its depth is n-1=2r-2, so Q=r-1. Hence weight is3-r<=-4.

After the packet,

    A1 = n(1(empty,L_[2,n-1]),empty),
    B1 = n(E2,empty),
    E_(2j) = 2j((2j-1)(empty,empty), E_(2j+2)),
    E_(n-1) = (n-1)((n-2)(empty,empty),empty).

The B identity is the inherited odd-vine maximum-splay induction. Its
inductive step is the actual RR formula
`a(A,b(B,n(C,D))) -> n(b(a(A,B),C),D)`.

## Exact rotation distances and interval counts

For any N-node tree T, `rot(T,R_N)=N-right_spine_length(T)`.
Each rotation changes that spine length by at most1, proving the lower
bound; right rotations at right-spine vertices with a nonempty left child
increase it by1 until the vine is reached. Thus

    rot(A0,B0)=n-2.

C(A0) and C(B0) intersect in exactly `[1,n]` and `[2,n]`.
C(A1) and C(B1) intersect in exactly `[1,n]` and `[1,n-1]`.
For the latter, all other A1 intervals are `[2,j]`, 2<=j<=n-1;
the other B1 intervals are `[2j-1,n-1]` (j>=2) or odd singletons.
None coincide. Consequently mis is n-2 at BOTH endpoints.

Since a rotation replaces one subtree interval, rot(A1,B1)>=n-2. For the
matching upper bound keep root n fixed. In B1.left=E2, right-rotate once
to promote1, leaving a right subtree rooted2 with no left child, of size
n-2. Transform that right subtree to its left vine with n-3 left rotations:
the mirror spine argument gives size minus left-spine length. The result
is exactly A1. Total rotations are1+(n-3)=n-2. Hence

    rot(A1,B1)=rot(A0,B0)=mis(A1,B1)=mis(A0,B0)=2r-3.

Every candidate debt in the stated class therefore has IDENTICAL endpoint
values, and its signed margin is exactly3-r<0. This is a uniform symbolic
refutation, not inference from passing/failing finitely many trees.

## Root-aware nonlinear summaries also fail jointly with reflection

Even allowing the common root key in the summary does not repair this
candidate class. Reflect the entire original source by k -> n+1-k and
swap left/right children. Ordinary bottom-up splays commute with this
reflection; the odd marked set is unchanged. Both metric values remain
n-2, but the reflected packet goes from common root n to common root1
with the SAME price3-r.

Write d1 and dn for arbitrary debt values of the summary
`(n,r,n-2,n-2,common_root)` at roots1 and n. The two valid ORIGINAL source
packets would require

    dn-d1 >= r-3,            d1-dn >= r-3.

Their sum is impossible for r>=7. Thus no function, even nonlinear and
support-dependent, of `(n,r,rot,mis,common_root_key)` can prove the stated
natural-packet law on the complete source domain. This uses two distinct
source histories, not a claimed concatenable negative source cycle. Finer
full A/B geometry or actual chart/history information remains outside
the refuted class. No width or Bank25 impossibility is inferred from it.

## Original reachable closed-source realization

Use the inherited W_r,H_r closed full-B words in
SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md. Let g be W_r's final
genuine K1, P the first Kn in H_r, and V the rest of H_r followed by W_r
with its final K1 omitted. Let Bprev be the actual tree before g. It has
root3, left L_[1,2], and right vine4,...,n.

The accepted UNIFORM_A_REALIZATION_OVER_CLOSED_B theorem gives actual
A-only finite transformation words Gamma on the same n>=4 keys. The
original word

    DELETE Gamma(Bprev,A0); K1; Kn; KEEP(V);
    DELETE Gamma(Av,Bprev)

starts from the common diagonal Bprev and closes A/full B exactly.
Av is A's actual state after KEEP(V). Every Gamma access is retained and
charged. No physical key is deleted. The original full B cycle has exactly
the r genuine odd KEEP keys. Actual finite-state recurrence supplies a
closed erased/chart period containing unchanged P occurrences. This uses
the inspected, pinned realization theorem, not a guessed abstract edge.

This is an exact mathematical existence counterfamily with a symbolic
source word parameterized by the inherited transformation words. A new
finite explicit Gamma replay is not performed or claimed. The local
source inequality fails in every such realized history independently of
the extra preparation/reset costs and of the actual chart states.

## Why this is not a donor or Coarse-Double counterexample

The preparation starts at Bprev where depth(n)=n-3 and ends at A0 where
depth(n)=1. One rotation reduces a fixed target depth by at most1; one
A StepEv uses at most2 rotations. Its actual preparation cost is therefore
at least ceil((n-4)/2)=r-2. The genuine K1 macro has Q=1 and H>=r-2.
The critical Kn macro has H=1,Q=r-1, natural deficit r-3. The preceding
macro has at least2r-5 natural spare bits, enough for that deficit.

Group these TWO actual adjacent macros. Their source-derived H>=r-1,
Q=r, so 2H-Q>=r-2. Every other genuine macro of W_r/H_r has Q<=2 and
H>=1. The disjoint source block rule in METRIC_FAMILY_SOURCE_FUNDING.md
therefore constructs a full h with working2 by the solvent-block theorem.
All actual preparation and reset costs remain included. The source is
funded; a failure of this geometric debt is not an unpaid physical gap.
