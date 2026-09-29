-- WP-6 STEP AR-00: MSTL-14P arithmetic backbone (present domain, Layer B partial).
--
-- Exact Nat lemmas behind Case A / t*-restart / D2 service reasoning.
-- Pure arithmetic over frozen conventions (depth+1 costs, 1-2 rotations per
-- StepEv, cap-2 greedy mobilization); NO splay model, NO ledger model, NO
-- history induction here. Those compositions live in Layer A prose.
-- Forbidden: sorry, admit, axioms. Kernel-checked via direct `lean` exit 0
-- (repo WP-1/WP-2 precedent; lakefile untouched).

-- WP-6 STEP AR-01: demand bounded by search depth (uses a >= 1 only).
-- Nat subtraction already encodes max(·, 0): need y a := y - 2 * a.
theorem need_le_pred (y a : Nat) (ha : 1 ≤ a) : y - 2 * a ≤ y - 1 := by
  omega

-- WP-6 STEP AR-02: rotations covered 1-2 per event (B-event count identity).
-- rots : rotations per B StepEv, each 1 or 2; e = number of events.
theorem rots_le_two_events : ∀ (rots : List Nat),
    (∀ r ∈ rots, r = 1 ∨ r = 2) → rots.sum ≤ 2 * rots.length := by
  intro rots h
  induction rots with
  | nil => simp
  | cons r t ih =>
    have hr : r = 1 ∨ r = 2 := h r (by simp)
    have ht : ∀ r_1 ∈ t, r_1 = 1 ∨ r_1 = 2 :=
      fun r_1 hr_1 => h r_1 (by simp [hr_1])
    have ihn := ih ht
    simp only [List.sum_cons, List.length_cons]
    omega

-- WP-6 STEP AR-03: greedy cap-2 mobilization exactness (no injection slice).
-- mob lat E = total moved by E events each moving min(lat,2) greedily.
def mob : Nat → Nat → Nat
  | _, 0 => 0
  | lat, e + 1 =>
    let m := Nat.min lat 2
    m + mob (lat - m) e

-- WP-6 STEP AR-03b: mobilization from an empty pool moves nothing.
theorem mob_zero : ∀ (e : Nat), mob 0 e = 0 := by
  intro e
  induction e with
  | zero => rfl
  | succ e2 ih2 => simp [mob, ih2]

-- WP-6 STEP AR-04: greedy total equals min(available, capacity).
theorem mob_exact : ∀ (lat nEv : Nat), mob lat nEv = Nat.min lat (2 * nEv) := by
  intro lat nEv
  induction nEv generalizing lat with
  | zero => simp [mob]
  | succ e ih =>
    simp only [mob]
    by_cases h : lat ≤ 2
    · -- thin pool: this event drains everything, rest move nothing.
      have hm : Nat.min lat 2 = lat := Nat.min_eq_left h
      have hle : lat ≤ 2 * (e + 1) := by omega
      rw [hm, Nat.sub_self, mob_zero, Nat.add_zero]
      exact (Nat.min_eq_left hle).symm
    · -- thick pool: this event moves exactly 2, recurse on remainder.
      have hlt : 2 < lat := Nat.lt_of_not_le h
      have hm : Nat.min lat 2 = 2 := Nat.min_eq_right (by omega)
      rw [hm, ih]
      by_cases hle2 : lat - 2 ≤ 2 * e
      · have e1 : Nat.min (lat - 2) (2 * e) = lat - 2 := Nat.min_eq_left hle2
        have e2 : Nat.min lat (2 * (e + 1)) = lat := Nat.min_eq_left (by omega)
        omega
      · have e1 : Nat.min (lat - 2) (2 * e) = 2 * e :=
          Nat.min_eq_right (by omega)
        have e2 : Nat.min lat (2 * (e + 1)) = 2 * (e + 1) :=
          Nat.min_eq_right (by omega)
        omega

-- WP-6 STEP AR-05: service composition (need vs B-event bandwidth).
-- need y a with a >= 1, B-rotations d = y - 1 covered 1-2 per event.
theorem service_bound (y a eB : Nat) (ha : 1 ≤ a) (hev : y - 1 ≤ 2 * eB) :
    (y - 2 * a) ≤ 2 * eB := by
  omega

-- WP-6 STEPS S3/S7 (quotient war): single-node divergence micro-bounds.
-- div v := dB v - 2 * dA v (Nat truncated). An A-StepEv moves the accessed
-- key up <= 2 levels (dA drops <= 2, dB fixed): its div rises <= 4.
-- Measured worst +4 over 5274 A-StepEvs (1252 hits at +4): the bound is
-- tight at the node level. Bystander/push-down accounting is Layer A prose.
-- STATUS (2026-09-29 session): added without kernel check (no Lean toolchain
-- in this environment; release download timed out). Proofs are omega-only in
-- the style of AR-01..AR-05 above; MUST be kernel-checked (lean 4.21.0
-- exit 0, no sorry) before citing as Layer B. Until then: SKELETON.

