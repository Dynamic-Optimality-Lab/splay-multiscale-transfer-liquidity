# A complete recent-support decomposition of actual closed cores

Status: uniform structural source theorem. It proves the hit side of the
decomposition; cache-miss debt comparisons remain unproved.

## Complement bound from the completed subtree theorem

For any nonempty V subset M, the components of S minus C_V are actual
subtrees at first departures from C_V. They contain only marks of M minus V.
The completed subtree-density bound gives at most twice as many nodes as
marks in each such component. Consequently

    |S minus C_V|<=2|M minus V|,
    |C_V|>=2|V|-1-delta,    delta=2|M|-1-|S|.          (1)

If equality holds in the first bound, every omitted mark lies outside C_V,
every component root is unmarked and each component has exactly twice as
many nodes as marks. A marked component root would lose one unit of the
subtree bound; an omitted mark inside C_V would leave too few outside marks.

## Recent distinct-key windows

Let V be the k most recently accessed DISTINCT KEEP keys at a boundary
of the periodically extended closed word. Start the source window just
after the oldest last occurrence among these k keys. Every KEEP since that
start belongs to V, and every member of V has been visited. The existing
growing-visited argument, starting from the root singleton, gives

    |C_V|<=2k-1.                                      (2)

DELETEs freeze B and do not affect this argument. At maximal core delta0,
(1)-(2) force equality, so all remaining marks lie in saturated unmarked-root
components with exactly two nodes per mark. The chosen key window is read
from the actual source word; no extra state or observable is inserted into
the frozen controller. Since every KEEP key occurs in one period, the
recent-key order has a unique periodic value after one whole period. Thus
its value at the two ends of the actual comparison period agrees.

## Six-key chart with five recent keys

For core11, the five recent keys have an EXACT nine-node ancestor core.
The omitted sixth key is the marked leaf of an unmarked-root two-node
twig. Until that key is accessed, every hit splays one of the five marked
keys. Their nine-node ancestor core cannot shrink: (1) still gives the
lower bound9. Its labels are therefore fixed throughout that hit run.

For core10, the five-key ancestor core has size8 or9, and the omitted key
is again a core leaf, alone or below an exclusive unmarked parent. Choose
the fixed nine-Score set S9=S minus {omitted key}. It is ancestor-closed.
Every hit rotates only these Scores, preserving the rooted S9 projection
even if its true marked ancestor core decreases from9 to8. An unmarked
Score leaf is allowed by the unchanged local predicates, as independently
established in NINE_SCORE_SOURCE_BRIDGE.md.

Therefore EVERY hit in BOTH residual cores has the old M3 signed inequality
with its exact source cost, including H1/q3 and H1/q4, and every old zero/+1
helper transfer. Only a miss changes the selected nine-Score chart. This
is a complete source partition, not a claim that its chart potentials
already telescope through misses.

## Four recent keys before a core11 miss

Let z be the omitted key being accessed and v the least recent of the
current five-key chart. The other four keys U have all been visited since
either v or z was last accessed. Their core is exactly7 by (1)-(2).
Its complement has four nodes, two unmarked and the two marks v,z, in
saturated unmarked-root components. There are only two structural types:

* two disjoint two-node twigs, one containing each mark;
* one four-node component with both marks.

In the second type, the old five-key core intersects that component in
the two-node path u0->v. The remaining pair u1->z is a twig attached to
v, or attached to the other child position of u0.

If attached to v, the last inner frame at v,u1,z must be LL/RR. A mixed
frame would leave unmarked u1 with no full marked descendant, contradicting
fixed full-core closure. If attached opposite v at u0, a same-side
u0,u1,z would put two unmarked labels consecutively between v,z, violating
maximal-core sorted alternation. A mixed frame drops u1. Hence the latter
type cannot be the actual miss in a closed maximal-core walk.

Every actual one-component miss consequently begins with one ordinary
same-side inner double at v,u1,z. It demotes v,u1 to a two-node private
twig. Before the remaining outer frames, the NEW five-key nine-Score core
has the old ordered shape with v replaced by adjacent marked z. This
source reduction is independent of all hanging BSTs and helper inventories.
The exact signed cost of the removed inner double is retained next.
