# A necessary funding condition for strict FI coverage

Status: PROVED—UNIVERSAL as a statement about the specified UD/FI source procedures on finite closed actual pair walks. This is an independently necessary filter for a strictness witness, not a proof of universal CD and not a claim that every non-dominated walk is FI-covered.

Let cyclic maximal A-root blocks have actual leader cost a_i>=1, B doubles q_i and delta_i=q_i-2a_i. KEEP changes both A and B; DELETE changes A alone and does not remove a key. A block may begin with DELETE and later have a starved KEEP of the same key; that is NOT a KEEP-less block. Define

    E=sum_i max(delta_i,0),
    C_D=sum_(j: block j has no KEEP) 2a_j.       (1)

Every KEEP-less block has q_j=0. The old UD and tightened FI procedures both use ceiling zero for it whenever a positive history exists, so its actual full pool is then available. This counts each physical source block once. No credit from the reachability prefix is part of (1).

## Explicit DELETE-only queue and correct cyclic cut

Ignore every possible loan from nonpositive blocks that have a KEEP. Those blocks still pay their own q_i demands locally, since q_i<=2a_i. Each positive pays its first 2a_i demands locally and places delta_i residual demands in chronological order. Each KEEP-less block lends at most its 2a_j units to oldest remaining residuals, then retires unused capacity. No negative credit is banked for future anchors.

For scalar queue accounting set

    v_i=delta_i, if delta_i>0;
    v_i=-2a_i, if block i has no KEEP;
    v_i=0, otherwise.

These cases are disjoint: a KEEP-less block cannot be positive. Queue debt updates exactly as D'=max(0,D+v_i). Suppose E<=C_D, so total S=sum_i v_i<=0. Let P_0=0 and P_t=sum_(i<t)v_i. Choose a MINIMUM of P_t, t in {0,...,m}, and start just before block t mod m.

For any prefix of that rotated period, its sum R is >=S. Without wrap R=P_u-P_t>=0>=S; with wrap R=S-P_t+P_u>=S. Therefore every suffix sum S-R is nonpositive. A zero-initialized reflected queue ends at

    D_end=max(0, all nonempty suffix sums)=0.   (2)

CW00's initial sketch said maximum rather than minimum. CW00A preserves and corrects that sign error. The minimum cut is essential: a credit-first ordering may waste capacity before a future demand, and no banking is allowed.

## Actual source units and old-UD membership

Give each A StepEv two distinguishable units (cycle occurrence,event index,bit). Give each B double demand identity (cycle occurrence,B-event index). A positive uses all its own 2a_i units for its first demands. Its residual cursor advances through distinct intervals as DELETE pools help it. A KEEP-less lender has no own B demand; its one outgoing cursor assigns distinct units in [0,2a_j), once. Nonpositive KEEP blocks pay locally and lend nothing in this proof. All source demands and units therefore occur at most once. Equation (2) pays every residual with internal period credits.

UD can do at least this well. At a KEEP-less block with pending debt it has a nonempty positive history, hence reservation zero and full available capacity 2a_j. With no history/debt, its zero loan changes nothing. Its extra certified KEEP loans can only reduce the total pending debt. The established total-debt comparison shows UD also finishes at zero on the minimum cut. This proves UD membership, not merely the scalar sum inequality.

If there are no positive blocks, all work pays locally and UD accepts. Empty walks and the A=0 closed-walk case have Q_B=0 by fixed-root closure and are covered separately. An all-positive nonempty period has E>0=C_D and does not meet this theorem. Repeated keys, seam-crossing blocks, arbitrary fringes and both orientations preserve the distinct occurrence accounting.

Consequently

    E<=C_D  implies UD membership,
    FI membership AND no UD cut implies E>C_D. (3)

The second implication is independently mandatory for any strict FI\UD witness. It is a filter, not a sufficient condition. Source-imposed restrictions have not been renamed as universal necessities: (3) explicitly applies to the requested strict difference, not every walk.

## Exact relation to the previous controls

Each row below represents a fixed word and its reflection. Both orientations have the same values.

| Prior control pair | E | C_D |
| --- | ---: | ---: |
| UD deep-KEEP cycle | 4 | 26 |
| SL essential split cycle | 5 | 28 |
| XR cross-run batch | 3 | 12 |
| SP shared payer | 3 | 8 |
| DS delayed payer | 1 | 10 |
| SC immediate child payer | 1 | 10 |

All twelve are strictly DELETE-dominated. Thus none can establish strict FI\UD closed-walk coverage by earlier repayment or an additional successful cut alone. Their full source words/costs were already banked; the current pointer audit verifies those source costs, all 432 old UD cut records and explicit minimum-cut DELETE-only injections. The 328 DELETE-only assignments are alternative proofs, not credits to pool with the old selected maps.

This result explains the existing family obstruction and narrows a genuine strictness search to E>C_D. It does not supply such a walk. Strategic elimination is recorded separately from advancement of the original CD theorem. Universal Step 3/CD and successful-cut availability remain OPEN; matching-terminal work and Stage 11G are unchanged.
