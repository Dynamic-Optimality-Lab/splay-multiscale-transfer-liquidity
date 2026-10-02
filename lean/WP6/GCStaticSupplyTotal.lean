-- WP-6 STEPS C140 (positional program): supply lift per access.
--
-- Self-contained (repo convention: no imports). Fused per-access supply:
-- on range-valid trees the emission trace length is covered by counted
-- supply (each event banks ≥ 1 site, summed). Combines the C136 counting
-- (sites_count floor) with the C139 event characterization (range +
-- distinctness per arm) in a single induction, so no cross-file import is
-- needed. With C139 (length agreement) the skeleton step count is covered
-- too: steps ≤ supply per access on range-valid trees. This closes the
-- event-to-supply chain per access in kernel; the remaining open wall
-- (violator-zone/matching universals) is mathematics, not formalization.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

def mem : STree → Nat → Prop
  | .leaf, _ => False
  | .node k l r, y => y = k ∨ mem l y ∨ mem r y

def allLT : STree → Nat → Prop
  | .leaf, _ => True
  | .node k l r, b => k < b ∧ allLT l b ∧ allLT r b

def allGT : STree → Nat → Prop
  | .leaf, _ => True
  | .node k l r, b => b < k ∧ allGT l b ∧ allGT r b

def valid : STree → Prop
  | .leaf => True
  | .node k l r => valid l ∧ valid r ∧ allLT l k ∧ allGT r k

theorem valid_L (k : Nat) (l r : STree) (h : valid (.node k l r)) :
    valid l := by
  simp only [valid] at h; exact h.1

theorem valid_R (k : Nat) (l r : STree) (h : valid (.node k l r)) :
    valid r := by
  simp only [valid] at h; exact h.2.1

theorem valid_LL (k : Nat) (p : Nat) (ll lr r : STree)
    (h : valid (.node k (.node p ll lr) r)) : valid ll := by
  simp only [valid] at h; exact h.1.1

theorem valid_LR (k : Nat) (p : Nat) (ll lr r : STree)
    (h : valid (.node k (.node p ll lr) r)) : valid lr := by
  simp only [valid] at h; exact h.1.2.1

theorem valid_RL (k : Nat) (l : STree) (p : Nat) (rl rr : STree)
    (h : valid (.node k l (.node p rl rr))) : valid rl := by
  simp only [valid] at h; exact h.2.1.1

theorem valid_RR (k : Nat) (l : STree) (p : Nat) (rl rr : STree)
    (h : valid (.node k l (.node p rl rr))) : valid rr := by
  simp only [valid] at h; exact h.2.1.2.1

def keyrange (t : STree) (n : Nat) : Prop :=
  ∀ y, mem t y → 1 ≤ y ∧ y ≤ n

def emit (a b : Nat) : Nat × Nat := (min a b, max a b)

def emit3 (a b c : Nat) : Nat × Nat :=
  (min (min a b) c, max (max a b) c)

def emitTrace (x : Nat) : STree → List (Nat × Nat)
  | .leaf => []
  | .node k l r =>
    if (x == k) = true then []
    else if x < k then match l with
      | .leaf => []
      | .node p ll lr =>
        if (x == p) = true then [emit x k]
        else if x < p then emitTrace x ll ++ [emit3 x p k]
        else emitTrace x lr ++ [emit3 x p k]
    else match r with
      | .leaf => []
      | .node p rl rr =>
        if (x == p) = true then [emit x k]
        else if p < x then emitTrace x rr ++ [emit3 x p k]
        else emitTrace x rl ++ [emit3 x p k]

-- `_sites` count model (C136 shape).
def sites_count (lo hi n : Nat) : Nat :=
  ((List.range' lo (hi - lo)).filter
    (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi))).length

theorem sites_ge_one (lo hi n : Nat) (h1 : 1 ≤ lo) (h2 : lo < hi)
    (h3 : hi ≤ n) : 1 ≤ sites_count lo hi n := by
  have hmem : lo ∈ List.range' lo (hi - lo) :=
    List.mem_range'.mpr ⟨0, by omega, rfl⟩
  have hP : 1 ≤ lo ∧ lo < n ∧ lo + 1 ≤ hi := ⟨h1, by omega, by omega⟩
  have hpred : (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi)) lo = true :=
    decide_eq_true hP
  have hfm : lo ∈ (List.range' lo (hi - lo)).filter
      (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi)) :=
    List.mem_filter.mpr ⟨hmem, hpred⟩
  simp only [sites_count]
  cases hfl : (List.range' lo (hi - lo)).filter
      (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi)) with
  | nil => rw [hfl] at hfm; simp at hfm
  | cons hd tl => simp only [sites_count, hfl, List.length]; omega

