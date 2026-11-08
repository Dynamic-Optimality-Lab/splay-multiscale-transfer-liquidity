# LR35 — two local relay constructions for source loss collisions

Status: symbolic derivations. Neither theorem proves that relay bits are
unowned under the original global owner policy. No new semantic execution
was needed. The universal mixed-target escape and Bank25 trace remain open.

## Box 1: simultaneous physical supply within one collision group

Target: give distinct actual physical bits to every demand in ONE group
of FP35 demands selecting the same loss bit.
Conditions: original exactly paired-closed period, the FP35 selected
source proxy and first/last loss bit for each demand.
Inheritance: FP35 within-macro and repeated-target noncollision; actual
A ancestor loss geometry and exact cyclic occurrence identities.
Ambiguity: collisions with other groups, prior owners and Bank25.
Bridge: successive actual targets are different, and each target becomes
the actual A root at its original access.

Let u be the shared loss bit. List the demands in chronological order
from u along their common marked pivot tenure, with original target
occurrences t1,...,tm and keys x1,...,xm. There is at most one demand
from a macro, since its proxy pivots are distinct. The xi are pairwise
distinct by FP35's disjoint intervals for any fixed target.

Give u to the first demand in an independent provisional comparison.
For each i>=2, A has root x_(i-1) after actual t_(i-1), and root xi after
the A phase of actual ti. Thus there is an actual first single rotation
in (t_(i-1),ti] losing x_(i-1)'s ancestor relation to xi. Its pivot is
x_(i-1), and its rotation bit is a genuine original A unit. Give it to
the i-th demand. These intervals are disjoint and exclude u. The proof
uses every original helper and does not require a positive final KEEP
event. Its occurrence order is cyclic within one actual source period.

This is an explicit one-group injection for arbitrary finite
multiplicity, with no claim that any endpoint is free under h0/fE.
Several groups may use the same relay. Treating each separately
does not prove a simultaneous injection across groups.

## Box 2: one destination macro and many earlier direct MD owners

Target: distinct source relay candidates for the blocked direct loss
bits of one later maximal-core macro, even with repeated owner keys.
Conditions: maximal full B core; actual marked grandparent source;
a common linearized ORIGINAL interval containing all referenced
genuine tenures, A loss events, owner macros and destination macro,
with no wrap in any of the comparisons below. Earlier owners in
this Box use one actual DIRECT MD35 loss rotation per demand.
Inheritance: marked-parent projection, marked demotion shrinkage,
original A ancestor losses and all physical bit identities.
Ambiguity: a relay can be already owned, collide with unblocked units,
or fail to satisfy extra block eligibility. These are not waived.
Bridge: common direct owners are separated by B's actual demotions;
repeated owner keys force intermediate actual resets of marked pivots.

### A. At most one common marked pivot per pair of macros

Suppose earlier macro s and later macro t both have a direct MD35
candidate loss bit for a pivot G with the same original bit identity.
The selected actual bit occurs no later than s and after the most
recent genuine KEEP G for each macro. So G is not genuinely accessed
between s and t on this original interval.

If two different pivots G and H had this property, both were marked
proper ancestors of the target of s. By the proved maximal-core
marked-parent projection, after s they are both children of that
target in the marked ancestor tree. In particular their full rooted
subtrees are disjoint: overlap would put one marked key above the other.
Neither pivot is genuinely accessed between s and t. Both descendant
sets only shrink, so they cannot both contain the target of t.
That contradicts both being its original marked B grandparent pivots.

This bounds common PIVOTS, not the number of all possible loss bits
for one pivot. When each demand has selected one direct loss bit, it
implies at most one collision between these two macro selections.
The common no-wrap interval hypothesis is essential to this argument;
cyclic tenures must not be identified across a different cut.

### B. Source separation for repeated earlier owner keys

Let t be the one later macro, with distinct selected MD35 bits for its
original demands. Each blocked bit is held by a distinct earlier
macro: two blocked bits from one earlier macro would contradict A.
Partition those earlier owner macros by their original target key y.
The key y cannot equal the target of t. In fact, whenever a mark G
is a pivot at an x access, its most recent genuine KEEP G must be
after the previous genuine x: after the previous x, x is B root and
is not below G, and G cannot regain it without a genuine G access.
Thus direct-loss witnesses for repeated x targets lie in disjoint
actual x-to-x intervals.

For a fixed owner key y, write its owner occurrences in chronological
order s1<...<s_l. Let G_(i+1) be the actual marked B pivot of the
owner demand at s_(i+1). After si, B root is y, so G_(i+1) does not
have y as a descendant. To be a pivot at s_(i+1), G_(i+1) must have
been genuinely accessed at an original occurrence vi strictly
between si and s_(i+1), by MD35 shrinkage. Pick the last such vi.

At si A root is y. At vi A root is G_(i+1), which differs from y.
The first A loss of y->G_(i+1) in (si,vi] supplies a real pivot-y
bit. Use this as the relay for the destination claim blocked by
the owner at si. For the last owner s_l use the first actual loss
of y->target(t) in (s_l,t], which likewise exists.

Within one y class the intervals are disjoint. Different y classes
have different loss pivots, hence different actual rotation bits.
Each proposed relay is strictly after its original blocking owner
occurrence, and therefore after its original blocked bit. The rule
gives distinct physical relay candidates for ALL blocked claims
of the one destination macro, including repeated owner keys.

### C. Exact missing implication

The new relay bits are not assumed to be h0-free, comparison-safe
under extra fE locks, or unused by another destination macro.
After using a relay an owner is no longer a direct MD35 owner;
part A cannot be applied to that changed owner graph without a
new invariant. The chronological increase of one candidate is
not a valid global termination proof when owners, cuts or source
eligibility change.

The next Box is to close mixed DIRECT/RELAY ownership components,
including the original seam and nonmaximal proxies. Prove a
source-derived new eligible endpoint or a licensed exchange without
displacing a frozen owner or treating analytical relay capacity as
extra bits. The two constructions above are local progress, not
universal JR35. Reservation compatibility remains deferred.
