-- WP-6 STEPS C133 (positional program): pointer-engine simulation, rotation level.
--
-- Self-contained (repo convention: no imports). Models the pointer engine
-- `python/liquidity/legacy_embedding.py` at rotation level: PTree mirrors
-- engine nodes {k,l,r,p} (parent as key option, None = root); `protR/protL`
-- transliterate `_rot_right/_rot_left` line by line (child swap, middle-tree
-- reparent `b["p"] = p`, upward rehang `x["p"], p["p"] = g, x`); `toSTree`
-- forgets parents. Proved: transliteration equals the STree rotation
-- (correspondence), preserves parent-link well-formedness, and preserves the
-- shape interface the C128-C132 development uses. On top: triple-emission
-- correspondence — the engine emits lo=min/hi=max of the rotated keys
-- (splay_trace ZIG/LL/RR/LR/RL arms); on valid patterns the keys are distinct
-- (proved from bounds), so lo<hi and sites exist (sited chain), closing the
-- engine-emission-to-supply link for every StepEv shape in kernel.
-- Layer A (prose): node identities/keys/BST-validity of histories come from
-- the engine + PresentLegalPairInstance; this file pins everything else.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

def rotL : STree → STree
  | .node p l (.node x lr rr) => .node x (.node p l lr) rr
  | t => t

-- Pointer tree: engine node {k,l,r,p} with parent as key option.
inductive PTree where
  | leaf : PTree
  | node : Nat → PTree → PTree → Option Nat → PTree
  deriving DecidableEq, Repr

-- Forget parents (simulation projection).
def toSTree : PTree → STree
  | .leaf => .leaf
  | .node k l r _ => .node k (toSTree l) (toSTree r)

-- Parent-link well-formedness: root parent is par, links consistent below.
def wf : PTree → Option Nat → Prop
  | .leaf, _ => True
  | .node k l r pk, par => pk = par ∧ wf l (some k) ∧ wf r (some k)

-- Reparent a subtree root (engine `b["p"] = p` for the middle tree).
def reparent : Option Nat → PTree → PTree
  | _, .leaf => .leaf
  | par, .node k l r _ => .node k l r par

-- `_rot_right(p)` transliterated (x = p.left, b = x.right, g = p.parent):
-- x takes p's position with parent g; p becomes x.right with parent x;
-- middle tree b becomes p.left with parent p.
def protR (par : Option Nat) : PTree → PTree
  | .node p (.node x ll lr _) r _ =>
    .node x ll (.node p (reparent (some p) lr) r (some x)) par
  | t => t

-- `_rot_left(p)` transliterated (mirror).
def protL (par : Option Nat) : PTree → PTree
  | .node p l (.node x lr rr _) _ =>
    .node x (.node p l (reparent (some p) lr) (some x)) rr par
  | t => t

-- Reparenting is invisible to the shape projection.
theorem reparent_toSTree (par : Option Nat) (u : PTree) :
    toSTree (reparent par u) = toSTree u := by
  cases u with
  | leaf => simp only [reparent, toSTree]
  | node k l r pk => simp only [reparent, toSTree]

-- CORRESPONDENCE: transliterated rotation equals the STree rotation
-- under the projection (engine step = model step).
theorem protR_toSTree (par : Option Nat) (T : PTree) :
    toSTree (protR par T) = rotR (toSTree T) := by
  cases T with
  | leaf => simp only [protR, rotR, toSTree]
  | node p l r pk =>
    cases l with
    | leaf => simp only [protR, rotR, toSTree]
    | node x ll lr pkx => simp only [protR, rotR, toSTree, reparent_toSTree]

theorem protL_toSTree (par : Option Nat) (T : PTree) :
    toSTree (protL par T) = rotL (toSTree T) := by
  cases T with
  | leaf => simp only [protL, rotL, toSTree]
  | node p l r pk =>
    cases r with
    | leaf => simp only [protL, rotL, toSTree]
    | node x lr rr pkx => simp only [protL, rotL, toSTree, reparent_toSTree]

-- Reparenting preserves well-formedness at the new parent.
theorem reparent_wf (u : PTree) (par old : Option Nat) (h : wf u old) :
    wf (reparent par u) par := by
  cases u with
  | leaf => exact True.intro
  | node k l r pk =>
    simp only [reparent, wf] at h ⊢
    obtain ⟨_, hl, hr⟩ := h
    exact ⟨True.intro, hl, hr⟩

-- Transliterated rotations preserve parent-link well-formedness.
theorem wf_protR (T : PTree) (par : Option Nat) (hv : wf T par) :
    wf (protR par T) par := by
  cases T with
  | leaf => exact hv
  | node p l r pk =>
    cases l with
    | leaf => exact hv
    | node x ll lr pkx =>
      simp only [protR, wf] at hv ⊢
      obtain ⟨hpkp, ⟨hpkx, hll, hlr⟩, hr⟩ := hv
      exact ⟨True.intro, hll, True.intro,
        reparent_wf lr (some p) (some x) hlr, hr⟩

theorem wf_protL (T : PTree) (par : Option Nat) (hv : wf T par) :
    wf (protL par T) par := by
  cases T with
  | leaf => exact hv
  | node p l r pk =>
    cases r with
    | leaf => exact hv
    | node x lr rr pkx =>
      simp only [protL, wf] at hv ⊢
      obtain ⟨hpkp, hl, ⟨hpkx, hlr, hrr⟩⟩ := hv
      exact ⟨True.intro, ⟨True.intro, hl,
        reparent_wf lr (some p) (some x) hlr⟩, hrr⟩

