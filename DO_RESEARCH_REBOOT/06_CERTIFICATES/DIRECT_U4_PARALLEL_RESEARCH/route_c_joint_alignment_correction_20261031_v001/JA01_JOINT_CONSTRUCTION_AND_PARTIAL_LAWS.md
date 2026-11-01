# A joint correction based on paired root alignment

This is an explicit unbounded correction using both tree structures and their root relation. It pays the earlier registered failures, but a DELETE that breaks equal-root alignment refutes its full source law. Both universal bounds remain required; the partial laws below are not a substitute.

## One fixed function

Use P=F-mu_r from [RS01](../route_c_root_safe_matching_20261031_v001/RS01_DEFINITION_AND_TRANSPORT_LAWS.md), where r=root(A), exact common proper-subtree pairs are fixed and mu_r is the maximum residual endpoint-matching rank using only B intervals excluding r. Put

    tau(A,B)=indicator(root(A)=root(B)),
    R_joint(A,B)=(1-tau) mu_r(A,B),
    H(A,B)=P(A,B)+R_joint(A,B)=F(A,B)-tau mu_r(A,B).

When the roots agree, no proper B interval contains r, so mu_r equals the unrestricted protected residual rank defining Ehat. Therefore the equivalent complete definition is

    H=Ehat when root(A)=root(B),
    H=F    when root(A)!=root(B).

This is one function on the current pair. It is not selected differently per operation. It uses no auxiliary-tree envelope or B-only subtraction, and has no unknown labels or existence premise. Set P=R_joint=H=0 for n=0; the one-key case is also zero. In general R_joint>=0 and Ehat<=H<=F.

On the old family (A_n,B_n), R_joint=n-2, so the correction is unbounded. The construction lies outside the earlier scalar-envelope class: H(A_n,B_n)=n-1, while max_T P(T,B_n)=n-2 and every nonnegative scalar-penalty envelope is at most that maximum. Nor is it the old J plus a B-only gauge: at fixed B_n the pairs A_n,T_n have equal H but J values differing by one. The function is defined directly by the paired root and matching data.

Reflection preserves root equality, interval endpoints, matching rank and source splays; increasing rank relabeling also preserves every value. No root-label spacing assumption is used.

## Exact DELETE boundary classification

The [source interval identity](../route_c_clade_correction_20261031_v001/CC01_SOURCE_ROTATION_IDENTITY.md) gives |Delta F|<=1 under one A primitive rotation, hence |Delta_DELETE F|<=d_A<=2a for a whole present-key splay.

If the input roots differ, H_source=F_source and H_destination<=F_destination, independently of whether the destination roots agree. Therefore

    Delta_DELETE H<=Delta_DELETE F<=d_A<=2a.

This proves the full DELETE law on that explicitly restricted input class, for arbitrary size, shape and fringes. A root access is a no-op. It is not universal DELETE.

If the input roots agree and a nonroot x is accessed, the destination A root is x and differs from the frozen B root. Thus the exact endpoint identity is

    Delta_DELETE H=Delta_DELETE F+mu_r(A,B).

The old matching discount is removed when alignment is broken. This is the unresolved boundary; JA02 refutes its uniform bound on an all-size family. For root-preserving primitive A rotations, the branch remains fixed and either the F or the Ehat one-Lipschitz law applies, but that restricted fact cannot control the alignment-breaking endpoint jump.

## Old root-drift and zero-double repairs

For n>=4 write

    A_n=1(empty,n(R_[2,n-1],empty)),
    T_n=n(1(empty,R_[2,n-1]),empty),
    B_n=2(leaf1,R_[3,n]), C_n=R_n.

The already proved matching identities give P(A_n,B_n)=1, mu_r=n-2, P(T_n,B_n)=n-2 and mu_r=1. Both pairs have different roots, so H=n-1 at both. The original single-zig DELETE n has Delta H=0; its n-3 excess is cancelled exactly by Delta R_joint=-(n-3).

The old zero-double KEEP1 changes (A_n,B_n) to (A_n,C_n) with a=q=0,z=1. The destination roots agree and P=Ehat=1. Consequently H changes n-1->1, paying this requirement. These identities hold at every n>=4; they are not inferred from six-key samples.

## Existing uniform helper and vine laws

For every established arbitrary-fringe whole helper in [FX03](../route_c_fixed_exact_pairs_20261031_v001/FX03_ARBITRARY_FRINGE_HELPER_PROOF.md), both roots agree at each whole-access endpoint. H therefore equals Ehat at both endpoints. The exact L change is 0, and the R change is in {-2,-1}, uniformly in arbitrary paired fringes and after reflection. These whole helpers have budget 0.

For opposite vines A=L_n,B=R_n and KEEP n, n>=2, the source roots differ, giving H_source=F_source=n-1. The destination roots agree. The [all-size Ehat formula](../route_c_fixed_exact_pairs_20261031_v001/FX02_OPPOSITE_VINE_PROOF.md) gives H_destination=floor(n/2)-1, so Delta H=-(q+1)<=-q. The n=1 case is a no-op; empty trees have no present-key accesses.

The seven finite controls in the certificate additionally confirm the old hook, padded hook, original P DELETE, zero-double KEEP and starved L-helper phase, plus the new DELETE failure. In the starved helper H drops 5->2 with q=2. Full universal B repayment for H is not proved or refuted in this audit. The complete candidate already fails DELETE, so no separate open B theorem is pursued after that refutation.
