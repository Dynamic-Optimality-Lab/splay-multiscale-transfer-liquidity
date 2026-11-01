# Right-spine retention in the exact splay source

Status: PROVED—UNIVERSAL for finite BSTs with distinct ordered keys and present target x, using the repository's bottom-up parent-first same-side convention. The proof is the six symbolic source formulas below. The finite source replay checks their binding to both implementations; it is not the justification for the universal quantifier.

Let RS(T) be the ordered list of vertices reached by following right children from the root. Write concatenation by commas. Empty fringe spines contribute the empty list. The source is python/independent/splay.py, functions _rebuild/trace, checked against python/liquidity/legacy_embedding.py, function splay_trace.

## Exhaustive source frames

Write k(L,R) for a node. A,B,C,D are arbitrary valid BST fringes, including empty fringes, in their indicated key intervals. In every row x is the accessed vertex throughout the bottom-up rebuild.

| Frame and pivot order | Before | After |
| --- | --- | --- |
| LL: x<p<g | g(p(x(A,B),C),D) | x(A,p(B,g(C,D))) |
| RR: g<p<x | g(A,p(B,x(C,D))) | x(p(g(A,B),C),D) |
| LR: p<x<g | g(p(A,x(B,C)),D) | x(p(A,B),g(C,D)) |
| RL: g<x<p | g(A,p(x(B,C),D)) | x(g(A,B),p(C,D)) |
| left zig: x<g | g(x(A,B),C) | x(A,g(B,C)) |
| right zig: g<x | g(A,x(B,C)) | x(g(A,B),C) |

The LL/RR formulas are exactly the source's parent-first double rotations. Their right-spine effects are:

| Frame | Old right spine | New right spine | Removed old vertices |
| --- | --- | --- | --- |
| LL | g,RS(D) | x,p,g,RS(D) | none |
| RR | g,p,x,RS(D) | x,RS(D) | g,p, both <x |
| LR | g,RS(D) | x,g,RS(D) | none |
| RL | g,p,RS(D) | x,p,RS(D) | g<x |
| left zig | g,RS(C) | x,g,RS(C) | none |
| right zig | g,x,RS(C) | x,RS(C) | g<x |

Every opaque fringe suffix is identical before and after. If the active subtree is attached off the global right spine, its replacement leaves that spine unchanged. If its root lies on the global right spine, the table gives the change to its suffix. The unchanged outer prefix cannot lose a vertex. Therefore every frame preserves each old global right-spine vertex whose key is greater than x. Induction over all frames proves

    {y in RS(T): y>x} is a subset of RS(S_x T).             (1)

The new root x is also on RS(S_x T). Root no-ops have no frames and satisfy (1). The argument handles arbitrary tree size, target depth and fringe shape. The reflected statement preserves every old left-spine vertex smaller than the accessed key.

## Elementary loss budget

An elementary left rotation at p changes the local right spine from p,x,RS(C) to x,RS(C), if the site is on the global right spine; it removes just p. An elementary right rotation changes p,RS(C) to x,p,RS(C), retaining all old vertices. Off-spine sites change no global right-spine vertex. Consequently a sequence of r elementary rotations removes at most r vertices from any counted subset of the old right spine, even if later rotations add new ones.

A source splay with q doubles and z in {0,1} final zigs has a=q+z grouped StepEvs and 2q+z elementary rotations. Thus

    raw rotations=2q+z<=2a.                                (2)

In particular one-StepEv work can remove at most two old counted spine vertices; a zig can remove at most one. The upper bound does not identify added vertices as spendable resources, and does not assume a deletion target stays off the access path.

## Source binding and reflection

spine_symbolic_certificate.json records every template, its right-spine token lists, pivot order, possible removals and unchanged arbitrary-fringe suffix. Each frame is also instantiated once on all thirteen existing keys, with every fringe nonempty, and checked against the tuple source. The pointer verifier checks those six instances and their six reflections, every input/output tree, event interval and zig direction. Its other fixed-word/control accesses independently check (1) and (2) as additional finite controls.

The universal proof uses the source rewrite identities and the global attachment argument; no enumeration of tree shapes, fit across n or extension from finite samples is used. No matching-terminal object is introduced.
