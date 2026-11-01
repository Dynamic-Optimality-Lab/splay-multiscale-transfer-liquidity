# A root completion correction has exact universal B repayment

The explicit joint correction below retains unbounded reserve on equal-root pairs and satisfies the full root-conditioned B law exactly. It is not a complete source potential: CP02 proves a cheap DELETE failure for every odd size n>=7. Both universal laws remain required for Step 3.

## Definition by one source operation

For same-key finite BSTs let r=root(A). Define C_r(B)=S_r B by the ordinary present-key source splay and Q_r(B)=floor(d_B(r)/2), its number of doubles. Fix

    Phi(A,B)=F(A,C_r(B))+Q_r(B),
    R(A,B)=Phi(A,B)-P(A,B).

Here F is the exact proper-subtree disagreement function and P is the protected root-eligible matching potential. The completed B is a deterministic function of the current A root and current B tree. No auxiliary maximum, scalar metric envelope, B-only gauge, unknown selector, fitted potential label or future history defines the function. The correction is genuinely joint: the root determining the B completion comes from A, and F compares the entire A tree with that completed B tree.

The completion is ONLY a potential evaluation. In particular DELETE does not execute any B access, and its actual q=z=0 even when the potential's Q_r(B) is positive. Distinguish these two counts throughout the source accounting.

Set all values zero for n=0; n=1 also gives zero. For n>=1, 0<=Phi<=n-1+floor((n-1)/2), so the definition is finite. R is allowed to have either sign. Rank relabeling and key-order reflection preserve source completion, depth, F, P, Phi and R.

## Exact full B proof for all sizes and shapes

Freeze A rooted at x, and execute its required B access x. Put C=S_x B and q=floor(d_B(x)/2). By the source root property, root(C)=x. A second splay of x in C is a no-op and has zero doubles. Thus

    Phi(A,B)=F(A,C)+q,
    Phi(A,C)=F(A,C),
    Phi(A,S_x B)-Phi(A,B)=-q.

This is the full requested root-conditioned B bound, with equality, for every finite same-key pair and every present accessed A root. It includes both orientations, arbitrary fringes, overwritten histories, q=0 final zigs and the root no-op. It uses source idempotence rather than numerical evidence or an unproved compensation premise.

For a general KEEP x, the A phase first roots A at x; the same identity then applies to B. If the SAME Phi also satisfied universal DELETE, the whole source law would follow by addition. CP02 refutes that missing law; the B theorem cannot be combined with another function's A theorem.

## Equal-root reserve and unboundedness

If root(A)=root(B), completion is a no-op and Q=0. Hence Phi=F and

    R=F-P=mu_r.

Unlike the previous root-switch correction, R does not vanish just because the two roots agree. On the previously proved family

    A_n=1(empty,n(R_[2,n-1],empty)), B=R_n,

the [exact interval/matching calculation](../route_c_joint_alignment_correction_20261031_v001/JA02_EQUAL_ROOT_DELETE_AND_CLASS_OBSTRUCTION.md) gives F=n-2 and P=1. Therefore R=n-3, which is unbounded and meets the earlier necessary equal-root reserve condition. On identical-tree diagonals, F=P=0 and R=0; this is consistent because equal roots alone do not mean identical trees.

The fixed six-key member of that family now has Phi=4->4 under DELETE6, with R=3->-1. The prior starved helper KEEP2 has Phi=5->3 and R=1->1, paying q=2 exactly. These finite checks are not a universal DELETE proof.

## Existing whole-helper and vine consequences

Both input roots and both output roots agree at each endpoint of the established arbitrary-fringe whole helpers. Thus Phi=F at their endpoints. The [proved F helper estimate](../route_c_clade_correction_20261031_v001/CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md) gives nonincrease for both branches, uniformly in paired fringe size/shape and reflection. This is a whole-helper result; the separate B law is already proved universally above.

Every opposite-vine starved KEEP is directly covered by the exact B identity at every size: Delta Phi=-q. No new vine matching count is needed. These positive results concern this one function and do not remove the full original CD premise once its DELETE condition fails.

Sources are the pinned [tuple engine](../../../../python/independent/splay.py) and [pointer engine](../../../../python/liquidity/legacy_embedding.py). The actual same-side order is retained in both physical and potential-completion traces; no replacement by move-to-root rotations is made.
