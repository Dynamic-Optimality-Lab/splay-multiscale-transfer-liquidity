# PIVOT-22: exact binary decision — n≤9 YES-certified, n≥10 wall (honest OPEN)

## A–H analog (YES for n≤9, certified)

**Theorem (finite, exact):** every reachable closed Pair-Access cycle
with n≤9 satisfies `Q_B ≤ 2A` (i.e. `W_Q = Q−2A ≤ 0).

- n≤6: analytic (`Q≤B` + `rho<2` ⇒ `Q<2A`; `A=0⇒B=Q=0`) + integer BF
  `rho_n` + fixed-Howard (0/1). Banked, re-verified via cleanroom replay
  (5/3 exact `A6Q4Z6`, self-loops `W=0`).
- n=7: Howard max-mean `μ*=0/1` (2 iters, exact cross-mult) + BF
  feasible (3 passes, 184K states) + INDEPENDENT verifier GREEN
  (2,576,574/2,576,574 edge inequalities, fresh trans derived).
- n=8: BF feasible (4 passes, 2M states) + verifier GREEN
  (32,718,400/32,718,400).
- n=9: BF feasible (7 passes, 23.6M states) + verifier GREEN
  (425,502,792/425,502,792).
- Dual potentials are integer vectors (`bf{7,8,9}.pkl`); telescoping
  gives `W≤0` on every closed cycle (exact, machine-checkable).
- Max-mean is EXACTLY 0 (attained by rooted self-loops), not just ≤0.

## n≥10: wall (why YES does not extend, why NO not found)

- Exact BF caps at n≈9 (n=10: 282M states, 5G edges/pass, ~2hr/pass —
  infeasible time; memory borderline-OOM).
- Finite-obstruction (support bound) is circular (support⟺N_*⟺m⟺states,
  no base; R1-contraction leaves symbolic chains; excision gives only
  n-dependent simple bound; integer W≥1 lands in E0 (wall)).
- NO-hunt (W_Q hillclimb n=10–12, bred/spliced/extremal/long + prior
  900+): best −2, all ≤0. Closed-construction methods preserve
  nonpositivity (splice sums, trajectory attractors, BFS marginal
  closers); mutation breaks closedness. Typical 2× margins make uphill
  futile (gradients point to slack).
- Universal routes (31 formulations: U4/Hall, E0/dance, era, sharing,
  sign-lock, path-hit, inventory, rotation, builder-tree, dual, mass
  displacement, hillclimb landscape, construction): all need A/B
  discrepancy control (margins vs sharing/depths/counts) with
  independent quantities; tails coherent (Gaussian/cancellation/
  marginal, ~5σ needs 10⁶ cycles); unobserved 900+; unproved (nonzero
  prob, short streaks k=2 at 0.04% expect ~0.4–4, 0 seen p~0.02–0.7).

## Verdict (honest, §33-honoring)

**n≤9: YES, PROVED** (certificates above, independently verified).
**n≥10: OPEN** (no proof (wall: obstruction circular + universal wall);
no witness (hunt negative)). NOT universal-YES (n≥10 unproved) and NOT
NO (no `Q_B>2A` witness). §32 binary unsatisfied; §33 honored (no
guessing). ONE missing lemma (unchanged kind): E0-dance / joint-marginal
unrealizability for n≥10 (tails need 10⁶ long cycles, infeasible here).
DO chain conditional throughout (C.ZIG-V1V3 + PIVOT-2-excision
mechanical). Zero kills (nothing refuted anywhere).
