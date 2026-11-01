# A contained subtree terminal function supplies the parity comb drop

The explicit terminal function below supplies the required unbounded drop on the previous parity-comb obstruction and has exact universal B repayment through completion. It does not satisfy both source bounds: CT02 refutes its completed DELETE bound on another explicit family.

## Definition

For same-key BSTs A,C let C0 be their distinct proper nonempty subtree intervals. Force every exact common pair I--I and remove those vertices. Write c for their number and F=n-1-c. On the residual bipartite graph allow I--J exactly when

    J is a strict subset of I, and min(J)=min(I) or max(J)=max(I).

Here I is an A interval and J is a C interval. Let beta be the maximum matching size and define

    D(A,C)=F(A,C)-beta(A,C).

There is no antichain constraint. The direction of containment is fixed. Exact pairs are counted first, rather than rejected for failing strict containment. D is a finite explicit joint function, with 0<=D<=F. It is invariant under rank relabeling and reflection of the key order. Define D=0 for n=0,1. Identical trees have D(A,A)=0.

This restriction distinguishes the old source and destination coupons structurally: in the parity-comb source, every residual B coupon contains the inaccessible extreme n and cannot fit inside any remaining A interval. At the destination the nested B suffixes fit inside larger A suffixes and all can be matched. Merely selecting minimum versus maximum endpoint matches would not provide this reflection-invariant distinction.

## Uniform fixed-C stability

A primitive A rotation replaces exactly one proper subtree interval J by L, preserving every other interval. Consider an old optimum including forced exact pairs and beta residual edges. Remove any edge at left J, losing at most one. All retained edges remain valid, including their containment condition, because neither endpoint changes.

If L is not a C interval, no new forced pair is required and the retained matching is feasible. If L is a C interval, force L--L. If right L was used by one residual edge, remove that edge first. Adding the forced pair then has net cost at most zero. It cannot interfere with an unchanged forced pair because L was absent from the old A interval collection. No other residual matching condition exists.

Thus the new protected rank c+beta is at least the old rank minus one. Applying the same argument to the inverse rotation gives

    |D(A_after,C)-D(A_before,C)|<=1.

This is PROVED—UNIVERSAL for arbitrary fixed C, all sizes, both rotation orientations and arbitrary fringes. It does not establish the completed function's DELETE bound when the A root changes.

## One completed potential and its exact B law

For r=root(A), put

    Phi(A,B)=D(A,S_r B)+Q_r(B),
    Q_r(B)=floor(d_B(r)/2).

Completion uses the actual pinned bottom-up source splay. During DELETE it is only an evaluation; physical B remains fixed and actual q=z=0. Empty-tree values are zero.

When A is rooted at x and B actually splays x, let C=S_x B and q=Q_x(B). Both potential endpoints have the same terminal pair (A,C). At the destination the completion is a no-op and Q=0. Hence

    Phi(A,S_x B)-Phi(A,B)=-q.

This is PROVED—UNIVERSAL for all finite same-key pairs. It includes arbitrary-fringe helpers, overwritten histories, root no-ops, zero-double zigs and all source double cases. The proof needs no finite fit or new exchange theorem.

## All odd parity-comb values

Use the established family from [RB01](../route_c_root_step_refutation_20261031_v001/RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md). Let n=2m+1>=7. The middle M_n has right spine 3,5,...,n-2, preceding even singleton left children, and final leaf n-1. Its full subtree intervals are

    [e,n-1], even e=2,4,...,n-3;
    {e},     even e=2,4,...,n-1.

Put A_n=1(empty,n(M_n,empty)), B=R_n and T_n=n(1(empty,M_n),empty). DELETE n is one A root zig with budget 2.

At the source the only exact common proper interval is [2,n], so F=n-2. Every remaining B interval contains n; every remaining A interval lies inside [2,n-1]. No B interval is contained in an A interval. Therefore beta_source=0 and

    D(A_n,R_n)=n-2=2m-1.

At the destination complete B to V_n=S_n R_n. Its proper intervals are [1,n-1], {1}, and [j,n-1],{j} for odd j=3,5,...,n-2. Only [1,n-1] is common, again giving F=n-2. Residual B singletons have odd endpoints, whereas every residual A endpoint is even, so all those singletons are isolated.

Exactly m-1 residual B vertices can have edges: the suffixes [j,n-1] for odd j=3,5,...,n-2. Each is contained in the distinct A interval [j-1,n-1] and shares its maximum endpoint. Those m-1 edges form a matching; the same m-1 right vertices cover every edge. Consequently

    beta_destination=m-1,
    D(T_n,V_n)=m.

The terminal difference is

    m-(2m-1)=1-m <= 2-m=-(n-5)/2.

It supplies the required unbounded drop, with one unit to spare. Completion Q changes 0->m, so this family's completed DELETE increment is exactly 1 at every odd n>=7. Reflection gives the opposite orientation.

At seven keys the exact values are (F,beta,D)=(5,0,5)->(5,2,3), Q=0->3 and Phi=5->6. The independent pointer verifier checks this member and its reflection with matching/cover certificates. The all-size conclusion follows from the complete interval proof, not extrapolation from those two local rows.

On the same equal-root source, the prior protected root-safe P has value m. Thus this formula also retains an unbounded correction reserve Phi-P=m-1 there. That component fact does not rescue the false universal DELETE bound proved in CT02.
