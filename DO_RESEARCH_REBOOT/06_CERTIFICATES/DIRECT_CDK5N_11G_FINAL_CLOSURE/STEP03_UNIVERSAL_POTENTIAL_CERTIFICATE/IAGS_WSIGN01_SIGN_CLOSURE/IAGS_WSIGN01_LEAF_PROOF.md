# IAGS-WS-01 LEAF PROOF — Rotation Joiner Bound, Single-Event Corollary, and the Exact Open Hole

## L1. Single-rotation joiner bound (PROVED)

Setting: frozen B-controller arrays; one `single_rot` application with
child x and parent p (mux-selected slots; no validity assumption beyond
the array rewiring the code performs). Claim: C_post subset C_pre union {x}.
Proof: the rewiring (i) moves x's rotation-side subtree S from x to p,
(ii) moves p under x, (iii) leaves L (x's other side), middle, gp-side,
and rest with identical descendant sets. A node can newly join C only by
gaining marked descendants (own markedness is fixed). Only x gains
descendants (p's side); all others keep-or-shrink theirs. Hence only x
can join. If x was already in C_pre, nothing joins: C_post subset C_pre.
No assumption about tree shape, validity, or path membership.

## L2. Marked-target splay monotonicity (PROVED)

Consider one frozen B-splay event whose target path[0] is marked (mu).
Every rotation the code performs has its rotated child on the witness
path (primA: path[t+1]; primB/zig: path[0]; verified parent links).
Claim: by induction over the rotation sequence, C_final subset C_0.
Proof: let R be the set of all rotated children across the event.
Per-rotation joining (L1) gives C_final subset C_0 union R. Every rotated
child is a path node (code inspection above), hence an ancestor-or-self
of marked path[0] in the verified pre-state tree, hence in C_0. So
R subset C_0 and C_final subset C_0. QED. Corollaries: (a) terminal
genuine marked KEEP events preserve inclusion; (b) DELETE/inactive events
are B-identity (b_blend) hence preserve inclusion; (c) any single-event
low edge satisfies C(t) subset C(s) (sole event must be terminal genuine
marked, else chg/mu conjuncts fail); (d) every contracted-high edge
satisfies C(t) subset C(s) (single marked-target splay to g.b, then
t.b == g.b by b_equal conjunct — all weights, incl. anomalous -3/-4).

## L3. Unmarked-target bound (PROVED, sharp form)

If the splay target x is unmarked, the same per-rotation analysis gives
C_final subset C_0 union R with R = rotated children (path nodes, not
necessarily in C_0). Joins are possible ONLY within R; the bound is sharp
in form (realizable: splay an unmarked root with marked elsewhere ->
root joins; measured 978/1882 in prior source experiments). Consequence:
multi-event low macros with unmarked-target B-changing KEEPs are NOT
covered by L2. This is precisely the open hole — stated, not bridged.

## What is NOT proved (explicit open hole)

No theorem is claimed for: intermediate unmarked-target B-changing
intermediate events (A8 admits them); the resulting R(P) sign for
excursions containing them (2 holding instances only); universal H1/H2/H3;
any potential inequality. The per-rotation and single-target machinery
above is complete and closed; the ONLY missing piece is compensation for
unmarked-target gains across multi-event macros, for which no
source-derived mechanism was found (candidate charging schemes fail the
interface-transport test; A-side cannot observe B-depth beyond shadow).