-- Total supply across an event list (structural, clean equations).
def supplyTotal : List (Nat × Nat) → Nat → Nat
  | [], _ => 0
  | e :: evs, n => sites_count e.1 e.2 n + supplyTotal evs n

theorem supplyTotal_append (l₁ l₂ : List (Nat × Nat)) (n : Nat) :
    supplyTotal (l₁ ++ l₂) n = supplyTotal l₁ n + supplyTotal l₂ n := by
  induction l₁ with
  | nil => simp [supplyTotal]
  | cons e rest ih =>
    rw [List.cons_append]; simp only [supplyTotal]; rw [ih]; omega

-- GRAND FUSED TOTAL: on range-valid trees, event count is covered by
-- counted supply (each event banks ≥ 1 site, summed over the trace).
theorem supply_total (x n : Nat) (t : STree) :
    valid t → keyrange t n → 1 ≤ x → x ≤ n →
    (emitTrace x t).length ≤ supplyTotal (emitTrace x t) n := by
  refine (emitTrace.induct x
    (fun t => valid t → keyrange t n → 1 ≤ x → x ≤ n →
      (emitTrace x t).length ≤ supplyTotal (emitTrace x t) n)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · intro _hv _hkr _hx1 _hxn
    simp only [emitTrace, supplyTotal, List.length, Nat.zero_le]
  · intro a a_1 a_2 h _hv _hkr _hx1 _hxn
    cases a_1 <;> cases a_2 <;> simp only [emitTrace] <;>
      (rw [if_pos h]; simp only [supplyTotal, List.length, Nat.zero_le])
  · intro a a_1 h1 h2 _hv _hkr _hx1 _hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2];
       simp only [supplyTotal, List.length, Nat.zero_le])
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]
       have hxp : x = a_2 := (beq_iff_eq).mp h3
       have hpk : a_2 < a := by
         have h2 := hv; simp only [valid, allLT] at h2; exact h2.2.2.1.1
       have hne : x ≠ a := by omega
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       have r1 : 1 ≤ (emit x a).1 := by simp only [emit]; omega
       have r2 : (emit x a).1 < (emit x a).2 := by simp only [emit]; omega
       have r3 : (emit x a).2 ≤ n := by simp only [emit]; omega
       have h2 : 1 ≤ sites_count (emit x a).1 (emit x a).2 n :=
         sites_ge_one _ _ _ r1 r2 r3
       simp only [supplyTotal, List.length, Nat.add_zero]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4]
       have hll : valid a_3 := valid_LL a a_2 a_3 a_4 _ hv
       have hkr3 : keyrange a_3 n :=
         fun y hm => hkr y (Or.inr (Or.inl (Or.inr (Or.inl hm))))
       have hI : (emitTrace x a_3).length ≤ supplyTotal (emitTrace x a_3) n :=
         ih hll hkr3 hx1 hxn
       have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
         hkr a_2 (Or.inr (Or.inl (Or.inl rfl)))
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       have hlt : a_2 < a := by
         have h2 := hv; simp only [valid, allLT] at h2; exact h2.2.2.1.1
       have hne : a_2 ≠ a := by omega
       have r1 : 1 ≤ (emit3 x a_2 a).1 := by simp only [emit3]; omega
       have r2 : (emit3 x a_2 a).1 < (emit3 x a_2 a).2 := by simp only [emit3]; omega
       have r3 : (emit3 x a_2 a).2 ≤ n := by simp only [emit3]; omega
       have h2 : 1 ≤ sites_count (emit3 x a_2 a).1 (emit3 x a_2 a).2 n :=
         sites_ge_one _ _ _ r1 r2 r3
       simp only [supplyTotal_append, supplyTotal,
         List.length_append, List.length, Nat.add_zero]
       omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4]
       have hlr : valid a_4 := valid_LR a a_2 a_3 a_4 _ hv
       have hkr4 : keyrange a_4 n :=
         fun y hm => hkr y (Or.inr (Or.inl (Or.inr (Or.inr hm))))
       have hI : (emitTrace x a_4).length ≤ supplyTotal (emitTrace x a_4) n :=
         ih hlr hkr4 hx1 hxn
       have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
         hkr a_2 (Or.inr (Or.inl (Or.inl rfl)))
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       have hlt : a_2 < a := by
         have h2 := hv; simp only [valid, allLT] at h2; exact h2.2.2.1.1
       have hne : a_2 ≠ a := by omega
       have r1 : 1 ≤ (emit3 x a_2 a).1 := by simp only [emit3]; omega
       have r2 : (emit3 x a_2 a).1 < (emit3 x a_2 a).2 := by simp only [emit3]; omega
       have r3 : (emit3 x a_2 a).2 ≤ n := by simp only [emit3]; omega
       have h2 : 1 ≤ sites_count (emit3 x a_2 a).1 (emit3 x a_2 a).2 n :=
         sites_ge_one _ _ _ r1 r2 r3
       simp only [supplyTotal_append, supplyTotal,
         List.length_append, List.length, Nat.add_zero]
       omega)
  · intro a a_1 h1 h2 _hv _hkr _hx1 _hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2];
       simp only [supplyTotal, List.length, Nat.zero_le])
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]
       have hxp : x = a_2 := (beq_iff_eq).mp h3
       have hpk : a < a_2 := by
         have h2 := hv; simp only [valid, allGT] at h2; exact h2.2.2.2.1
       have hne : x ≠ a := by omega
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       have r1 : 1 ≤ (emit x a).1 := by simp only [emit]; omega
       have r2 : (emit x a).1 < (emit x a).2 := by simp only [emit]; omega
       have r3 : (emit x a).2 ≤ n := by simp only [emit]; omega
       have h2 : 1 ≤ sites_count (emit x a).1 (emit x a).2 n :=
         sites_ge_one _ _ _ r1 r2 r3
       simp only [supplyTotal, List.length, Nat.add_zero]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4]
       have hrr : valid a_4 := valid_RR a _ a_2 a_3 a_4 hv
       have hkr4 : keyrange a_4 n :=
         fun y hm => hkr y (Or.inr (Or.inr (Or.inr (Or.inr hm))))
       have hI : (emitTrace x a_4).length ≤ supplyTotal (emitTrace x a_4) n :=
         ih hrr hkr4 hx1 hxn
       have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
         hkr a_2 (Or.inr (Or.inr (Or.inl rfl)))
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       have hlt : a < a_2 := by
         have h2 := hv; simp only [valid, allGT] at h2; exact h2.2.2.2.1
       have hne : a_2 ≠ a := by omega
       have r1 : 1 ≤ (emit3 x a_2 a).1 := by simp only [emit3]; omega
       have r2 : (emit3 x a_2 a).1 < (emit3 x a_2 a).2 := by simp only [emit3]; omega
       have r3 : (emit3 x a_2 a).2 ≤ n := by simp only [emit3]; omega
       have h2 : 1 ≤ sites_count (emit3 x a_2 a).1 (emit3 x a_2 a).2 n :=
         sites_ge_one _ _ _ r1 r2 r3
       simp only [supplyTotal_append, supplyTotal,
         List.length_append, List.length, Nat.add_zero]
       omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4]
       have hrl : valid a_3 := valid_RL a _ a_2 a_3 a_4 hv
       have hkr3 : keyrange a_3 n :=
         fun y hm => hkr y (Or.inr (Or.inr (Or.inr (Or.inl hm))))
       have hI : (emitTrace x a_3).length ≤ supplyTotal (emitTrace x a_3) n :=
         ih hrl hkr3 hx1 hxn
       have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
         hkr a_2 (Or.inr (Or.inr (Or.inl rfl)))
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       have hlt : a < a_2 := by
         have h2 := hv; simp only [valid, allGT] at h2; exact h2.2.2.2.1
       have hne : a_2 ≠ a := by omega
       have r1 : 1 ≤ (emit3 x a_2 a).1 := by simp only [emit3]; omega
       have r2 : (emit3 x a_2 a).1 < (emit3 x a_2 a).2 := by simp only [emit3]; omega
       have r3 : (emit3 x a_2 a).2 ≤ n := by simp only [emit3]; omega
       have h2 : 1 ≤ sites_count (emit3 x a_2 a).1 (emit3 x a_2 a).2 n :=
         sites_ge_one _ _ _ r1 r2 r3
       simp only [supplyTotal_append, supplyTotal,
         List.length_append, List.length, Nat.add_zero]
       omega)
