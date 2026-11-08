# Repeat-gap compensation for B-return pulses, without an A reset

## Original source class

Let gamma be an original reachable fully paired-closed walk with exactly six
genuine KEEP keys and marked B-core of size8. Choose z in its genuine support.
Every KEEP z must belong to a disjoint B-return pulse of the following form:
at pulse entry B has root y!=z and z is a same-side grandchild; the first KEEP z
and any further KEEPs before the next non-z KEEP target z; that next KEEP is y.
All intervening DELETEs may access ANY present key. Consecutive repeated KEEPs
z may be arbitrarily many. A may have any valid source tree; it is not required
to have root y, put z near its root, or return its full tree across the pulse.

This is a structural subclass, not a claimed favorable-key theorem. All Kz are
accounted for. The full B pulse has one double at its first Kz and the inverse
double at its return Ky; both are genuinely B-changing. The exact RR/LL or
LL/RR identity restores the FULL B tree. Other Kz are root identities. No
third retained KEEP key is admitted before the return; DELETEs remain arbitrary.

## Erased source closure and strong independent auxiliary funding

Erase all Kz, preserving the complete A trajectory. Cut the periodic walk just
after a retained return KEEP, so the cut lies outside active B pulses. Full and
erased B start equal. In the erased history a pulse has no B change at all;
return Ky is a root identity. Outside pulses both B histories take identical
steps. Thus they resynchronize exactly after every pulse and close in one
selected period (u=0,L=1). Arbitrary active input cuts use the already derived
one-period transient and aligned comparison; no transient credits are used.

Let M0 be the remaining KEEP support, at most five. At the selected cut,
C_M0(B) is a subset of the original eight-node marked core. Every erased
KEEP is marked in M0, so its core never grows; DELETEs freeze B. The erased
closed period therefore has core<=8. The completed B-only RT2/K4/K5-LOW
theorems give, on this actual closed B history,

    Q_E <= 2 C_E,

where C_E counts cyclic key changes in its KEEP-only word. If its genuine
support is empty, Q_E=0. For five keys, the core<=8 condition is essential:
this is the completed stronger K5-LOW theorem, NOT the general scalar CD(5)
statement and NOT an unproved B-only nine-core assertion. No old check is rerun.

## Source-gap reservation, independent of erased demand allocation

Consecutive retained erased KEEP occurrences partition the selected period
into gaps (after the preceding KEEP, up to and including the next KEEP).
A begins each gap at the preceding retained key, since A executes every access.

For a CHANGE gap, whose endpoint keys differ, there is a first request to a
different key from the beginning root. Its actual source pre-depth is positive,
so it performs at least one ordinary A StepEv. Reserve both bits of its FIRST
real StepEv. Different change gaps have disjoint occurrence sets; these are
C_E distinct real A events and a2C_E-unit pool. The completed Q_E<=2C_E theorem
funds all auxiliary B-double demands from this pool. This is a scalar counting
reservation using real units; it asserts no acceptance by the frozen matching-
terminal protocol and imposes no unproved eligibility property on that protocol.

For a B pulse returning to y, the preceding erased KEEP also has target y:
before the pulse the erased/full B root is y, and no other retained KEEP occurs
before its return. Hence its return ends a REPEAT gap. That gap contains a z
request with z!=y. Starting A at root y and ending it at root y forces at least
one event leaving y and a later event returning to y. Both are real original
source events even when the Kz and/or Ky consumers themselves are starved.

Choose the FIRST actual A StepEv of the first request leaving y in that repeat
gap. The request is an original DELETE or an erased Kz; its source event can
be ZIG, LL, RR, LR or RL. It occurs before or at the first full Kz. Declare its
two units eligible for this pulse alone:

    bit0 -> full B DOUBLE at the first Kz (direct marginal1),
    bit1 -> full B DOUBLE at the return Ky (indirect marginal1).

It precedes both consumers in the selected period. Different pulse returns
are different retained KEEP occurrences, so they end DIFFERENT repeat gaps.
Thus donor events and bit IDs are distinct across all pulses and repetitions.
Repeat gaps and change gaps are disjoint. No marginal donor belongs to the
auxiliary funding pool. This establishes the reservation without assuming
Delta<=R_z or the slack of an unspecified auxiliary allocation.

## Exact signed transfer

There is no indirect effect outside the B pulses because full B trees rejoin.
The only direct charge per pulse is1 and the only indirect difference is1 at
its return. For m pulses, on the actual aligned period,

    D=m, J=m, Delta=2m, Q_full=Q_E+2m.

Change gaps supply at least C_E A events. The m disjoint repeat gaps each
supply at least TWO A events (leave and return), all outside the change pool.
Consequently source event counting gives

    A >= C_E+2m,
    Q_full <=2 C_E+2m <=2A-2m.

The first event's two bits pay the marginal; the second event per repeat gap
is unused surplus. This is a primitive physical charging proof, not a rewritten
desired residual bound. It permits arbitrary A-tree changes across a B pulse
and arbitrary DELETE interleaving. No paired-identity contraction is used.

## Precise scope and uniform extension boundary

The lemma works more generally whenever the erased B history has an ALREADY
PROVED Q_E<=2C_E certificate and all erased-key KEEPs are the stated B-return
pulses. Six-key/core8 makes that funding unconditional from completed proofs.
An original core9 exposed-leaf case may also qualify if its actual remaining
core is proved<=8; no universal leaf-selection result is assumed here.

The scalar CD(r-1) premise alone is insufficient to fund this particular gap
pool, because it bounds Q_E by2A, not by2C_E. Five-key/core9 already has a
known B-only obstruction. For unrestricted induction one must supply an
appropriate independent funding/transfer mechanism for the residual, together
with source-complete key selection or classification. Neither is asserted.
Third KEEP interventions, deeper/nonreturning B erasures and uncovered
auxiliary funding remain OPEN. Full original CD stays OPEN.
