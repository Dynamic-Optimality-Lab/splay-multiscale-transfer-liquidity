# CORE-01B First-Birth and Survival Analysis (Gate C)

A new member x in G first appears at some intermediate rotation (as a
rotated child gaining marked descendants) or via terminal restructuring.
For x to SURVIVE to C_n, x must retain a marked descendant through all
later rotations, INCLUDING the terminal marked-target splay. The terminal
splay restructures around the marked target y: any surviving x must either
be y, an ancestor of y's final position with marked below, or carry its
own marked subtree untouched through the terminal rotations. The analysis
identifies the exact survival condition but NO universal removal theorem:
whether a given x is dislodged depends on concrete ancestor relations the
abstract relation does not constrain. Repeated targets: U is a set;
re-entry is membership (idempotent), no double-counting issue arises.
Dangling case (documented OPEN): unmarked intermediate target retained
as marked ancestor through terminal splay with no compensating loss —
predicate-admitted, uncertified either way.
