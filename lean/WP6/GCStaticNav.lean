-- WP-6 STEPS C137 (positional program): navigation + position-correct rewriting.
--
-- Self-contained (repo convention: no imports). Loop machinery, part 1:
-- search paths (`getPath`, root-to-node directions by comparison), subtree
-- rewriting at a path with CORRECT parent threading (`rewriteAtAux`: the
-- rotation par is always the true enclosing key, engine-faithful), its
-- shape-projection correspondence (`toSTree` after rewriting = STree plug
-- of the model rotation), link-preservation (`wf` through rewriting), and
-- BST-validity preservation through single pointer rotations (`pvalid`
-- through `protR/protL`, mirroring C131 with parent-ignoring bounds).
-- Key-set preservation through rewriting (for bounds at ancestors) queued
-- with the loop itself (C138).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

inductive SDir where
  | L : SDir
  | R : SDir
  deriving DecidableEq, Repr

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

-- STree plug at a path (C128 under-operators iterated).
def plugPath : List SDir → (STree → STree) → STree → STree
  | [], f, t => f t
  | .L :: p, f, .node k l r => .node k (plugPath p f l) r
  | .R :: p, f, .node k l r => .node k l (plugPath p f r)
  | _ :: _, _, .leaf => .leaf

inductive PTree where
  | leaf : PTree
  | node : Nat → PTree → PTree → Option Nat → PTree
  deriving DecidableEq, Repr

def toSTree : PTree → STree
  | .leaf => .leaf
  | .node k l r _ => .node k (toSTree l) (toSTree r)

def wf : PTree → Option Nat → Prop
  | .leaf, _ => True
  | .node k l r pk, par => pk = par ∧ wf l (some k) ∧ wf r (some k)

def reparent : Option Nat → PTree → PTree
  | _, .leaf => .leaf
  | par, .node k l r _ => .node k l r par

theorem reparent_toSTree (par : Option Nat) (u : PTree) :
    toSTree (reparent par u) = toSTree u := by
  cases u with
  | leaf => simp only [reparent, toSTree]
  | node k l r pk => simp only [reparent, toSTree]

def protR (par : Option Nat) : PTree → PTree
  | .node p (.node x ll lr _) r _ =>
    .node x ll (.node p (reparent (some p) lr) r (some x)) par
  | t => t

theorem protR_toSTree (par : Option Nat) (T : PTree) :
    toSTree (protR par T) = rotR (toSTree T) := by
  cases T with
  | leaf => simp only [protR, rotR, toSTree]
  | node p l r pk =>
    cases l with
    | leaf => simp only [protR, rotR, toSTree]
    | node x ll lr pkx => simp only [protR, rotR, toSTree, reparent_toSTree]

-- Search path root-to-key by comparison (engine `_depth_to` directions).
def getPath : PTree → Nat → List SDir
  | .leaf, _ => []
  | .node k l r _, x =>
    if (x == k) = true then []
    else if x < k then .L :: getPath l x
    else .R :: getPath r x

theorem getPath_root (k : Nat) (l r : PTree) (pk : Option Nat) :
    getPath (.node k l r pk) k = [] := by
  simp only [getPath]
  rw [if_pos ((beq_iff_eq).mpr rfl)]

theorem getPath_left (k : Nat) (l r : PTree) (pk : Option Nat) (x : Nat)
    (hne : x ≠ k) (hlt : x < k) :
    getPath (.node k l r pk) x = .L :: getPath l x := by
  simp only [getPath]
  have hbe : ¬((x == k) = true) := fun h => hne ((beq_iff_eq).mp h)
  rw [if_neg hbe, if_pos hlt]

theorem getPath_right (k : Nat) (l r : PTree) (pk : Option Nat) (x : Nat)
    (hne : x ≠ k) (hlt : k < x) :
    getPath (.node k l r pk) x = .R :: getPath r x := by
  simp only [getPath]
  have hbe : ¬((x == k) = true) := fun h => hne ((beq_iff_eq).mp h)
  have hltk : ¬ x < k := by omega
  rw [if_neg hbe, if_neg hltk]

-- Subtree rewriting at a path with CORRECT parent threading: the rotation
-- par is always the true enclosing key (engine-faithful rehang).
def rewriteAtAux (up : Option Nat) : List SDir → (Option Nat → PTree → PTree)
    → PTree → PTree
  | [], f, t => f up t
  | .L :: p, f, .node k l r par => .node k (rewriteAtAux (some k) p f l) r par
  | .R :: p, f, .node k l r par => .node k l (rewriteAtAux (some k) p f r) par
  | _ :: _, _, .leaf => .leaf

-- Single rotations preserve parent-link well-formedness (root case of
-- the rewrite induction; C133 cores restated for the loop).
theorem reparent_wf (u : PTree) (par old : Option Nat) (h : wf u old) :
    wf (reparent par u) par := by
  cases u with
  | leaf => exact True.intro
  | node k l r pk =>
    simp only [reparent, wf] at h ⊢
    obtain ⟨_, hl, hr⟩ := h
    exact ⟨True.intro, hl, hr⟩

theorem wf_protR_single (T : PTree) (par : Option Nat) (hv : wf T par) :
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

