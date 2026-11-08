# Complete source classification of common-prefix eviction

**PROVED—UNIVERSAL for one original paired KEEP source transition.**
All BST sizes, unrelated interiors, external paths and both orientations
are included. This strengthens UI's even/even refinement theorem.
It identifies an actual old ancestor and source event when retention
fails; it does not turn that eviction into a new B-double debt.

Use BL01 notation. The accessed key x is outside the old common prefix
K unless explicitly stated otherwise. A correction's NAME is the tuple
(original external key, original child key, direction). Its name is
absent when no correction is made. Call a level asymmetric if these
named corrections differ in A and B. Two active flags at the innermost
odd/odd boundary have DIFFERENT names because the interval roots differ.

## Exact retention criterion

For h>=1, every old common-prefix key survives in the new canonical
common prefix IFF the appropriate source condition in this table holds:

|Internal source parities|Necessary and sufficient condition for retention|
|---|---|
|even/even|Always|
|odd/odd|Both first internal directions cross the interval-entry direction: s_A!=t_(h-1), s_B!=t_(h-1)|
|even/odd or odd/even|The odd side crosses the interval entry, AND every adjacent pair in the common external direction word alternates|

The mixed condition means t_j!=t_(j+1) for0<=j<h-1. For h=1 that
last requirement is empty. At h=0 there are no old common keys and
retention is automatic. A target already in K retains the old prefix
under identical source-path operations; its nontrivial block is negative.

Equivalently, for a disagreement-interval target retention holds IFF
the source recurrence has NO asymmetric named correction. In every
retention case, x becomes the common root and was not previously in K,
so the new common prefix contains K union{x} and strictly grows.

## Sufficiency from the source recurrence

At the innermost level, even/even makes neither correction. Odd/odd
with both directions cross also makes neither correction. In either
case the lifted partial tree has all old external common nodes still
exposed, with arbitrary paired interval children as holes. At every
remaining outer level the two internal parities agree, and any active
correction uses the SAME original external keys in both trees. The
same base lift and same named rotation preserve the shared partial
tree and every already exposed common key. Induction retains all K.

In mixed parity, parity remains opposite at every level. The innermost
odd side's cross makes no correction. Alternation in the remaining
common external word makes every later potential odd-side pair cross
too, so neither side ever corrects. The identical sequence of base
lifts preserves the common partial tree with arbitrary unequal holes.
Again all old common keys survive and x is added.

This argument preserves each named old key and each common off-path
subtree, not merely a count, and uses no matching of the unrelated
interval interiors.

## Necessity and an explicit evicted source ancestor

**Destructive odd/odd.** If either initial direction is straight, the
first boundary lift is corrected on at least one side. On the branch
toward the old external ancestor g_(h-1), the two resulting child roots
are either a distinct pair of interval roots or one interval root and
g_(h-1). They differ, so g_(h-1) is hidden by a prefix mismatch.

At the next outer level both original local parities are even, so
neither side corrects. Any further active corrections use identical
SHARED outer keys on both sides. The already mismatching inner branch
is carried as a whole paired hole: none of these operations inspects
its interior or pivots at its hidden g_(h-1). It cannot expose that
key again during this access. Thus g_(h-1) is an actual evicted old
common key. This is the only possible asymmetric level in odd/odd.

**Destructive mixed parity.** At every level at most one correction
is active. If the mixed table condition fails, there is at least one
such asymmetric level. Choose the OUTERMOST one, with smallest original
index j. Immediately after that lift one tree has child root g_j
on the branch toward g_j, while the corrected tree has its distinct
original child root p instead. Hence the old common key g_j is hidden
by the mismatch. Every remaining OUTER level has no correction in
either tree by this choice of j. A base zig only wraps an entire
current left/right subtree; it cannot look inside the mismatching
branch and expose g_j. Therefore g_j is still evicted in the full
source output. The recurrence supplies its real same-side source
double index on the correcting side.

Even/even has no asymmetric level; the table exhausts all parity
possibilities. This proves necessity, sufficiency and the constructive
source witness for every failure, for arbitrary path length. An
evicted ancestor may carry arbitrarily many hidden common descendants;
that mass remains irrelevant to this classification and to physical cost.

## Exact example locations in frozen controls

- W's saturated KEEP5 has odd/odd cross entry and preserves old common
  keys. Its positive KEEP7 has destructive odd/odd entry.
- AD overlap4's two nonnegative blocks are odd/odd cross.
- AD overlap2 additionally has a mixed even/odd cross entry at its
  saturated KEEP2, with a one-edge common external path.
- OR's actual FE02 episode has B-only straight corrections at its
  positive and helper, then differing A/B same-side parents at the
  restoring LL. The recurrence identifies its exact source ancestors.

These are source checks and nonvacuity, not finite proof of the table
or a strict new FI/PF/FE coverage claim.

## Consequence for the unrestricted remaining obstruction

An exactly closed all-nonnegative FE02 candidate MUST contain an
asymmetric named correction of the destructive kinds above. Otherwise
every nontrivial block enters an interval and grows K by at least one,
contradicting complete paired closure. This makes the remaining event
source-identifiable rather than treating every odd entry as destructive.

It does NOT prove that these remaining corrections cannot compose
freely, or that they already supply a spare physical A bit. Those
are the separate Step2 obligations assessed in BL00A and BL03.
