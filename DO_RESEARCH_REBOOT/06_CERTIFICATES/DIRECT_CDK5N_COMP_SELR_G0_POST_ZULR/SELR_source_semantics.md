# SELR original source semantics (arbitrary ambient scope)

T0 fixture (witnesses only):
[9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],null]]],[8,[7,null,null],null]],null].
Both A and B start at T0. KEEP(x) splays x in A and B. DELETE(x) splays x
only in A and freezes B. DELETE removes nothing; every target must exist
(absent-key replay raises: fail-closed). Pre-access edge depths (root 0):
a=ceil(dA/2); KEEP q=floor(dB/2); DELETE q=0. A=Σa, Q=Σq. Exact closure =
equality of the entire labeled A/B pair state (root equality insufficient).
Universal theorem scope: arbitrary admissible ambient BST sizes and access
lengths. Nine-node constraint applies to the complete marked B-ancestor
core (ancestor-closed path union), not the ambient tree; for genuine KEEPs
the core bound gives d_B≤8, q≤4 definitionally.
