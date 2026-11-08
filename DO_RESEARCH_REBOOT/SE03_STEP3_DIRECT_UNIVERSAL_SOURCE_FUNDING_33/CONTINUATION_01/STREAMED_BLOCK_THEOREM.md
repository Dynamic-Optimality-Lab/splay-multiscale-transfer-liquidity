# Selected-bit streaming for an independently licensed source block

This is a construction theorem, not a proof that the source supplies its
budget. Its applicability is the ORIGINAL static within-block counting
license of C14: all source executions are fixed, actual donor/demand IDs
are certified, and a within-packet donor may follow its demand in source
time. It makes NO online/all-original-event endpoint claim. In particular
it cannot license any unproved target restriction or extra reservation.

Fix a disjoint original packet. Select2c actual bits, including every one
of the n fixed natural h0 owner bits. List its Q-n remaining actual demands
in original ordinal order. Incoming b_s unused actual units are disjoint
from the packet. Required outgoing count is b_t; 0<=b_s,b_t<=K. Suppose

    b_s+(2c-n)-(Q-n)=b_t+s,  s>=0.

Then the SAME local source budget has an allocation working queue of at
most K+2 actual unassigned bits, independent of c,Q,H. It preserves every
h0 value, emits every missing demand once, retains exactly b_t actual
unused bits, and explicitly releases the rest. No unused bit is stored
as an uncounted IOU or resurrected after release.

## Construction

Process the original A-event records of this packet in their source order.
At most two physical bits enter the working queue per event. Nonselected
bits are immediately released. A selected h0-owned bit immediately emits
its specified h0 pair; it is assigned, never a free bank token. Such a pair
is a completed static block assignment in the proof output, not a claim
that the original B operation occurred earlier. No native event is reordered
or rerun; the funding computation consumes already certified source records.

For each missing demand, first use an available carried/free bit. If the
queue is empty, advance the local event stream until a selected free bit
appears, then assign it to that demand. Advance the stream ONLY at an
empty free queue while missing demands remain. Thus this phase never needs
more than max(K,2) unassigned working bits. Fixed h0 pairs are emitted at
their actual donor-record visit, independently of the missing-demand list.

After every missing demand is paid, release any queue excess above b_t.
Continue the A stream, retaining free bits only until exactly b_t remain;
release further free bits immediately. Finish all remaining h0 pairs.
One event temporarily adds at most2 bits to a queue already at most K,
so the total physical unassigned working buffer never exceeds K+2.

## Sufficiency and ownership proof

Before all missing demands are paid, no free unit is released. If j such
demands have been paid, remaining queue plus unread selected FREE bits
minus(Q-n-j) equals b_t+s. Hence an empty queue with a missing demand
cannot exhaust the stream: unread free capacity is positive. All demands
are paid. There are at least b_t free units left afterward, so retention
finishes. Every input unit is either assigned to one fixed/missing demand,
retained unused, or released once; these statuses are disjoint. Distinct
source IDs and disjoint packets prove injectivity inductively.

For a signed source license put b_s=K-D(s), b_t=K-D(t). Its source inequality
is precisely the displayed sufficiency identity. A legal actual maximum-D
cut starts and ends with an empty queue; both-endpoint period transport is
the accepted one. Thus K<=23 is a sufficient Bank25 condition even when
packet c is unbounded. This does not prove bounded K for arbitrary sources.

## Applicability boundary

This algorithm is an OFFLINE STATIC BLOCK comparison construction: emitted
pairs are assigned output, and unassigned selected units alone form this
working queue. This is the original independent-construction bank, not
the stronger endpoint bank. If a supplied source policy forbids committing
a named assignment until a later physical time, or requires additional
reservation of that bit, its retained token must still be counted and this
particular bound does not apply. No universal extra-policy license follows.
All final effective common/frozen-owner exchange requires its own original
license, exactly as in C14. No old fE/h0/a value is changed by this theorem.
