# A six key obstruction to monotone scalar aggregation

The capped repair achieves the four named requirements but underpays another six-key starved KEEP. Comparing that operation with the opposite-vine operation excludes every coordinatewise nondecreasing scalar aggregation of (F,Ehat) lying between Ehat and F as a universal potential. This does not refute all structural corrections or Coarse-Double.

## The new actual source operation

Let L_[a,b] be the left vine on the integer keys a through b. Use

    A_P=1(empty,5(L_[2,4],leaf 6)),
    B_P=5(L_[1,4],leaf 6).

The common leaf 6 pads a five-core hook. KEEP 1 leaves A_P unchanged and splays depth four in B_P, giving a=0,q=2,z=0. The actual B events are LL on 1,2,3 followed by LL on 1,4,5. The destination is

    B'_P=1(empty,4(2(empty,3),5(empty,6))).

At the source the proper sets are

    C0(A_P)={[2,2],[2,3],[2,4],[2,6],[6,6]},
    C0(B_P)={[1,1],[1,2],[1,3],[1,4],[6,6]}.

Only {6} is an exact pair. After it is fixed, the residual graph has exactly the three disjoint edges [2,k]--[1,k], k=2,3,4. These edges and their three A endpoints as a cover certify mu=3. Therefore

    c_source=1, F_source=4, Ehat_source=1.

The destination B sets are [2,6],[2,3],{3},[5,6],{6}. The forced exact pairs are [2,6],[2,3],{6}. The residual A vertices {2},[2,4] and B vertices {3},[5,6] have no endpoint edge. Hence

    c_destination=3, F_destination=2, Ehat_destination=2.

For the fixed t_6=1 candidate,

    J_source=3, J_destination=2,
    Delta_KEEP J=-1>-2=2a-q.                           (6)

This is a legal whole source KEEP, not a micro-step inequality. CR03 gives its complete closed replay from a diagonal.

## The entire scalar class

Fix size n and consider ANY function

    T(A,B)=phi_n(F(A,B),Ehat(A,B))

which is coordinatewise nondecreasing and obeys Ehat<=T<=F on actual pairs. No Lipschitz, DELETE or helper assumption is needed for the following contradiction. Those properties cannot repair a contradiction already forced by B accesses.

At n=6 the two required source operations have these exact realized coordinates, in the order (F,Ehat):

| Starved KEEP | Source | Destination | Required change |
| --- | --- | --- | --- |
| Opposite vines, access 6 | (5,5) | (4,2) | <=-2 |
| Padded hook, access 1 | (4,1) | (2,2) | <=-2 |

The bracket forces phi_6(5,5)=5 and phi_6(2,2)=2. The two source inequalities then require

    phi_6(4,2)<=3,
    phi_6(4,1)>=4.

But (4,1)<=(4,2) coordinatewise, so monotonicity requires phi_6(4,1)<=phi_6(4,2). Combining gives

    4<=phi_6(4,1)<=phi_6(4,2)<=3,                       (7)

an exact contradiction. Every coordinate point above comes from an actual six-key physical source state; no abstract infeasible labels were introduced. Allowing phi to vary arbitrarily with n cannot change this single-size contradiction.

Both inputs are reachable from the SAME diagonal (B_P,B_P). The padded pair uses the DELETE prefix saved in CR03. To reach the opposite pair from that diagonal, use common KEEP requests 6,5,4,3,2,1, obtaining (R6,R6), then DELETE 2,3,4,5,6 to obtain (L6,R6). Each of these preparatory accesses is a root-child zig: KEEP6 first converts B_P to L6, then the descending pass gives R6; the DELETE pass converts only A to L6. Thus the obstruction does not depend on changing initial-tree components. It also applies when the scalar rule is indexed by that fixed initial tree.

## Every nonnegative size cap is excluded globally

For any alternative nonnegative cap t_6, opposite vines have source value 5 and destination 4-min(2,t_6). Full q=2 requires t_6>=1. The padded pair has source 4-min(3,t_6) and destination 2. Full q=2 requires min(3,t_6)=0, hence t_6=0. These are incompatible.

This is a corollary of the same two witnesses. No cap was searched or fitted. A larger finite corpus cannot remove this already exact six-key obstruction.

## Scope

The excluded class is specifically a coordinatewise nondecreasing function of ONLY n,F,Ehat with Ehat<=T<=F. The result does not exclude functions using additional tree structure, nonmonotone combinations, functions outside that bracket, or all-size potentials in general. It adds no new existence premise to the original pipeline. Universal Coarse-Double remains OPEN, and the capped J is REFUTED as a universal potential despite its four proved named properties.
