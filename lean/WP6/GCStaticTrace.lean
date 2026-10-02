-- WP-6 STEPS C135 (positional program): trace induction, skeleton side.
--
-- Self-contained (repo convention: no imports). Trace-level simulation,
-- skeleton side: `steps` emits one SStep per recursion level of `splay`,
-- bottom-up (mirroring the engine's one-event-per-iteration emission in
-- splay_trace). Proved: root access emits nothing (both models idle at
-- the root — engine loop-exit agreement); splay acts iff steps emits
-- (no-op agreement: steps x t = [] → splay x t = t); trace length fits
-- tree size (length (steps x t) ≤ tsize t, bounding engine iterations on
-- present keys by structure). Engine-side event accounting (triples to
-- Aev supply) queued.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

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

-- Trace emission: one step per recursion level, bottom-up (engine order).
def steps (x : Nat) : STree → List SStep
  | .leaf => []
  | .node k l r =>
    if (x == k) = true then []
    else if x < k then match l with
      | .leaf => []
      | .node p ll lr =>
        if (x == p) = true then [.zig]
        else if x < p then steps x ll ++ [.ll]
        else steps x lr ++ [.lr]
    else match r with
      | .leaf => []
      | .node p rl rr =>
        if (x == p) = true then [.zig]
        else if p < x then steps x rr ++ [.rr]
        else steps x rl ++ [.rl]

def tsize : STree → Nat
  | .leaf => 0
  | .node _ l r => 1 + tsize l + tsize r

-- Root access emits nothing (engine loop-exit agreement: node without
-- parent takes zero iterations).
theorem steps_nil_root (x : Nat) (l r : STree) : steps x (.node x l r) = [] := by
  cases l <;> cases r <;> simp only [steps] <;>
    (by_cases h : ((x == x) = true)
     · rw [if_pos h]
     · exact absurd ((beq_iff_eq).mpr rfl) h)

-- NO-OP AGREEMENT: splay acts iff steps emits (both models idle together).
theorem splay_noop (x : Nat) (t : STree) (h : steps x t = []) :
    splay x t = t := by
  induction t with
  | leaf => rfl
  | node k l r =>
    cases l with
    | leaf =>
      cases r with
      | leaf =>
        simp only [steps] at h; simp only [splay]
        by_cases h1 : ((x == k) = true)
        · rw [if_pos h1] at h ⊢
        · rw [if_neg h1] at h ⊢
          by_cases h2 : x < k
          · rw [if_pos h2] at h ⊢
          · rw [if_neg h2] at h ⊢
      | node q rl rr =>
        simp only [steps] at h; simp only [splay]
        by_cases h1 : ((x == k) = true)
        · rw [if_pos h1] at h ⊢
        · rw [if_neg h1] at h ⊢
          by_cases h2 : x < k
          · rw [if_pos h2] at h ⊢
          · rw [if_neg h2] at h ⊢
            by_cases h3 : ((x == q) = true)
            · rw [if_pos h3] at h ⊢; simp at h
            · rw [if_neg h3] at h ⊢
              by_cases h4 : q < x
              · rw [if_pos h4] at h ⊢; simp at h
              · rw [if_neg h4] at h ⊢; simp at h
    | node p ll lr =>
      cases r with
      | leaf =>
        simp only [steps] at h; simp only [splay]
        by_cases h1 : ((x == k) = true)
        · rw [if_pos h1] at h ⊢
        · rw [if_neg h1] at h ⊢
          by_cases h2 : x < k
          · rw [if_pos h2] at h ⊢
            by_cases h3 : ((x == p) = true)
            · rw [if_pos h3] at h ⊢; simp at h
            · rw [if_neg h3] at h ⊢
              by_cases h4 : x < p
              · rw [if_pos h4] at h ⊢; simp at h
              · rw [if_neg h4] at h ⊢; simp at h
          · rw [if_neg h2] at h ⊢
      | node q rl rr =>
        simp only [steps] at h; simp only [splay]
        by_cases h1 : ((x == k) = true)
        · rw [if_pos h1] at h ⊢
        · rw [if_neg h1] at h ⊢
          by_cases h2 : x < k
          · rw [if_pos h2] at h ⊢
            by_cases h3 : ((x == p) = true)
            · rw [if_pos h3] at h ⊢; simp at h
            · rw [if_neg h3] at h ⊢
              by_cases h4 : x < p
              · rw [if_pos h4] at h ⊢; simp at h
              · rw [if_neg h4] at h ⊢; simp at h
          · rw [if_neg h2] at h ⊢
            by_cases h3 : ((x == q) = true)
            · rw [if_pos h3] at h ⊢; simp at h
            · rw [if_neg h3] at h ⊢
              by_cases h4 : q < x
              · rw [if_pos h4] at h ⊢; simp at h
              · rw [if_neg h4] at h ⊢; simp at h

-- TRACE LENGTH BOUND: emitted steps fit tree size (engine iterations on
-- present keys bounded by structure, one step per level).
theorem steps_length (x : Nat) (t : STree) :
    (steps x t).length ≤ tsize t := by
  refine (steps.induct x (fun t => (steps x t).length ≤ tsize t)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · simp only [steps, tsize, List.length]; omega
  · intro a a_1 a_2 h
    cases a_1 <;> cases a_2 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      rw [if_pos h] <;> simp only [List.length] <;> omega
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4]; simp only [List.length, List.length_append]; omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp only [steps, tsize, List.length, List.length_append] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4]; simp only [List.length, List.length_append]; omega)

