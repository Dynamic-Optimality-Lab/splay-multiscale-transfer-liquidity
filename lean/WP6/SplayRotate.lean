-- WP-6 STEP C107: rotation-row kernel for 8W (Layer B: single-rotation depth table).
--
-- Functional BST skeleton (shapes mirror `python/liquidity/legacy_embedding.py`
-- _rot_right/_rot_left, which rebuild the same rotated triples). depth = edges
-- root->key (none if absent). Per-region tables (local depths; rotation rehangs
-- the matched subtree at the same position, so all other keys keep depth):
--   rotR (.node p (.node x ll lr) r): x -1, p +1, ll -1 (rides with x),
--     lr 0 (middle), r +1 (outer); needs x < p (left-child shape).
--   rotL mirror: x -1, p +1, rr -1, rl 0, l +1; needs p < x.
-- Ordering hypotheses stand in for BST-validity facts (Layer A proves BST
-- invariance separately; splay_trace callers supply them). This grounds 8W's
-- per-StepEv rows: single rotation deepens any bystander by at most +1
-- (zig: p-or-outer +1; zigzig/zagzag second rotation re-applies: +2 max).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

def sdepth : STree → Nat → Option Nat
  | .leaf, _ => none
  | .node k l r, x =>
    if x == k then some 0
    else if x < k then Option.map (· + 1) (sdepth l x)
    else Option.map (· + 1) (sdepth r x)

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

def rotL : STree → STree
  | .node p l (.node x lr rr) => .node x (.node p l lr) rr
  | t => t

theorem sdepth_self (k : Nat) (l r : STree) :
    sdepth (.node k l r) k = some 0 := by
  unfold sdepth
  cases h : (k == k) with
  | true => rfl
  | false =>
    have t : (k == k) = true := (beq_iff_eq).mpr rfl
    rw [t] at h
    exact Bool.noConfusion h

-- Right rotation: rotated-up child x goes 1 -> 0.
theorem rotR_up (xk pk : Nat) (ll lr r : STree) (hne : xk ≠ pk) (hlt : xk < pk) :
    sdepth (.node pk (.node xk ll lr) r) xk = some 1 ∧
    sdepth (rotR (.node pk (.node xk ll lr) r)) xk = some 0 := by
  have h1 : xk ≠ pk := hne
  simp [sdepth, rotR, beq_iff_eq, h1, hlt, sdepth_self] <;> omega

-- Right rotation: parent p goes 0 -> 1.
theorem rotR_down (xk pk : Nat) (ll lr r : STree) (hlt : xk < pk) :
    sdepth (.node pk (.node xk ll lr) r) pk = some 0 ∧
    sdepth (rotR (.node pk (.node xk ll lr) r)) pk = some 1 := by
  have h2 : pk ≠ xk := by omega
  have h3 : ¬ pk < xk := by omega
  simp [sdepth, rotR, beq_iff_eq, hlt, h2, h3, sdepth_self] <;> omega

-- Right rotation: ll-subtree rides up with x (-1).
theorem rotR_ll (xk pk : Nat) (ll lr r : STree) (y d : Nat)
    (hyx : y < xk) (hlt : xk < pk) (h : sdepth ll y = some d) :
    sdepth (.node pk (.node xk ll lr) r) y = some (2 + d) ∧
    sdepth (rotR (.node pk (.node xk ll lr) r)) y = some (1 + d) := by
  have h1 : y ≠ pk := by omega
  have h2 : y ≠ xk := by omega
  have hp1 : y < pk := by omega
  simp [sdepth, rotR, beq_iff_eq, h1, h2, hp1, hyx, h] <;> omega

-- Right rotation: middle lr-subtree unchanged (0).
theorem rotR_lr (xk pk : Nat) (ll lr r : STree) (y d : Nat)
    (hgt : xk < y) (hlt2 : y < pk) (h : sdepth lr y = some d) :
    sdepth (.node pk (.node xk ll lr) r) y = some (2 + d) ∧
    sdepth (rotR (.node pk (.node xk ll lr) r)) y = some (2 + d) := by
  have h1 : y ≠ pk := by omega
  have h2 : y ≠ xk := by omega
  have hn : ¬ y < xk := by omega
  simp [sdepth, rotR, beq_iff_eq, h1, h2, hn, hlt2, h] <;> omega

