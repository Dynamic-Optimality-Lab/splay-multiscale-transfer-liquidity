# Exact physical reserve after frozen full successes

This refines the inherited C33 GLOBAL_SOURCE_SUPPLY_DEMAND_IDENTITY.md with
the ACTUAL a0 occupancy. It is an identity, not a source expansion proof.

Write F=D\E for full-only demands, N=E\D, C=D intersect E. Let fE:E->U
be the supplied certified fixed smaller map. Let a0 extend its common
restriction l, and put X=dom(a0)\C. Since a0 is a full-demand map, X subset F.
Then P=F\X. The actual alternative full-ledger free inventory is exactly

    U\im(a0) = ((U\im(fE)) disjoint_union fE(N)) \ a0(X).

Proof. fE injectivity makes im(l) and fE(N) disjoint, so removing im(l)
from U leaves precisely the displayed reserve-plus-retired pool. Every
additional a0 image is outside im(l), and deleting those exact images
leaves U\im(a0). No source unit or old owner is redefined. N retires only
under the original alternative-ledger license; archived fE stays fixed.
Any genuinely additional unretired reservation in Gamma must still be
removed or legally released. A refined new auxiliary map is not fE.

Consequently

    |U\im(a0)|-|P| = |U|-|D|
      = (|U|-|E|)+|N|-|F|.

Thus unrestricted same-period COUNTING feasibility does not depend on
which legitimate successful full-only claims X have already been paid.
Frozen occupancy changes donor locations and routing, but cancels from
the raw total-capacity condition. A count-only 'frozen ownership prevents
every extension despite enough original units' counterexample is impossible.
It would require an additional real eligibility/storage restriction.

This does NOT establish |U|>=|D| for arbitrary original sources; that is
the missing source capacity implication. It also does not identify eligible
neighbors, prove joint source repair, or satisfy Bank25. Hall with complete
pair eligibility only restates this unproved capacity condition. No claim
of principal completion follows from the identity.
