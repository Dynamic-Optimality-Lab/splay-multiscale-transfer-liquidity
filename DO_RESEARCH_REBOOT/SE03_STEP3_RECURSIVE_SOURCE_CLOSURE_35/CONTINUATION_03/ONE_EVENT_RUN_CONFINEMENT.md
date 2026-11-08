# OR35 — anonymous-operand confinement for arbitrarily long H=1 runs

This theorem is independent of maximal B-core assumptions. It is an exact
source representation theorem, not a signed credit theorem.

## 1. One-event natural macro normal form

Let a genuine natural macro go from previous genuine key y to x, x!=y,
and have total A-event count H=1. Its starting A and B roots are both y.
There is exactly one positive A access. Every preceding zero-event access
targets the unchanged root y. Every subsequent zero-event access targets
the new A root. Since the final KEEP is x, that positive access MUST be x.
It has initial A depth1 or2. It is either the KEEP x itself or an earlier
DELETE x followed only by zero-event DELETE x until the final KEEP x.
Before it, root-repeat KEEP/DELETE y operations are retained literally.

In particular the actual A endpoint is Splay_x(A_start), one zig or one
bottom-up double. No positive access to an anonymous or different marked
helper is hidden inside an H1 macro. This argument uses the original h=0
root-repeat semantics and does not omit an original operation or event.

## 2. First-use theorem

Fix ANY finite consecutive run of such macros. M is the whole original
genuine key set, |M|=r, not just keys occurring in this run. At its entry
let P0 be all unmarked nodes which are the IMMEDIATE parent of some marked
node in the actual A tree. The entry root is marked. Hence |P0|<=r-1:
every member has a distinct chosen marked child, none of them the root.

Claim: every anonymous operand of EVERY positive A event in the run belongs
to P0. A zig has marked old root and marked target and no anonymous operand.
A double has marked old root y and marked target x; its only possible
anonymous operand is their intermediate parent p.

Suppose p is used for the first time. Before that first use its CHILD
pointers are unchanged from entry. Indeed an H1 event is at the root:
the only nonoperand external parent of an inner rotation is its marked
old root, and all other modified child pointers are those of its operands.
An anonymous node's child pointer can therefore change only when that
node itself is the intermediate operand of one of these events. Incoming
parent edges may change, but that does not change its own child pointers.
At first use p has marked child x, so it had that same child at entry.
Thus p was in P0. Contradiction to any first use outside P0. QED.

The proof allows arbitrarily many events and both mixed/SS doubles. It
does not assume an initially prepared A, a depth bound on other keys, or
finite private populations. Operands of an individual event are not
mistaken for all vertices whose incoming parent edge moves with a hanger.

## 3. Exact marked-shadow lifting

Retain all r marks, the entry unmarked branchers of their A ancestor core,
and P0. A marked-rooted core has at most r-2 unmarked branchers (the
inherited binary branching count). Thus at most

    r+(r-2)+(r-1)=3r-3

named vertices suffice for this A shadow over the ENTIRE H1 run. Retain
these nodes even if their later branch/unary status changes. Every other
unmarked unary core vertex is an inactive operand by section2. Contract
it only as a remembered ordered unary CONTEXT, and keep every off-core
private BST as an arbitrary rigid term. These contractions commute with
every actual event: a contracted vertex cannot lie on an actual active
search path, otherwise it would be an operand of that depth<=2 event.
Its term/context is moved whole at a side port, never entered or modified.

All original root-repeat operations remain as identity rows. All actual
A events, physical bit labels and reduced endpoints are preserved. Full
physical endpoints can be reconstructed using the SAME context assignments;
reduced equality alone is not declared full-state closure while ignoring
these remembered contexts.

For an original B-closed source its fixed full core S_B has at most2r-1
labels. B's off-core terms are rigid under all genuine accesses. Combining
the two views names at most4r-4 distinct core/shadow labels, because the
r marks are shared. A known label of one view may be hidden in a rigid
term of the other: preserve physical alias/order/membership annotations.
This is two finite SKELETON views with arbitrary actual ordered contexts;
it is not a claim that both full trees have at most4r-4 physical nodes.

## Limits relevant to the parent

The lifting is complete FROM actual H1 source runs; it does not realize
every abstract skeleton path. A negative path still needs an original
source embedding. A future H>=2 macro can expose a previously inactive
anonymous node, so P0 must be recomputed at the next run entry. No permanent
global deletion/contraction or support reduction is allowed.

This removes dependence of the H1-run shadow size on run length and
private unary populations. It does not prove a nonnegative cycle, bounded
path deficit, source supply at the high-run boundaries, or Bank25 for an
uncompleted comparison. Those are the actual remaining credit obligations.