-- Right rotation: outer r-subtree deepens (+1).
theorem rotR_r (xk pk : Nat) (ll lr r : STree) (y d : Nat)
    (hgt : pk < y) (hlt : xk < pk) (h : sdepth r y = some d) :
    sdepth (.node pk (.node xk ll lr) r) y = some (1 + d) ∧
    sdepth (rotR (.node pk (.node xk ll lr) r)) y = some (2 + d) := by
  have h1 : y ≠ pk := by omega
  have h2 : y ≠ xk := by omega
  have hn1 : ¬ y < pk := by omega
  have hn2 : ¬ y < xk := by omega
  simp [sdepth, rotR, beq_iff_eq, h1, h2, hn1, hn2, hlt, h] <;> omega

-- Left rotation: rotated-up child x goes 1 -> 0.
theorem rotL_up (xk pk : Nat) (l lr rr : STree) (hne : xk ≠ pk) (hlt : pk < xk) :
    sdepth (.node pk l (.node xk lr rr)) xk = some 1 ∧
    sdepth (rotL (.node pk l (.node xk lr rr))) xk = some 0 := by
  have h1 : xk ≠ pk := hne
  have hn : ¬ xk < pk := by omega
  simp [sdepth, rotL, beq_iff_eq, h1, hn, hlt, sdepth_self] <;> omega

-- Left rotation: parent p goes 0 -> 1.
theorem rotL_down (xk pk : Nat) (l lr rr : STree) (hlt : pk < xk) :
    sdepth (.node pk l (.node xk lr rr)) pk = some 0 ∧
    sdepth (rotL (.node pk l (.node xk lr rr))) pk = some 1 := by
  have h2 : pk ≠ xk := by omega
  have hp : pk < xk := hlt
  simp [sdepth, rotL, beq_iff_eq, hlt, h2, hp, sdepth_self] <;> omega

-- Left rotation: rr-subtree rides up with x (-1).
theorem rotL_rr (xk pk : Nat) (l lr rr : STree) (y d : Nat)
    (hgt : xk < y) (hlt : pk < xk) (h : sdepth rr y = some d) :
    sdepth (.node pk l (.node xk lr rr)) y = some (2 + d) ∧
    sdepth (rotL (.node pk l (.node xk lr rr))) y = some (1 + d) := by
  have h1 : y ≠ pk := by omega
  have h2 : y ≠ xk := by omega
  have hn1 : ¬ y < pk := by omega
  have hn2 : ¬ y < xk := by omega
  simp [sdepth, rotL, beq_iff_eq, h1, h2, hn1, hn2, hlt, h] <;> omega

-- Left rotation: middle rl-subtree unchanged (0).
theorem rotL_rl (xk pk : Nat) (l lr rr : STree) (y d : Nat)
    (hlt2 : pk < y) (hgt : y < xk) (h : sdepth lr y = some d) :
    sdepth (.node pk l (.node xk lr rr)) y = some (2 + d) ∧
    sdepth (rotL (.node pk l (.node xk lr rr))) y = some (2 + d) := by
  have h1 : y ≠ pk := by omega
  have h2 : y ≠ xk := by omega
  have hnp : ¬ y < pk := by omega
  simp [sdepth, rotL, beq_iff_eq, h1, h2, hnp, hlt2, hgt, h] <;> omega

-- Left rotation: outer l-subtree deepens (+1).
theorem rotL_l (xk pk : Nat) (l lr rr : STree) (y d : Nat)
    (hlt3 : y < pk) (hlt : pk < xk) (h : sdepth l y = some d) :
    sdepth (.node pk l (.node xk lr rr)) y = some (1 + d) ∧
    sdepth (rotL (.node pk l (.node xk lr rr))) y = some (2 + d) := by
  have h1 : y ≠ pk := by omega
  have h2 : y ≠ xk := by omega
  have hltx : y < xk := by omega
  simp [sdepth, rotL, beq_iff_eq, h1, h2, hltx, hlt3, hlt, h] <;> omega

