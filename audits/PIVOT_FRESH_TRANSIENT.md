# PIVOT-20: FRESH-TRANSIENT COMPENSATION (attempt + verdict)

## A. Sign quantity (exact, code)

`sigma(y;x) = (sgn(ΔdB(x)), sgn(ΔdA(x)))` around builder KEEP-y
(`wp6_signed.py`: depths via `depths_of` on pointer copies, before/after
full splay). Positive = deepening (+1 net), negative = lifting (−1),
zero = still. "Mixed" = opposite `(+−,−+)` or one-sided (`(1,0),(0,1)`).
"Locked" = sustained runs show only `(++,−−,00)`. "Fresh" = after
x-access (rooting resets shapes, unlocking transients).

## B. FRESH (structural)

FRESH(t) ⟺ x-access with `d_A>0` (arrival) whose preceding x-gap
contains a sign-change (mixed motion) on x, OR first x-touch of
T0-eternal structure (genesis Lap-1). Recognizable on any closed walk
(arrival + sign-change audit). Cyclic-cut independent (mod-m events).

## C. T0-marginal

B-ancestry with no in-period builder (T0-eternal preserved via quiet
all-far (still `(0,0)`), or first-touch). Must be restored for closure
(consumed ⇒ rebuilt ⟹ KEEP ⇒ A-work). Cleanest compensation route —
fails: restoration pools are unnamed (restorers post-date consumption;
different edges) ⟹ ineligible ⟹ invisible to Hall (global slack only).

## D. E0 requires freshness: PARTIAL (sustained-sign-locked ⇒ no
builder-built discrepancy; T0/preservation path remains (marginal))

Sustained builders move same-sign-or-still (0/15000+, p<1e-9 ⟹
builder-built discrepancy impossible in sustained runs (would need
counter-motion, absent)). But T0-gratis + preserved + arrival-marginal
path stays coherent (no builder needed). So freshness-necessity holds
for BUILDER-sourced discrepancy, not T0-sourced. Gap identified, not
closed.

## E–I. Classes + compensation ledgers

F-D (DELETE divergence): A-work pure (`2a`, no B-demand); credits
already counted in setup pool (tight E0: saturated, no headroom).
F-K (KEEP rebuild): A-work + B-demand jointly; locals-first absorbs;
residual small (L3); needs creator room (concentration wall).
F-T0 (inherited): closure-restoration unnamed (ineligible) — see C.
comp(f) = fresh headroom + eliminated residuals − created residuals:
F-D gives pool (saturated), F-K gives room-iff-fat (unproved),
F-T0 gives global-only (ineligible). No class yields proven ≥1.

## J. FRESH_TRANSIENT_COMPENSATION: OPEN

Neither per-fresh (saturated/terminal/ineligible) nor aggregate
(telescoping NET zero over closed cycles kills prefix gains) closes.
Alternating chains = Kuhn paths = Hall (circular). Dependency loops
are sharing-cycles (consistent, finite). Minimal one-fresh witness:
needs marginal T0+arrival conjunction (coherent, unobserved).

## K–L. E0_CORE/E0/U4/COARSE-DOUBLE: OPEN (compositions ready;
unrefuted 900+; §26/§38/§44 never fired)

ONE atomic missing (post-fresh-analysis, strictly smaller than E0):
**SUSTAINED SIGN-LOCK THEOREM:** in sustained other-key runs
(co-evolved shapes, no x-access), builder motions on x are
same-sign-or-still (never counter/one-sided). Proving it makes
builder-built discrepancy impossible ⇒ E0 needs T0-marginal ⇒
T0-marginal + closure-restoration accounting (F-T0, global sums
not Hall) may close Q≤2A directly. Current status: 0/15000+
(p<1e-9) empirical; mechanism unknown (mean-reversion suspected).
Lean gap: sign model + lock theorem (~120 lines over U1 kernel).
DO conditional (C.ZIG-V1V3 + PIVOT-2-excision mechanical).
