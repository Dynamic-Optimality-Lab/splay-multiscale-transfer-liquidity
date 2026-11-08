# Conditional lazy-escape theorem for arbitrary finite ownership chains

Status: DERIVED proof; distinct implementation audit pending. The
universal SOURCE-EXISTENCE premise is not proved by this theorem.

## Statement

Let D,U be the actual finite inventories of one licensed source interval,
a0:D0->U the frozen injective paid map and h0:D\R->U an injective source
comparison (here h_Lambda). Select any finite set P of missing roots.
Assume that whenever the procedure below reaches an undefined comparison
d, a finite source-derived recipe returns an eligible original unit
u outside the CURRENT im(h), with a proved receipt for the ESCAPE/PAY
interface in OWNERSHIP_TRANSFER_SYSTEM. In particular this premise must
survive all earlier escapes and payments. No freedom under a is assumed.

Then the procedure appends distinct free endpoints to every root of P,
fixes ALL a0 values and every earlier successful addition, uses at most
|R| escape edges and |P| payments, and visits at most |D| distinct demands
over the whole run. The bound depends on the finite source, not a fixed
lookback radius. It asserts static source/block funding at its receipt's
scope, not a new arbitrary-r Bank25 schedule.

## Procedure

Maintain a extending a0 and h extending h0, both injective. For each
unpaid root p, set d=p. If h(d) is undefined, ask the specified source
recipe for an eligible fresh-image unit and set h(d)=u. Inspect u=h(d).
If u has a current owner, continue at that owner. Otherwise append p->u
to a and freeze it. If the source recipe supplies no proved edge, return
BLOCKED at d instead of claiming the theorem's premise holds.

`adaptive_transfer.py` implements this conditional algorithm. Its recipe
is an explicit input, never an oracle that assumes the desired donor.

## Proof of no repeated path vertex

For fixed injective h,a, a demand reached after the root has a unique
incoming unit a(d), and that unit has at most one h predecessor. If a
rooted path repeated a demand, reverse these unique predecessors back
to its first entry; either two predecessors coincide all the way back
to the root, making that root an a owner, or a cycle has an outside
incoming predecessor. Both are impossible. A missing root is not in
dom(a). The same argument excludes intersection of two missing-root
paths. A free terminal is a real unit outside im(a).

Now add h(d)=u at a reached hole, with u outside current im(h). If u
has owner d', d' cannot be a previously visited nonroot: its incoming
a unit was already a comparison value on its prior path and would
therefore be in im(h). Nor can it be an unpaid root, which is not an
a owner. A previously paid root's new a unit is the h value at its
successful terminal, also already in im(h). Thus an escape cannot
enter any previously explored rooted component. It can enter a previously
unexplored paid component; the fixed-map uniqueness argument still
excludes a reached cycle. The new h value is distinct by construction,
so all invariants survive the insertion.

After a payment, the new a unit is an existing h terminal. Any future
entry into this paid root would have to use that same h unit and hence
the unique predecessor on its already visited path; the fresh-image
escape rule cannot add another one. This proves the global no-repeat
claim by induction over every escape and payment, not just for one path.

## Termination and rank

At an escape, `( |D\dom(h)|, |P\dom(a)| )` decreases lexicographically
in its first coordinate. At a payment its first coordinate stays fixed
and its second decreases. Neither coordinate increases. There are at
most |R|+|P| such actions. Between actions no demand repeats, by the
preceding proof; the stronger global proof bounds all demand visits by
|D|. Finite source size alone was not used to assume away cycles.

Under the stated finite source recipe premise every reached hole is
filled; the walk therefore cannot stop at an undefined comparison or
loop, and must reach a free terminal. Append that pair. Induction over
P proves total required coverage and literal preservation of a0.

If the recipe premise is absent the same algorithm still terminates
with explicit blocked frontiers and valid successful partial additions.
It does NOT prove those frontiers contradict the source. Establishing
that contradiction, or deriving their escape events, is Gate D's open
mathematical obligation. The conditional rank theorem is not reported
as U16-NONLOCAL or as a replacement existence proof.

## Conservative specialization to an inherited complete family map

If a separately certified complete injective H extends h0 and the recipe
uses H(d) at every reached hole, then h always remains a restriction of
H. Injectivity of H proves H(d) is outside the current comparison image
whenever d is a hole. Every step taken is therefore identical to the
same fixed-owner path computed with complete H from the outset. Unvisited
holes can remain undefined without affecting any required payment.
This proves equality with that inherited complete-map exchange for the
processed roots, not a new source-supply theorem. It allows the known
reset-family proof to be reused without completing irrelevant holes.