-- Uniform +1 bound, right rotation: comparisons + presence suffice, no BST hyp
-- (search path is comparison-determined; presence gives local depth).
theorem rotR_bound (xk pk : Nat) (ll lr r : STree) (y m : Nat)
    (hlt : xk < pk) (h : sdepth (.node pk (.node xk ll lr) r) y = some m) :
    ∃ m', sdepth (rotR (.node pk (.node xk ll lr) r)) y = some m' ∧ m' ≤ m + 1 := by
  cases Decidable.em (y = pk) with
  | inl heq =>
    rw [heq] at h ⊢
    obtain ⟨hb, ha⟩ := rotR_down xk pk ll lr r hlt
    have hm : 0 = m := Option.some_inj.mp (hb ▸ h)
    exact ⟨1, ha, by omega⟩
  | inr hne =>
    cases Decidable.em (y = xk) with
    | inl heq2 =>
      rw [heq2] at h ⊢
      have hne_p : xk ≠ pk := by omega
      obtain ⟨hb, ha⟩ := rotR_up xk pk ll lr r hne_p hlt
      have hm : 1 = m := Option.some_inj.mp (hb ▸ h)
      exact ⟨0, ha, by omega⟩
    | inr hne2 =>
      cases Decidable.em (y < pk) with
      | inr hnp =>
        have hgt : pk < y := by omega
        have h1 : y ≠ pk := by omega
        have h2 : y ≠ xk := by omega
        have hn2 : ¬ y < xk := by omega
        have bpk : (y == pk) = false := by simpa [beq_iff_eq] using h1
        have bxk : (y == xk) = false := by simpa [beq_iff_eq] using h2
        simp only [sdepth, bpk, bxk, hnp, hn2, ↓reduceIte] at h
        cases hh : sdepth r y with
        | none => simp_all
        | some d =>
          rw [hh] at h
          simp only [Option.map_some] at h
          have e : d + 1 = m := Option.some_inj.mp h
          obtain ⟨hb, ha⟩ := rotR_r xk pk ll lr r y d hgt hlt hh
          exact ⟨2 + d, ha, by omega⟩
      | inl hlt2 =>
        cases Decidable.em (y < xk) with
        | inl hyx =>
          have h1 : y ≠ pk := by omega
          have hp1 : y < pk := by omega
          have bpk : (y == pk) = false := by simpa [beq_iff_eq] using h1
          have bxk : (y == xk) = false := by simpa [beq_iff_eq] using hne2
          simp only [sdepth, bpk, bxk, hp1, hyx, ↓reduceIte] at h
          cases hh : sdepth ll y with
          | none => simp_all
          | some d =>
            rw [hh] at h
            simp only [Option.map_some] at h
            have e : d + 1 + 1 = m := Option.some_inj.mp h
            obtain ⟨hb, ha⟩ := rotR_ll xk pk ll lr r y d hyx hlt hh
            exact ⟨1 + d, ha, by omega⟩
        | inr hnx =>
          have hgt : xk < y := by omega
          have h1 : y ≠ pk := by omega
          have bpk : (y == pk) = false := by simpa [beq_iff_eq] using h1
          have bxk : (y == xk) = false := by simpa [beq_iff_eq] using hne2
          simp only [sdepth, bpk, bxk, hnx, hlt2, ↓reduceIte] at h
          cases hh : sdepth lr y with
          | none => simp_all
          | some d =>
            rw [hh] at h
            simp only [Option.map_some] at h
            have e : d + 1 + 1 = m := Option.some_inj.mp h
            obtain ⟨hb, ha⟩ := rotR_lr xk pk ll lr r y d hgt hlt2 hh
            exact ⟨2 + d, ha, by omega⟩

