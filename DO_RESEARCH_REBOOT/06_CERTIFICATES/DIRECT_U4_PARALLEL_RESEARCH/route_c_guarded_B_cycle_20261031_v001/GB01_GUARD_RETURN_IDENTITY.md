# Exact upper-guard source recurrence

Status: PROVED—UNIVERSAL for the stated source identity on finite BSTs. This is an identity for B splaying, not an A/B repayment or strictness theorem.

Write a tree as T=r(U,V), where all U keys are below the guard r and all V keys are above it. The guard is above the queried subtree; V may be a nonempty unrequested fringe. Fix present x in U, let u be U's root and d=d_U(x). Apply S_x to T, then S_r. Same-side doubles use the source parent-first convention.

The exact double counts are

    q_x=ceil(d/2),
    q_r=1 if d is odd and x<u,
    q_r=0 otherwise.                           (1)

The final tree is r(H_x(U),V), where

    H_x(U)=S_x U, if d is even or x>u;
    H_x(U)=U^-_x, if d is odd and x<u.          (2)

Here U^-_x is the result of the inner local doubles, with the last local left zig omitted. If the complete local splay has shape x(A,u(B,C)), then

    U^-_x=u(x(A,B),C).                         (3)

This explicit inverse of the final local zig is only a way to compute the partial result. The global source operations remain exactly S_x followed by S_r.

## Even local depth

Let d=2k, including zero. The local path consumes k doubles and ends at x with no local final zig. In the global tree, those same local doubles occur first and leave the guard's one left frame unconsumed. Writing S_x U=x(A,B), the final global zig gives

    r(x(A,B),V) -> x(A,r(B,V)).

Returning to r is its inverse right zig, giving r(S_x U,V). Thus q_x=k and q_r=0. At d=0 both operations are single zigs and the whole round trip is the identity. This is a genuine zero-double boundary case.

## Odd local depth, toward the guard

Let d=2k+1 and x>u. After k inner local doubles, the remaining local shape is u(A,x(B,C)); the unconsumed root direction is right. The full local splay would finish with a right zig. In the global tree, the final two frames instead form an LR double:

    r(u(A,x(B,C)),V)
      -> x(u(A,B),r(C,V)).

Now r is x's right child. Its return is one right zig:

    x(u(A,B),r(C,V))
      -> r(x(u(A,B),C),V).

The left child is exactly S_x U. The query has k+1 doubles and the return has zero doubles, proving (1)-(2) in this case.

## Odd local depth, away from the guard

Let d=2k+1 and x<u. After k inner local doubles, the remaining local shape is u(x(A,B),C). The global final two frames are LL. The actual source parent-first LL gives

    r(u(x(A,B),C),V)
      -> x(A,u(B,r(C,V))).

The guard is now at depth two. Its source return is RR:

    x(A,u(B,r(C,V)))
      -> r(u(x(A,B),C),V).

The left subtree is U^-_x, with local root u retained. The query has k+1 doubles and the return has one double. This proves the remaining cases and (3).

All transformations carry arbitrary fringe trees A,B,C,V unchanged internally. No bound on local depth, tree size or fringe shape appears. Reflection exchanges left/right and gives the lower-guard version: the return has one double exactly at odd local depth with x above the local root, away from the lower guard.

## Surplus consequence

The return contributes no max(q-2,0), since q_r<=1. A query contributes exactly

    max(ceil(d/2)-2,0).                        (4)

In particular, odd local depth five supplies one surplus unit, unlike the unguarded floor(d/2) count. This is the source mechanism used in GB02's fixed construction, not a fitted parity correction.

The identity also explains why B surplus alone does not settle later A coupling. The guard is the pre-query B root and is shallow on return, making it an available old-UD payer. GB03 records that necessary scope audit separately.
