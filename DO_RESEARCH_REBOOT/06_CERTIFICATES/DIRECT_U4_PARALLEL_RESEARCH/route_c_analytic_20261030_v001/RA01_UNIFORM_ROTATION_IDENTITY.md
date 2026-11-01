# Uniform source rotation identity for the complete joint-depth profile

**Status: exact universal source mechanics. This is a transport identity, not a signed repayment theorem.**

For finite present-key BSTs A,B on the same ordered keys, define

    H(A,B;z,w)=sum_y z^{d_A(y)} w^{d_B(y)}.

For a key subset E write H_E for its contribution measured in CURRENT GLOBAL depths, and e_y=z^{d_A(y)}w^{d_B(y)}. For an A rotation let T_s multiply every monomial by z^s; for a B rotation let T_s multiply by w^s. Negative exponents in the formal operator cause no actual negative depth, since those operators act only on regions deep enough to rise.

## Primitive rotation (all sizes, arbitrary hanging trees)

Consider a right rotation of child x over parent p, with x.left=L, x.right=M and p.right=R before rotation. The exact identity is

    H_after-H_before = (T_{-1}-I)(e_x+H_L) + (T_{+1}-I)(e_p+H_R).

M has zero depth displacement. Keys outside the old p-subtree are unchanged. The left-rotation formula is its reflection: the child-side outer subtree rises, the opposite parent-side outer subtree descends, and the middle subtree stays at the same global depth.

Proof: source _rot_right writes x.right=p and p.left=M, preserves the external attachment, and changes no internal hanging-tree pointer. Thus x and L rise one level; p and R descend one; M stays fixed. The other tree is frozen, so its depth exponent is unchanged. Summing the corresponding monomials proves the identity. _rot_left is exactly reflected. This proves arbitrary cardinalities and arbitrary internal A/B geometry without enumeration.

Sources: python/liquidity/legacy_embedding.py:_rot_right (line77), _rot_left (line92), splay_trace (line107); python/independent/splay.py:_rebuild (line92). These are PHYSICAL splay operations, not symbolic high witnesses.

## Source StepEv composition

For each double, T1..T4 are the four hanging subtrees in inorder. Region monomials below always use their actual pre-StepEv global joint depths.

|Kind|Depth -2|Depth -1|Depth +1|Depth +2|Depth unchanged|
|---|---|---|---|---|---|
|LL|x,T1|T2|T3|g,T4|p|
|RR|x,T4|T3|T2|g,T1|p|
|LR|x|T2,T3|g,T4|none|p,T1|
|RL|x|T2,T3|g,T1|none|p,T4|

Definitions: LL has T1=x.left,T2=x.right,T3=p.right,T4=g.right; RR is its reflection. LR has T1=p.left,T2=x.left,T3=x.right,T4=g.right. RL has T1=g.left,T2=x.left,T3=x.right,T4=p.right.

The formula for a row is the sum over its nonzero columns of (T_s-I) times the listed region profiles. For example,

    Delta_LL H = (T_-2-I)(e_x+H_T1)+(T_-1-I)H_T2
                 +(T_+1-I)H_T3+(T_+2-I)(e_g+H_T4).

The source performs parent-over-grandparent THEN target-over-parent for LL/RR, and target-over-parent THEN target-over-grandparent for LR/RL. Substituting the primitive identity in that order yields the table. It is valid independently in A or B, with z or w shifts respectively. Both zig orientations are already the primitive identity. Reflection preserves all depth exponents after the corresponding key relabeling.

Checks: evaluate z=w=1 to obtain cardinality conservation. An A rotation preserves H(1,w), and a B rotation preserves H(z,1). The first depth moments reproduce the historical total-depth formulas in scripts/wp6_symtable.py; those first-moment formulas are inherited, not new discoveries.

## Whole access

Sum these exact identities along the actual A trace and then along the actual B trace, with DELETE omitting the latter. Regions/profiles must be refreshed at each step. One cannot substitute a single source profile for every later occurrence of a changing region. In particular, commuting formal shift operators does not license commuting changing SOURCE regions.

The identities hold for every n. However H does not specify the region decomposition H_L,H_M,H_R (nor the double word). Hence the identity is not a deterministic update on global H alone. RA02 gives an exact same-input/different-output example and its arbitrary-fringe extension.

This reconstructs and strengthens the explicit algebra of the older wp6_jointupdate.py rigid-carrier mechanics. It does not by itself bound a nonlinear function F(H_after)-F(H_before), allocate credits, or prove CD-U. No potential-existence assertion is smuggled into the statement.
