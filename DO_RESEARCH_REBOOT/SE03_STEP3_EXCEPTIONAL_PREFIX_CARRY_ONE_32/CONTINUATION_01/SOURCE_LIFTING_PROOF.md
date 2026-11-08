# Uniform lifting of the new source syntax

This is a symbolic completeness proof, not a test on bounded BST populations.
The inherited Unary14 FULL_PROOF sections2-3 prove the branch quotient and
active-frame lift. Here both distinguished physical keys7 and9 are retained
until the actual rotations finish. The extension changes only the finite
number of retained marks; no source operation or private inventory is erased.

## 1. Boundary grammar for seven retained marks

Prune mark-free subtrees for proof and contract unmarked unary vertices of
the marked ancestor core. Keep every marked vertex and unmarked brancher.
A genuine boundary root is the actual last marked target. Every brancher
has marks on both sides, and at most one brancher occupies an adjacent-mark
gap: its separating neighboring marked intervals uniquely determine their
LCA. There are at most five such branchers for seven marks and a marked root.
Normalize marks to1000,...,7000, branchers in gap j to1000j+500.

The recursive grammar chooses either a marked root and disjoint left/right
mark intervals, or a gap root and two NONEMPTY mark intervals. Empty intervals
are arbitrary independent ordered private terms. This enumerates every
boundary quotient, independently of the number or height of original unary
vertices and private nodes. The marked-root count is5947; before cold9 the
source root is neither7 nor9, leaving5577 bases. Counts follow from
F(0)=1, R(n)=sum_i F(i-1)F(n-i),
F(n)=R(n)+sum_(1<=i<n) F(i)F(n-i); R(6)=974 and R(7)=5947.

## 2. Every whole macro of H<=2 is represented

At most two positive A accesses occur. If there is one, its target is the
final genuine marked target x; its depth is1..4. Otherwise they are y then x,
each of depth1 or2. Every other original operation is an A root repeat and
leaves the actual A state unchanged. A positive access to a different helper
followed by a zero-event final x cannot occur: its root would be that helper,
not x. Original operation kinds and all their actual costs are retained.

Contract only source unary vertices that are operands of neither positive
access. They remain in rigid hangers at each rotation, so contraction commutes
with both frames and with final projection. Keep every original brancher
through the actual middle state, even if the first access makes it unary.
Then the source alternatives are exactly the inherited active-frame grammar:

* A single x access: all unary path decorations with actual depth<=4.
* First helper y: retained mark/brancher, old marked-carrying unary, private
  root, private depth-two child, or a private child opposite the marked side
  of an OLD unary parent at depth one. All depth<=2 decorations are retained.
* A second-only unary operand: it belongs to a rigid marked-carrying hanger
  outside the first operand set. The second depth bound permits at most one,
  precisely when the reduced second path has depth one. Insert it in either
  orientation at its ORIGINAL source location, then replay both accesses.

These cases partition actual path vertices by marked descendants and operand
membership. They do not bound unexposed nodes or require a fixed private tree.
All ordered gaps, both orientations and aliases are included. The proof is
unchanged for seven retained marks; the path bounds depend on H, not support.

For cold9, keep seven marks through both frames, then project the source
onto M_old={1,3,5,7,11,13} and destination onto M_new={1,3,5,9,11,13}.
These are the ACTUAL two projections, not a claimed commuting splay on the
same mark set. `cold_source_relation_complete.json` contains554 H1 and2279
H2 pairs of old/new A indices. Both rotation/projection kernels produce
exactly the same complete union. Every one of5577 bases was completed in
both kernels, including the explicit impossible-depth exclusions.

That exclusion is uniform: H<=2 permits at most four actual rotations.
One rotation changes a fixed node's depth by at most one. Since9 ends at
the root, its source depth is<=4, and quotient contraction only reduces it.
A base with quotient9 depth>4 therefore has no LOW realization.

## 3. Complete H1 closure from the prescribed entry

For H1 there is just one positive access, to the final genuine target.
Use the same seven-mark grammar with every depth<=2 unary decoration.
No two-frame/private helper rule is needed. Initial quotients are

    6000(4000(3000(L,.),5000),7000),

where L is the two-mark left chain, right chain or single unmarked brancher.
These are exactly the quotients of the original PREFIX frame at u.
Close under every marked target other than physical7; a target7 is retained
as a terminal relation and is not queued for continuation. Ordinary root
repeats change no state. `cold013_h1_relation.json` and
`verify014_h1_relation.json` agree on the complete closure and its rows.

Every actual all-H1 prefix from u maps inductively into this closure. The
actual BF transition and the one cold chart switch select which rows can
be combined. This forward simulation does NOT claim that an abstract path
can be lifted by splicing unrelated private subtrees.

## 4. HIGH and arbitrary source length

After a first H>=2 macro, the accepted six-mark LOW/HIGH relations apply
on each fixed chart. H2 uses its COMPLETE two-frame lift. H>=3 uses capped
price6-Q and ALL root-synchronized A endpoints, a necessary enlargement.
A q5/q1 pair of total H>=4 uses price2 and all final synchronized endpoints;
the smaller pairs retain their shared A midpoint. Actual per-macro capped
credit dominates this conservative pair price. Thus no depth, inventory,
support-within-EXC or return-length cutoff appears in the proof.

New code kernels are mutable and immutable ordinary bottom-up rotations
with distinct quotient projection. They share the mathematically proved
grammar. Gap payloads remain arbitrary ordered terms. No external/kernel
audit is asserted; the complete relations and static certificate have
separate same-agent implementation checks.
