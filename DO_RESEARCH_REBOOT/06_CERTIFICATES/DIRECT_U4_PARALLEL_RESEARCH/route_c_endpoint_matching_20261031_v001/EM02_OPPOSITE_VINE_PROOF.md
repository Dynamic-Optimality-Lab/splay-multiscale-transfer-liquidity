# Endpoint matching pays the full opposite vine demand

For every n, the candidate E obeys the full B-repayment inequality on the opposite-vine access. This is an analytic result from explicit matchings and vertex covers, not a fit.

Let R_n be the right vine on 1 through n and L_n the left vine on the same keys. Set A=L_n,B=R_n and KEEP n. A does not move; B has depth n-1, q=floor((n-1)/2), and V_n=S_n R_n is its destination.

For n>=2, the proper A subtree sets are prefixes [1,k], k=1,...,n-1, while the proper B sets are suffixes [j,n], j=2,...,n. Their minima cannot agree, and their maxima cannot agree. Thus the graph has no edges:

    nu(L_n,R_n)=0, E(L_n,R_n)=n-1.                       (1)

## The source destination shape

The RR source recurrence consumes two outer ancestors k,k+1 and replaces the target's old left subtree J by (k+1)(leaf k,J). If n is odd, V_n has root n and left subtree with right spine 2,4,...,n-1 and preceding odd singleton left children. If n is even, a final zig leaves left-subtree root 1 followed by right spine 3,5,...,n-1 and preceding even singleton left children. The right subtree of n is empty. This is the same exact source parity recurrence used in CC03 of the previous audit.

All proper A vertices have minimum 1. Call a B vertex broad when its minimum is 1; it is then adjacent to every A vertex. All other B vertices are adjacent only to the one A prefix with the same maximum, if present.

## Even sizes

Write n=2m>=4. There is one proper broad B vertex, [1,n-1]. The distinct maxima of the ordinary B vertices form

    S={2,4,...,n-2,n-1}, |S|=m.

The broad B vertex together with the m A prefixes whose maxima lie in S is a vertex cover, giving nu<=m+1. For the reverse bound, match one ordinary B vertex of each maximum k in S to A's prefix [1,k], then match the broad vertex to [1,1], which was not used. All edges and endpoints are distinct, so this is a matching of size m+1. Thus

    nu(L_n,V_n)=m+1,
    E(L_n,V_n)=(2m-1)-(m+1)=m-2.                       (2)

## Odd sizes

Write n=2m+1>=5. There are two proper broad B vertices, [1,n-1] and {1}. The distinct ordinary maxima form

    S={3,5,...,n-2,n-1}, |S|=m.

These two broad vertices together with the m A prefixes indexed by S give a vertex cover of size m+2. Match one ordinary B vertex of each maximum in S to its A prefix, then match the broad vertices to [1,1] and [1,2]. These two A vertices are outside S. The resulting matching has size m+2, proving

    nu(L_n,V_n)=m+2,
    E(L_n,V_n)=2m-(m+2)=m-2.                           (3)

Every matching cardinality is bounded by every vertex-cover cardinality because distinct matching edges require distinct cover vertices. The displayed matching and equal-size cover therefore prove each value without an external matching theorem.

## Demand and boundary cases

Equations (1)-(3) give, for n>=4,

    E(L_n,V_n)-E(L_n,R_n)=-(q+2)<=-q.

At n=2 the values are 1 and 0 with q=0. At n=3 the values are 2 and 0 with q=1. At n=1 both values and q are zero; empty trees have no present-key access. Reflection gives the opposite orientation. Thus every size and both orientations are covered.

Relative to F, the repair H=E-F is zero at the opposite-vine source. For n>=4 it equals -floor(n/2) at the destination. The nonlinear matching bonus therefore supplies precisely the previously missing unbounded decrease while keeping the universal DELETE bound from EM01.

This proves only this specified B family. It gives no general matching augmentation theorem for all root-conditioned splays or zero-weight helpers.
