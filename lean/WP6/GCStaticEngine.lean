-- WP-6 STEPS C138 (positional program): engine-side emission trace.
--
-- Self-contained (repo convention: no imports). The engine loop acts and
-- emits per level; this models the emission side as `emitTrace` (one interval
-- per recursion level, mirroring `splay`'s control exactly: zig emits the
-- node/parent pair, doubles the node/parent/grandparent triple — the
-- splay_trace ZIG/LL/RR/LR/RL arms). Proved: every emitted interval is
-- proper (lo < hi) on valid trees (distinctness from bounds); trace length
-- fits tree size. With C136 (valid intervals bank counted supply), valid
-- emission traces carry counted supply end to end. Loop-lifted agreement
-- (engine iterations to skeleton steps) queued.
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

def emit (a b : Nat) : Nat × Nat := (min a b, max a b)

def emit3 (a b c : Nat) : Nat × Nat :=
  (min (min a b) c, max (max a b) c)

theorem emit_lt (a b : Nat) (hne : a ≠ b) :
    (emit a b).1 < (emit a b).2 := by
  simp only [emit]; omega

theorem emit3_lt (a b c : Nat) (hbc : b ≠ c) :
    (emit3 a b c).1 < (emit3 a b c).2 := by
  simp only [emit3]; omega

-- Emission trace: one interval per level, mirroring splay's control.
-- Zig emits node/parent keys; doubles emit node/parent/grandparent keys.
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

def tsize : STree → Nat
  | .leaf => 0
  | .node _ l r => 1 + tsize l + tsize r

-- EVERY EMITTED INTERVAL IS PROPER on valid trees (distinctness from
-- bounds; zig via node-key identity + parent separation, doubles via
-- parent/grandparent separation).
theorem emitTrace_valid (x : Nat) (t : STree) :
    valid t → ∀ e ∈ emitTrace x t, e.1 < e.2 := by
  refine (emitTrace.induct x
    (fun t => valid t → ∀ e ∈ emitTrace x t, e.1 < e.2)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · intro _hv e he; simp only [emitTrace] at he; simp at he
  · intro a a_1 a_2 h _hv
    cases a_1 <;> cases a_2 <;> simp only [emitTrace] <;>
      (rw [if_pos h]; intro e he; simp at he)
  · intro a a_1 h1 h2 _hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2]; intro e he; simp at he)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]
       have hxp : x = a_2 := (beq_iff_eq).mp h3
       have hpk : a_2 < a := by
         simp only [valid, allLT] at hv; exact hv.2.2.1.1
       have hne : x ≠ a := by omega
       intro e he; simp at he
       rw [he]; exact emit_lt _ _ hne)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4]
       have hll : valid a_3 := valid_LL a a_2 a_3 a_4 _ hv
       intro e he; simp at he
       obtain h | h := he
       · exact ih hll e h
       · rw [h]
         have hbc : a_2 ≠ a := by
           have h2 := hv
           simp only [valid, allLT] at h2
           have hlt : a_2 < a := h2.2.2.1.1
           omega
         exact emit3_lt _ _ _ hbc)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4]
       have hlr : valid a_4 := valid_LR a a_2 a_3 a_4 _ hv
       intro e he; simp at he
       obtain h | h := he
       · exact ih hlr e h
       · rw [h]
         have hbc : a_2 ≠ a := by
           have h2 := hv
           simp only [valid, allLT] at h2
           have hlt : a_2 < a := h2.2.2.1.1
           omega
         exact emit3_lt _ _ _ hbc)
  · intro a a_1 h1 h2 _hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2]; intro e he; simp at he)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]
       have hxp : x = a_2 := (beq_iff_eq).mp h3
       have hpk : a < a_2 := by
         simp only [valid, allGT] at hv; exact hv.2.2.2.1
       have hne : x ≠ a := by omega
       intro e he; simp at he
       rw [he]; exact emit_lt _ _ hne)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4]
       have hrr : valid a_4 := valid_RR a _ a_2 a_3 a_4 hv
       intro e he; simp at he
       obtain h | h := he
       · exact ih hrr e h
       · rw [h]
         have hbc : a_2 ≠ a := by
           have h2 := hv
           simp only [valid, allGT] at h2
           have hlt : a < a_2 := h2.2.2.2.1
           omega
         exact emit3_lt _ _ _ hbc)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv
    cases a_1 <;> simp only [emitTrace] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4]
       have hrl : valid a_3 := valid_RL a _ a_2 a_3 a_4 hv
       intro e he; simp at he
       obtain h | h := he
       · exact ih hrl e h
       · rw [h]
         have hbc : a_2 ≠ a := by
           have h2 := hv
           simp only [valid, allGT] at h2
           have hlt : a < a_2 := h2.2.2.2.1
           omega
         exact emit3_lt _ _ _ hbc)

-- TRACE LENGTH BOUND: emitted events fit tree size (one per level).
theorem emitTrace_length (x : Nat) (t : STree) :
    (emitTrace x t).length ≤ tsize t := by
  refine (emitTrace.induct x (fun t => (emitTrace x t).length ≤ tsize t)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · simp only [emitTrace, tsize, List.length]; omega
  · intro a a_1 a_2 h
    cases a_1 <;> cases a_2 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_pos h]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3];
       simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4];
       simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4];
       simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3];
       simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4];
       simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [emitTrace, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4];
       simp only [List.length, List.length_append]; omega)
