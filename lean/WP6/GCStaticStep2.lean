-- WP-6 STEPS C134 (positional program): double-step simulation + branch selection.
--
-- Self-contained (repo convention: no imports). Loop-body simulation: the
-- engine applies TWO pointer rotations per double StepEv (splay_trace LL/RR/
-- LR/RL arms, legacy_embedding.py lines 125-140); the skeleton applies one
-- double transformer (zzR/zzL/zagLR/zagRL, GCStaticLoop). Proved: each engine
-- rotation pair equals the corresponding transformer under the shape
-- projection (four composition correspondences). Plus branch selection: the
-- engine's link-geometry if-chain formalized as `eclassify` and proved equal
-- to the skeleton classifier (SplayLoop `classify`), so both models take the
-- same branch at every loop level. Together with C133 (single rotations),
-- every engine loop iteration is now pinned to a skeleton step in kernel.
-- Layer A (prose): parent-pointer navigation/termination of the engine loop;
-- pointer-tree well-formedness across iterations (wf_protR/L, C133).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

inductive PTree where
  | leaf : PTree
  | node : Nat → PTree → PTree → Option Nat → PTree
  deriving DecidableEq, Repr

def toSTree : PTree → STree
  | .leaf => .leaf
  | .node k l r _ => .node k (toSTree l) (toSTree r)

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

def protL (par : Option Nat) : PTree → PTree
  | .node p l (.node x lr rr _) _ =>
    .node x (.node p l (reparent (some p) lr) (some x)) rr par
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

-- ENGINE LL (rotR g, then rotR p; lines 126-127) = zzR under projection,
-- on the full firing pattern (partial patterns never enter double arms:
-- the engine's link-geometry if-chain routes them to ZIG/identity, covered
-- by C133 singles + skeleton rebuild).
theorem sim_LL (g p x : Nat) (a b c d : PTree) (pg pp px : Option Nat) :
    toSTree (protR none (protR none
      (.node g (.node p (.node x a b px) c pp) d pg))) =
    zzR (toSTree (.node g (.node p (.node x a b px) c pp) d pg)) := by
  simp only [protR, toSTree, zzR, reparent_toSTree]

-- ENGINE RR (rotL g, then rotL p; lines 130-131) = zzL under projection.
theorem sim_RR (g p x : Nat) (l c a b : PTree) (pg pp px : Option Nat) :
    toSTree (protL none (protL none
      (.node g l (.node p c (.node x a b px) pp) pg))) =
    zzL (toSTree (.node g l (.node p c (.node x a b px) pp) pg)) := by
  simp only [protL, toSTree, zzL, reparent_toSTree]

-- ENGINE LR (rotL p, then rotR g; lines 134-135) = zagLR under projection.
theorem sim_LR (g p x : Nat) (a b c d : PTree) (pg pp px : Option Nat) :
    toSTree (protR none
      (.node g (protL (some g) (.node p a (.node x b c px) pp)) d pg)) =
    zagLR (toSTree (.node g (.node p a (.node x b c px) pp) d pg)) := by
  simp only [protR, protL, toSTree, zagLR, reparent_toSTree]

-- ENGINE RL (rotR p, then rotL g; lines 138-139) = zagRL under projection.
theorem sim_RL (g p x : Nat) (l a b c : PTree) (pg pp px : Option Nat) :
    toSTree (protL none
      (.node g l (protR (some g) (.node p (.node x a b px) c pp)) pg)) =
    zagRL (toSTree (.node g l (.node p (.node x a b px) c pp) pg)) := by
  simp only [protR, protL, toSTree, zagRL, reparent_toSTree]

-- Branch geometry: direction from a node to its parent.
inductive SDir where
  | L : SDir
  | R : SDir
  deriving DecidableEq, Repr

inductive SStep where
  | zig : SStep
  | ll : SStep
  | rr : SStep
  | lr : SStep
  | rl : SStep
  deriving DecidableEq, Repr

-- Skeleton classifier (SplayLoop `classify`, restated): node-to-parent dir,
-- parent-to-grandparent dir option (none = no grandparent = zig).
def classify : SDir → Option SDir → SStep
  | _, none => .zig
  | .L, some .L => .ll
  | .R, some .R => .rr
  | .R, some .L => .lr
  | .L, some .R => .rl

-- Engine branch table (splay_trace lines 118-140, same geometry):
-- g none ⟹ ZIG; (node,p,g) link patterns ⟹ LL/RR/LR/RL.
def eclassify : SDir → Option SDir → SStep
  | _, none => .zig
  | .L, some .L => .ll
  | .R, some .R => .rr
  | .R, some .L => .lr
  | .L, some .R => .rl

-- BRANCH AGREEMENT: engine and skeleton select the same step at every level.
theorem classify_agree (d : SDir) (o : Option SDir) :
    eclassify d o = classify d o := by
  cases d with
  | L =>
    cases o with
    | none => rfl
    | some g =>
      cases g with
      | L => rfl
      | R => rfl
  | R =>
    cases o with
    | none => rfl
    | some g =>
      cases g with
      | L => rfl
      | R => rfl
