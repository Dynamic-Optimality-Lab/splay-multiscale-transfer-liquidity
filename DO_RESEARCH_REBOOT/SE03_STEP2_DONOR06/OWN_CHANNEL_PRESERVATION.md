# A preserved source statistic within each signed channel

Use CORE_DEFICIENCY_CHANNELS.md on an arbitrary closed original B history.
For channel h let K_h count unmarked channel-h core vertices whose OWN
channel subtree mass is1. Every such mass is0 or1. The theorem is:

    A KEEP of a mark of channel h NEVER INCREASES K_h.

This is not an A-dependent repayment inequality. In particular, it
does not assert that a foreign-channel KEEP preserves K_h.

## Persistence and the rebuilt target

Fix a genuine target x in channel h. Give its own-channel marked/unmarked
labels weights+1/-1 and every foreign-channel label weight0. Every source
subtree has channel mass0 or1. An own-channel marked root has mass1.
The processed-subtree persistence proof from DONOR05 is purely a source
frame fact: all later outer frames reattach processed G/P subtrees whole.
Their masses already have their FINAL values. Thus every proper child
of the rebuilt x has nonnegative own-channel mass, and its whole mass
is at least1. Its label set is an original source subtree of mass<=1;
it has mass1 and its two proper child masses are0 at every completed frame.

## Exhaustive next-frame calculation

For LL use the actual source and target

    G(P(x(A,B),C),D) -> x(A,P(B,G(C,D))).

Let g,p be G/P's channel weights, and c,d the channel masses of C,D.
The rebuilt target mass1 and a=b=0 give

    g+p+c+d=0,   0<=c,d<=1.

P cannot be an own-channel mark: its source subtree would have mass>=2.
Its possibilities are own U(p=-1), or foreign(p=0). Final processed G/P
must have masses>=0, with lower bound1 when they are own marks. These
facts give ALL possible cases relevant to K_h:

| P | G | Consequence | Delta K_h |
|---|---|---|---|
|own U|own M|c=d=0|0|
|own U|foreign|c+d=1|-c<=0|
|own U|own U|c=d=1|-1|
|foreign|foreign|c=d=0|0|
|foreign|own U|source P mass1+c<=1, hence c=0,d=1|-1|

The missing foreign-P/own-M case would require1+c+d=0 and is impossible.
In all rows an own-U P has final mass0. When G is own U, its source
mass1 changes to1 or0 as shown. No foreign vertex is counted in K_h.
RR is the reflected source calculation with its ACTUAL hangers; its
possible changes are again0,-c or-1, all nonpositive.

For LR use

    G(P(A,x(B,C)),D) -> x(P(A,B),G(C,D)).

The new target children have channel mass0, so p+a=0 and g+d=0.
Neither G nor P can be an own mark. Each own U among them has SOURCE
mass1 and final mass0; each foreign vertex contributes nothing to K_h.
Hence Delta K_h=-I[G own U]-I[P own U]<=0. RL has the same conclusion
from its own primitive formula. Hangers and untouched subtrees keep
their rooted label sets and their channel masses.

At a terminal zig the old full root is marked. It cannot be an own
mark, because its source channel mass would be at least2. If it is
foreign, its weight is0 and no own U is rotated, so Delta K_h=0.
DELETEs and root identities fix B. Summing the exhaustive source frames
proves the theorem for every actual own-channel KEEP, with all original
operands, hangers and occurrences retained.

## Exact flux identity and the remaining ownership issue

On an actual fully closed period, sum Delta K_h=0. Therefore the signed
sum of foreign-channel changes equals the nonnegative total of the
decreases at own-channel accesses. This is an exact source interface
identity, not an A-unit injection. Foreign changes must retain their
signs; none is declared a free source of units.

At core10, K_0+K_1 is at most(r_0-1)+(r_1-1)=4. This bounds the number
of own-channel positive unmarked vertices, NOT full A debt or reserved
units. It does not remove cross-channel KEEP effects, prove the sign
of each foreign change, or permit spending one A bit on both channels.

At deficiency0 there is just one channel. Full closure then eliminates
all strict decreases and recovers the completed maximal-source argument.
This consistency implication reuses that theorem; no old row is replayed.
