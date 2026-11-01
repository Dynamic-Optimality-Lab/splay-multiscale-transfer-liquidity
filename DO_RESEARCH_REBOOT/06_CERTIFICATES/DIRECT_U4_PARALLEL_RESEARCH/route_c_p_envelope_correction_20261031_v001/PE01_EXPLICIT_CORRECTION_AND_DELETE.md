# An explicit unbounded correction restores DELETE

There is a determined unbounded correction R to P that cancels the root-changing DELETE drift and proves the full universal DELETE law. Its corrected potential J nevertheless fails full B repayment, even on a zero-double B zig. Both conclusions concern the same function.

## Definition on all sizes

Use the root-restricted protected matching potential P from [RS01](../route_c_root_safe_matching_20261031_v001/RS01_DEFINITION_AND_TRANSPORT_LAWS.md). For same-key BSTs let rho(A,T) be the undirected shortest-path distance using unit primitive rotations. This is finite: repeatedly rotate left children upward to convert any finite tree to a right vine, and reverse such paths to connect any two trees. For n>=1 define

    J(A,B)=max_{T on the same keys} [P(T,B)-rho(A,T)],
    R(A,B)=J(A,B)-P(A,B).

The maximum is finite and attained because there are finitely many trees on the fixed finite key set. The formula is explicit, with no fitted coefficients, unknown potential labels, future accesses or feasibility premise. Computational efficiency is not assumed. For n=0 define P=J=R=0; n=1 has only one tree and the same values.

Taking T=A gives J>=P, hence R>=0. The known subtree-disagreement function F is one-Lipschitz in A under primitive rotations and P<=F. Thus, for any auxiliary T,

    P(T,B)-rho(A,T) <= F(T,B)-rho(A,T) <= F(A,B).

Consequently P<=J<=F. This is a finite current-state construction and a proved comparison, not the old monotone scalar cap.

## Universal DELETE proof

For each fixed auxiliary T and B, triangle inequality gives

    |rho(A',T)-rho(A,T)|<=rho(A,A').

Every function P(T,B)-rho(A,T) is therefore one-Lipschitz in A, with the same constant. Taking the maximum preserves the bound:

    |J(A',B)-J(A,B)|<=rho(A,A').

An actual present-key source splay S_x uses exactly d_A(x) primitive rotations, two per double and one for an optional final zig. Hence

    Delta_DELETE J <= rho(A,S_x A) <= d_A(x)
                   <= 2 ceil(d_A(x)/2)=2a.

This holds for every finite same-key pair, every present key, arbitrary fringes, both orientations and root-changing accesses. A root access is a no-op. DELETE removes no BST nodes, so the key set and metric space stay fixed.

In fact J is the least one-Lipschitz majorant of P in A: if H>=P is one-Lipschitz, then H(A,B)>=P(T,B)-rho(A,T) for every T, hence H>=J. This minimality does not say that J preserves P's B differences. PE02 demonstrates the opposite.

## The correction is genuinely unbounded

For n>=4 put M=R_[2,n-1] and define

    A_n=1(empty,n(M,empty)),
    T_n=n(1(empty,M),empty),
    B_n=2(leaf1,R_[3,n]).

The known P drift family has P(A_n,B_n)=1 and P(T_n,B_n)=n-2. DELETE n changes A_n to T_n by one root zig. The exact extrema in PE02 prove

    J(A_n,B_n)=n-3, J(T_n,B_n)=n-2.

Therefore

    R(A_n,B_n)=n-4, R(T_n,B_n)=0,
    Delta_DELETE R=-(n-4), Delta_DELETE J=1.

As n grows, R has no size-independent bound. It cancels the old n-3 drift down to +1, within budget 2. This supplies the requested kind of unbounded DELETE correction, but not a correction satisfying both full laws: its B failure is proved next.

Rank relabeling and reflection preserve primitive rotation distance, P, J and R, so no orientation or key-spacing exception is hidden. The old [G-envelope failure](../route_c_potential_20261031_v001/SP03_ENVELOPE_LAW_AND_ALL_SIZE_REFUTATION.md) used a different raw reserve. The triangle method and alignment risk are inherited ideas; they are not claimed as new original-theorem progress. Here the exact global maxima of the present P yield the stronger coefficient obstruction in PE02.
