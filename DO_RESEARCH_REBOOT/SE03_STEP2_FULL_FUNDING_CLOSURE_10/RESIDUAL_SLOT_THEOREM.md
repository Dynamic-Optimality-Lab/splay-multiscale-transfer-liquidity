# Uniform physical residual-slot and frozen-owner theorem

Status: PROVED, for ANY finite support and any actual disjoint cyclic
source packet partition. It is a reduction of funding obligations, NOT
a proof that its remaining physical donor requirements are satisfied.

Fix ONE actual aligned source period I and actual maps/identities. Let D
be its full demand set and U its physical A-event bits. Let C be common
full demands paired by occurrence/ordinal with auxiliary demands. Pull
back the actual fixed fE on these common pairs to a locked injection
l:C->U. Its image and original values must stay fixed. Auxiliary-only
claims N are retired only for the alternative full allocation, as in the
inherited signed-cancellation theorem; the archived fE stays unchanged.

## An independently constructed partial full map

For each ACTUAL full packet e, list its 2H_e physical bits in replay
order and Q_e full demand IDs in replay order. Let h0 assign the first
min(Q_e,2H_e) demands to the same number of its OWN first bits. If the
packet crosses I's seam, construct at a packet cut and transport BOTH
IDs by the accepted period bijection. Distinct packets have disjoint
source occurrences, bits and demands. Thus h0 is injective independently
of CD, any global debt, fE, or availability under fE.

Write

    R = D minus domain(h0),
    R_e = final max(Q_e-2H_e,0) demands of packet e.

The sets R_e are disjoint and R=union R_e. These are actual demand IDs,
not synthetic credits or a deficit counted without an owner. All original
A events are retained; clipped allowances2min(H,4) are not substituted.

## Exact partial exchange, including failure

For every p in (D minus C) intersect domain(h0), start at h0(p). If it
is not locked, assign that terminal unit to p. If it is l(c), continue
at h0(c) WHEN c belongs to domain(h0). If it does not, STOP BLOCKED at
the actual common demand c in C intersect R. Never declare that unit
free or invent h0(c). The algorithm physical_exchange.py implements this.

Paths terminate or stop blocked. A reached common-only cycle would have
an incoming path but every vertex/unit has at most one incoming edge,
by injectivity of h0 and l; reversing predecessors would identify the
initial unmatched p with a common demand. This is impossible. The same
predecessor argument proves two different unmatched roots cannot meet.
Consequently all successful terminal units are distinct, outside im(l),
and all blocked roots have DISTINCT blocked common owners in C intersect R.

Keep EVERY locked l(c) unchanged. Add the successful terminal assignments.
This defines an injective partial full map a. Its only unfunded demands are

    Pstar = ((D minus C) intersect R) disjoint_union blocked_roots.

Define anchor:Pstar->R by anchor(p)=p in the first component, and the
blocked common owner c in the second. Within each component it is injective;
the first lies in R minus C and the second in R intersect C. Therefore

    anchor is an EXPLICIT injection,
    |Pstar| <= sum_e max(Q_e-2H_e,0).

This does not assume a desired matching or its equivalent cardinality
bound. It constructs a, all paths, every blocked owner and each anchor.
Some unfunded p can occur in a safe packet: its anchor lies in a deficit
packet because of a cross-packet fixed auxiliary lock. This is exactly
why independently safe packet capacities do not establish availability.

The remaining available actual units are

    Wstar = U minus im(a).

Their ownership status is exact; no l(c) unit is in Wstar. In particular,
every unit in U minus (im(h0) union im(l)) is STILL in Wstar: successful
terminal units lie in im(h0), and locked assignments lie in im(l). This
gives a concrete intersection of full-unused and auxiliary-unowned reserves.
Retired fE(N) units and U_E must be counted through their actual IDs, never
twice. The complete full injection is still missing unless an independent
source rule assigns DISTINCT Wstar units to all Pstar.

## Six-key consequence and the closed core6 case

For full core6, Q_e<=floor(5/2)=2 for every natural macro and H_e>=1.
Thus R is EMPTY, h0 is already a complete independent full map, no path
can block, and a is a complete full injection preserving every common
fixed fE value whenever that certified auxiliary map is supplied on I.
This proves original CD6 on the entire CORE6 subclass, unconditionally
by h0, and the corresponding ownership extension for any such fixed fE.
It neither assumes that Step1's special debt allocator covers smaller
auxiliary cores nor replaces an existing fE by a convenient new map.

At six keys, nonempty R can arise only from H1/Q3 (one slot), H1/Q4
(two slots), or actual paired H2/Q6(two slots). Core7/8 admit the first;
core9/10 admit the first two; core11 admits all three. This is the exact
physical residual supply target, not a positive theorem about its repair.

## Universal source-time and ownership scope

The theorem is independent of support size, order orientation, private
populations, history length, chart labels or a constant debt width. All
edges reference actual event/bit and demand identities in ONE period.
Its allocations are cyclic/block allocations; no native strict temporal
or matching-terminal eligibility follows. Those conditions need a further
source proof if required. Partial exchange does not grow a token bank or
alter Bank25; recorded paths are proof receipts, not controller state.

The new explicit source families have complete full repairs using actual
spare bits in their preceding preparation packet. But the stronger claim
that EVERY deficit is repaired that way is REFUTED by the pinned Sigma
predecessor: the H1/Q4 packet at occurrence46 needs two bits, while its
immediately preceding H1/Q1 packet at45 has only one spare bit. No choice
or exchange limited to that packet can provide two units after paying it.
This is not a counterexample to CD6 or to unrestricted physical repayment.
