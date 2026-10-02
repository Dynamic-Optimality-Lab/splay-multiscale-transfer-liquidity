-- WP-6 STEPS C131 (positional program): BST validity + rotation preservation.
--
-- Self-contained (repo convention: no imports). BST validity over STree
-- (all-left-keys-below / all-right-keys-above, mirroring the BST invariant
-- `python/liquidity/legacy_embedding.py` relies on for splay correctness).
-- Proved: bound-membership routing (allLT/allGT-mem), bound monotonicity,
-- search correctness (membership + order pinpoints the child), and the key
-- structural fact that single rotations preserve validity (rotR/rotL).
-- These are the premises C132 needs for conditional root delivery
-- (valid + member ⟹ splayed key reaches root) and the simulation relation
-- with the pointer engine.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

def mem : STree → Nat → Prop
  | .leaf, _ => False
  | .node k l r, y => y = k ∨ mem l y ∨ mem r y

-- All keys in t below / above a bound.
def allLT : STree → Nat → Prop
  | .leaf, _ => True
  | .node k l r, b => k < b ∧ allLT l b ∧ allLT r b

def allGT : STree → Nat → Prop
  | .leaf, _ => True
  | .node k l r, b => b < k ∧ allGT l b ∧ allGT r b

-- BST validity: children valid, left keys below, right keys above.
def valid : STree → Prop
  | .leaf => True
  | .node k l r => valid l ∧ valid r ∧ allLT l k ∧ allGT r k

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

def rotL : STree → STree
  | .node p l (.node x lr rr) => .node x (.node p l lr) rr
  | t => t

-- Bound-membership routing: a member respects the bounds.
theorem allLT_mem (t : STree) (y b : Nat)
    (hm : mem t y) (hb : allLT t b) : y < b := by
  induction t with
  | leaf => simp only [mem] at hm
  | node k l r ihl ihr =>
    simp only [mem] at hm
    simp only [allLT] at hb
    obtain h | h | h := hm
    · omega
    · exact ihl h hb.2.1
    · exact ihr h hb.2.2

theorem allGT_mem (t : STree) (y b : Nat)
    (hm : mem t y) (hb : allGT t b) : b < y := by
  induction t with
  | leaf => simp only [mem] at hm
  | node k l r ihl ihr =>
    simp only [mem] at hm
    simp only [allGT] at hb
    obtain h | h | h := hm
    · omega
    · exact ihl h hb.2.1
    · exact ihr h hb.2.2

-- Bound monotonicity (bounds tighten freely).
theorem allLT_mono (t : STree) (b c : Nat)
    (h : allLT t b) (hle : b ≤ c) : allLT t c := by
  induction t with
  | leaf => simp only [allLT]
  | node k l r ihl ihr =>
    simp only [allLT] at h ⊢
    obtain ⟨hk, hl, hr⟩ := h
    exact ⟨by omega, ihl hl, ihr hr⟩

theorem allGT_mono (t : STree) (b c : Nat)
    (h : allGT t b) (hle : c ≤ b) : allGT t c := by
  induction t with
  | leaf => simp only [allGT]
  | node k l r ihl ihr =>
    simp only [allGT] at h ⊢
    obtain ⟨hk, hl, hr⟩ := h
    exact ⟨by omega, ihl hl, ihr hr⟩

-- Search correctness: membership + order pinpoints the child (splay
-- descent is correct on valid trees).
theorem mem_search_L (k : Nat) (l r : STree) (y : Nat)
    (hv : valid (.node k l r)) (hm : mem (.node k l r) y) (hlt : y < k) :
    mem l y := by
  simp only [valid, mem] at hv hm
  obtain h | h | h := hm
  · exact (False.elim (by omega))
  · exact h
  · have hky : k < y := allGT_mem r y k h hv.2.2.2
    exact (False.elim (by omega))

theorem mem_search_R (k : Nat) (l r : STree) (y : Nat)
    (hv : valid (.node k l r)) (hm : mem (.node k l r) y) (hlt : k < y) :
    mem r y := by
  simp only [valid, mem] at hv hm
  obtain h | h | h := hm
  · exact (False.elim (by omega))
  · have hky : y < k := allLT_mem l y k h hv.2.2.1
    exact (False.elim (by omega))
  · exact h

-- Single rotations preserve BST validity (the structural fact behind
-- validity maintenance across every splay StepEv).
theorem valid_rotR (T : STree) (hv : valid T) : valid (rotR T) := by
  cases T with
  | leaf => exact hv
  | node p l r =>
    cases l with
    | leaf => exact hv
    | node x ll lr =>
      simp only [rotR, valid, allLT, allGT] at hv ⊢
      obtain ⟨⟨hll, hlr, hlt_ll_x, hgt_lr_x⟩, hr,
        ⟨hxp, hlt_ll_p, hlt_lr_p⟩, hgt_r_p⟩ := hv
      exact ⟨hll, ⟨hlr, hr, hlt_lr_p, hgt_r_p⟩, hlt_ll_x,
        ⟨hxp, hgt_lr_x, allGT_mono r p x hgt_r_p (by omega)⟩⟩

theorem valid_rotL (T : STree) (hv : valid T) : valid (rotL T) := by
  cases T with
  | leaf => exact hv
  | node p l r =>
    cases r with
    | leaf => exact hv
    | node x lr rr =>
      simp only [rotL, valid, allLT, allGT] at hv ⊢
      obtain ⟨hl, ⟨hlr, hrr, hlt_lr_x, hgt_rr_x⟩, hlt_l_p,
        ⟨hxp, hgt_lr_p, hgt_rr_p⟩⟩ := hv
      exact ⟨⟨hl, hlr, hlt_l_p, hgt_lr_p⟩, hrr,
        ⟨hxp, allLT_mono l p x hlt_l_p (by omega), hlt_lr_x⟩, hgt_rr_x⟩