-- Uniform +1 bound, left rotation (mirror).
theorem rotL_bound (xk pk : Nat) (l lr rr : STree) (y m : Nat)
    (hlt : pk < xk) (h : sdepth (.node pk l (.node xk lr rr)) y = some m) :
    ∃ m', sdepth (rotL (.node pk l (.node xk lr rr))) y = some m' ∧ m' ≤ m + 1 := by
  cases Decidable.em (y = pk) with
  | inl heq =>
    rw [heq] at h ⊢
    obtain ⟨hb, ha⟩ := rotL_down xk pk l lr rr hlt
    have hm : 0 = m := Option.some_inj.mp (hb ▸ h)
    exact ⟨1, ha, by omega⟩
  | inr hne =>
    cases Decidable.em (y = xk) with
    | inl heq2 =>
      rw [heq2] at h ⊢
      have hne_p : xk ≠ pk := by omega
      obtain ⟨hb, ha⟩ := rotL_up xk pk l lr rr hne_p hlt
      have hm : 1 = m := Option.some_inj.mp (hb ▸ h)
      exact ⟨0, ha, by omega⟩
    | inr hne2 =>
      cases Decidable.em (y < pk) with
      | inl hlt3 =>
        have h1 : y ≠ pk := by omega
        have h2 : y ≠ xk := by omega
        have hltx : y < xk := by omega
        have bpk : (y == pk) = false := by simpa [beq_iff_eq] using h1
        have bxk : (y == xk) = false := by simpa [beq_iff_eq] using h2
        simp only [sdepth, bpk, bxk, hltx, hlt3, ↓reduceIte] at h
        cases hh : sdepth l y with
        | none => simp_all
        | some d =>
          rw [hh] at h
          simp only [Option.map_some] at h
          have e : d + 1 = m := Option.some_inj.mp h
          obtain ⟨hb, ha⟩ := rotL_l xk pk l lr rr y d hlt3 hlt hh
          exact ⟨2 + d, ha, by omega⟩
      | inr hnp =>
        cases Decidable.em (y < xk) with
        | inl hgt =>
          have h1 : y ≠ pk := by omega
          have hlt2 : pk < y := by omega
          have bpk : (y == pk) = false := by simpa [beq_iff_eq] using h1
          have bxk : (y == xk) = false := by simpa [beq_iff_eq] using hne2
          simp only [sdepth, bpk, bxk, hnp, hgt, ↓reduceIte] at h
          cases hh : sdepth lr y with
          | none => simp_all
          | some d =>
            rw [hh] at h
            simp only [Option.map_some] at h
            have e : d + 1 + 1 = m := Option.some_inj.mp h
            obtain ⟨hb, ha⟩ := rotL_rl xk pk l lr rr y d hlt2 hgt hh
            exact ⟨2 + d, ha, by omega⟩
        | inr hnx =>
          have hgt2 : xk < y := by omega
          have h1 : y ≠ pk := by omega
          have h2 : y ≠ xk := by omega
          have hn2 : ¬ y < xk := by omega
          have bpk : (y == pk) = false := by simpa [beq_iff_eq] using h1
          have bxk : (y == xk) = false := by simpa [beq_iff_eq] using h2
          simp only [sdepth, bpk, bxk, hn2, hnp, ↓reduceIte] at h
          cases hh : sdepth rr y with
          | none => simp_all
          | some d =>
            rw [hh] at h
            simp only [Option.map_some] at h
            have e : d + 1 + 1 = m := Option.some_inj.mp h
            obtain ⟨hb, ha⟩ := rotL_rr xk pk l lr rr y d hgt2 hlt hh
            exact ⟨1 + d, ha, by omega⟩

-- Splay-StepEv bounds (C109): one StepEv is one zig (single rotation, +1) or
-- one double (two rotations, +2 by composing uniform bounds; second rotation
-- falls back to identity on shape mismatch, which can only help).
-- Splay-StepEv doubles LL/RR (C111): two rotations compose through the
-- intermediate existential depth (definitional unfolding links the middle
-- state). LR/RL act on a proper subtree first (need subtree framing:
-- region-split on y in psub/r/={g}), queued with that note. Loop-level
-- de-pathing/lift-accounting needs the splay-loop model, also queued.
theorem zigzigLL_bound (x p g : Nat) (a b c d : STree) (y m : Nat)
    (h1lt : x < p) (h2lt : p < g)
    (h : sdepth (.node g (.node p (.node x a b) c) d) y = some m) :
    ∃ m', sdepth (rotR (rotR (.node g (.node p (.node x a b) c) d))) y = some m'
      ∧ m' ≤ m + 2 := by
  obtain ⟨m1, hh1, hb1⟩ := rotR_bound p g (.node x a b) c d y m h2lt h
  have hh1' : sdepth (.node p (.node x a b) (.node g c d)) y = some m1 := hh1
  obtain ⟨m2, hh2, hb2⟩ := rotR_bound x p a b (.node g c d) y m1 h1lt hh1'
  have hfin : sdepth (rotR (rotR (.node g (.node p (.node x a b) c) d))) y
      = some m2 := hh2
  exact ⟨m2, hfin, by omega⟩

