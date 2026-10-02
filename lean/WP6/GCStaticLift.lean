-- WP-6 STEPS C139 (positional program): loop-lifted agreement + event range.
--
-- Self-contained (repo convention: no imports). Loop-lifted agreement: the
-- engine emission trace and the skeleton step trace take one element per
-- level under identical control, so their lengths agree
-- (length (emitTrace x t) = length (steps x t)) — engine iterations and
-- skeleton steps stay in lockstep over full traces. Fused per-event claim:
-- on range-valid trees every emitted event satisfies 1 ≤ lo < hi ≤ n
-- (properness from bounds-distinctness (C138 shape) + range from key-range
-- containment), exactly the hypothesis the supply machinery (C136 shape)
-- needs. With C140 (supply lift) this closes event-to-supply per access.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

inductive SStep where
  | zig : SStep
  | ll : SStep
  | rr : SStep
  | lr : SStep
  | rl : SStep
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

def steps (x : Nat) : STree → List SStep
  | .leaf => []
  | .node k l r =>
    if (x == k) = true then []
    else if x < k then match l with
      | .leaf => []
      | .node p ll lr =>
        if (x == p) = true then [.zig]
        else if x < p then steps x ll ++ [.ll]
        else steps x lr ++ [.lr]
    else match r with
      | .leaf => []
      | .node p rl rr =>
        if (x == p) = true then [.zig]
        else if p < x then steps x rr ++ [.rr]
        else steps x rl ++ [.rl]

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

-- Key range: all tree keys inside [1, n] (histories are key-valid, Layer A).
def keyrange (t : STree) (n : Nat) : Prop :=
  ∀ y, mem t y → 1 ≤ y ∧ y ≤ n

-- LOOP-LIFTED AGREEMENT: engine emission trace and skeleton step trace
-- take one element per level under identical control, so lengths agree.
theorem trace_length_eq (x : Nat) (t : STree) :
    (emitTrace x t).length = (steps x t).length := by
  refine (emitTrace.induct x (fun t => (emitTrace x t).length = (steps x t).length)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · simp [emitTrace, steps]
  · intro a a_1 a_2 h
    cases a_1 <;> cases a_2 <;>
      simp [emitTrace, steps, h]
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2, h3]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2, h3, h4, ih]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2, h3, h4, ih]
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2, h3]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2, h3, h4, ih]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [emitTrace, steps, h1, h2, h3, h4, ih]

-- FUSED PER-EVENT CLAIM: on range-valid trees every emission satisfies
-- 1 ≤ lo < hi ≤ n (exactly the supply machinery hypothesis).
theorem event_ok (x n : Nat) (t : STree) :
    valid t → keyrange t n → 1 ≤ x → x ≤ n →
    ∀ e ∈ emitTrace x t, 1 ≤ e.1 ∧ e.1 < e.2 ∧ e.2 ≤ n := by
  refine (emitTrace.induct x
    (fun t => valid t → keyrange t n → 1 ≤ x → x ≤ n →
      ∀ e ∈ emitTrace x t, 1 ≤ e.1 ∧ e.1 < e.2 ∧ e.2 ≤ n)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · intro _hv _hkr _hx1 _hxn e he; simp only [emitTrace] at he; simp at he
  · intro a a_1 a_2 h _hv _hkr _hx1 _hxn
    cases a_1 <;> cases a_2 <;> simp only [emitTrace] <;>
      (rw [if_pos h]; intro e he; simp at he)
  · intro a a_1 h1 h2 _hv _hkr _hx1 _hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2]; intro e he; simp at he)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]
       have hxp : x = a_2 := (beq_iff_eq).mp h3
       have hpk : a_2 < a := by
         have h2 := hv; simp only [valid, allLT] at h2; exact h2.2.2.1.1
       have hne : x ≠ a := by omega
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       intro e he; simp at he
       rw [he]; simp only [emit]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4]
       have hll : valid a_3 := valid_LL a a_2 a_3 a_4 _ hv
       have hkr3 : keyrange a_3 n :=
         fun y hm => hkr y (Or.inr (Or.inl (Or.inr (Or.inl hm))))
       intro e he; simp at he
       obtain h | h := he
       · exact ih hll hkr3 hx1 hxn e h
       · rw [h]; simp only [emit3]
         have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
           hkr a_2 (Or.inr (Or.inl (Or.inl rfl)))
         have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
         have hlt : a_2 < a := by
           have h2 := hv; simp only [valid, allLT] at h2; exact h2.2.2.1.1
         have hne : a_2 ≠ a := by omega
         omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4]
       have hlr : valid a_4 := valid_LR a a_2 a_3 a_4 _ hv
       have hkr4 : keyrange a_4 n :=
         fun y hm => hkr y (Or.inr (Or.inl (Or.inr (Or.inr hm))))
       intro e he; simp at he
       obtain h | h := he
       · exact ih hlr hkr4 hx1 hxn e h
       · rw [h]; simp only [emit3]
         have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
           hkr a_2 (Or.inr (Or.inl (Or.inl rfl)))
         have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
         have hlt : a_2 < a := by
           have h2 := hv; simp only [valid, allLT] at h2; exact h2.2.2.1.1
         have hne : a_2 ≠ a := by omega
         omega)
  · intro a a_1 h1 h2 _hv _hkr _hx1 _hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2]; intro e he; simp at he)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]
       have hxp : x = a_2 := (beq_iff_eq).mp h3
       have hpk : a < a_2 := by
         have h2 := hv; simp only [valid, allGT] at h2; exact h2.2.2.2.1
       have hne : x ≠ a := by omega
       have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
       intro e he; simp at he
       rw [he]; simp only [emit]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4]
       have hrr : valid a_4 := valid_RR a _ a_2 a_3 a_4 hv
       have hkr4 : keyrange a_4 n :=
         fun y hm => hkr y (Or.inr (Or.inr (Or.inr (Or.inr hm))))
       intro e he; simp at he
       obtain h | h := he
       · exact ih hrr hkr4 hx1 hxn e h
       · rw [h]; simp only [emit3]
         have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
           hkr a_2 (Or.inr (Or.inr (Or.inl rfl)))
         have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
         have hlt : a < a_2 := by
           have h2 := hv; simp only [valid, allGT] at h2; exact h2.2.2.2.1
         have hne : a_2 ≠ a := by omega
         omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hkr hx1 hxn
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4]
       have hrl : valid a_3 := valid_RL a _ a_2 a_3 a_4 hv
       have hkr3 : keyrange a_3 n :=
         fun y hm => hkr y (Or.inr (Or.inr (Or.inr (Or.inl hm))))
       intro e he; simp at he
       obtain h | h := he
       · exact ih hrl hkr3 hx1 hxn e h
       · rw [h]; simp only [emit3]
         have ha2 : 1 ≤ a_2 ∧ a_2 ≤ n :=
           hkr a_2 (Or.inr (Or.inr (Or.inl rfl)))
         have ha : 1 ≤ a ∧ a ≤ n := hkr a (Or.inl rfl)
         have hlt : a < a_2 := by
           have h2 := hv; simp only [valid, allGT] at h2; exact h2.2.2.2.1
         have hne : a_2 ≠ a := by omega
         omega)
