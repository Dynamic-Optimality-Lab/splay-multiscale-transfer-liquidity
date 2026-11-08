# FR32-CARRY1 — source-uniform carry-one theorem

**OUTCOME A.** At the frozen EXC seven-key/core13 source scope, every actual
first genuine full return tau7 satisfies D_out<=1. The bound is sharp by
the inherited W101 source with D_out=1. This is a computer-assisted symbolic
proof with separate same-agent rotation and static certificate checks.
It is not formal proof-assistant verification or external peer review.

## The exact statement and reduction

Use `SOURCE_SPEC.md` and the immutable parent scope. This includes all
original-source-reachable deeper PREFIX parameters, arbitrary private BSTs,
DELETEs, nongenuine KEEPs, changing charts and finite return lengths.
No full tree is fixed by choosing its shallow quotient. EXC fixes the
first-upper u11/H1 case; outside-EXC upper13/entry0/entry2 are not added.
The exact intrinsic comparison gives

    R=sum_(u,tau] sigma=P(tau)+E7(tau),
    D_out=max(0,1-R).

Thus prove R>=0. All original costs and the final E correction are retained.

## 1. Histories returning before activation9

The parent `PRE_ACTIVATION_CARRY_THEOREM.md` proves FR32-N9. In the fixed
old chart D_old(u)>=1. Complete old packets have nonnegative price+DeltaD.
At return, D_old(tau)<=E7(tau)+1. If tau itself is Q5, its singleton margin
can lose at most1, but then E7(tau)=4,D_old(tau)<=3, which pays that loss.
An earlier q5 cannot be cut before interior7. Hence R>=0 in every no9 case.
The old proof and static audit are reused, not rerun as finite source tests.

## 2. The source-exact activated representation

The fixed old/new core and packet lemmas and the exact cold seam are proved
in `COLD_CHART_COMPARISON.md`. The new source grammar is proved complete
in `SOURCE_LIFTING_PROOF.md`. In particular it retains BOTH7 and9 through
the actual rotations and only then changes the A proof mark set.

Complete cold LOW pairs:554 for H1 and2279 for H2. Both independent kernels
cover all5577 source bases and agree on the entire relations. HIGH retains
all synchronized endpoints. Exact static arithmetic establishes gamma>=-2.
Every fixed-chart packet has nonnegative integer price+DeltaD. Terminal
M>=-3 on the entire necessary syntax. Thus old C>=5 or new C>=3 is safe.

It remains to establish a forward-closed necessary representation below
those thresholds. Losing physical7/9 placement prematurely admits false
paths; the theorem does NOT use the failed two-chart overapproximation.

## 3. Retain the whole H1 source phase

Before the FIRST nonreturn macro of H>=2, every positive A access is a single
H1 access to its final genuine target. The source-uniform seven-mark H1
grammar therefore applies. Start from all three prescribed entry quotients,
and synchronize every admitted A row with its ACTUAL fixed-core B row.
Before cold, physical7 is forbidden as an intermediate full target and9
is the one cold switch. After cold all six new targets are included;7 is
only the terminal target. Do not infer source realizability of graph paths.

All H1 q5/q1 pairs retain their shared seven-key A midpoint. At the first
packet containing an H>=2 nonreturn macro, the departures include:

|Packet|Necessary representation retained|
|---|---|
|Singleton H2|Complete old six-key H2 source relation|
|Singleton H>=3|Every synchronized endpoint, price6-Q|
|Cold H2|Complete two-projection cold H2 relation|
|Cold H>=3|Every synchronized new-root9 endpoint, price6-Q|
|q5 H1 then q1 H2|Actual seven-key H1 midpoint, then complete six-key H2|
|q5 H2 then q1 H1|Complete six-key H2 midpoint shared with H1 successor|
|Pair total H>=4|Every synchronized endpoint, conservative price2|

The pair table is exhaustive: each macro H>=1, and total H2 is(H1,H1),
total H3 is(H1,H2) or(H2,H1), all other totals are HIGH. Source packet
seams cannot conceal a cold switch or terminal return. All original macro
segments and intervening operations remain in these comparisons.

After such a departure the accepted six-mark LOW/HIGH packet relation is
a necessary enlargement of every remaining fixed-chart source transition.
If the departure preceded activation, the exact complete cold relation
bridges it once into the new chart. This partitions every possible source
history by activation and first H>=2 occurrence; no LOW terminal class is
left out. The final return's own H can be arbitrary in both representations.

## 4. Explicit finite certificate and its induction

`threephase2_analysis.json` gives lower labels d on these necessary states:

|Representation|States|Label range needed|
|---|---:|---|
|Full seven-key H1 source prefix|52|old<=4 or new<=2|
|Old six-key continuation after first H>=2|1167|<=4|
|New six-key continuation after first H>=2|2853|<=2|

The defining certificate assertions are:

1. Each of the three original entry states has d<=D_old(u).
2. Each necessary H1 edge/pair and every first-H>=2 departure is included
   whenever its candidate label is within the relevant cutoff, with
   d(dest)<=d(source)+the conservative exact packet margin.
3. Every later complete LOW/HIGH single/pair is included under the same
   inequality. Every necessary cold bridge is included once with its gamma.
4. At every admitted new-chart terminal source, d+M_min>=0. For H1-prefix
   states use the retained seven-key depth of physical7; for later states
   use the complete six-mark necessary hidden7 depth bound. An actual
   larger H_return only increases M.

`audit_finalind.py` separately checks these closure assertions directly;
it does not rerun the producer's shortest-path algorithm. It recomputes all
terminal predicates using leaf/branch counts rather than the producer's
excess formula, checks every LOW/HIGH row including larger-H duplicate
endpoints, all first-H2 packet cases, and the cold gamma floor. It reports
PASS_COMPLETE_FR32_CARRY_ONE_STATIC_CERTIFICATE. There are61505 terminal
syntax checks and10 canonical terminal checks; no adverse terminal remains.

Induct along an arbitrary ACTUAL source history. While within the relevant
cutoffs its accumulated C is at least the certificate lower label: initial
inclusion gives the base; source completeness and closure give each step.
Leaving a cutoff is safe by the uniform thresholds in section2, so no
longer source path needs enumerating. At the terminal source, either the
cutoff argument gives C+M>=0, or inclusion gives C+M>=d+M_min>=0.
This proves R>=0 for every activated history. Together with section1 it
proves the entire frozen EXC theorem, not just immediate activation.

## 5. Consequences and preserved distinctions

Therefore D_out=max(0,1-R)<=1. W101 belongs to EXC and attains1, so no
unconditional zero-reset law follows. W105's intermediate debt2 is compatible
with this first-return theorem. All these statements retain their original
symbolic closure/executed replay distinctions; no factorial source word was
newly replayed. Reflection transports the complete ordered source, relations
and debt table and exchanges LL/RR, proving the reflected version as well.

The terminal interface retains full actual A/BF/BE, charts, provenance,
signed balance, source occurrence and frozen owners. No geometric root7
reset, subsequent11 access, bounded future repayment horizon or physical
spare is inferred. No donor is reassigned or spent. R1-R4, Bank25, CD6 and
all frozen allocations remain intact.

FR31-FIX's universal ZERO-return statement remains separately OPEN; where
its source lies in EXC it inherits this WEAKER carry-one result only.
Repeated carry, eventual repayment, normalized-owner supply, unconditional
Gate U, Universal Coarse-Double and Dynamic Optimality remain OPEN.
