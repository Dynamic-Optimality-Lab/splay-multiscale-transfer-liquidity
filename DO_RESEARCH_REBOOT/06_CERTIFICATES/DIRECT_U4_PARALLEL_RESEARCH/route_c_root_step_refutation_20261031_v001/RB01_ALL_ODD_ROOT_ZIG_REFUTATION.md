# The universal antichain root step bound is false

The fixed completed antichain potential has a legal A-root zig with increment3 at seven keys, against the proposed bound2. An exact family gives increment(n-1)/2 for every odd n>=7. This refutes the universal zig/double statement and the candidate's universal DELETE law; separate classification of doubles is unnecessary and is not claimed.

## Unchanged candidate

Use exactly the [AT terminal definition](../route_c_antichain_terminal_20261031_v001/AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md). All exact common proper-subtree pairs are forced. Among residual endpoint matchings, alpha is the maximum cardinality with selected RIGHT intervals pairwise disjoint. Forced exact pairs are exempt. Put

    K=F-alpha,
    Phi(A,B)=K(A,S_root(A) B)+Q_root(A)(B),
    Q_r(B)=floor(d_B(r)/2).

No coefficient, antichain constraint, source operation or definition is altered here. The previous fixed-C stability and exact universal B law remain true component results.

## Explicit odd family

Let n=2m+1, m>=3. Construct M_n on keys2,...,n-1 with odd-key right spine3,5,...,n-2, each having its preceding even singleton as left child, and with final right leaf n-1. Equivalently start with leaf(n-1) and, for odd k=n-2,n-4,...,3, replace the tree by k(leaf(k-1),tree).

Its complete nonempty subtree intervals are

    [e,n-1] for even e=2,4,...,n-3,
    {e}     for even e=2,4,...,n-1.

Every endpoint is even. The counts are(m-1)+m=n-2 distinct intervals, including the full middle set [2,n-1]. Use

    A_n=1(empty,n(M_n,empty)), B=R_n,
    T_n=n(1(empty,M_n),empty).

DELETE n changes A_n to T_n by one root zig. Thus d_A(n)=1,a=1 and actual q=z=0; the required bound is2. B stays R_n. The potential completion at the source is a no-op because both roots are1. At the destination it is V_n=S_n R_n, with Q=m. This completion is an evaluation of the potential, not a physical B operation on the DELETE edge.

## Source terminal: F=n-2 and alpha=1

The proper A_n intervals are [2,n] together with all intervals of M_n. Proper R_n intervals are [k,n],2<=k<=n. Their only common interval is [2,n], so F_source=n-2.

After fixing that pair, all residual B vertices are suffixes [k,n],3<=k<=n, a single nested chain. No antichain matching can select more than one such right interval. The edge

    A{n-1} -- B[n-1,n]

exists through its equal minimum endpoint and attains one. Therefore alpha_source=1 and K_source=n-3.

For clarity, the ordinary unrestricted residual rank is m-1: the nonzero right neighbors are exactly [e,n] for even e=4,6,...,n-1. Match each of them to A{e}; those right vertices also form a cover of all residual edges. Hence P_source=(n-2)-(m-1)=m.

## Destination terminal: the same F, alpha and K

The actual A destination has proper intervals [1,n-1] together with all intervals of M_n. The source-exact odd-vine RR recurrence gives

    C0(V_n)={[1,n-1],{1}}
             union {[j,n-1],{j}: j=3,5,...,n-2 odd}.

The sole common interval is [1,n-1]. Every other A endpoint is even, whereas the B singleton endpoints are odd. Thus residual B singletons, including {1}, are isolated in the endpoint graph. The only B vertices with neighbors are [j,n-1], j odd3,...,n-2: they form ONE nested chain, matched via the common maximum n-1.

An antichain matching therefore has size at most one. The edge

    A[2,n-1] -- B[3,n-1]

attains that bound. Consequently

    F_destination=n-2, alpha_destination=1,
    K_destination=n-3=K_source.

No larger finite fit or auxiliary-tree enumeration is used: these are complete interval lists and an exact global upper/attaining-edge argument for every odd n in the stated family.

## Violated source inequality

The potential values are

    Phi_source=n-3,
    Phi_destination=n-3+m,
    Delta_DELETE Phi=m=(n-1)/2>2.

This is a root-depth-one access with one A StepEv. Thus it is a direct counterexample to the universal A-root zig/double bound and to universal DELETE for this SAME Phi. Reflection gives the other zig orientation. No conclusion about the double-only subproblem is needed or claimed.

The raw actual destination has P=n-1=2m because every proper R_n interval contains the new A root n and is ineligible. The correction R=Phi-P is therefore m-2 at BOTH endpoints. It is unbounded on this family but does not drop during the failed zig. The retained equal-root reserve does not by itself establish repayment.

The source coupons use equal minima and the destination coupons use equal maxima. The antichain count assigns each chain the same discount1, leaving the completion-charge jump unpaid. This identifies the failed mechanism; it is not a proposed replacement correction.

## Same-witness scalar consequence and scope

For any finite scalar function f_n, the form f_n(K(A,S_root(A) B))+Q_root(A)(B) has the same f_n argument n-3 at both endpoints. Its increment is still m. Hence scalar reparametrization of this K within the same completion form cannot repair the root bound.

This does not exclude different joint terminal functions, modified coupon mechanisms or general potentials. It does not refute Coarse-Double. It refutes the fixed AT candidate, whose valid B and fixed-C laws cannot compensate for its false DELETE bound.
