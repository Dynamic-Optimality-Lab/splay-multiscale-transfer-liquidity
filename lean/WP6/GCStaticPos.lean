-- WP-6 STEPS C128 (positional program): migration locality / sibling rigidity.
--
-- Imports the STree/sdepth model from SplayRotate (same shapes as
-- `python/liquidity/legacy_embedding.py` _rot_right/_rot_left). Result:
-- NO operation strictly inside one child subtree moves keys in the sibling
-- subtree (depths there are bit-identical). This bounds migration (8AC-MW:
-- keys move only via rotations on their own root path; W/co-location can only
-- change through on-path action). Rotation rows (8W) give the on-path shifts;
-- these give the off-path zeros. Together they are the full per-StepEv
-- displacement table the multi-session build needs.
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

-- Apply any operation strictly inside the left child (rotation or deeper
-- splay step that keeps the root key): root key and right child untouched.
def underL (f : STree → STree) : STree → STree
  | .node k l r => .node k (f l) r
  | t => t

-- Mirror: operate strictly inside the right child.
def underR (f : STree → STree) : STree → STree
  | .node k l r => .node k l (f r)
  | t => t

-- RIGHT-SIBLING RIGIDITY: action under the left child never moves keys in
-- the right subtree (search for y > k goes right regardless of left).
theorem rigid_R_underL (f : STree → STree) (k : Nat) (l r : STree) (y : Nat)
    (h : k < y) :
    sdepth (underL f (.node k l r)) y = sdepth (.node k l r) y := by
  have h1 : y ≠ k := by omega
  have h2 : ¬ y < k := by omega
  simp [sdepth, underL, beq_iff_eq, h1, h2]

-- LEFT-SIBLING RIGIDITY: action under the right child never moves keys in
-- the left subtree.
theorem rigid_L_underR (f : STree → STree) (k : Nat) (l r : STree) (y : Nat)
    (h : y < k) :
    sdepth (underR f (.node k l r)) y = sdepth (.node k l r) y := by
  have h1 : y ≠ k := by omega
  simp [sdepth, underR, beq_iff_eq, h1, h]

-- ROOT-KEY RIGIDITY: operating under either child keeps the root key at
-- depth 0 (splay steps that keep the root never move it).
theorem rigid_root_underL (f : STree → STree) (k : Nat) (l r : STree) :
    sdepth (underL f (.node k l r)) k = some 0 := by
  have h1 : (k == k) = true := (beq_iff_eq).mpr rfl
  simp [sdepth, underL, h1]

theorem rigid_root_underR (f : STree → STree) (k : Nat) (l r : STree) :
    sdepth (underR f (.node k l r)) k = some 0 := by
  have h1 : (k == k) = true := (beq_iff_eq).mpr rfl
  simp [sdepth, underR, h1]

-- ABSENT-KEY RIGIDITY: absent keys stay absent under either-side action
-- (no operation creates keys; none iff search misses everywhere).
theorem rigid_absent_underL (f : STree → STree) (k : Nat) (l r : STree) (y : Nat)
    (h : k < y) (hmiss : sdepth (.node k l r) y = none) :
    sdepth (underL f (.node k l r)) y = none := by
  rw [rigid_R_underL f k l r y h, hmiss]

theorem rigid_absent_underR (f : STree → STree) (k : Nat) (l r : STree) (y : Nat)
    (h : y < k) (hmiss : sdepth (.node k l r) y = none) :
    sdepth (underR f (.node k l r)) y = none := by
  rw [rigid_L_underR f k l r y h, hmiss]
