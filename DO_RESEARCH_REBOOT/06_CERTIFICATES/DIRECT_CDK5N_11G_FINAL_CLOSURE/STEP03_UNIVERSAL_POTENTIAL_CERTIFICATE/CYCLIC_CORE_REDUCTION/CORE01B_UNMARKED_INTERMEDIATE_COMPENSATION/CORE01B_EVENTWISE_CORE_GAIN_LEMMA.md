# CORE-01B Eventwise Core-Gain Lemma (PROVED; corrects the {x_i} form)

LEMMA (single rotation): only the rotated child c can newly join C;
if c in C before, C is nonincreasing. Proof: only c gains descendants
(p-subtree); everyone else's marked-descendant sets shrink-or-stay
(p loses x-side; S keeps its subtree; middle/gp/rest unchanged); c's own
markedness unchanged; a node joins only by gaining marked descendants.
COROLLARY (splay event): joiners are among rotated children (path nodes).
CORRECTION to naive B1: G_i is NOT in general subset of {target}: zigzig
primA rotates an ancestor child, which may itself join. Precise bound:
G_i subset R_i (rotated-child set). For zig/zigzag-only splays,
R_i = {target} (both rotations target path[0]). For zigzig, R_i includes
the pair ancestor. All bounds are exact rewiring consequences; no
validity/path-consistency assumption beyond the witness itself.
