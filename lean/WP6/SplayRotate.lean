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
