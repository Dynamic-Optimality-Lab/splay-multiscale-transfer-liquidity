# FD35 — exact dual for the complete original proof-carrying system

This is a logical characterization, NOT a source feasibility proof, an
implemented exhaustive solver, or a new universal eligibility policy.

## Fixed legitimate input and fixed original license

Fix finite (W,I,fE,a0,Gamma). Fix an admissible original license pi: its
independently justified Type A/B source rule/arithmetic, selectors and
block/output permissions, period/chart/retirement constraints, and original
full-h-then-exchange protocol. Do NOT include the desired successful bank
trace or complete output matching as an ASSUMED premise of pi. An absent
source arithmetic proof is a missing license, not a license granting success.

Form the finite labelled physical execution system X_pi. A state records
the original event frontier; each actual unit's status (not admitted,
unassigned, assigned, released); partial comparison output; covered demand
IDs; original phase/cut/chart/reservation flags; and the finite data of
the licensed exchange. a0 and fE are immutable inputs. The unassigned bank
contains <=25 actual units. Full output records and owner path records are
assigned/proof data under the original convention, not extra unused banks.

Transitions are ONLY the original pi-licensed admissions, within-block
assignments, releases, ledger retirements, transports and exchanges. The
original permitted static output may mention a later demand occurrence;
no unprovided chronological endpoint deadline is imposed. An event is
admitted once and no released unit is resurrected. Accepting states have
complete h, all physical demand coverage, empty legal closing bank,
unchanged owners, and all original compatibility predicates discharged.

All labels and inventories are finite. D values and arbitrarily long
source proof terms belong to fixed pi's proof, not an unbounded state
variable; only their actual permissions/cut facts enter X_pi. Proof-only
repetition can be erased. The state system is thus finite for a fixed
input and fixed semantic permission footprint. No state cap is assumed
large enough to enumerate it.

## Exactness

An execution of the unchanged original pi route gives a path in X_pi by
recording precisely these physical fields/actions. Conversely an accepting
path supplies a legitimate witness because every transition and terminal
predicate uses that SAME original license. These are inverse encodings of
permitted constructions; incompatible permissions from different licenses
must never be mixed along a path.

## Closed-state-cut dual

For this fixed pi, there is no accepting path iff a set R_pi exists with:

* every legal initial state is in R_pi;
* R_pi is closed under EVERY pi-licensed transition;
* R_pi contains no accepting state.

Proof. Infeasibility implies that the set of all reachable states is such
an R_pi. Conversely induction on path length keeps every reachable state
in a forward-closed R_pi, which excludes all accepting states. QED.

For the COMPLETE original system, infeasibility is the assertion that
such a rejecting cut exists for EVERY admissible original license pi.
Empty license family is a source-rule failure; it must be PROVED empty,
not inferred because the few tested rules failed. Two proof presentations
with the same physical initial/terminal/transition permissions have the
same footprint and same cut test. There are finitely many footprints on
a fixed finite physical universe. This does NOT give an effective list of
which footprints admit a valid SOURCE proof. Establishing that membership
or a complete source normal form is a separate, unresolved obligation.

## What an actual parent countercertificate needs

It needs a genuine original source AND legitimate frozen inputs, plus an
exhaustive account of all permitted original license footprints, and a
rejecting cut for each. A negative Hall set in one pool graph, failure
of one algorithm, or one bank trace with excessive carry is insufficient.
No such all-license rejection certificate is constructed here.

No static Hall equivalence is claimed for the whole system. The full
dual is deliberately not replaced by SI34, MOP, a comparison-image-only
restriction or a naive time-expanded flow with unauthorized deadlines.
