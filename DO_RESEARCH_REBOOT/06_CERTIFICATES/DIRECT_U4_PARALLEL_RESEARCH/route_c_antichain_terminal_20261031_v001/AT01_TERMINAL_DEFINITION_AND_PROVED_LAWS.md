# A disjoint subtree terminal potential beyond scalar F

The explicit terminal function below distinguishes the two completed pairs that defeated scalar F, retains unbounded equal-root reserve and gives exact full B repayment through source completion. Universal DELETE for the completed potential remains unproved. This audit does not claim both required bounds.

## Terminal function

For arbitrary same-key finite BSTs A,C, let C0 denote distinct proper nonempty node-rooted subtree key sets, represented by rank intervals. Fix all exact common pairs I--I. Write c for their count and F=n-1-c. Remove those vertices, leaving the usual equal-minimum-or-equal-maximum endpoint graph.

Let alpha(A,C) be the largest cardinality of a residual matching with the additional requirement that its selected RIGHT C intervals are pairwise disjoint. Since C intervals are laminar, this is exactly an antichain under containment. Left and right matched vertices must still be distinct. The disjointness condition applies ONLY to residual nonexact right intervals. Forced exact pairs remain counted without being subject to that antichain restriction.

Define

    K(A,C)=F(A,C)-alpha(A,C).

The empty residual matching is feasible, so K is a finite explicit present-pair function. Let mu be the unrestricted residual rank used by Ehat. Then alpha<=mu and

    Ehat<=K<=F.

No coefficient, unknown potential label or feasibility premise defines alpha. This is global coupon allocation: different A features cannot reuse a B vertex, and nested residual B coupons cannot both be counted. The actual interval geometry matters. On the seven-key former obstruction, the two terminal pairs both have F=5, but their K values are5 and3, so K is not f_7(F) for ANY scalar function f_7.

For n=0 set K=0; n=1 has empty proper collections and K=0. On identical trees K(A,A)=0 because all proper sets are fixed exact pairs. Rank relabeling and reflection preserve the graph, disjointness, alpha and K.

## Universal fixed-C A stability

One primitive A rotation replaces exactly one proper interval J by a new interval L, retaining every other interval and the full key set. This is the pinned [source interval identity](../route_c_clade_correction_20261031_v001/CC01_SOURCE_ROTATION_IDENTITY.md). Consider an old optimum consisting of its forced exact pairs and its residual antichain matching, with total rank c+alpha.

Delete the edge at left J if it exists, losing at most one. Every unchanged forced pair remains valid, and removing a residual matching edge preserves right disjointness. If new L is not a C interval, no new forced pair is required and the retained matching is already feasible.

If L is a C interval, add the new forced edge L--L. Its right vertex may have been used by at most one old residual edge; remove that edge first. It cannot have been an unchanged forced pair, because L was absent from the old A collection. Removing that residual edge and inserting the forced pair has net cardinality change at least zero. The remaining residual right intervals retain their antichain property. The newly forced pair is exempt from that property, as required by the definition.

Thus the new total protected rank is at least the old rank minus one. Apply the same construction to the inverse rotation to obtain the reverse inequality. Since K=n-1-(c+alpha),

    |K(A_after,C)-K(A_before,C)|<=1.

This holds for every primitive A rotation, arbitrary C, all fringes, sizes and orientations. It includes changes in the forced exact set. It is a terminal stability theorem with C fixed, not yet the completed potential's DELETE law.

## Completed joint correction and full B law

For r=root(A), put C_r(B)=S_r B and Q_r(B)=floor(d_B(r)/2), using the actual ordinary source splay. Define

    Phi(A,B)=K(A,C_r(B))+Q_r(B),
    R(A,B)=Phi(A,B)-P(A,B).

This is one explicit joint correction beyond the scalar-F terminal family. Completion is a current-state evaluation, not an actual B operation during DELETE. Actual DELETE still has q=z=0. Define Phi=R=0 at n=0; n=1 also has zero values. For every finite pair the function is finite, with 0<=Phi<=n-1+floor((n-1)/2).

If A is rooted at x and B actually splays x, both potential endpoints use the same completed tree C=S_x B. At the source the completion count is q; at the destination root(C)=x makes the next completion a no-op with count0. Therefore

    Phi(A,S_x B)-Phi(A,B)=-q

for every finite pair, all shapes, fringes and both orientations. This is PROVED—UNIVERSAL for the full root-conditioned B law. It does not depend on finite audit survival.

On equal-root pairs completion is a no-op. Since P=F-mu there,

    R=mu-alpha>=0.

The right-vine-middle family in AT02 has R=n-4, proving retained reserve and unboundedness. R need not be nonnegative on other pairs; the six-key control has a destination correction of-1. Identical-tree diagonals still have R=0.

## What is not yet proved

K's fixed-C A law does not by itself prove DELETE for Phi: an A-root change replaces C_r(B) by C_x(B) and changes Q. The exact remaining root-step obligation is given in AT02. Arbitrary-fringe whole-helper safety for the new K is also not inherited merely from Ehat<=K<=F; the old before/after bounds for Ehat or F cannot be transferred across functions. Only the frozen empty-fringe helper controls are finite-exact here.
