# Typed ownership system with explicit source escape premise

Status: DERIVED conditional system, new independent audit pending.
It is NOT a complete characterization of all legal transfers in H_r.

Fix the original aligned interval I and its finite typed inventories
D and U. A demand is a pair (occurrence,double ordinal); a unit is a
triple (occurrence,A event ordinal,bit). Let a be the accepted injective
partial full map, including every common frozen smaller-support value
and every already successful full value. Let h be the injective partial
source comparison h_Lambda, possibly extended by certified escapes.

The proof state is (a,h,receipts), not a new splay/controller state. Each
receipt records actual source occurrences, original trees/frames or an
inherited theorem path, source-block eligibility, cut transport and any
working restriction relevant to that rule. Full/erased states and charts
are immutable input data, not recomputed by choosing representatives.

The certified subrelation has these rules:

1. COMPARE: from actual d in dom(h), inspect actual u=h(d). The original
   comparison edge has its source receipt; it does not spend u effectively.
2. OWNER: if u is already assigned, continue to the unique d'=a^{-1}(u).
   This is an ownership proof edge, not a new source operation, and leaves
   the old assignment unchanged.
3. ESCAPE: at d outside dom(h), accept (d,u) only with a separately
   proved source rule and receipt, u in U minus im(h), and all original
   period/block/storage guards. Add h(d)=u. u is allowed to be owned under
   a; that fact triggers OWNER, not double spending. No generic edge from
   every frontier to every spare actual bit is authorized.
4. PAY: after a complete such rooted path ends at u outside im(a), append
   only p->u to a, using the inherited fixed-owner/block exchange receipt.
   Every earlier a entry is literally fixed. No locked owner is reassigned.
5. BLOCKED: if no certified ESCAPE recipe is available, retain the actual
   undefined d and unpaid root. Termination at this state is not funding.

Known unconditional ESCAPE recipes in this campaign are only the inherited
explicit reset-family rules. In a general source ESCAPE availability is
OPEN. In particular the numerical condition u in U minus im(h) is not
itself a source license; neither is u being free under a.

For fixed h, the graph has outdegree at most one at every demand/unit and
indegree at most one at reached demands: injectivity of both maps gives
the latter. A missing root cannot have an incoming owner edge since it
is outside dom(a). This is the exact static path reduction used below.
Adding a certified fresh-image edge changes h monotonically; a changes
only by frozen successful additions. No Hall theorem or assumed complete
static eligibility graph is used. The validity of a sequential source
recipe after earlier escapes is a hypothesis to prove, not a consequence
of cardinalities.

The legacy predecessor JSON field `unit` in a frontier map can contain a
two-coordinate DEMAND. Only three-coordinate actual unit values belong
to U. The new path and escape records name `frontier`, `demand`, `unit`
and `current_owner` explicitly.
