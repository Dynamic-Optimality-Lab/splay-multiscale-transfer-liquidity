# A fully fringed spine defeats the completed contained terminal potential

The same Phi from CT01 has an unbounded one-zig DELETE increment on the family below. This refutes its universal DELETE law on the stated domain of all finite same-key pairs. No diagonal reachability or actual closed-walk counterexample is claimed.

## A minimum-group identity for one terminal shape

Fix A=n(R_[1,n-1],empty) and C=n(U,empty), with U any BST on 1,...,n-1. Put p=n-1. The proper A intervals are exactly I_k=[k,p], 1<=k<=p. Every proper C interval is a subtree interval J=[a,b] of U.

If b=p, J=I_a is an exact forced pair. If b<p, a residual contained-endpoint edge can only go to I_a: equality of maximum endpoints is impossible, and equality of minimum endpoints requires k=a. Each minimum group therefore contributes exactly one to the protected total c+beta. Prefer the forced suffix if it exists; otherwise choose any interval of that minimum and match it to its I_a. Distinct groups use distinct A vertices, and no group can contribute more than one.

The distinct subtree minima of U are precisely the keys of nodes with no left child. Every subtree minimum is its leftmost node; conversely such a node is the minimum of its own subtree. If ell(U) counts nonempty left-child links, U has p-ell(U) nodes with no left child. Hence

    D(n(R_[1,n-1],empty), n(U,empty))=ell(U).       (1)

This identity includes forced exact pairs and arbitrary U. It is not an assumption about a future matching witness.

## Explicit all-size adversary

Let n=2m with m>=7. Define H_n by its even right spine 2,4,...,n, with left singleton leaves 1,3,...,n-1 and empty final right subtree:

    H_n=2(leaf1,4(leaf3,...,n(leaf(n-1),empty))).

Use the actual pair

    A_n=1(empty,n(R_[2,n-1],empty)), B=H_n.

DELETE n gives

    T_n=n(1(empty,R_[2,n-1]),empty)
       =n(R_[1,n-1],empty).

The A access has depth 1, a=1, one right zig. Actual B is unchanged, actual q=z=0, and the required potential budget is 2.

## Source terminal has D=m-1

The source A root is 1, at B depth 1. Its completion C_1=S_1 H_n is one left zig, with Q_1=0. Its proper intervals are

    [2,n];
    [2i-1,n], i=2,...,m;
    {2i-1},  i=2,...,m.

The A_n proper intervals are [2,n] together with all suffixes [k,n-1], 2<=k<=n-1. Exactly [2,n] and {n-1} are common, so F=n-3=2m-3.

Every residual C_1 interval containing n is too large to be contained in a residual A interval, all of which end at n-1. The only nonisolated residual right vertices are the singletons j=3,5,...,n-3. Match each {j} to [j,n-1]. These m-2 distinct right vertices also cover every edge. Thus

    beta_source=m-2,
    D(A_n,C_1)=m-1,
    Phi(A_n,H_n)=m-1.                              (2)

## Destination terminal has the same D

Access n in H_n at depth m-1. Its source doubles are all RR, with an additional right zig exactly when m-1 is odd. During each bottom-up RR group the local shape is

    g(U,p(V,n(W,Z))) -> n(p(g(U,V),W),Z).

The surviving ancestors g,p retain their original nonempty odd singleton left fringes U,V. The target n begins with nonempty W=leaf(n-1), and rebuilding keeps W nonempty. All three changed nodes have a nonempty left child both before and after. The fringes themselves are unchanged. Thus each RR group preserves the global left-link count ell.

If a final right zig occurs, p(U,n(W,Z))->n(p(U,W),Z), with U,W nonempty. It also preserves ell: two nonempty left-child links before and after. This uses the actual source parent-over-grandparent same-side order.

Initially ell(H_n)=m. Therefore C_n=S_n H_n still has ell(C_n)=m. Its root n has a nonempty left subtree U_n, so ell(U_n)=m-1. Applying (1),

    D(T_n,C_n)=m-1.                                (3)

The completion count is Q_n(H_n)=floor((m-1)/2). Combining (2) and (3),

    Delta_DELETE Phi=floor((m-1)/2)>2, m>=7.        (4)

The increment is unbounded while A always performs one zig. Reflection preserves the formula and gives the other orientation. The candidate therefore cannot provide both universal source bounds.

## Exact fourteen-key witness

Take m=7, n=14. H_14 has right spine 2,4,6,8,10,12,14 and preceding odd left leaves. The completed destination is

    14(4(2(1,3),8(6(5,7),12(10(9,11),13))),empty),

where omitted leaf children are empty. Its total left-link count is 7; its left subtree has 6. The dual-certified terminal values are

| Endpoint | F | beta | D | completion Q | Phi |
| --- | ---: | ---: | ---: | ---: | ---: |
| Source | 11 | 5 | 6 | 0 | 6 |
| Destination | 9 | 3 | 6 | 3 | 9 |

DELETE14 has a=1, actual q=z=0. Its increment is 3 against budget 2. The source completion has one zero-double zig; the destination completion has three RR doubles. Both orientations are independently replayed using the pointer source, with all eight terminal matching/cover equalities checked across the repair and counterexample rows.

This is one analytically derived witness at 14 keys, not a size sweep, potential fit, or larger state graph. The all-size failure follows from (1)-(4). As a direct cancellation corollary, any exact-completion form f_n(D(A,S_r B))+Q_r(B) has the same failure because its two D arguments are identical. No scalar function is fitted or tested.

## Limits of the conclusion

The claimed universal formula is quantified over all same-key pairs, and the displayed transition lies in that domain. A new diagonal-reachability theorem for this counterfamily was not established or assumed. No actual closed paired walk or CD counterexample follows from this local refutation.

Unlike the old parity-comb source, these physical source roots differ: A is rooted at 1, B at 2. The weaker B law may allow positive off-terminal slack at this source. Therefore the result does not exclude every weak-B extension with this equal-root terminal boundary; it excludes the stated exact-completion function and its scalar reparametrizations. Arbitrary other terminal functions, generic Step 3, and CD remain OPEN.
