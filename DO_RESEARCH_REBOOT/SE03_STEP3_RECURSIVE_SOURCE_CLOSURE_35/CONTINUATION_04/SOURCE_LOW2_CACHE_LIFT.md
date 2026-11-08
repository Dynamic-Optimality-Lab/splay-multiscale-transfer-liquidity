# CF35-2 — exact LOW2 source-frame reuse

The rigid-filler proof in SOURCE_CACHE_FRAME_LIFT.md works unchanged for
any fixed root-to-target path of length d<=4. There are d+1<=5 active
operands and d+2 ordered hanging ports. Embed the active path in the
accepted native-ten cache, put its unused keys in one rigid rightmost
filler subtree, then generalize that entire untouched filler to its port.
All d+1 active operands remain. The accepted action gives the actual
ordinary bottom-up destination and H=ceil(d/2). There are30 path patterns
of lengths1..4, not a population truncation. Port substitution never
searches or rotates a new source state; it instantiates a pinned action
identity. Raw template substitutions are reported separately from fresh
original source-engine calls, which remain zero.

For H=2, the source contains either one marked access at depth3/4 or two
one-event accesses y then the genuine marked target x. The complete source
case proof is C14 FULL_PROOF section3, whose depth and operand argument
does not depend on having exactly six marks. Change only the finite
ordered branch-boundary grammar to the seven-mark grammar; retain ALL
the previously required source sectors, especially the private child of
an old unary parent and the second-only unary inside an unchanged rigid
hanger. The source root before the first event is marked; do not reduce
the full middle tree before the second event.

The new generator uses the accepted cache identities for each access.
The independent check must use a different decomposition (bottom local
double plus final root event) or independently bound cache substitutions.
No actual source helper or physical bit is erased. The generated relation
is a necessary source cover for arbitrary private populations and unary
inventories; splicing quotient edges does not establish full closure.
