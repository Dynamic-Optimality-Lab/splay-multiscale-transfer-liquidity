# RV26-R — exact canonical token lifetime, not a full source feasibility proof

NEW manuscript derivation, independent audit pending. No source engine,
debt evaluator or allocator process ran. The bank selection code was read
unchanged. Nonvacuity under the full two-arrival guard remains separate.

## 1. High-core rank/price law

Use the ACTUAL canonical six-key core9--11 comparison h6 and its legal
maximum-debt cut. For one original packet let B=2min(H,4), Q its true
auxiliary doubles, n its fixed natural-own count, S=B-n selected fresh
spares, M=Q-n missing demands. The code pays missing demands in original
packet order from pool=fresh_spares+old_bank, then retains its PREFIX
of length L_after=top-D_after<=3. Its signed price is w=B-Q.

Suppose a physical old token u has incoming one-based bank rank r.
It is outside the global natural-own image and occurs once. Its pool
position is S+r. Therefore EXACTLY one of the following happens:

    PAID iff M>=S+r, equivalently r+w<=0;
      consumer is missing-demand list element S+r;
    KEPT iff 1<=r+w<=L_after, outgoing rank r+w;
    DISCARDED iff r+w>L_after (with positive r+w).

Proof: sequential prefix payment removes the first M elements. An
unconsumed token's remaining position is S+r-M=r+w. Prefix truncation
gives the other two cases. Both payment and discard remove it permanently;
it cannot be selected by a later packet. All labels remain actual source
units/demands, not tokens borrowed from a previous cyclic copy.

Let sigma=w+D_after-D_before>=0 be the ACTUAL accepted certificate slack
and g=L_before-r the number of bank tokens behind u. Along a KEPT step,

    g_after=g_before-sigma.

Thus accumulated integer certificate slack cannot exceed the initial g
while the token survives. This uses the original fixed six-key source
debt, not any changing-chart normalized M3 candidate. It gives a signed
source-path restriction; it does not assert abstract tight paths realizable.

## 2. Immediate source consequence at v,p

The R-type v and next p are consecutive auxiliary singleton H1,Qepsilon
macros: the preceding t and v have Q<=1, so neither is paired with q5.
There are no local missing demands. At birth the v-second bit has rank
r_v=2-epsilon if retained. At p, w_p=2-epsilon, so its new rank would be

    r_p=4-2epsilon.

If epsilon0 this is4, greater than EVERY possible bank length3. Hence
the bit is DISCARDED AT p, with no raw h6 payment at v or p or later.
This strengthens T25-C's retention threshold; it does not erase an older
common owner or call the physical bit free under the full allocation.

If epsilon1 the bit survives p iff L_p>=2, and then its rank is2.
Its remaining gap g_p=L_p-2 is0 or1. Until first payment/discard, all
subsequent KEPT packets have cumulative slack at most ONE. If g_p=0
they must all be tight. Arbitrarily long zero-slack source paths are
not ruled out by this bound. The terminal consuming packet is not
included in a bound that was proved only for kept steps.

## 3. Exhaustive high-core RAW consuming-packet types

An old token can be paid only if w<0. The actual packet partition has
singletons Q<=4,H>=1 or a genuine q5/q1 pair Q6,H>=2. Thus the ONLY
negative cases are the following; r is the rank BEFORE that packet:

| Actual packet | Incoming ranks consumed | First consumer of this token |
|---|---|---|
| singleton H1,Q3 |1|terminal auxiliary double3|
| singleton H1,Q4 |1 or2|terminal auxiliary double(2+r)|
| q5/q1 pair, both H1 |1 or2|FIRST macro auxiliary double(3+r)|

For the pair, the three missing IDs are first-macro doubles3,4,5. One
fresh spare from the ACTUAL successor precedes old bank units, so rank1
pays double4 and rank2 double5. Every original operation in the pair
remains, including the successor's true positive occurrence/bit. H>=3
q5/q1 pairs have w>=0 and cannot consume this OLD token: fresh selected
spares cover their missing demands first. In particular T25-C's broad
H_E2/Q5 natural-excess possibility is NOT an old-bank consumer here.

Given an ACTUAL source trace, the first consuming packet is precisely
the first packet satisfying r+w<=0 after applying the KEPT recurrence;
if discard occurs first there is no raw payment. Empty final bank at
the legal cut makes this dichotomy exhaustive for one period. This is
an exact receipt trace rule, not a complete classification of which
guarded source geometries can realize each outcome.

## 4. Other canonical backend cases

Core6 is natural-only and cannot use v-second. Core7 can use a producer
spare only as the actual predecessor of a Q3 critical macro, but the
next p has Qepsilon<=1. It therefore never uses this bit.

Core8 has FIFO-style old_bank+spares and bank span<=1. Epsilon0 cannot
retain v-second. If epsilon1 was retained, it is the sole old token.
At subsequent macros it remains first, is discarded when the outgoing
bank is0, or is consumed by the FIRST natural-excess macro. Since Q<=3,
H>=1, that consumer can ONLY be H1,Q3,double3. New spares cannot move
ahead of the old token in this backend. Never apply the high-core
fresh-prefix rank law to this different FIFO rule.

## 5. Physical/effective limit

These are AUXILIARY COMPARISON payments. A consuming ID c may be common
with the full source or auxiliary-only. Older f5 normalization may give
u a different initiating auxiliary owner. The original full a0 may fix
u to that common owner or to its own full v-second demand. Those steps
are proved separately in RV_EFFECTIVE_OWNER_CERTIFICATE. Retained, raw
paid and effective frozen are not identified.
