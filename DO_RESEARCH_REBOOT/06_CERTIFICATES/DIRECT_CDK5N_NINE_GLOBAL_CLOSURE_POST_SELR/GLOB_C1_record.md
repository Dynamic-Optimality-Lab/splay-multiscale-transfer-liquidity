# GLOB C1 compensation-feasibility record (§8) — HONEST STATUS: OPEN

## C1 candidate statement (frozen for audit)

C1-GAP: Let I_j be E3 (H=1,c=1,q=3) with target v. Then (a) g(v) falls
from ≥4 at interval start P to 0 at interval end Q (T_4 token consumed);
(b) total other-key positive-gap creation in I_j is ≤3, hence net
Γ(P)−Γ(Q) ≥1; (c) each unit of Γ increase anywhere is traceable to a
source operation carrying A-cost, so E3 deficits are covered by
source-paid Γ production within the same closed cycle.

## What is PROVED

(a) Per-key elimination: g_P(v)≥4 by L0; at Q both roots are v (terminal
KEEP splays v to both roots) so d_A=d_B=0, g_Q(v)=0. T_4 token consumed
669/669 corpus E3 (verified). This is a real structural recovery event
with demonstrated application to every observed E3 (incl. nonzero-on-DELETE
cases). No global repayment assumed; no matching; fixture-free.

## What is NOT proved (exact obstruction)

(b) Net-drop bound: observed rises ∈{1,2,3} (max exactly 3, n=669) and net
drops ∈{1,2,3}, but no universal proof that other-key rises ≤3 on an E3
interval. Requires splay-perturbation analysis (A-ZIG + B depth-6/7 chain
effects on all marked gaps) analogous to row-diameter work; not closed here.
(c) Creation-cost link: no proved lemma that Γ/T_4 production implies
quantified A-expenditure elsewhere. Preceding-KEEP creation argument gives
no clean lower bound (splaying u perturbs v arbitrarily). Hence no
constructed charge from deficit to source-paid surplus; any Ψ_W would be
assumed matching (circular per §7.3).

## Feasibility decision

C1 establishes a genuine disparity-recovery event but NOT the required
nontrivial source-compensation relation (creation/recovery vs actual
A-expenditure). Per §8 criteria 4–6 (nontrivial compensation consequence,
demonstrated payment relevance, no assumed matching): NOT MET.

**R2-F: FAIL/OPEN.** Recorded obstruction: universal other-key rise bound
(≤3) + Γ-production cost link unproved. No second mechanism introduced;
no restricted pivot; no promotion. The main diagnostic audit below runs as
falsification support only and cannot pass R2-U.
