# The proper-ancestor reset shortens the next path by one or two

Status: PROVED—UNIVERSAL local source identity, with the same finite ordered BST and present-key assumptions as the exact source. This records the correction made before the gate: the depth drop is not always two. It does not assert that a next KEEP's grouped cost decreases, and no A policy is executed after the failed B gate.

Suppose the next target y has A edge depth d>=3. Let u be its depth-two ancestor, with parent p and grandparent/root g. DELETE u has exactly one source double and a_D=1. The key u differs from the current A root and from y, so the new block is genuinely KEEP-less when followed by the next KEEP y. The elementary rotations are the repository's parent-first LL/RR or mixed LR/RL pair.

The four source formulas and the tracked u-fringe changes are:

| Frame | Before | After | Tracked target fringe | Target depth drop |
| --- | --- | --- | --- | ---: |
| LL | g(p(u(A,B),C),D) | u(A,p(B,g(C,D))) | A | 2 |
| LL | same | same | B | 1 |
| RR | g(A,p(B,u(C,D))) | u(p(g(A,B),C),D) | C | 1 |
| RR | same | same | D | 2 |
| LR | g(p(A,u(B,C)),D) | u(p(A,B),g(C,D)) | B | 1 |
| LR | same | same | C | 1 |
| RL | g(A,p(u(B,C),D)) | u(g(A,B),p(C,D)) | B | 1 |
| RL | same | same | C | 1 |

Before rebuilding, the tracked fringe root lies three edges below g. A fringe kept directly under u lies one edge below the new root, giving drop two. A fringe reattached beneath p or g lies two edges below the new root, giving drop one. The target's depth within its fringe cancels. This covers both sides of u, all orientations, arbitrary nonempty tracked fringes and any depth within them. Other fringes can be empty or arbitrary. No zero-weight helper assumption is used.

Thus the future target has depth d-1 or d-2 after the reset. Its grouped cost ceil(d/2) can drop by zero or one: a one-edge drop from even d need not change it. The reset's own capacity is always two physical units and must still be counted in C_D. Neither direct path shortening nor a syntactically starved future KEEP proves net E>C_D.

If d<=2, the declared fallback DELETE of the current A root is a no-op with a_D=0. It cannot count toward the requested two effective one-StepEv resets. The B preflight stopped this run before any such choice was made. The identity is a local component, not a completed A/B coupling, an allocation rule or a replacement for the failed source budget.