theorem zigzigRR_bound (x p g : Nat) (d c b a : STree) (y m : Nat)
    (h1lt : g < p) (h2lt : p < x)
    (h : sdepth (.node g d (.node p c (.node x b a))) y = some m) :
    ∃ m', sdepth (rotL (rotL (.node g d (.node p c (.node x b a))))) y = some m'
      ∧ m' ≤ m + 2 := by
  obtain ⟨m1, hh1, hb1⟩ := rotL_bound p g d c (.node x b a) y m h1lt h
  have hh1' : sdepth (.node p (.node g d c) (.node x b a)) y = some m1 := hh1
  obtain ⟨m2, hh2, hb2⟩ := rotL_bound x p (.node g d c) b a y m1 h2lt hh1'
  have hfin : sdepth (rotL (rotL (.node g d (.node p c (.node x b a))))) y
      = some m2 := hh2
  exact ⟨m2, hfin, by omega⟩

-- Queued (C112b): zigzag LR/RL doubles (subtree framing: invert via
-- rw [sdepth_node]-style one-level unfolding + by_cases on Prop conditions;
-- simp-normalization proved shape-unstable across nesting depths).
-- Splay-loop de-pathing/lift-accounting needs the loop model (SplayLoop.lean
-- skeleton exists: classifier + fuel driver + trace bound).

-- Splay progress, zig node-rise (C117): accessed key at depth 1 reaches root.
-- Doubles (LL/RR node 2->0) and LR/RL (subtree framing) queued; simp-shape
-- fragility documented in history (uniform simp normal forms vary with nesting
-- depth; prefer explicit rw/if_pos/if_neg chains for new cases).
theorem zigNodeR (xk pk : Nat) (ll lr r : STree)
    (hlt : xk < pk) :
    sdepth (.node pk (.node xk ll lr) r) xk = some 1 ∧
    sdepth (rotR (.node pk (.node xk ll lr) r)) xk = some 0 := by
  have hne : xk ≠ pk := by omega
  have bpk : (xk == pk) = false := by simpa [beq_iff_eq] using hne
  have bself : (xk == xk) = true := (beq_iff_eq).mpr rfl
  have nlt : ¬ xk < xk := by omega
  have er : rotR (.node pk (.node xk ll lr) r)
      = .node xk ll (.node pk lr r) := rfl
  simp only [sdepth, er, bpk, bself, hlt, nlt, Option.map_some,
    Bool.false_eq_true, ↓reduceIte]
  exact ⟨trivial, trivial⟩

-- BST range validity + rotation preservation (C113): half-open key intervals,
-- widening (range relaxation), rotR/rotL preserve validity. Grounds the
-- ordering hypotheses used throughout (caller proves BST once; comparisons
-- then locate keys soundly).
def bstR : STree → Nat → Nat → Prop
  | .leaf, _, _ => True
  | .node k l r, lo, hi => lo ≤ k ∧ k < hi ∧ bstR l lo k ∧ bstR r k hi

theorem bstR_widen (t : STree) (lo hi lo' hi' : Nat)
    (hlo : lo' ≤ lo) (hhi : hi ≤ hi') (h : bstR t lo hi) : bstR t lo' hi' := by
  induction t generalizing lo hi lo' hi' with
  | leaf => simp [bstR]
  | node k l r ihl ihr =>
    simp only [bstR] at h ⊢
    obtain ⟨h1, h2, h3, h4⟩ := h
    exact ⟨by omega, by omega, ihl _ _ _ _ hlo (by omega) h3,
      ihr _ _ _ _ (by omega) hhi h4⟩

