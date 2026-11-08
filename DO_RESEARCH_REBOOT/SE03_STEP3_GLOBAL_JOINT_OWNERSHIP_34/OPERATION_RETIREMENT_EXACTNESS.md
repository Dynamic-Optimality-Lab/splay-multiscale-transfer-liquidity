# Operation retirement exactly captures rotation retirement

## Box OR34 — PROVED

Target: a raw rotation ticket must not disappear when PR groups an entire
A splay into one operation pool. Conditions: ordinary actual bottom-up
splay, arbitrary ordered keys and independent private subtrees. Inheritance:
original zig/LL/RR/LR/RL frames and C33 AR1. Ambiguity: none for this lemma.
Bridge: every inherited extreme raw ticket lies in its demand's PR pool.

Fix an A access to y. For any other key v and any key z, if a rotation
in this splay removes v's ancestry of z, v is an ancestor of z before the
whole operation and is not one after it. There is exactly one rotation
in the operation pivoting v at which such a loss can occur. Conversely,
an endpoint loss has a rotation loss. This is a statement about actual
ancestry, not the root-to-y depth or a quotient.

Proof. AR1 allows a loss only at the old pivot. At each bottom-up double,
the old parent P and grandparent G are consumed; all subsequent outer
frames preserve their final rooted subtrees as rigid hangers. Neither can
be a pivot or be promoted later. A processed node cannot regain ancestry.

In LL the two successive trees are

    G(P(y(A,B),C),D)
    P(y(A,B),G(C,D))
    y(A,P(B,G(C,D))).

G loses only labels in {P,y} union A union B, all in its initial subtree;
its final subtree G(C,D) is already fixed after the first rotation.
P first gains G and D, then loses y and A. The gained and lost sets are
disjoint, and the lost labels were in P's initial subtree. Its final
subtree P(B,G(C,D)) is rigid after its pivot. Thus no newly gained
ancestry is lost and no lost ancestry is regained. RR is the reflected
formula with the same disjointness.

In LR the trees are

    G(P(A,y(B,C)),D)
    G(y(P(A,B),C),D)
    y(P(A,B),G(C,D)).

P loses y and C, G loses P,y,A,B; the corresponding final subtrees are
rigid immediately after their pivot. RL is the reflection. A zig has
one pivot, whose final subtree is rigid. Unconsumed off-path nodes retain
their own rooted subtree relations. The accessed y only gains descendants
and is never a pivot. These exhaustive free-term formulas and induction
over any number of outer frames prove the assertion for every key,
including keys inside arbitrary private terms. Endpoint loss conversely
must first occur in one of the actual rotations. QED.

## Corollary EX-PR34 — simultaneous exterior pool compatibility

On the inherited closed maximal-core source domain, all min/max B
demands together have an injection into their PR retirement pools T_m.
Multiplicity, source length and private populations are arbitrary.

Proof. Reuse C33 EXTREME_TARGET_JOINT_TICKETS.md at its exact scope. It
assigns all those demands distinct actual first-retirement rotation bits,
including both orientations and repeated/shared targets. OR34 makes
every chosen bit's whole operation an endpoint retirement after the
relevant last genuine g KEEP. That operation is in R_m, so its bit is
in T_m. No bit identity changes. Therefore every coalition consisting
only of exterior macros satisfies GPR. This is raw compatibility, not
availability under fixed owners. Inherited verification labels are not
promoted by this corollary. QED.

No analogous global ticket noncollision is asserted for interior targets.
The C33 three-demand collision explicitly forbids that inference.
