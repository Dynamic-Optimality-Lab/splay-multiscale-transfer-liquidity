# CORE-01 Rotation Lemmas (PROVED from frozen code; no solver)

R1 (single rotation, child in closure): let R(x,p) be single_rot with
child x, parent p, x in C(before). Then C(after) subset C(before). Proof:
the rewiring moves S (x's rotation-side child) from x to p (same ancestor
SET: {x,p,gp,...} both sides), middle untouched, gp's descendant set
unchanged, rest untouched; x gains p-side (x already in C: no entry);
p loses x-side (may only drop); S keeps its marked-descendant set
(identical subtree) so its membership is UNCHANGED; no other node gains
marked descendants. Only x could enter, and x is already a member. QED.
R2 (primA zigzig): all relinked nodes are path nodes (ancestors of marked
target, hence in C); S keeps its ancestor set; same conclusion. R3
(primB/zig/zigzag with path[0] marked): identical shape. R4 (DELETE/
inactive/no-op): b_blend identity -> equality. Corollary: any single
marked-target splay (any zig/zigzig/zagzag composition, any depth, any
witness path consistent with the tree) preserves C (nonincreasing).
Independence: holds per rotation regardless of event count or H/q.
