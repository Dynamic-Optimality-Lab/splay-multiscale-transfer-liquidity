# T25-C — exact R-type v-bit carry gate; universal closure still open

Status: NEW allocator-level necessary retention conditions, audit pending.
This is not a source-valid counterexample or an asserted potential value.

For an R-type hard-unary producer the auxiliary macro v has H1 and
Q=epsilon0/1, with actual units v0,v1. The previous auxiliary t macro
has Q<=1, so v is not part of a q5/q1 pair. Natural h0_E uses v0 if
epsilon1 and nothing if epsilon0. The candidate bit v1 is natural-full
second-double funding but not auxiliary-natural funding.

For cores9--11 let L be the ACTUAL outgoing retained-bank length at v,
L=top-D_after in{0,1,2,3}. branch_funding's pool is new_spares+old_bank
and there are no missing local demands. Therefore:

| epsilon | new spares | v1 retained at v IFF |
|---|---|---|
|0|[v0,v1]|L>=2|
|1|[v1]|L>=1|

For core8, pool is old_bank+spares and debt span<=1. If epsilon0, v1
cannot be retained. If epsilon1, it is retained iff L=1 and the old
bank is empty. Cores6/7 cannot use it: own excludes it, and the next
auxiliary macro p has Q<=1, so v cannot be core7's critical predecessor.

An initial retained bit is NOT necessarily a final h6 payment. Later
prefix replenishment can discard it. If it is used, its actual first
consuming auxiliary demand is non-natural, with one of the source types
H_E1,Q_E3..5,k>=3 or H_E2,Q_E5,k5. These follow from natural excess
Q_E>2H_E and the accepted closed six-key Q_E<=5 bound. The initiating
owner after common normalization need not be that consuming demand.

The analogous full-natural undefined common types have H_F1,k>=3 up
to min(qF,qE,5), or H_F2,k5. In all cases the actual shared source
states and allocator receipt are required; no formal L value or cost
signature is claimed globally realizable merely because the code permits it.

This pinpoints the next open source bridge: determine whether the actual
two-arrival pre-j source and mandatory receipts force this bit to be
discarded, or classify its consuming demand/owner and provide a different
eligible endpoint. No theorem currently supplies that implication for
all R-type producers. T25-U's G exclusion cannot be extended by analogy:
G has six local auxiliary units, R only two. Nested older-common locks
and noncanonical receipts remain additional explicit cases.
