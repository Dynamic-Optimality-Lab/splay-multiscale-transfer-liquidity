# An independent full-core11 negative-price seed

Scope: actual six-key closed maximal sources, and their exact same-side
source term class from CLOSED_MAXIMAL_SAME_SIDE.md. This constructs a
seed for negative segments; it is NOT a full Step2 potential.

Call a B tree admissible here if it has the eleven alternating labels,
six marked nodes of subtree mass1, five unmarked nodes of mass0, and
marked root. A legal source splay has only marked-G/unmarked-P same-side
doubles. Such a splay preserves the whole labeled core and this source
class, directly by the zero-change mass case. All actual closed core11
KEEPs are legal in this sense. Off-core gap BSTs remain arbitrary.

## Fan with mass-zero ports

A legal q-double access has a source path with q+1 marked and q unmarked
vertices. Pruning its off-path hangers gives a Hamiltonian alternating
path. The already proved source fan induction applies to these PATH
labels, with their own relative ordering: its output is the canonical
fan F_(q+1) rooted at the target. Every original off-path hanger remains
whole in one of the fan's actual ports. Each has GLOBAL signed mass0:
both children of a marked node have0 mass, and the off-path child of
an unmarked parent has0 mass since its path child has mass1.

There are exactly5-q marked and5-q unmarked core labels outside the
path. Thus all ports together contain5-q two-node blocks, in the exact
representation proved above. This is counting actual labels, not an
assumption that they are free capacity.

## Accessibility from an exact fan

Among the path marked vertices of a fan, only its root and its extreme
marks can occur on a later legal same-side target path. Each nonroot
extreme is at depth2. A different path-mark has either odd depth or a
first opposite-direction pair; extending that prefix into a hanger
cannot repair it. The old source fan path formulas give this directly.

If a new target lies in a port with k blocks, its legal path can reach
that port through the root (zero prefix doubles) or an extreme path-mark
(one prefix double). Inside the port at most k doubles are possible,
because it contains exactly k unmarked and k marked vertices. Hence

    next legal q <=1+k <=1+(5-q_previous).            (1)

For a following q>=3 after q3, equality in (1) requires BOTH outside
blocks to belong to ONE port at an extreme path-mark, and all four
vertices of that port to lie on its alternating same-side target path.
No outside marked node is left inside that port.

## Why there cannot be three consecutive q3 accesses

After the second q3 in that equality case, its own seven path labels
form F4. The two original path marks omitted by its path are rigid
leaves in one or two UNMARKED FAN ARMS attached to the former root.
This follows from the first fan formula: the path to the selected
extreme uses the first unmarked node and its extreme marked child;
all remaining first-fan arms are its opposite port or the old root's
other port. The second source's outer SS formula attaches those arms
to the old root; its inner two frames never enter them. The old root
is an extreme of the second path, since the new marks in the chosen
extreme's port all lie on the same side of it.

An unmarked fan arm has a marked LEAF child on one side and another
unmarked fan arm on the other. A legal path from a marked parent must
choose that marked child to make its first same-side pair; it then
stops. Choosing the other child instead encounters an unmarked node
where the next source grandparent would have to be marked. It follows
that such an arm contributes at most ONE legal double. Therefore the
next access has at most one prefix double plus one arm double, q<=2.

This is a source-term argument for arbitrary fan arms, not an enumeration
of shapes or a tested absence of a third transition.

## All negative-only words have total deficit at most2

In the full paired partition, negative prices are:

    singleton H1/q3: -1;
    singleton H1/q4: -2;
    paired Hsum2/q5,1: -2.

After q4, (1) gives every following legal q<=2, so no further negative
segment can follow without intervening nonnegative work. After q3,
(1) gives q_next<=3; the only further negative possibility is another
q3, and the preceding argument then forces q_next<=2.

After a q5/q1 packet, the entire core has no outside labels. Its extreme
return leaves the old target at depth2, with proper unmarked fan arms.
A following legal marked path reaches that old target in one double and
can then enter at most one arm double. Hence every following q<=2.

Consequently the complete negative-only source words are one -2 segment,
one -1 segment, or two consecutive -1 segments. Each has deficit<=2.

## Explicit seed, independent of the desired full cost bound

Let N1 consist of exact B outputs of ONE legal q3 splay. Let N2 consist
of outputs of ONE legal q4 splay, ONE legal q5/q1 packet, or TWO
consecutive legal q3 splays. Define the current-source function

    psi11(B)=2 on N2;
    psi11(B)=1 on N1 minus N2;
    psi11(B)=0 otherwise.                            (2)

Membership is a finite source WORD-SCHEMA predicate on actual tree
identities; it is not a fitted label, a search result, or a definition
by the desired global inequality. It quantifies no source A inventory.
All hanging BSTs are unrestricted. No graph is constructed or altered.

The preceding classification gives: a psi11=2 source has no negative
outgoing segment; a psi11>=1 source has no q4 or q5 outgoing access.
Every q3 from an N1 source reaches N2. Thus on EVERY actual negative
full segment,

    w+psi11(B_after)-psi11(B_before)>=0.              (3)

It also proves (3) for singleton H2/q3 and H2/q4: their prices are1,0;
a q3 source has psi11<=1, and a q4 source has psi11=0. A paired Hsum3
zero segment ends in N2, so is paid by range2. All remaining prices>=2
are range-paid. The ONLY unproved full segment types for this SEED are

    singleton H1/q1 (price+1), H1/q2 (price0).         (4)

Those two types are substantial. A B-only function cannot be globally
valid, by B_ONLY_SOURCE_OBSTRUCTION.md. An A-dependent signed completion
must settle them and preserve all rows just proved, including helpers.

## Useful source floor for an independent candidate audit

Every N2 output has at least FOUR marked core leaves. A q4 output has
four relative path-mark leaves; its single extra block can replace at
most one such leaf by one extra marked leaf. A q5/q1 output has exactly
four marked leaves by the completed barrier theorem. A q3/q3 output
has three proper relative path-mark leaves; the former root contains
the two remaining old marks in leaf-fan arms, so replacing its one
relative leaf by those two gives four. Hence

    fewer than4 marked core leaves => psi11<=1.       (5)

Neither (2) nor (3) is claimed on deficiency-one core10. No nonnegative
closure, universal D6, full original allocation or donor injection has
been proved by this seed alone. Step2 remains OPEN until those gaps and
the other required source classes are closed.
