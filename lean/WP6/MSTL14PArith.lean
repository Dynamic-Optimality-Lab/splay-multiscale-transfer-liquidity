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
