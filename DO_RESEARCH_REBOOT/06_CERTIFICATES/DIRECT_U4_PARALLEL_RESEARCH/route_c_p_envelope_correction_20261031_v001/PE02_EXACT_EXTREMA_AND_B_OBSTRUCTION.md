# Exact extrema show the correction loses B repayment

The corrected reserve J rises by one on a whole KEEP with no A work and no B double. Exact global maxima over all auxiliary trees prove this for every n>=4. The same two source operations exclude every nonnegative rotation-distance coefficient, even if chosen separately for each size.

## Four exact P evaluations

For n>=3 use A_n,T_n,B_n from PE01 and put C_n=R_n. The [prior matching/cover calculation](../route_c_root_safe_matching_20261031_v001/RS03_UNBOUNDED_DELETE_OBSTRUCTION.md) gives

    P(A_n,B_n)=1, P(T_n,B_n)=n-2.

For C_n, its proper intervals are [k,n],2<=k<=n. The proper A_n intervals are [2,n] and [k,n-1],2<=k<=n-1. Exactly [2,n] is common; fix it. All B intervals are eligible because root(A_n)=root(C_n)=1. The remaining endpoint edges are precisely

    [k,n-1]--[k,n], 3<=k<=n-1.

These n-3 disjoint edges, and their right endpoints as a cover, prove residual rank n-3. Hence P(A_n,C_n)=(n-2)-(n-3)=1. The formula includes n=3, when the residual edges are empty.

Every proper T_n interval ends at n-1. Every proper C_n interval ends at n, so there are no exact pairs. All proper C_n intervals contain root(T_n)=n and are ineligible. Thus

    P(T_n,C_n)=n-1.

These four evaluations have direct complete matching/cover certificates at n=6 and after reflection. Their all-size proof is the displayed interval argument, not finite extrapolation.

## Global maxima over every auxiliary tree

For ANY tree U on these keys, the total protected matching rank at (U,B_n) is at least one. If there is an exact pair this is immediate. Otherwise consider two cases.

* If root(U)!=1, key 1 lies in a proper U subtree I with minimum 1. The proper B_n interval {1} is eligible because it excludes root(U). Since there are no exact pairs, I--{1} is a legal residual endpoint edge.
* If root(U)=1, key n lies in a proper U subtree I with maximum n. The proper B_n interval {n} is eligible because n!=1. Again I--{n} is a legal residual endpoint edge when there are no exact pairs.

Thus in every case P(U,B_n)<=n-2. The evaluated T_n attains equality. The general range bound P<=n-1, together with P(T_n,C_n)=n-1, similarly gives

    max_U P(U,B_n)=n-2,
    max_U P(U,C_n)=n-1.

The proof covers all auxiliary root labels and all internal shapes. It uses no classification or enumeration of auxiliary trees.

## Exact envelope values

The distinct trees A_n,T_n differ by the one root zig DELETE n. Therefore rho(A_n,T_n)=1: the zig gives an upper bound of one, and distinct trees give the matching positive-integer lower bound. For any nonnegative real lambda define

    J_lambda(A,B)=max_U[P(U,B)-lambda rho(A,U)].

At A_n the self candidate U=A_n has value 1, and every different U has distance at least one. The two global maxima above are each attained at the one-rotation neighbor T_n. These upper bounds and attaining witnesses prove exactly

    J_lambda(A_n,B_n)=max(1,n-2-lambda),
    J_lambda(A_n,C_n)=max(1,n-1-lambda).

At T_n the global maximum for B_n is already attained by the self candidate, so

    J_lambda(T_n,B_n)=n-2.

All three identities hold for every n>=3 and every nonnegative real lambda. No parameter is fitted. The fixed correction uses lambda=1; for n>=4 the first two values are n-3 and n-2.

## A whole zero-double KEEP refutes the fixed correction

KEEP 1 from (A_n,B_n) leaves A_n unchanged. In B_n, key 1 is the root's left child. One left-oriented ZIG produces C_n=R_n. Thus

    a=0, q=0, z=1,
    J(A_n,C_n)-J(A_n,B_n)=1>0=2a-q, n>=4.

Root(A_n)=1 is the accessed key throughout. This is the full source KEEP law, not a stronger optional micro-step condition. Although P stays 1->1, R increases n-4->n-3. The extra reserve uses an auxiliary tree rooted at n; the actual B zig makes that auxiliary reserve larger. The correction has regained DELETE control by losing the target-conditioned B guarantee.

It is enough to fail q=0: full repayment requires nonincrease even when no double is charged. The reflected access gives the other orientation.

## No size-dependent coefficient can satisfy both laws

At the SAME size n>=6 and SAME source pair, DELETE n requires

    (n-2)-max(1,n-2-lambda)<=2.

Since n-4>=2>1, this forces n-2-lambda>=n-4, or lambda<=2. In contrast, the zero-double KEEP 1 requires

    max(1,n-1-lambda)<=max(1,n-2-lambda).

If n-1-lambda>1, it strictly exceeds both terms on the right. Hence this requires lambda>=n-2. At n=6 the necessary bounds are already

    lambda<=2 AND lambda>=4,

an exact contradiction. No nonnegative lambda works at this single size. Allowing an arbitrary coefficient lambda_n for each n cannot repair it. The proof is a same-witness algebraic corollary, not a numerical sweep or a new finite fit.

The excluded class is precisely max_U[P(U,B)-lambda_n rho(A,U)] with nonnegative coefficients. It does not exclude other penalties, nonminimal majorants, B-dependent corrections or all unbounded structural potentials. The universal DELETE theorem for lambda=1 remains true; the full candidate is refuted because its B law fails. Universal Coarse-Double remains open.
