# E0 one-positive suffix — exact placements and remaining cases

Target: P0 --0*--> +1 --0*--> F11. Conditions: total remaining budget1,
actual original source packets/complete boundaries. Inheritance: full
cost grammar, final incoming classification and new zero frontier.
Ambiguities: arbitrary upper-crossing/high-zero source preservation
remains OPEN. Bridge: isolate the final edge and use exact output
marked-parent counts, without moving the sole +1 by assumption.

The +1 is H1/Q1 OR H2/Q3. H2/Q3 remains allowed at an intermediate
state; every such output has at least three marked children and L>=3.
If a return ends with a zero packet after that +1, a subsequent3->2
zero loss is necessary, then the final neutral zero. Thus H2/Q3 cannot
occupy or bypass the final L2 tail, but it can alter A and create
the later loss state. Its helpers and source credit are retained.

## Final-edge split

1. Final edge positive: it must be H1/Q1 as inherited. The actual q1
   BF inverse, one-event A inverse, cold chart and BE source equation
   must match. H2/Q3 is impossible only HERE, not throughout the path.
2. Final edge zero: it is H1/Q2 neutral L2->L2 into Fork41. Its source
   is J2 or K2. If another ZERO immediately precedes, that edge is
   necessarily a3->2 loss into J2. If the +1 is immediately before it,
   it may instead have created that L2 source. No source operation is
   moved past the intervening zero history.

The universal last-two-zero characterization therefore remains valid
after the sole positive edge, whenever there are at least two trailing
zeros. A trailing one-zero segment is a separate source case. Its L2
origin can come from the defining/last lowering or directly from P1.

## Exceptional paired zero is sharply located

Along a zero history L1 cannot be entered. Therefore an H3/Q6 paired
zero in the one-unit suffix requires the preceding sole +1 to have
created L1 and must occur IMMEDIATELY after it. There is at most one
such pair. That +1 is H1/Q1: H2/Q3 has output L>=3. After the pair,
L4 is restored and the remaining zero history has the same terminal
loss/neutral requirement if it reaches F11.

If the final destination is a q5 forced-zero source (L1), the final
packet MUST itself be the sole H1/Q1 +1, with no trailing zero at all.
This is another exact backward restriction, not an exclusion of that
source transition. Cold status and actual A successor geometry still
require proof.

## Current proof boundary

The inherited E0 witness's complete one-unit suffix certificate remains
valid at its exact arbitrary-fringe scope; it is not rerun or extended
by assertion. The new turnaround shielding theorem rules out source
subclasses whose entire remaining operation range stays below its cut.
An H2/Q3 or zero H2/Q4 helper crossing that cut can invalidate the shield;
no universal repayment or donor ownership for that crossing is proved.

General E0 +1 closure is OPEN in the following explicit leaves: final
H1/Q1 entry; one trailing neutral zero after a +1-created L2 state;
or a later last3->2 loss and neutral after a nontrivial regenerated
prefix. The exceptional paired zero is confined as above. These are
necessary actual-source cases, not new abstract graph signatures.
