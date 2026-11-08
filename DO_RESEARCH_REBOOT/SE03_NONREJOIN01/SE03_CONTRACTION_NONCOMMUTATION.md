# Removing an extreme key does not commute with ordinary splay

This rejects an alternate uniform reduction candidate and retains the
precise parity defect. It does not refute support erasure or original CD.

Let z<x<p<g, with A,B,C,D arbitrary BSTs in the successive inorder gaps.
Set T=g(z(empty,p(x(A,B),C)),D). Key z is the minimum key of this tree
apart from the stipulated empty left fringe. Define pi_z by ordinary
BST removal of this minimum: splice its right subtree at its former site.

The original path to x in T is L,R,L. An inner RL double at z,p,x and a
terminal left ZIG at g give exactly

    S_x(T)=x(z(empty,A),g(p(B,C),D)).

Removing z afterwards gives

    pi_z(S_x(T))=x(A,g(p(B,C),D)).                           (1)

Removing z first instead gives g(p(x(A,B),C),D). Its x path is L,L and
the original LL double gives

    S_x(pi_z(T))=x(A,p(B,g(C,D))).                          (2)

The right-subtree roots in (1)-(2) are g and p, so they differ under every
legal hanger substitution. The projected depths differ by one, but the
outcome defect is a rotation, not only a cost-parity correction. Thus a
proof that contracts an extreme key in both trees cannot simply apply the
smaller-support induction hypothesis to the projected access word. It must
first establish a source-valid dynamic repair law for this noncommutation,
including repeated defects and complete closure.

Changing the erasure model to silently splice z would also change original
DELETE semantics and is forbidden. This construction is an analysis of a
rejected auxiliary projection, never a modification of any inherited source.
