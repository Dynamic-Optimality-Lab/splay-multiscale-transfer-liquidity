# MSTL-14P conditional t*-restart theorem (present domain)

Status: CONDITIONAL THEOREM (gap hypothesis explicit; NOT claimed closed).

## Definitions (frozen semantics, P_all k=6 C=2 rho=FLAT(2), present domain)

- lat_e = LATENT just before event e's mobilization (post-own-injection for
  A-events). Every event fires (P_all) with cap exactly 2.
- t* = last event strictly before KEEP j's discharge with lat_e < 2.
  If none, t* = start (pools 0). Suffix S = (t*, j-discharge].
- E(S) = A-events + B-events in S. N(S) = sum of needs of KEEPs in S
  excluding j's own demand... precisely: SPENT(S) covers KEEPs in S before j.

## Exact steps (all rigorous)

T1. M(S) = 2*E(S): every event in S has lat >= 2 by maximality of t*, so
    each mobilizes min(lat,2) = 2 exactly. (A-events: lat measured
    post-injection; B-events: lat as-is.)
T2. ACTIVE_pre(j) = ACTIVE(t*+) + M(S) - SPENT(S) (exact pool accounting).
T3. ACTIVE(t*+) >= 0 (counts); SPENT(S) = N(S) by IH (no violations before j).
    Hence ACTIVE_pre(j) >= 2*E(S) - N(S).
T4. N(S) + need_j vs 2*E(S): suffices 2*E(S) >= N(S) + need_j =: Nfull(S).

## Gap hypothesis (NOT closed)

G_tstar: 2*E(S) >= Nfull(S) for the t*-suffix of every KEEP j.
Via need <= y-1 per KEEP and rotation telescoping this is implied by
R^B(S) + ABSENT_Y(S) <= 2*E(S); on present domain ABSENT_Y = 0, leaving
R^B(S) <= 2*E(S), which holds since each B-event covers <= 2 rotations...
BUT: Nfull(S) <= R^B(S) requires need_i <= y_i - 1 per KEEP (true) AND the
suffix R^B must cover j's FULL y_j - 1 INCLUDING B-rotations before t*.
B-rotations of j occurring BEFORE t* (j's early B-phase, when t* falls inside
j's B-phase under thin pools) are EXCLUDED from E(S) while need_j still
charges the full y_j - 1. THIS is the exact flaw: t*-before-discharge splits
j's own B-phase. Thin pools (k=3) put t* inside B-phases routinely (hence the
n192 death is consistent); thick pools (k=6) make t* rare/early but the proof
must still handle t*-inside-B-phase, which it cannot without the pools at t*.
Therefore G_tstar is FALSE as stated in full generality; it holds iff t* never
falls strictly inside a B-phase with uncovered early rotations, which is an
unproven pool-thickness property, not a combinatorial identity.

## Consequence

The t* restart is banked as a conditional result with machine-checked
arithmetic backbone (need<=y-1; e_B>=(y-1)/2; M_B=min(L0,2e_B) greedy
exactness; conservation) and an EXPLICITLY OPEN gap hypothesis. No status
change (MSTL-14P stays UNPROVED/NO_WITNESS). The gap is now the single
sharpest formulation of the remaining obstruction: B-sub-2 events inside B
phases under thin pools.
