# Original-rotation ancestor retirement

## Box AR

Target: identify actual source A-bit units forced by a return, without
assuming a prepared A state or unowned credits. Conditions: ordinary
bottom-up splay on actual ordered keys, all original operations retained.
Inheritance: one or two actual rotations per StepEv and two physical bit
units `(t,j,0),(t,j,1)` per such event. Ambiguity: a raw witness unit may
already be owned by another demand. Bridge: the following source rule
supplies distinct tickets; the later capacity/ownership theorem must
identify actual usable donor units.

## AR1 — one rotation removes only one ancestor

A right rotation `g(p(A,B),C) -> p(A,g(B,C))` can remove an ancestor
relation to a fixed key mu ONLY for old root g. Its lost descendant set
is p together with A, all below p<g. The promoted p gains descendants;
every other node's descendant set is unchanged. The mirror statement
holds for a left rotation, whose lost set lies above its old root.

Thus one physical rotation removes at most one marked ancestor of mu.
Give the first rotation of StepEv j bit0, the second bit1; a zig uses
bit0. These are actual available A-bit units, not new rotation credits.
Two removed-ancestor witnesses cannot occupy the same rotation bit.

## AR2 — ordered access preserves a witnessed ancestor

If mu<v<y and v is an ancestor of mu before an ordinary splay of y, then
v remains an ancestor of mu afterward. Every right-rotation pivot in
that splay is greater than y; a pivot v<y therefore cannot undergo the
right rotation needed to lose a smaller descendant mu. Left rotations
of v preserve all its smaller descendants. AR1 handles all other pivots.
Reflection gives the statement for y<v<mu.

This proof allows v to be promoted as an intermediate parent: promotion
only grows its descendant set. It does not incorrectly assume that every
off-path term at v has the same immediate parent throughout the splay.
All anonymous nodes and arbitrary BST hangers are allowed.

## AR3 — monotone pass return supplies tickets

Consider ANY original source segment whose genuine full-B KEEP sequence is

    x0 < x1 < ... < xk, followed by x0,

with arbitrary DELETEs and nongenuine root-repeat KEEPs interleaved. A is
rooted at xi immediately after its genuine KEEP, irrespective of the
preceding helpers. After access xi, mark the fact that xi is an ancestor
of x0. Select its FIRST subsequent loss before the closing return to x0.
It exists because the closing A splay makes x0 the root. By AR2 no later
monotone genuine KEEP can cause this loss. Consequently the selected
rotation occurs in an auxiliary operation or in the closing return macro.

Each xi is marked once, and AR1 makes the k tickets distinct. No fixed
initial A shape, minimum-cost preparation or private-inventory bound is
assumed. For a closing natural macro of actual cost Hc, at most2Hc tickets
occur in that macro. Therefore at least `(k-2Hc)_+` distinct tickets occur
in auxiliary A events of the preceding k natural macros. All costs and
occurrences are the original source ones.

The same argument applies in the decreasing order. Distinct declared
source blocks have disjoint original rotation occurrences, so arbitrarily
many repeated/reflected blocks do not duplicate tickets. It does NOT
permit overlapping blocks to claim the same bit without another proof.
