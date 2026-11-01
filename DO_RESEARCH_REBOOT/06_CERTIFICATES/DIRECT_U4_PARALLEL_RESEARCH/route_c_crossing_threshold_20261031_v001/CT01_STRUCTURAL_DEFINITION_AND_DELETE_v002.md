# Structural crossing counts and universal DELETE

Counting multiple boundary conflicts is a concrete structural alternative to the previous scalar cap. It gives a uniform DELETE law, but the same function fails B repayment on the four-key source operation in CT02. The full potential construction remains open.

## Definition on arbitrary finite ordered key sets

Relabel the common finite key set increasingly as 1,...,n. Rank relabeling preserves actual source splays and their event costs. Every nonempty node-rooted subtree has a contiguous interval of these ranks. Let C0(T) be the collection of proper such intervals; exclude the full key set. There are exactly n-1 distinct intervals when n>=1. Do not insert a singleton for an internal node merely because its key exists.

For I=[l,h], put e(I)=(l-1,h+1), with endpoints among 0,...,n+1. Define a strict crossing of e(I)=(a,b) and e(J)=(c,d) by

    a<c<b<d OR c<a<d<b.

Shared endpoints do not cross. Let b_B(I) count the distinct J in C0(B) whose chords cross e(I). For one fixed positive integer k define

    Hk(A,B)=sum_{I in C0(A)} indicator(b_B(I)>=k).

The principal candidate is k=2. It is a finite, determined function of the present full pair. No unknown labels, future accesses, parameter fit or existence premise define it. Put Hk=0 when n=0 or n=1. In general 0<=Hk<=n-1. A DELETE omits a B occurrence and keeps all keys, so n and the rank coordinate system are fixed along every source edge.

## Exact increment and proof of DELETE

The [source rotation identity](../route_c_clade_correction_20261031_v001/CC01_SOURCE_ROTATION_IDENTITY.md) proves that one primitive A rotation replaces one proper interval J by one new interval K and retains all the others. In a left rotation p(L,x(M,R))->x(p(L,M),R), these intervals are exactly keys(x(M,R)) and keys(p(L,M)); reflection gives the other orientation. Empty fringe slots do not change the identity.

B is fixed during the A phase. Each retained interval therefore has exactly the same crossing degree before and after. Consequently

    Hk(A_after,B)-Hk(A_before,B)
      = indicator(b_B(K)>=k)-indicator(b_B(J)>=k).

Both indicators are in {0,1}, so the absolute increment is at most one. This proof includes arbitrary fringe size and shape, all ancestor contexts, both rotation orientations and every fixed positive k.

An actual present-key bottom-up splay of depth d_A uses exactly d_A primitive rotations: two per double and one for an optional final zig. The source counts a=ceil(d_A/2) grouped A events. Summing the increment bound proves universally

    |Hk(S_x A,B)-Hk(A,B)| <= d_A(x) <= 2a.

This is PROVED—UNIVERSAL for the DELETE law only. If d_A=0 the tree is unchanged and the increment is zero. Empty trees admit no present-key accesses; singleton trees have zero potential. No later B failure invalidates this A proof.

## Symmetries and the old scalar obstruction

Rank reflection sends [l,h] to [n+1-h,n+1-l] and a chord endpoint v to n+1-v. It preserves strict crossings, degrees and Hk, and exchanges the two source orientations. Thus the construction and its A bound are invariant under reflection and arbitrary increasing rank relabeling.

The definition uses crossing multiplicities, rather than only the exact-common count and residual endpoint-matching rank. At CT02's four-key source, F=3 and Ehat=2, whereas H2=1. The proper A intervals are {1},[1,3],{3}; B has [2,4],[3,4],{4}. There are no common intervals, and the entire endpoint-matching graph has just one edge, {3}--[3,4]. Its matching rank is exactly one; hence Ehat=3-1=2.

Therefore H2 lies outside the bracket Ehat<=T<=F used in the prior monotone-aggregation impossibility theorem. That earlier theorem does not itself reject this candidate. The new whole-source witness does. No claim is made here about information-theoretic independence from every conceivable scalar representation.

## Source dependencies

The mathematical replacement identity is inherited as cited. Present-key source costs, actual LL/RR/LR/RL/ZIG ordering and endpoints are the implementations in [tuple source](../../../../python/independent/splay.py) and [pointer source](../../../../python/liquidity/legacy_embedding.py), pinned at entry. CT02 gives complete finite crossing incidences and source replays. The [independent verifier](independent_verify.py) imports no producer and regenerates all finite incidences using a different crossing predicate.
