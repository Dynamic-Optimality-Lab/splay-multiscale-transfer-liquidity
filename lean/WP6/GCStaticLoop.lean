-- WP-6 STEPS C130 (positional program): structural splay skeleton + key safety.
--
-- Self-contained (repo convention: no imports). Faithful recursive splay
-- skeleton over STree (shapes mirror `python/liquidity/legacy_embedding.py`
-- splay_trace cases: zig at depth 1, zigzig/zagzag/zigzag doubles at depth 2
-- with conditional fixup after recursion, identity otherwise). All transformers
-- and fixups are total and non-recursive (clean equation lemmas); the skeleton
-- recurses on strict subtrees (termination free) with matches only on arguments
-- (splitter-friendly shape equations + functional induction with exact IHs).
-- Proved: every transformer and fixup preserves key membership; the skeleton
-- preserves membership (functional induction); root-hit is identity. Full root
-- delivery needs BST validity (queued C131: validity predicate + conditional
-- delivery + simulation relation with the pointer engine).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

-- Key membership (search-result presence, independent of shape/validity).
def mem : STree → Nat → Prop
  | .leaf, _ => False
  | .node k l r, y => y = k ∨ mem l y ∨ mem r y

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

def rotL : STree → STree
  | .node p l (.node x lr rr) => .node x (.node p l lr) rr
  | t => t

def zzR : STree → STree
  | .node g (.node p (.node x a b) c) d => .node x a (.node p b (.node g c d))
  | t => t

def zzL : STree → STree
  | .node g l (.node p c (.node x a b)) => .node x (.node p (.node g l c) a) b
  | t => t

def zagLR : STree → STree
  | .node g (.node p a (.node x b c)) d => .node x (.node p a b) (.node g c d)
  | t => t

def zagRL : STree → STree
  | .node g l (.node p (.node x a b) c) => .node x (.node g l a) (.node p b c)
  | t => t

-- All transformers preserve key membership (they only rehang subtrees).
theorem mem_rotR (T : STree) (y : Nat) : mem (rotR T) y ↔ mem T y := by
  cases T with
  | leaf => rfl
  | node p l r =>
    cases l with
    | leaf => rfl
    | node x ll lr => simp only [or_assoc, or_comm, or_left_comm, rotR, mem]

theorem mem_rotL (T : STree) (y : Nat) : mem (rotL T) y ↔ mem T y := by
  cases T with
  | leaf => rfl
  | node p l r =>
    cases r with
    | leaf => rfl
    | node x lr rr => simp only [or_assoc, or_comm, or_left_comm, rotL, mem]

theorem mem_zzR (T : STree) (y : Nat) : mem (zzR T) y ↔ mem T y := by
  cases T with
  | leaf => rfl
  | node g l r =>
    cases l with
    | leaf => rfl
    | node p ll lr =>
      cases ll with
      | leaf => rfl
      | node x a b => simp only [or_assoc, or_comm, or_left_comm, zzR, mem]

theorem mem_zzL (T : STree) (y : Nat) : mem (zzL T) y ↔ mem T y := by
  cases T with
  | leaf => rfl
  | node g l r =>
    cases r with
    | leaf => rfl
    | node p c rr =>
      cases rr with
      | leaf => rfl
      | node x a b => simp only [or_assoc, or_comm, or_left_comm, zzL, mem]

theorem mem_zagLR (T : STree) (y : Nat) : mem (zagLR T) y ↔ mem T y := by
  cases T with
  | leaf => rfl
  | node g l r =>
    cases l with
    | leaf => rfl
    | node p a lr =>
      cases lr with
      | leaf => rfl
      | node x b c => simp only [or_assoc, or_comm, or_left_comm, zagLR, mem]

theorem mem_zagRL (T : STree) (y : Nat) : mem (zagRL T) y ↔ mem T y := by
  cases T with
  | leaf => rfl
  | node g l r =>
    cases r with
    | leaf => rfl
    | node p rl rr =>
      cases rl with
      | leaf => rfl
      | node x a b => simp only [or_assoc, or_comm, or_left_comm, zagRL, mem]

