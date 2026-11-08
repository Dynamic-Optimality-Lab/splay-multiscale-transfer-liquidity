# Complete local H1/Q2 leaf-loss classification

Target: characterize every actual core11 singleton H1/Q2 with deltaL<0.
Conditions: actual closed maximal six-key source; original macro context.
Inheritance: all-SS theorem, marked-parent compression, deltaL=a-b and
the inherited H1 macro grammar. Ambiguities: local conditions do not
certify a history's reachability/closure or an entire T11->F11 return.
Bridge: classify source path and exactly which marked vertices change
leaf status; then apply the original one-event A formulas.

## B geometry, necessary and sufficient on an admitted source

The original B path is exactly

    g, u, h, v, x,

with g,h,x marked, u,v unmarked; its FOUR search edges are LLLL, LLRR,
RRLL or RRRR. The two actual doubles are performed inner pair first.
There is no five-edge B case here: odd source depth/terminal zig is
excluded by the original CLOSED maximal-core source theorem. That
exclusion is not asserted on core10.

Since deltaL=a-b and a>=0,b in{0,1}, strict loss is equivalent to:

1. x is a marked leaf in the actual full core;
2. g retains a marked child branch off its path to h;
3. h retains a marked child branch off its path to x.

Under these three conditions the loss is exactly one. They are also
sufficient for the leaf loss, conditional on an admitted legal source
splay. The accessed x may have arbitrary physical Score-free children;
marked leaf does not mean physically empty BST children.

The only three marked vertices outside the path are divided between
the off-path groups attached to g and h. Both groups are nonempty; all
off-path marks belong to one group because x has no marked descendant.
Their sizes are(1,2) or(2,1). After the splay, the marked-parent root is
x and its EXACT marked children are g and h, with subtree sizes2 and3.
Both children are nonleaves. The size2 branch is a chain; the size3
branch is either a chain or a two-leaf fork. Consequently the only
possible marked-leaf changes are

    3 -> 2, or 4 -> 3.                         (C)

In particular a leaf-lowering q2 packet cannot start with five leaves,
and its output cannot itself support a q4/q5 path: its largest marked
branch has size3, so marked-parent depth is at most3. This last assertion
is B geometry, not payment for a subsequent sequence of zero packets.

Every port is an ACTUAL source subtree with fixed ordered contents.
Grouping marks by nearest marked ancestor does not delete separators,
move marked ownership, or assume all combinatorial port choices are
source-realizable.

## A geometry and the complete original operation grammar

The synchronized source A root is the same g. H1 has exactly one positive
A access, to x at actual depth1 or2. If x<g its source path is L, LL or
LR; if x>g it is R, RR or RL. Thus there are three possible A cases for
each of the four B orientations, subject to actual key order and whole
source consistency. We do not assert every formal combination is reachable.

A zig uses one rotation. A double uses two primitive rotations but is
ONE StepEv. H1 never means two A StepEvs. For the old A root's position,
L gives R; LL gives RR; LR gives R. Independently,
R gives L; RR gives LL; RL gives L. Thus old-root exposure can be at
L,R,LL or RR, never LR or RL.

The positive access can be terminal Kx or an actual Dx followed by the
terminal root Kx. Before it, zero A requests target g; afterwards they
target x. All nongenuine full Kg requests precede that positive event,
and their auxiliary BE action must be retained. Multiple Kg requests
have one idempotent endpoint action, not zero full-history ownership.
Every original timestamp remains in its natural macro. No positive
anonymous Dy with y!=x can occur in an H1 macro.

Anonymous nodes can still be the actual A parent in a double, and all
hangers may have arbitrary finite inventories. The six one-event formulas
are equations in these subtrees, so the classification includes them.
It imposes no equality of A/B/BE private populations or of changing charts.

## Geometry independent of six keys

For any actual maximal source with r marked keys, the same q2 path and
deltaL characterization hold. After a loss the two marked child branches
have sizes i,j>=2 with i+j=r-1. Thus r>=5 is necessary. Every source
supporting q doubles has at least q nonleaf marked ancestors, so

    L(source)<=r-q.                            (P)

For six keys, i,j must be2,3, yielding(C). The precise numbers depend on
r=6; the path, leaf identity, anonymous-parent treatment and source
rotation formulas do not. No donor bits or regeneration price are
deduced from this count alone.
