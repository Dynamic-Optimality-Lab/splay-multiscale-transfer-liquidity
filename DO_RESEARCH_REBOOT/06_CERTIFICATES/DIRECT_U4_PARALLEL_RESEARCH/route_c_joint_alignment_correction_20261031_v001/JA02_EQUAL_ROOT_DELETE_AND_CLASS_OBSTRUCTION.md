# Equal roots can still require an unbounded correction reserve

One A zig from an equal-root pair refutes the explicit joint correction. The same family excludes every nonnegative joint correction that vanishes on all equal-root pairs. Equal roots here do not mean the two trees are identical.

## All-size source family

For n>=3 put

    A_n=1(empty,n(R_[2,n-1],empty)),
    C_n=R_n,
    T_n=n(1(empty,R_[2,n-1]),empty).

A_n and C_n are different trees with the SAME root1. DELETE n changes A_n to T_n by one root zig, leaving C_n frozen. Hence a=1 and q=z=0; the budget is2.

The complete proper intervals are

    C0(A_n)={[2,n]} union {[k,n-1]:2<=k<=n-1},
    C0(T_n)={[1,n-1]} union {[k,n-1]:2<=k<=n-1},
    C0(C_n)={[k,n]:2<=k<=n}.

At the source exactly [2,n] is common. Fix it. The residual endpoint edges are precisely [k,n-1]--[k,n], 3<=k<=n-1. The n-3 disjoint edges and their right endpoints as a cover prove residual rank n-3. Root(A_n)=root(C_n)=1 makes every proper B interval eligible. Thus

    F_source=n-2, mu_r_source=n-3, P_source=1.

At the destination, no proper intervals are common: every T_n interval ends at n-1, while every C_n interval ends at n. All proper C_n intervals contain root(T_n)=n and are ineligible, so

    F_destination=n-1, mu_r_destination=0,
    P_destination=n-1.

The joint correction is zero at the source because the roots agree, and zero at the destination because mu_r=0. Therefore

    H_source=1, H_destination=n-1,
    Delta_DELETE H=n-2.

Every n>=5 violates budget2. Reflection gives the other orientation. This is an exact all-size interval/matching proof, not a larger finite fit. Equivalently the boundary formula in JA01 has Delta F=1 and old discount n-3, giving the same n-2 jump.

## Consequence for arbitrary joint corrections

For ANY correction R satisfying the universal DELETE bound for P+R, the same family forces

    R(T_n,C_n)-R(A_n,C_n)<=4-n.

Suppose additionally R is nonnegative on all pairs. Then R(T_n,C_n)>=0 implies

    R(A_n,C_n)>=n-4.

Thus a nonnegative valid correction must carry an unbounded reserve on these internally different, equal-root pairs. In particular no nonnegative correction that vanishes on EVERY equal-root pair can work: its source correction would be0 and its destination correction nonnegative, giving an increment at least n-2.

This excludes that explicitly stated normalization class, regardless of how richly R depends on the two trees. It is not an exclusion of signed joint corrections. If R is allowed to be negative, a zero source correction would instead require a destination value at most4-n. Nor does the result forbid R(A,A)=0 on identical-tree diagonals: the source A_n!=C_n is not diagonal. Nonnegativity and equal-root vanishing are candidate-class assumptions, not additional requirements of original CD.

The necessary family inequality is a constraint on any proposed R, not a newly assumed compensation theorem or a construction of R. No original proof obligation is discharged by merely writing it.

## Reachability at six keys and actual closure

Start diagonally at B_6=2(leaf1,R_[3,6]). The already certified prefix D4 D6 D3 D6 D1 reaches (A_6,B_6). KEEP1 leaves A_6 fixed and splays B_6 into C_6=R6. This reaches the new equal-root input pair. The following DELETE6 is the failure, with

    a=1, q=z=0, P=1->5, R_joint=0->0,
    H=1->5, Delta H=4>2.

The complete actual closed word is

    D4 D6 D3 D6 D1 K1 D6 K1 K2 K3 K4 K5 K6 K5 K4 K3 K2 K1 K2.

The failed DELETE6 is zero-based position6. Common ascending and descending accesses synchronize the trees at R6; the final KEEP2 returns both to B_6. Independent replay gives

    A_total=20, Q_B=0, Z_B=12.

This is not a Coarse-Double counterexample. No new search is needed, and no potential labels are claimed on other closed-replay states. The [certificate](joint_alignment_certificate.json) and [independent audit](independent_audit.json) bind every local graph, event, cost, source-state sharing and physical paired endpoint.