-- Non-recursive fixup helpers (one per double case): apply the double exactly
-- when the recursion delivered x to the fixup point, else rebuild.
def fixLL (x k p : Nat) (ll' lr r : STree) : STree :=
  match ll' with
  | .node q _ _ =>
    if (x == q) = true then zzR (.node k (.node p ll' lr) r)
    else .node k (.node p ll' lr) r
  | .leaf => .node k (.node p ll' lr) r

def fixLR (x k p : Nat) (ll lr' r : STree) : STree :=
  match lr' with
  | .node q _ _ =>
    if (x == q) = true then zagLR (.node k (.node p ll lr') r)
    else .node k (.node p ll lr') r
  | .leaf => .node k (.node p ll lr') r

def fixRR (x k p : Nat) (l rl rr' : STree) : STree :=
  match rr' with
  | .node q _ _ =>
    if (x == q) = true then zzL (.node k l (.node p rl rr'))
    else .node k l (.node p rl rr')
  | .leaf => .node k l (.node p rl rr')

def fixRL (x k p : Nat) (l rl' rr : STree) : STree :=
  match rl' with
  | .node q _ _ =>
    if (x == q) = true then zagRL (.node k l (.node p rl' rr))
    else .node k l (.node p rl' rr)
  | .leaf => .node k l (.node p rl' rr)

-- Fixups preserve membership (transformer-or-rebuild).
theorem mem_fixLL (x k p : Nat) (ll' lr r : STree) (y : Nat) :
    mem (fixLL x k p ll' lr r) y ↔ mem (.node k (.node p ll' lr) r) y := by
  cases ll' with
  | leaf => rfl
  | node q a b =>
    simp only [fixLL]
    by_cases h : ((x == q) = true)
    · rw [if_pos h]; exact mem_zzR _ _
    · rw [if_neg h]

theorem mem_fixLR (x k p : Nat) (ll lr' r : STree) (y : Nat) :
    mem (fixLR x k p ll lr' r) y ↔ mem (.node k (.node p ll lr') r) y := by
  cases lr' with
  | leaf => rfl
  | node q a b =>
    simp only [fixLR]
    by_cases h : ((x == q) = true)
    · rw [if_pos h]; exact mem_zagLR _ _
    · rw [if_neg h]

theorem mem_fixRR (x k p : Nat) (l rl rr' : STree) (y : Nat) :
    mem (fixRR x k p l rl rr') y ↔ mem (.node k l (.node p rl rr')) y := by
  cases rr' with
  | leaf => rfl
  | node q a b =>
    simp only [fixRR]
    by_cases h : ((x == q) = true)
    · rw [if_pos h]; exact mem_zzL _ _
    · rw [if_neg h]

theorem mem_fixRL (x k p : Nat) (l rl' rr : STree) (y : Nat) :
    mem (fixRL x k p l rl' rr) y ↔ mem (.node k l (.node p rl' rr)) y := by
  cases rl' with
  | leaf => rfl
  | node q a b =>
    simp only [fixRL]
    by_cases h : ((x == q) = true)
    · rw [if_pos h]; exact mem_zagRL _ _
    · rw [if_neg h]

-- Faithful recursive splay skeleton: descend by key comparison; on the way up
-- apply the matching single/double fixup. Matches only on arguments (l, r);
-- recursion on strict subtrees (termination free). Splitter-friendly: one
-- equation per (l, r) shape combination + functional induction with exact IHs.
def splay (x : Nat) : STree → STree
  | .leaf => .leaf
  | .node k l r =>
    if (x == k) = true then .node k l r
    else if x < k then match l with
      | .leaf => .node k l r
      | .node p ll lr =>
        if (x == p) = true then rotR (.node k l r)
        else if x < p then fixLL x k p (splay x ll) lr r
        else fixLR x k p ll (splay x lr) r
    else match r with
      | .leaf => .node k l r
      | .node p rl rr =>
        if (x == p) = true then rotL (.node k l r)
        else if p < x then fixRR x k p l rl (splay x rr)
        else fixRL x k p l (splay x rl) rr

-- Root hit is identity (already splayed). Shape-split exposes the equation;
-- the root test resolves positively in every shape.
theorem splay_at_root (x : Nat) (l r : STree) :
    splay x (.node x l r) = .node x l r := by
  cases l <;> cases r <;> simp only [splay] <;>
    (by_cases h : ((x == x) = true)
     · rw [if_pos h]
     · exact absurd ((beq_iff_eq).mpr rfl) h)

-- The skeleton preserves key membership (functional induction: cases follow
-- the algorithm arms with IHs exactly at recursive calls; conditions rewrite
-- via case hypotheses; fixup/interface lemmas rewrite recursive occurrences,
-- transformer cores handle rehangs).
theorem mem_splay (x y : Nat) (t : STree) : mem (splay x t) y ↔ mem t y := by
  refine (splay.induct x (fun t => mem (splay x t) y ↔ mem t y) ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · simp only [splay]
  · intro a a_1 a_2 h
    cases a_1 <;> cases a_2 <;> simp only [splay] <;> rw [if_pos h]
  · intro a a_1 h1 h2
    cases a_1 <;> simp only [splay] <;> rw [if_neg h1, if_pos h2]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]; exact mem_rotR _ _)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4, mem_fixLL]
       simp only [mem]; rw [ih])
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4, mem_fixLR]
       simp only [mem]; rw [ih])
  · intro a a_1 h1 h2
    cases a_1 <;> simp only [splay] <;> rw [if_neg h1, if_neg h2]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]; exact mem_rotL _ _)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4, mem_fixRR]
       simp only [mem]; rw [ih])
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4, mem_fixRL]
       simp only [mem]; rw [ih])
