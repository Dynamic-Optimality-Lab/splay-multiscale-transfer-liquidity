# PIVOT-18R: corrected residual accounting → joint tradeoff → verdict

## A. Residual demand (corrected, physical units)

Canonical locals-first (WLOG for sufficiency: locals exclusive to own
access, using them never harms others; NOT claimed necessary — Kuhn may
reassign, and charge() does). After `min(q_t,2a_t)` locally: residual
`R_t=(q_t−2a_t)^+` (starved: full `q_t`; nonst: small extremal part).
Total `R = total_overflow`. Residual units `R=(access, B-double index)`.

## B. Headroom (physical, counted once)

Headroom `H_e=(2a_e−q_e)^+` per access (locals-leftover) plus DELETE-setup
full `2a_s` (no locals used, `q=0`). Total `H = total_slack`. Each
physical credit once. Residual eligibility: creator/setup pools only
(locals exhausted by canonical).

## C. Corrected GAP identity

`GAP_res = R − H = total_overflow − total_slack = Q_B − 2A` (identity,
using `R−H = Σ(q−2a)^+ − Σ(2a−q)^+ = Σ(q−2a)`). Minimal residual
obstruction: `R = H+1` (one-unit deficiency), all headroom contested,
all residuals necessary, no privates/peelables.

## D. Minimal residual obstruction normal form

Starved residuals (full `q`, setup+creator pools) + nonst residuals
(small, L3-extremal, locals+creator+setup pools) + sharing exact +
zero-fat creators (else pools bigger) + E0 equation
`(q_t−2a_s)+(q'−2a')=1` + dance order. Strictly stronger (narrower) than
PIVOT-18 namer-excess: locals/tight pools excluded correctly.

## E. Era/concentration interaction (JOINT — the new content)

Disentangling fails: starved-deficit `d_s` and nonst-residual `r'`
satisfy `d_s+r'=1`, so fat-nonst (`r'≪0`) forces massive starved deficit
(`d_s≫0`, absurd cancellation luck), while extremal nonst (`r'=1`)
allows mild starved (`d_s=0`, era-boundary). THE LUCK CONCENTRATES
wherever the equation demands it — no side is independently killable.
Conditional era (§7): competitor eligibility (order-forced, no arrival)
adds NO headroom (absence, not event). Conditional concentration (§8):
near-saturation forces exact depths whose builders are marginal
(cancellation-luck). Joint tradeoff: TOTAL luck (depth-boundary ×
cancellation × order-exactness × sharing) is conserved — squeezing one
side inflates another. Formally: the E0 conjunction is marginal in
EVERY projection (depths marginal (boundary), A-nets marginal
(cancellation), order marginal (exact arrivals), sharing marginal
(exact co-naming)).

## F. Joint statement + falsification attempts (all fail = support)

Target: era-saturation + concentration cannot co-occur to GAP=+1.
Greedy discrepancy-steer (0 violations; gradient-flat ⇒ joint motion
forced). Cancellation construction (collapses to shallow attractors;
deep transient-only 22/22). Bubble concentration (mutual dethrone ⇒
per-key setups; L2 defends). Extremal loops (pre-states never recur).
Long-splice (93/86): full. Room-hunt 150: full. Shape-hunt 133: 0
shapes. Every joint attack bounces off — because each conjunct is
individually coherent and only their CONJUNCTION is rare.

## G–J. RESIDUAL_CAPACITY / E0 / U4 / COARSE-DOUBLE: OPEN

`R≤H` unproved (needs joint conjunction control = E0 itself).
E0 impossible unproved. U4 open. `total_overflow≤total_slack` open
(900+ green). `Q_B≤2A` open (composition ready; unrefuted; no witness
to classify per §31/§44 — nothing with `R>H` found).

ONE atomic missing statement (post-joint-analysis, per §42/§38):
**JOINT MARGINAL EXCLUSION:** no closed walk realizes E0-marginals
jointly — i.e., starved-deficit + nonstarved-residual + sharing +
zero-fat + dance-order with `d_s+r'=1` exactly. (Not "E0
unrealizability" in the abstract — the concrete joint-marginal form
with tail quantification below.) Why atomic: it is exactly minimal
residual-obstruction nonexistence; anything weaker (era alone,
concentration alone, per-side margins) leaves the other side free to
compensate (joint tradeoff §E). Tail quantification: violation needs
~5σ A/B-net decoupling (prob ~1e-6/long-cycle — explains 0/900 while
remaining coherent; needs 10⁶ long cycles to probe, infeasible here).
Lean: U1 kernel green; residual/block model gap stands.
DO chain conditional (C.ZIG-V1V3 + PIVOT-2-excision mechanical).
