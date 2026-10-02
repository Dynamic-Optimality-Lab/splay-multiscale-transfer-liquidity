-- WP-6 STEPS C129 (positional program): one-double-step delivery + side dynamics.
--
-- Self-contained STree/sdepth model (repo convention: no imports; shapes mirror
-- `python/liquidity/legacy_embedding.py`). One double-step (zigzig/zagzag/
-- zigzag, the splay-loop bodies from SplayLoop `classify`) brings the accessed
-- key from depth 2 to the root (delivery), and root rotations preserve or
-- break search-side membership with the exact condition (co-location dynamics:
-- keys on the same side of the NEW root stay; keys between old and new root
-- switch sides — the migration 8AC-MW tracks via W). Off-path zeros are in
-- GCStaticPos (rigidity); on-path motion is here.
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

theorem sdepth_self (k : Nat) (l r : STree) :
    sdepth (.node k l r) k = some 0 := by
  unfold sdepth
  cases h : (k == k) with
  | true => rfl
  | false =>
    have t : (k == k) = true := (beq_iff_eq).mpr rfl
    rw [t] at h
    exact Bool.noConfusion h

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

def rotL : STree → STree
  | .node p l (.node x lr rr) => .node x (.node p l lr) rr
  | t => t

-- Double-step transformers (one splay-loop double iteration at the root).
-- LL zigzig: two right rotations (inner at p, then at g).
def zzR : STree → STree
  | .node g (.node p (.node x a b) c) d => .node x a (.node p b (.node g c d))
  | t => t

-- RR zagzag: two left rotations.
def zzL : STree → STree
  | .node g l (.node p c (.node x a b)) => .node x (.node p (.node g l c) a) b
  | t => t

-- LR zigzag: left rotation at p, then right rotation at g.
def zagLR : STree → STree
  | .node g (.node p a (.node x b c)) d => .node x (.node p a b) (.node g c d)
  | t => t

-- RL zigzag: right rotation at p, then left rotation at g.
def zagRL : STree → STree
  | .node g l (.node p (.node x a b) c) => .node x (.node g l a) (.node p b c)
  | t => t

-- DELIVERY: each double step brings x from depth 2 to the root (depth 0).
theorem zzR_deliver (x p g : Nat) (a b c d : STree)
    (h1 : x < p) (h2 : p < g) :
    sdepth (.node g (.node p (.node x a b) c) d) x = some 2 ∧
    sdepth (zzR (.node g (.node p (.node x a b) c) d)) x = some 0 := by
  have hxp : x ≠ p := by omega
  have hxg : x ≠ g := by omega
  have hxg2 : x < g := by omega
  simp [sdepth, zzR, beq_iff_eq, hxp, hxg, h1, hxg2, sdepth_self]

theorem zzL_deliver (x p g : Nat) (l c a b : STree)
    (h1 : g < p) (h2 : p < x) :
    sdepth (.node g l (.node p c (.node x a b))) x = some 2 ∧
    sdepth (zzL (.node g l (.node p c (.node x a b)))) x = some 0 := by
  have hxp : x ≠ p := by omega
  have hxg : x ≠ g := by omega
  have hgp : ¬ x < g := by omega
  have hpp : ¬ x < p := by omega
  simp [sdepth, zzL, beq_iff_eq, hxp, hxg, hgp, hpp, sdepth_self]

theorem zagLR_deliver (x p g : Nat) (a b c d : STree)
    (h1 : p < x) (h2 : x < g) :
    sdepth (.node g (.node p a (.node x b c)) d) x = some 2 ∧
    sdepth (zagLR (.node g (.node p a (.node x b c)) d)) x = some 0 := by
  have hxp : x ≠ p := by omega
  have hxg : x ≠ g := by omega
  have hpp : ¬ x < p := by omega
  simp [sdepth, zagLR, beq_iff_eq, hxp, hxg, hpp, h2, sdepth_self]

theorem zagRL_deliver (x p g : Nat) (l a b c : STree)
    (h1 : g < x) (h2 : x < p) :
    sdepth (.node g l (.node p (.node x a b) c)) x = some 2 ∧
    sdepth (zagRL (.node g l (.node p (.node x a b) c))) x = some 0 := by
  have hxp : x ≠ p := by omega
  have hxg : x ≠ g := by omega
  have hgp : ¬ x < g := by omega
  simp [sdepth, zagRL, beq_iff_eq, hxp, hxg, hgp, h2, sdepth_self]

-- Search-side membership at the root (co-location primitive: two keys are
-- co-located iff they go the same way at every ancestor; root side is step 1).
def goesL : STree → Nat → Prop
  | .node k _ _, y => y < k
  | .leaf, _ => False

def goesR : STree → Nat → Prop
  | .node k _ _, y => k < y
  | .leaf, _ => False

-- SIDE PRESERVATION: operating strictly under either child keeps the root
-- key, hence keeps every key's root side (co-location at the root survives
-- all off-path action; only root rotations can break it).
def underL (f : STree → STree) : STree → STree
  | .node k l r => .node k (f l) r
  | t => t

def underR (f : STree → STree) : STree → STree
  | .node k l r => .node k l (f r)
  | t => t

theorem sideL_under (f : STree → STree) (t : STree) (y : Nat) :
    goesL (underL f t) y ↔ goesL t y := by
  cases t with
  | leaf => rfl
  | node k l r => rfl

theorem sideR_under (f : STree → STree) (t : STree) (y : Nat) :
    goesR (underL f t) y ↔ goesR t y := by
  cases t with
  | leaf => rfl
  | node k l r => rfl

theorem sideL_underR (f : STree → STree) (t : STree) (y : Nat) :
    goesL (underR f t) y ↔ goesL t y := by
  cases t with
  | leaf => rfl
  | node k l r => rfl

theorem sideR_underR (f : STree → STree) (t : STree) (y : Nat) :
    goesR (underR f t) y ↔ goesR t y := by
  cases t with
  | leaf => rfl
  | node k l r => rfl

-- SIDE DYNAMICS at a root right rotation (root key p -> x, x < p):
-- keys below the new root stay left; keys between old and new root switch
-- from left to right (the co-location break 8AC-MW tracks).
theorem rotR_side_keep (p x : Nat) (ll lr r : STree) (y : Nat)
    (_hlt : x < p) (h : y < x) :
    goesL (.node p (.node x ll lr) r) y ∧
    goesL (rotR (.node p (.node x ll lr) r)) y := by
  have hp : y < p := by omega
  simp [goesL, rotR, hp, h]

theorem rotR_side_break (p x : Nat) (ll lr r : STree) (y : Nat)
    (h1 : x < y) (h2 : y < p) :
    goesL (.node p (.node x ll lr) r) y ∧
    goesR (rotR (.node p (.node x ll lr) r)) y := by
  simp [goesL, goesR, rotR, h1, h2]

-- Mirror at a root left rotation (root key p -> x, p < x).
theorem rotL_side_keep (p x : Nat) (l lr rr : STree) (y : Nat)
    (_hlt : p < x) (h : x < y) :
    goesR (.node p l (.node x lr rr)) y ∧
    goesR (rotL (.node p l (.node x lr rr))) y := by
  have hp : p < y := by omega
  simp [goesL, goesR, rotL, hp, h]

theorem rotL_side_break (p x : Nat) (l lr rr : STree) (y : Nat)
    (h1 : p < y) (h2 : y < x) :
    goesR (.node p l (.node x lr rr)) y ∧
    goesL (rotL (.node p l (.node x lr rr))) y := by
  simp [goesL, goesR, rotL, h1, h2]
