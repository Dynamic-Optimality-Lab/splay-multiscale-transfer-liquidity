# Universal private Score-support erasure lemma

Status: PROVED as a structural term lemma, under the explicit source-image
premises below. It is not a shared-state J, a complete LOW reduction or an
M3 proof. No population tests establish this statement: the proof is
algebraic and by structural/path induction for arbitrary finite terms.

## Objects and premises

Use a proper private A prefix after the already proved erasure of invalid
nonactive child references. A node is Score-labelled or anonymous; a port
has its PRIVATE exact Score inventory. Treat a port as opaque: no physical
allocation of hidden anonymous payload is assumed. In particular original
weak LE need not imply a literal physical completion of that payload.
The port inventory supplies Score support for this PRIVATE proof object,
not a new observable. Active paths contain present real nodes and avoid
ports/dangling references, as in the original parent/depth/no-repeat proof.

Let S(T) be the set of Score labels in explicit nodes and port inventories.
Let Z be a canonical opaque object with empty Score support. Define C:

* A Score-empty port is sent to Z; a Score-bearing port keeps its Score data.
* C(Node_l(L,R))=Z if its TOTAL Score support is empty.
* Otherwise C(Node_l(L,R))=Node_l(C(L),C(R)).

Anonymous identities/relative order are retained whenever their node remains.
This is an auxiliary projection of a private witness. Original shared states,
sigmas, inventory bills and transitions are not modified or identified.

## Support and idempotence

Structural induction gives S(C(T))=S(T). At a port this is immediate. At a
node, the support is its own Score label, if any, union the two child
supports; erasure occurs exactly when that union is empty. By the child
induction hypotheses the same condition holds after pruning the children.

The same induction gives C(C(T))=C(T). A collapsed object remains Z; at a
retained node its support remains nonempty and its projected children are
fixed points. Thus support preservation and idempotence do not depend on
any anonymous population, gap colour or numeric rank-room assumption.

Define the smart constructor K_l(U,V) to collapse to Z iff the total Score
support of Node_l(U,V) is empty. Then

    C(Node_l(U,V)) = K_l(C(U),C(V)),
    C(K_l(U,V))    = K_l(C(U),C(V)).

The second identity uses support preservation, not an assumption that l
remains Score-bearing after a rotation.

## Rotation identity under the required path premise

Consider a RIGHT rotation at two real nodes p,x:

    Node_p(Node_x(A,B),C) -> Node_x(A,Node_p(B,C)).

Assume p and x have nonempty Score support BEFORE this rotation. They are
therefore retained by C before the rewrite. Projecting the rotated term
has the normal form

    K_x(C(A), K_p(C(B),C(C))).

Projecting first, performing the SAME rotation, and projecting again gives
the same form, by idempotence. The node p may become Score-empty afterwards;
K_p correctly collapses it on BOTH sides. No post-rotation support premise
for p is smuggled into the proof. The LEFT rotation has the dual form

    Node_p(A,Node_x(B,C)) -> Node_x(Node_p(A,B),C),
    K_x(K_p(C(A),C(B)), C(C)).

Tree variables A,B,C are arbitrary port-bearing subtrees. These are universal
equational identities, not checks of particular trees or support-bit cases.
The separate symbolic auditor computes the two normal forms without using
certificate labels or population data. Its trust boundary is this stated
term algebra; it is not a proof-assistant verification of all source code.

If C(U)=C(V), replacing U by V in any fixed surrounding context preserves
equality after C. Prove by context induction using the smart constructors
and support preservation. This lifts the local identity to the whole tree.

## Access congruence and arbitrary repeated access

Let z be a present target whose initial subtree contains a Score label.
Every ancestor on its path to the root is Score-bearing, so C retains the
entire path with the same actual identities and depth. The initial subtree
of z remains inside z while splaying it upward: target rotations enlarge
that subtree; an initial zig-zig parent rotation does not remove it.
Consequently each rotating pair lies above this same nonempty support.

Apply the rotation/context identity at every primitive. Any old ancestor
that becomes Score-empty has left the remaining target-to-root path and
may be removed without changing subsequent target ancestors or directions.
Thus the deterministic splay path in the pruned term agrees step by step,
and the final identity is

    C(Splay_z(T)) = C(Splay_z(C(T))).

The initial target depth is unchanged. Thus its A charge ceil(depth/2)
is unchanged. Leave B and its access word untouched: original B depths,
q and signed weight are unchanged too. Repeating the argument proves the
same statement for any finite sequence of accesses whose target subtree
is Score-bearing when accessed. Core accesses always satisfy the premise.

This handles arbitrary anonymous population and arbitrary exposure of
Score-FREE decorations for those accesses. It does not remove newly exposed
SCORE-BEARING anonymous nodes, and it does not permit accessing a deleted
Score-empty anonymous helper.

## Exact limits of the lemma

1. C depends on private port Score inventories. The frozen state records
   only(mu,b,alpha7,sigma), not those inventories. Existing accepted original
   GAPMULTI01 witnesses have identical complete shared endpoints and sigma
   but different hidden Score splits. Their private projected objects differ.
   This rules out assuming that the entire private C object is determined by
   the shared state. It does NOT rule out finding a potential insensitive to
   those differences; that is a separate unproved invariant/descent theorem.
2. Private witnesses on successive original edges can be chosen independently.
   A potential on private projected objects cannot be telescoped around an
   original shared-state cycle unless its shared-state descent is proved.
3. A Score-empty anonymous helper can be an original real active target. C
   deletes it. This lemma alone provides no corresponding helper transition;
   the existing accounting or an additional weighted simulation would have
   to cover it for the proposed projected potential. No helper class is
   excluded from the original graph.

The universal M3 proof route therefore still lacks a single shared bounded
J and complete signed preservation. Introducing these as assumptions would
reintroduce the open compatibility/feasibility burden. No M3 promotion is
made from the universal private erasure lemma.
