# A B dependent correction repairs the previous two source failures

Subtracting the maximum raw P reserve for the current B shape preserves universal DELETE and cancels the previous zero-double B failure. The resulting correction is unbounded and lies outside the prior scalar rotation-distance envelope class. It still fails full B repayment on the existing six-key helper, as proved in BN02.

## One explicit function on every finite pair

Use P from [RS01](../route_c_root_safe_matching_20261031_v001/RS01_DEFINITION_AND_TRANSPORT_LAWS.md) and J from [PE01](../route_c_p_envelope_correction_20261031_v001/PE01_EXPLICIT_CORRECTION_AND_DELETE.md). Define

    M(B)=max_{T on the same keys} P(T,B),
    Phi(A,B)=J(A,B)-M(B),
    R(A,B)=Phi(A,B)-P(A,B).

These finite maxima use only present same-key trees. There are no fitted labels, future accesses or unproved feasibility premises. Set all values to zero for n=0; n=1 has only one tree and also gives zero. Since P<=J<=M(B)<=n-1,

    -M(B)<=Phi<=0, R<=0.

The correction may be negative, which is permitted for a potential difference. Its range may grow with n. Increasing relabeling and key-order reflection preserve P, the rotation metric, J, M, Phi and R.

This normalization changes B differences, not just notation. The old nonnegative-coefficient scalar-distance envelopes are >=P>=0. The present Phi takes value -1 on the source family below and has a B-dependent subtraction. Hence it is outside that previously excluded class. This does not assert that every B-only subtraction works.

## Universal DELETE remains proved

B and its finite key set stay fixed during DELETE. Therefore M(B) has zero increment. The established one-Lipschitz A law for J gives

    |Phi(A',B)-Phi(A,B)|=|J(A',B)-J(A,B)|<=rho(A,A').

For an actual present-key source splay, rho(A,S_x A)<=d_A(x), so

    Delta_DELETE Phi<=d_A(x)<=2 ceil(d_A(x)/2)=2a.

This is a universal law for this SAME corrected potential, including root changes, arbitrary fringes and both orientations. A root access is a no-op. Subtracting an A-constant B value requires no new reweighting or eligibility assumption.

## Exact all-size repair of the registered drift and B zig

For n>=4 use

    A_n=1(empty,n(R_[2,n-1],empty)),
    T_n=n(1(empty,R_[2,n-1]),empty),
    B_n=2(leaf1,R_[3,n]), C_n=R_n.

The [exact all-auxiliary maxima and envelope identities](../route_c_p_envelope_correction_20261031_v001/PE02_EXACT_EXTREMA_AND_B_OBSTRUCTION.md) give

| Pair | P | J | M | Phi | R |
| --- | --- | --- | --- | --- | --- |
| (A_n,B_n) | 1 | n-3 | n-2 | -1 | -2 |
| (T_n,B_n) | n-2 | n-2 | n-2 | 0 | -(n-2) |
| (A_n,C_n) | 1 | n-2 | n-1 | -1 | -2 |

DELETE n changes the first pair to the second using one A zig. Thus Delta Phi=1<=2 and Delta R=-(n-4), cancelling the old unbounded n-3 drift. KEEP1 changes the first pair to the third, with a=q=0,z=1. Now Delta Phi=0, repairing the old envelope's +1 failure. R is genuinely unbounded because R(T_n,B_n)=-(n-2).

These identities are analytic for every n>=4, rather than extrapolated from finite controls. The n=6 matching/cover certificates and both reflected source operations are independently verified in this run. Repairing these two operations does not establish the full B law; the helper obstruction is a separate required test of this same Phi.
