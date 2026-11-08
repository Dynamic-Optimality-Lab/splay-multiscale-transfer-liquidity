# Independent source and ownership audit for Step1

This is a separate source/mathematical derivation and checker audit within
the campaign. It reuses accepted source/graph theorems. It is not external
peer review or formal verification of the original compiler. The Step1
publication gate requires its machine certificate and resource controller
to pass; the following is its mathematical audit record.

## 1. Reconstruct the proof from source prefixes

For any ordinary prefix ending at boundary k of the chosen rotated period,
let P_k be the number of selected A units minted so far, Q_k the number
of auxiliary doubles paid, and d_k the sealed ordinary debt. Summing the
original M3 inequalities gives a NONNEGATIVE certified cumulative release

    S_k=P_k-Q_k+d_k-d_star.

The algorithm's cumulative surplus releases are exactly S_k, by its local
release formula. Its remaining working units must therefore number

    P_k-Q_k-S_k=d_star-d_k>=0.                            (A)

This provides a prefix derivation independent of the main proof's local
bank algebra. Each next macro begins with(A); after minting its selected
units its terminal demand cannot exceed the available units because the
post-payment quantity is the next nonnegative bank plus the nonnegative
local release. No abstract initial balance is needed at d_0=d_star.

At the last prefix d_k=d_star. Thus working units end at0 and the released
units are all and only the selected capacity not used for Q_E. Adding
unselected tail units gives exactly2A-Q_E. The same identity alone would
not be a source allocation; the ownership argument below supplies it.

## 2. Every unit retains one actual source owner

The allocator has only these ownership transitions:

    fresh selected unit -> working bank;
    fresh unselected tail unit -> reserve;
    bank unit -> one auxiliary payment;
    bank unit -> reserve.

Every fresh unit has an immutable actual A-event/time/local-index and
bit0/1. Different source events/bit positions are distinct by source
definition. No transition returns a paid or reserved unit to the bank.
The code only appends freshly created selected units, and removes units
with popleft for payments or pop for certified surplus. Each actual
auxiliary DOUBLE ID is visited once. Therefore a unit cannot pay twice,
belong to both funding and reserve, or be silently created by a debt
change. An old carried unit released at a helper keeps its old event ID.

Each actual A event is inspected in original replay order; its two bits
go to exactly one branch. The selected FIRST min(H,3) events are original
events, not T266 proxy events. B demands occur only at the terminal
genuine KEEP and after its whole A replay. Nongenuine B changes, source
ZIGs and DELETEs keep their actual transitions/costs as in the source
bridge; only B DOUBLE IDs demand one C=2 unit each.

## 3. Source graph and signed orientation

The per-macro price is exactly2min(H,3)-q. The aggregate inequality
w(P)<=2A-Q alone would not suffice for the clipped theorem; the audited
dependency is the stronger original11F per-macro equality. Its low/high
source images retain every occurrence and have the same shared full raw
boundaries, mu/sigma and actual midpoint. Only the source auxiliary core9
is mapped. Full original core10/11 is never inserted into M3.

The literal raw chi8 is nondecreasing on all image edges and equal at the
full closed endpoints, hence constant. No graph filtering is performed.
Then Phi_next-Phi_source=d_source-d_next, so the correct NONNEGATIVE
quantity is w+d_next-d_source. Using the opposite sign would invalidate
the bank. Midpoint D is never evaluated; HIGH is handled by adding its
original OM and MO inequalities. The h0 entering case remains an allowed
edge; its one-way flag prevents its occurrence in a full closed image.

The ACTUAL sealed D includes F4 and4359 completion clauses at its defined
scope. No incomplete lower-floor helper, new observable or private witness
is an input to this allocation. Different full states with the same debt
remain different full states. The charging queue is an accounting device,
not a quotient of graph states or a replacement matching protocol.

## 4. Full source closure, reachability and period alignment

Start with the actual common recurrent period I after the erased preperiod.
Actual full and erased endpoint pairs each repeat; equality of debts or
roots is not used as a substitute. The maximum-debt macro boundary is a
legal cyclic source rotation. The explicit t->t' map moves any wrapped
prefix occurrence to its ACTUAL occurrence in the next common period;
it uses one length-T interval I', not two copies or preperiod credit.
Each history reaches its own chosen cut by a legal prefix. Both A histories
coincide there and throughout I'. Costs and D+J over one common period
are invariant under this simultaneous rotation. All physical accounting
is integral on I', before any per-original-period division by L.

The allocator rejects a trace not already at its maximum-debt cut; it
does not reorder absolute timestamps. Its zero-start claim is cyclic,
not a zero-start causal theorem for every arbitrary input seam. For a
specified fixed seam an initial working balance would need a separate
source justification and is not claimed here.

## 5. Signed interface and what remains unproved

Retiring auxiliary-only demand assignments releases their actual assigned
units. Common-demand assignments remain injective, and the old unused
reserve is disjoint from all of them. Thus the original available pool
U union f_E(N) is explicit and contains no duplicates. Ordinal matching
compares unit demand counts, not identical rotations in distinct trees.
It imposes no new native matching-terminal eligibility.

The equality P-N=D+J retains both interference signs. The final injection
of unmatched original demands P into that available pool is not supplied.
It would be the substantive signed repayment Step2. Step1 neither assumes
it nor guarantees positive universal reserve, source-complete erased-key
selection, new original CD-domain coverage or unrestricted CD.

## 6. Verification discipline

The derivation checker validates universal affine equalities and exact
source certificate metadata. The separate independent checker verifies
the prefix derivation, allocator mutation sites, dependency hashes and
claim boundaries. No concrete source history, new population/mask, graph
search or old semantic proof row is executed. The algorithm is delivered
for source-certified records; it is not empirically tested on finite
examples in this campaign. Its input source validity is the inherited
original model and11F/M3 theorem, not inferred by this wrapper from arbitrary
user-provided lists.

The active unit queue has at most2 units between macros and8 while minting
the next selected pool. Input/output storage is not claimed to be bounded
by8. All continuation CPU and whole controllers remain in the ORIGINAL
SE03 groups, with no reset or increase. R1-R4 and Bank25=25 are preserved.
