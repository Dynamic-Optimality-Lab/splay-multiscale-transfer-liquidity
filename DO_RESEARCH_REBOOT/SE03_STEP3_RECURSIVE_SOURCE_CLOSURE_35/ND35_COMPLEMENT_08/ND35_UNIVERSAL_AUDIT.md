# Reconstructed ND35 universal raw-matching proof

Status: symbolic proof reconstructed at its RAW physical scope; separate
review pending. No full neutral, bank or owner theorem is claimed.

For M nonempty fix the original carrier S. Every S key of B is an
accounting anchor. Its subtree label contains that key, so the nonempty
B labels are all distinct; off-S nodes have empty labels. During each
B access its path operands belong to S, and all off-path hangers stay
rigid. Thus J_S(B) has exactly |S| distinct nonempty labels, at every
fine B rotation, and includes the full S label.

For an arbitrary A single rotation, only the promoted child's old
proper-subtree label and the old pivot's new proper-subtree label can
change in J_S(A). The label of their whole subtree persists at its new
root. All other subtree labels persist. Duplicate anonymous labels can
make a putative deletion/addition disappear at SET level, so there is
at most one set deletion and at most one addition, without a population
bound. Relative to fixed B this implies DeltaPsi in{-1,0,1}.

After A has processed KEEP x, x is its actual root. In every ordinary
B rotation, including the first parent rotation of LL/RR, the promoted
child's old proper subtree contains x and the old pivot's new subtree
does not. Both operands are distinct keys of S. Hence the exchanged
B labels I,J are different, proper, nonempty; I contains x and J does
not. I cannot be an A-subtree label: every proper A subtree excludes
the actual root x. No other B label is lost or gained. Therefore B's
missing-label set loses I and either gains J if J is absent from A,
or gains nothing if J is present. DeltaPsi is0 or-1.

These arguments use the complete source operations, every orientation,
and arbitrary ordered hanging terms. Nongenuine KEEP has no B rotations;
DELETE has only its actual A phase. A B terminal zig can decrease Psi
but is NOT a B-double demand. No core11/maximal-core premise is used.

Classify every double by its actual total drop m=0,1,2. This is exhaustive
since each of its two rotations drops0/1. Let D0 be m0 and D+ be m1/m2.
Mark actual A positive bits P. Record each negative step as a slot:
the first drop of each D+ is its payment slot; A-negative, extra B2 and
B-zig drops are release slots. Full A/B closure balances every integer
level. Consecutive cyclic level crossings pair every down slot bijectively
with an actual A up bit on the SAME period. Choose its bit for each
payment slot. This gives g+:D+->C_A injectively and with exact event IDs.

Let N count A negatives, B1/B2 count drop types, Z1 decreasing B zigs.
The exact identities are

    P=N+B1+2B2+Z1,
    |R|=2A-P+N+B2+Z1,
    2A-Q_B=|R|-B0.

The sets R are the actual nonpositive-rotation/virtual units and the
positive bits paired to release slots. These are disjoint from im(g+).
The identities are not a proof that B0<=|R|.

Thus ND35's raw partial injection is uniform over ALL required original
closed sources. It is not restricted to the saved controls. It does not
promise that g+ avoids natural h0/fE, has a causal cut schedule, or fits
all input reservations. Those are explicitly outside the theorem being
imported. M empty is handled by Q_B=0, without invoking this construction.

The pointwise proof and cyclic level pairing justify source coverage;
no graph path is presumed source-realizable and no finite passing tests
or CD6 extension supply this proof. The accepted older audit is reused;
this reconstruction will be challenged by the new lifetime calculation.
