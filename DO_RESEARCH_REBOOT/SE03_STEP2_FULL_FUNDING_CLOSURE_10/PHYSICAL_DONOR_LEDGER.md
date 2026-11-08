# Physical donor ledger and exact remaining ownership

For the chosen actual aligned interval I, U consists ONLY of(t,j,b),
1<=j<=actual a_t, b0/1. D consists ONLY of actual full BF double IDs(t,k).
Auxiliary IDs carry a separate execution tag. At each retained occurrence
pair the first min(qF,qE) full/aux ordinal demands. These are unit-demand
correspondences, not equality of rotations or trees. C,P,N partition the
common, full-only and auxiliary-only claims; erased Kz has no E demands.

| Unit/claim status | Physical meaning |
|---|---|
|fE(C)|LOCKED common owners, carried over at the exact original values|
|U_E|Actual Step1 unused physical reserve, no prior E owner|
|fE(N)|Retired auxiliary-only claims for alternative full funding; same original bit IDs|
|V=U_E disjoint_union fE(N)|All units outside the locked common image|
|h0(d)|Independent own-packet partial full assignment; MAY collide with a locked owner|
|a(d), after partial exchange|Locked common assignments plus successful unmatched roots; actual injective partial full map|
|Wstar=U minus im(a)|EXACT currently unused physical units, not assumed accessible by any unproved rule|
|Pstar|Unfunded full roots; each has a DISTINCT anchor in a physical excess slot R|

The disjoint accounting is

    U = im(fE(C)) disjoint_union V,
    U = im(a) disjoint_union Wstar,
    |P|-|N|=QF-QE=D_erased+J_retained.

J is signed, including negative retained interference and full-root repeats
which may change BE. Its negative part is not new credit: it retires actual
E owner claims, each identified once. The archived fE receipt remains
unchanged. No full demand is silently discarded; Pstar explicitly lists
everything still unpaid after the proved partial exchange.

The h0 construction uses all physical2H bits, not clipped2min(H,4).
Every high-H tail is still a real unit even when excluded from a particular
clipped argument. A refined gE protection after a repeat's FIRST event
does not make that unit free under fixed fE; only proven fixed-fE exclusions
or completed exchange justify availability. No fE numeric values are
invented on unavailable source boundaries.

Machine receipts: core6_physical_receipt.json contains an explicit example
of the universal core6 own-packet map; family_funding_receipts.json gives
complete independent full receipts for six specified arbitrary-gap words.
They preserve relative operation/event/bit ordinals. The source-period
transport theorem realizes both donor and demand IDs in the actual aligned
Step1 interval. No second cyclic copy is a second source for the same bit.

The original Gamma two-block reserve has a stronger independently checked
physical guarantee: event(10,3) is overall auxiliary-macro A-event4, so both
bits are outside fixed fE's first-three selector. They also lie outside
the independent h0 image for the full preparation macro, whose Q is1.
Hence neither common locks NOR successful partial-exchange endpoints can
consume those bits. They remain in Wstar and pay full demands(9,1),(13,5)
at distinct bits0/1. All three occurrences lie in the same legal Step1
period by the forced D12=0,D13=2 cut audit. This family repair is not a
universal assertion that every residual anchor has such an event.

Every arbitrary-history Pstar still needs a source-derived DISTINCT Wstar
donor. |Pstar|<=|Wstar| is not established; stating it would just hide the
remaining CD6 inequality. Blocked-root injectivity alone does not imply it.