-- Rewriting projects to STree plugging (par-agnostic: projection forgets it).
theorem rewrite_toSTree (up : Option Nat) (path : List SDir) (T : PTree) :
    toSTree (rewriteAtAux up path protR T) =
    plugPath path rotR (toSTree T) := by
  induction path generalizing T up with
  | nil => simp only [rewriteAtAux, plugPath, protR_toSTree]
  | cons d p ih =>
    cases T with
    | leaf => simp only [rewriteAtAux, plugPath, toSTree]
    | node k l r pk =>
      cases d with
      | L => simp only [rewriteAtAux, plugPath, toSTree, ih]
      | R => simp only [rewriteAtAux, plugPath, toSTree, ih]

-- Link well-formedness survives position-correct rewriting.
theorem wf_rewrite (up : Option Nat) (path : List SDir) (T : PTree)
    (hv : wf T up) : wf (rewriteAtAux up path protR T) up := by
  induction path generalizing T up with
  | nil => simp only [rewriteAtAux]; exact wf_protR_single _ _ hv
  | cons d p ih =>
    cases T with
    | leaf => simp only [rewriteAtAux, wf]
    | node k l r pk =>
      simp only [rewriteAtAux, wf] at hv ⊢
      cases d with
      | L =>
        obtain ⟨hpk, hll, hrr⟩ := hv
        exact ⟨hpk, ih (some k) l hll, hrr⟩
      | R =>
        obtain ⟨hpk, hll, hrr⟩ := hv
        exact ⟨hpk, hll, ih (some k) r hrr⟩

def protL (par : Option Nat) : PTree → PTree
  | .node p l (.node x lr rr _) _ =>
    .node x (.node p l (reparent (some p) lr) (some x)) rr par
  | t => t

-- Pointer-side BST bounds and validity (parent fields ignored).
def pallLT : PTree → Nat → Prop
  | .leaf, _ => True
  | .node k l r _, b => k < b ∧ pallLT l b ∧ pallLT r b

def pallGT : PTree → Nat → Prop
  | .leaf, _ => True
  | .node k l r _, b => b < k ∧ pallGT l b ∧ pallGT r b

def pvalid : PTree → Prop
  | .leaf => True
  | .node k l r _ => pvalid l ∧ pvalid r ∧ pallLT l k ∧ pallGT r k

theorem pallLT_mono (t : PTree) (b c : Nat)
    (h : pallLT t b) (hle : b ≤ c) : pallLT t c := by
  induction t with
  | leaf => simp only [pallLT]
  | node k l r pk ihl ihr =>
    simp only [pallLT] at h ⊢
    obtain ⟨hk, hl, hr⟩ := h
    exact ⟨by omega, ihl hl, ihr hr⟩

theorem pallGT_mono (t : PTree) (b c : Nat)
    (h : pallGT t b) (hle : c ≤ b) : pallGT t c := by
  induction t with
  | leaf => simp only [pallGT]
  | node k l r pk ihl ihr =>
    simp only [pallGT] at h ⊢
    obtain ⟨hk, hl, hr⟩ := h
    exact ⟨by omega, ihl hl, ihr hr⟩

theorem pallLT_reparent (u : PTree) (par : Option Nat) (b : Nat) :
    pallLT (reparent par u) b ↔ pallLT u b := by
  cases u with
  | leaf => rfl
  | node k l r pk => simp only [reparent, pallLT]

theorem pallGT_reparent (u : PTree) (par : Option Nat) (b : Nat) :
    pallGT (reparent par u) b ↔ pallGT u b := by
  cases u with
  | leaf => rfl
  | node k l r pk => simp only [reparent, pallGT]

theorem pvalid_reparent (u : PTree) (par : Option Nat) :
    pvalid (reparent par u) ↔ pvalid u := by
  cases u with
  | leaf => rfl
  | node k l r pk => simp only [reparent, pvalid]

-- Single pointer rotations preserve BST validity (bounds juggling;
-- C131 cores at pointer level).
theorem pvalid_protR (T : PTree) (par : Option Nat) (hv : pvalid T) :
    pvalid (protR par T) := by
  cases T with
  | leaf => exact hv
  | node p l r pk =>
    cases l with
    | leaf => exact hv
    | node x ll lr pkx =>
      simp only [protR, pvalid, pallLT, pallGT, pvalid_reparent,
        pallLT_reparent, pallGT_reparent] at hv ⊢
      obtain ⟨⟨hll, hlr, hlt_ll_x, hgt_lr_x⟩, hr, ⟨hxp, hlt_ll_p, hlt_lr_p⟩,
        hgt_r_p⟩ := hv
      exact ⟨hll, ⟨hlr, hr, hlt_lr_p, hgt_r_p⟩, hlt_ll_x,
        ⟨hxp, hgt_lr_x, pallGT_mono r p x hgt_r_p (by omega)⟩⟩

theorem pvalid_protL (T : PTree) (par : Option Nat) (hv : pvalid T) :
    pvalid (protL par T) := by
  cases T with
  | leaf => exact hv
  | node p l r pk =>
    cases r with
    | leaf => exact hv
    | node x lr rr pkx =>
      simp only [protL, pvalid, pallLT, pallGT, pvalid_reparent,
        pallLT_reparent, pallGT_reparent] at hv ⊢
      obtain ⟨hl, ⟨hlr, hrr, hlt_lr_x, hgt_rr_x⟩, hlt_l_p,
        ⟨hxp, hgt_lr_p, hgt_rr_p⟩⟩ := hv
      exact ⟨⟨hl, hlr, hlt_l_p, hgt_lr_p⟩, hrr,
        ⟨hxp, pallLT_mono l p x hlt_l_p (by omega), hlt_lr_x⟩, hgt_rr_x⟩
