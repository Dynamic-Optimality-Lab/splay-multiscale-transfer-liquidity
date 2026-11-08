# Exact local zero-hole grammar; full ownership completeness remains open

Status: DERIVED symbolic lemmas, independent audit pending. Scope is the
actual closed MAXIMAL full core. Smaller cores do not inherit this grammar.

## 1. Source objects, not synthetic chart edges

A natural full macro begins immediately after a genuine full KEEP y and
ends at the next genuine full KEEP x!=y. It contains every intervening
DELETE and nongenuine KEEP. B_F stays fixed before the last operation;
B_E executes every retained KEEP, including repeats which may not be
repeats in B_E. A executes every original operation.

For each actual macro retain its full start/end A,B_F,B_E trees, operation
word with absolute IDs, actual A frame/event list, full and erased B
frames, actual chart endpoints, all own units, all B demand ordinals and
the original owner map. Frame guards are ordinary ordered BST guards;
off-path subtrees are arbitrary ordered BSTs, including marked content
where allowed. No proposed row is declared reachable just because it
satisfies local guards. Reachability and full closure remain source guards.

There are two distinct relations: (i) consecutive original source
operations; (ii) comparison/owner edges D->U->D in the proof. An owner
edge can jump to another source macro, even a positive-weight macro.
Consecutive source zeros need not be consecutive ownership edges. No
unpaid positive macro is deleted from the word to make a zero chain.

## 2. Complete local obstruction classification

Use the inherited actual marked-parent tree. In a macro, u is the count
of old unary marked ancestors, beta the count of branching marked
ancestors and z in {0,1} indicates that x was a marked leaf. The verified
source identity is Q=u+beta and DeltaL=u-z. The number of undefined
branch comparison slots is

    R_e = (beta+z-2H)_+.

Suppose a declared integer source selector 0<=c<=H has zero price Q=2c. Substitution,
without clipping the actual physical inventory, gives

    beta+z-2H = z-u-2(H-c).                     (Z1)

All terms are integers, z<=1, u>=0, H-c>=0. Hence R_e is nonzero IF AND
ONLY IF

    H=c, z=1, u=0, beta=Q=2H; then R_e=1.      (Z2)

Proof: if H>c the right side of Z1 is at most-1; otherwise it is z-u,
which is positive exactly at z1/u0 and equals1 there. The converse
substitutes directly. Thus nonleaf targets, a unary marked ancestor,
and selector-clipped zero macros with unused physical cost have NO
undefined branch slot. This does not assert availability of their raw
bits under a fixed owner map.

For the physical price 2H-Q, take c=H. The dangerous local source shape
is therefore a marked-leaf target with ALL 2H marked ancestors branching.
Each ancestor has an off-path marked child component. These components
are pairwise disjoint and disjoint from the ancestor path and target:
the next path ancestor contains only the continuing path component,
whereas the chosen component leaves that path at its own distinct vertex.
Select one marked key in each component. The 2H ancestors, x, and those
2H witnesses are distinct. Consequently

    r >= 4H+1.                                 (Z3)

This is a necessary source restriction, NOT proof that every such mask
or A shadow has a reachable closed embedding. At r=7/8 only H1/Q2 can
cause a zero-hole. H2/Q4 is not excluded for r>=9, H3/Q6 for r>=13, etc.
Those higher-event obligations must not be lost by reusing six-key rows.

A genuine natural macro has H>=1: it starts with A root y and ends
with a different root x. A literal zero-A root repetition has H=Q=0
and no full demand, but must still be retained in the erased execution.
A positive-A root-return gap with Q=0 retains its actual supply/cost;
it is not a physically zero transition. Persistent full/erased disagreement
can make qE differ from qF, including qE>0 when qF=0. None of these
operations is removed. A multi-macro packet with total price zero can
contain nonzero-priced constituents; Z2 is not falsely asserted for
each constituent of such a packet. Those packet/owner interfaces remain
part of Gate A's unclosed completeness obligation.

## 3. Exact H=1 A-word normal form

At the preceding full genuine boundary both A and B_F have root y.
If the macro has exactly one positive A event, all earlier zero-event
accesses target y. The single positive access must target x: after it,
every zero-event access has that new root as target, and the final KEEP
is x. Its old A depth is1 or2. It is either the terminal KEEP itself or
a DELETE x followed by zero-event DELETE x occurrences and the terminal
KEEP x. An earlier KEEP x would already be the macro boundary.

Thus the event is exactly one of zig-L, zig-R, LL, RR, LR, RL, with the
original root y, actual target x and (for a double) actual middle operand.
The middle operand can be marked or anonymous; all ordered off-path
BSTs and legal aliases are retained. Arbitrary zero prefixes/suffixes
are retained, not charged an invented event. Root-y KEEPs before the
positive event still execute in B_E where retained, with actual costs.

Proof: every positive A access changes its root to its target. With only
one such access, the final A root forces the target x; the definition
ceil(depth/2)=1 gives precisely depth1/2 and the six listed orientations.
All remaining accesses must be to the current root. These facts also
prove the converse description for an already admissible source macro.

The full B event sequence in a dangerous H1 zero macro consists of two
actual same-side doubles, with two branching marked ancestors and a
marked-leaf target. Four combinations of the two LL/RR orientations
are kept with their actual order and source guards. Reflection swaps
L/R, LL/RR and LR/RL while preserving the classification and bit IDs.

## 4. Higher H and private/anonymous ancestors

For general H, record the actual positive A accesses in order with
event counts h1+...+hk=H, hi>=1. Their source depths are2hi-1 or2hi.
Keep the ordinary bottom-up frame sequence at each access and every
zero-event original operation between them. Internal KEEP targets must
be the unchanged full B root y; the final genuine target is x. This is
a complete forward description of source macros, not a reverse
realization theorem for arbitrary lists of projected endpoints.

Campaign14's uniform active-operand theorem supplies a necessary free-tree
syntax with at most2r+2H-3 known A nodes, arbitrary inactive unary chains
and ordered hangers. It is independent of fringe population. It does
not give a signed debt or an owner escape theorem at arbitrary H,r.

## 5. Ownership part not yet complete

The exact known owner rules are recorded in OWNERSHIP_TRANSFER_SYSTEM.
They cover all h_Lambda edges, exact inverse-a edges and explicitly
source-certified family escapes. A complete universally sufficient
Z_r^own would additionally need the source escape rule at every reached
Z2 frontier (and any other admitted frontier reached by that owner walk).
No such rule has been proved here. Gate A is PARTIAL, not accepted as a
complete ownership grammar by calling the set of actual histories a
grammar or by excluding an unhandled owner/chart case.