theorem rotR_bst (xk pk : Nat) (ll lr r : STree) (lo hi : Nat)
    (hlt : xk < pk)
    (h : bstR (.node pk (.node xk ll lr) r) lo hi) :
    bstR (rotR (.node pk (.node xk ll lr) r)) lo hi := by
  simp only [bstR] at h
  obtain ⟨h1, h2, h3, h4⟩ := h
  obtain ⟨h5, h6, h7, h8⟩ := h3
  have e : rotR (.node pk (.node xk ll lr) r)
      = .node xk ll (.node pk lr r) := rfl
  rw [e]
  simp only [bstR]
  exact ⟨h5, by omega, h7, ⟨by omega, h2, h8, h4⟩⟩

-- Key membership + search correctness (C114): BST range soundness (present
-- keys lie in range) and findability (search finds present keys). Grounds
-- "comparisons locate keys" for the loop model (region membership from
-- comparisons + presence, no separate hypotheses needed at call sites).
def smem : STree → Nat → Prop
  | .leaf, _ => False
  | .node k l r, x => x = k ∨ smem l x ∨ smem r x

theorem bstR_mem_range (t : STree) (lo hi x : Nat)
    (h : bstR t lo hi) (hm : smem t x) : lo ≤ x ∧ x < hi := by
  induction t generalizing lo hi with
  | leaf => simp [smem] at hm
  | node k l r ihl ihr =>
    simp only [bstR] at h
    obtain ⟨h1, h2, h3, h4⟩ := h
    simp only [smem] at hm
    cases hm with
    | inl heq =>
      subst heq
      exact ⟨h1, h2⟩
    | inr hr =>
      cases hr with
      | inl hml =>
        obtain ⟨a, b⟩ := ihl _ _ h3 hml
        exact ⟨by omega, by omega⟩
      | inr hmr =>
        obtain ⟨a, b⟩ := ihr _ _ h4 hmr
        exact ⟨by omega, by omega⟩

theorem bstR_find (t : STree) (lo hi x : Nat)
    (h : bstR t lo hi) (hm : smem t x) : ∃ d, sdepth t x = some d := by
  induction t generalizing lo hi with
  | leaf => simp [smem] at hm
  | node k l r ihl ihr =>
    simp only [bstR] at h
    obtain ⟨h1, h2, h3, h4⟩ := h
    simp only [smem] at hm
    cases Decidable.em (x = k) with
    | inl heq =>
      rw [heq]
      exact ⟨0, sdepth_self k l r⟩
    | inr hne =>
      have b1 : (x == k) = false := by simpa [beq_iff_eq] using hne
      cases hm with
      | inl heq => exact absurd heq hne
      | inr hr =>
        cases hr with
        | inl hml =>
          have hlt : x < k := (bstR_mem_range _ _ _ _ h3 hml).2
          obtain ⟨d, hd⟩ := ihl _ _ h3 hml
          exact ⟨d + 1, by simp [sdepth, b1, hlt, hd, Option.map_some]⟩
        | inr hmr =>
          obtain ⟨a, _⟩ := bstR_mem_range _ _ _ _ h4 hmr
          have hnlt : ¬ x < k := by omega
          obtain ⟨d, hd⟩ := ihr _ _ h4 hmr
          exact ⟨d + 1, by simp [sdepth, b1, hnlt, hd, Option.map_some]⟩

theorem rotL_bst (xk pk : Nat) (l lr rr : STree) (lo hi : Nat)
    (hlt : pk < xk)
    (h : bstR (.node pk l (.node xk lr rr)) lo hi) :
    bstR (rotL (.node pk l (.node xk lr rr))) lo hi := by
  simp only [bstR] at h
  obtain ⟨h1, h2, h3, h4⟩ := h
  obtain ⟨h5, h6, h7, h8⟩ := h4
  have e : rotL (.node pk l (.node xk lr rr))
      = .node xk (.node pk l lr) rr := rfl
  rw [e]
  simp only [bstR]
  exact ⟨by omega, by omega, ⟨h1, hlt, h3, h7⟩, h8⟩
