# An explicit unbounded correction and its proved partial laws

The subtree-set correction cancels the old root-changing DELETE obstruction and obeys DELETE on every source edge. It also preserves a strict B decrease and the earlier arbitrary-fringe zero-weight helpers. Its decrease does not always repay the full q, so it is not a complete Route C potential.

## Explicit definition

Retain r=1/8 and edge depths. For actual same-key BSTs put

    G(A,B)=sum_y r^{d_A(y)}d_B(y),
    F(A,B)=n-|C(A) intersection C(B)|,
    R(A,B)=F(A,B)-G(A,B),
    Psi(A,B)=G(A,B)+R(A,B)=F(A,B).

Every term is determined by the current physical pair. There is no unknown function to construct and no compatibility assumption hidden in the definition. Merely writing R=F-G supplies no proof; the content is the source rotation identity for this specified F and the laws below. This correction uses labeled subtree-set agreement, beyond a global joint-depth histogram.

## Universal DELETE bound

An A splay at x uses exactly d_A(x) primitive rotations: each double consumes two levels and a final zig consumes one. Formula (1) of CC01 bounds the increase of F by one per rotation with B fixed. Therefore

    Delta_DELETE Psi <= d_A(x) <= 2 ceil(d_A(x)/2)=2a.     (4)

This holds for all finite valid pairs, both orientations, every present x and arbitrary fringes. When d_A=0, the A tree is unchanged. DELETE omits a request from B; no BST node is removed.

## Exact cancellation on the old unbounded-drift family

For n>=3 and ANY BST M on keys 2 through n-1, take

    A=1(empty,n(M,empty)),
    B=2(leaf 1,right vine on 3 through n),
    A_d=S_n A=n(1(empty,M),empty).

The one root zig changes only the A weights at 1 and n; every M key keeps its A depth. Since d_B(1)=1 and d_B(n)=n-2,

    Delta_DELETE G=(1-r)(n-3)=7(n-3)/8.

Both before and after, the only subtree key set shared with B is the full set. B's proper sets are {1} and suffixes containing n but excluding 2. A's proper M sets contain neither 1 nor n; the remaining proper set is [2,n] before or [1,n-1] after. Neither occurs in C(B). Hence

    F(A,B)=F(A_d,B)=n-1,
    Delta_DELETE R=-7(n-3)/8,
    Delta_DELETE Psi=0.                                   (5)

This is the demanded unbounded negative correction under one rotation, not a bounded reserve or B-only gauge. The oscillation of R on these endpoints tends to infinity with n, proving R is unbounded on the all-size domain.

KEEP 1 from the SAME source has a=q=0 and one B zig. B becomes the right vine on 1 through n. Its new proper set [2,n] agrees with A's child subtree; no other proper agreement occurs. Thus Delta Psi=-1. The correction passes BOTH operations that defeated the previous root-envelope repairs.

## B repayment that is actually proved

When root(A)=x, CC01 gives

    Delta_B Psi <= -1, if d_B(x)>0;
    Delta_B Psi = 0,   if d_B(x)=0.                       (6)

This is uniform in n and fringe shape and uses no setup identity, latest arrival or history restriction. It pays the required -q for q<=1. It does NOT establish the required -q at larger demand.

For a whole KEEP, compose the A and B phases in the actual source order. After A splays x, it is rooted at x, so (6) applies to B. Consequently

    Delta_KEEP Psi <= d_A(x)-indicator(d_B(x)>0).         (7)

Let epsilon_A=d_A(x) mod 2, so 2a=d_A+epsilon_A. Bound (7) implies the required Delta Psi<=2a-q for every KEEP with d_B=0, and for every other KEEP satisfying

    q <= 1+epsilon_A.                                    (8)

This includes all q<=1 edges and all q=2 edges with odd A depth. Closed source walks entirely in this stated class satisfy Q_B<=2A by exact telescoping. This is a restricted-domain result, not a mandatory property of all source walks or a completed universal reduction.

## Arbitrary-fringe zero-weight helpers

Both branches of the existing [arbitrary-fringe helper family](../route_c_analytic_20261030_v001/RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md) have d_A=1 and d_B=4, hence a=1,q=2 and budget zero. Formula (7) gives Delta Psi<=1-1=0 for ALL of them, independently of fringe cardinality, internal paired shapes or reflection. No new helper corpus was needed.

The correction therefore survives that specific all-size helper obstruction and the old cheap-DELETE/zero-demand-KEEP pair. Whole overwritten-setup histories with unrestricted q remain outside (8); CC03 supplies an actual starved q=2 failure. Success on the earlier necessary tests is not sufficient for the universal theorem.