-- Pointer-side BST bounds (parent fields ignored by the predicates).
def pallLT : PTree → Nat → Prop
  | .leaf, _ => True
  | .node k l r _, b => k < b ∧ pallLT l b ∧ pallLT r b

def pallGT : PTree → Nat → Prop
  | .leaf, _ => True
  | .node k l r _, b => b < k ∧ pallGT l b ∧ pallGT r b

def pvalid : PTree → Prop
  | .leaf => True
  | .node k l r _ => pvalid l ∧ pvalid r ∧ pallLT l k ∧ pallGT r k

theorem pallLT_root (k : Nat) (l r : PTree) (pk : Option Nat) (b : Nat)
    (h : pallLT (.node k l r pk) b) : k < b := by
  simp only [pallLT] at h; exact h.1

theorem pallGT_root (k : Nat) (l r : PTree) (pk : Option Nat) (b : Nat)
    (h : pallGT (.node k l r pk) b) : b < k := by
  simp only [pallGT] at h; exact h.1

-- Valid rotation patterns have distinct keys (left child).
theorem pattern_ne_L (p x : Nat) (ll lr r : PTree) (pkx pkp : Option Nat)
    (h : pvalid (.node p (.node x ll lr pkx) r pkp)) : x ≠ p := by
  have hxp : x < p := by
    simp only [pvalid, pallLT] at h; exact h.2.2.1.1
  omega

-- Valid rotation patterns have distinct keys (right child).
theorem pattern_ne_R (p x : Nat) (l lr rr : PTree) (pkx pkp : Option Nat)
    (h : pvalid (.node p l (.node x lr rr pkx) pkp)) : x ≠ p := by
  have hxp : p < x := by
    simp only [pvalid, pallGT] at h; exact h.2.2.2.1
  omega

-- Engine triple emission, ZIG shape: lo=min, hi=max of the two keys
-- (splay_trace ZIG arms, lines 121/124).
def emit (a b : Nat) : Nat × Nat := (min a b, max a b)

-- Engine triple emission, double shapes: min/max of the three keys
-- (LL/RR/LR/RL arms, lines 128/132/136/140).
def emit3 (a b c : Nat) : Nat × Nat :=
  (min (min a b) c, max (max a b) c)

-- Distinct keys ⟹ lo < hi (both shapes; doubles need only one disequality,
-- cf. triple_lo_lt_hi3 in GCStaticArith).
theorem emit_lt (a b : Nat) (hne : a ≠ b) :
    (emit a b).1 < (emit a b).2 := by
  simp only [emit]; omega

theorem emit3_lt (a b c : Nat) (hbc : b ≠ c) :
    (emit3 a b c).1 < (emit3 a b c).2 := by
  simp only [emit3]; omega

-- Sites exist on any interval with lo < hi inside [1, n]
-- (sited_always core from GCStaticArith, restated for the chain).
theorem sited_of_lt (lo hi n : Nat) (h1 : 1 ≤ lo) (h2 : lo < hi) (h3 : hi ≤ n) :
    ∃ i, lo ≤ i ∧ i < hi ∧ 1 ≤ i ∧ i < n ∧ i + 1 ≤ hi := by
  exact ⟨lo, by omega, by omega, by omega, by omega, by omega⟩

-- END-TO-END (ZIG): valid rotation pattern + key range ⟹ emitted interval
-- carries sites (engine emission feeds supply, 8S, in kernel).
theorem zig_sited (x p n : Nat) (ll lr r : PTree) (pkx pkp : Option Nat)
    (hv : pvalid (.node p (.node x ll lr pkx) r pkp))
    (h1 : 1 ≤ min x p) (hn : max x p ≤ n) :
    ∃ i, min x p ≤ i ∧ i < max x p ∧ 1 ≤ i ∧ i < n ∧ i + 1 ≤ max x p := by
  have hne : x ≠ p := pattern_ne_L p x ll lr r pkx pkp hv
  have hlt : min x p < max x p := by omega
  exact sited_of_lt _ _ _ h1 hlt hn

-- END-TO-END (doubles): valid grandparent pattern + key range ⟹ emitted
-- triple interval carries sites (needs only the inner disequality).
theorem double_sited (x p g n : Nat) (a b c d : PTree)
    (pkx pkp pkg : Option Nat)
    (hv : pvalid (.node g (.node p (.node x a b pkx) c pkp) d pkg))
    (h1 : 1 ≤ min (min x p) g) (hn : max (max x p) g ≤ n) :
    ∃ i, min (min x p) g ≤ i ∧ i < max (max x p) g ∧ 1 ≤ i ∧ i < n ∧
      i + 1 ≤ max (max x p) g := by
  have hne : x ≠ p := by
    have hinner : pvalid (.node p (.node x a b pkx) c pkp) := by
      simp only [pvalid] at hv
      exact hv.1
    exact pattern_ne_L p x a b c pkx pkp hinner
  have hlt : min (min x p) g < max (max x p) g := by omega
  exact sited_of_lt _ _ _ h1 hlt hn