-- WP-6 STEP AR-06: per-A-StepEv node divergence rise (accessed key).
theorem div_rise_A (dA dA' dB : Nat) (hdrop : dA ≤ dA' + 2) :
    dB - 2 * dA' ≤ (dB - 2 * dA) + 4 := by
  omega

-- WP-6 STEP AR-07: per-B-StepEv node divergence rise (pushed-down key).
-- One StepEv pushes a bystander down <= 1 level (dB rises <= 1, dA fixed).
theorem div_rise_B (dA dB dB' : Nat) (hpush : dB' ≤ dB + 1) :
    dB' - 2 * dA ≤ (dB - 2 * dA) + 1 := by
  omega

-- WP-6 STEP AR-08: per-record capped-mass gain (cap C, e.g. C = 2).
-- The 3-record composition (Lemma A) is Layer A; this is the record slice.
theorem capped_gain (div div' C : Nat) :
    Nat.min div' C ≤ Nat.min div C + C := by
  omega

-- WP-6 STEP AR-09: global greedy discharge pool (forward accumulator).
-- poolAux p is ds threads the running pool; a step with demand d <= i + p
-- leaves exactly i + p - d (no shortfall). Prefix-coverage composition
-- (pool closes iff every prefix earned >= spent) is Layer A prose + the
-- OPEN B-source lemma, NOT proved here.
def poolAux : Nat → List Nat → List Nat → Nat
  | p, [], _ => p
  | p, _, [] => p
  | p, i :: ir, d :: dr =>
    poolAux (if d ≤ i + p then i + p - d else 0) ir dr

-- WP-6 STEP AR-09b: single covered step leaves income + pool - demand.
theorem pool_step (p i d : Nat) (h : d ≤ i + p) :
    (if d ≤ i + p then i + p - d else 0) = i + p - d := by
  rw [if_pos h]

-- WP-6 STEPS IV/ST/RB/HC (vault descent): step-depth relations + stock
-- composition. Pure Nat (no splay model): per splay, with D doubles + Z zigs
-- (Z in {0,1}), events e = D + Z and depth d = 2*D + Z. STATUS: same as
-- AR-06..AR-09 (added 2026-09-29, kernel check PENDING, omega-only style).

-- WP-6 STEP AR-10: B-steps bounded by B-depth (e = D+Z <= 2*D+Z = d).
theorem steps_le_depth (D Z : Nat) : D + Z ≤ 2 * D + Z := by
  omega

-- WP-6 STEP AR-11: A-depth bounded by twice A-steps (d = 2*D+Z <= 2*(D+Z)).
theorem depth_le_two_steps (D Z : Nat) : 2 * D + Z ≤ 2 * (D + Z) := by
  omega

-- WP-6 STEP AR-12: genesis need is zero (A0 = B0 so d_A = d_B = d).
theorem genesis_need_zero (d : Nat) : d - 2 * d - 1 = 0 := by
  omega

-- WP-6 STEP AR-13: STOCK COMPOSITION (conditional vault door).
-- N = total need, X = total B-StepEvs: D2-sum gives N <= 2*X (proved in
-- Layer A prose + code); E_B-link gives X <= 3*S_A (OPEN). Together: stock.
theorem stock_composition (N X SA : Nat) (hD2 : N ≤ 2 * X) (hEB : X ≤ 3 * SA) :
    N ≤ 6 * SA := by
  omega

-- WP-6 STEPS N-FIRST (C20): genesis first-divergence arithmetic.
-- First divergence on key x from A=B=T0: arrival DELETE-x splays x in T0
-- (e_0 StepEvs, d = T0-depth, d/2 <= e_0 <= d); x-tenure DELETEs are no-ops
-- (B frozen at T0); cash-x replays the SAME T0-splay in B (e_B = e_0 by
-- determinism). Funding 3*e_0 >= e_0; need d-1 covered by 6*e_0.
-- STATUS: arithmetic here kernel-pending (omega-only style); same-splay
-- determinism (e_B = e_0) is a Layer-A code fact (exec engine determinism),
-- subsequent (non-first, reshaped) divergence NOT covered (pool/marginal).
-- WP-6 STEP AR-14: first-divergence need covered (d-1 <= 6*e_0 from d<=2*e_0).
theorem first_div_need (d e0 : Nat) (h : d ≤ 2 * e0) : d - 1 ≤ 6 * e0 := by
  omega

-- WP-6 STEP AR-15: same-shape replay funded 3x (e_B = e_A => e_B <= 3*e_A).
theorem same_shape_funded (e : Nat) : e ≤ 3 * e := by
  omega

-- WP-6 STEP AR-16: strict D2 (need <= 2*e_B - 1 from d_B <= 2*e_B).
theorem strict_D2 (dB dA eB : Nat) (h : dB ≤ 2 * eB) :
    dB - 2 * dA - 1 ≤ 2 * eB - 1 := by
  omega
