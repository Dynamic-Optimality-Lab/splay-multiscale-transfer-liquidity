-- WP-6 STEPS C162 (positional program): loop correspondence, engine counts.
--
-- Self-contained (repo convention: no imports). The engine loop emits one
-- StepEv per iteration (C135 `steps`: [.zig]/[.ll]/... per recursion level);
-- the skeleton counts one step per recursion level (C161 `ecount`). Both
-- mirror `splay`'s control exactly. Proved: step-trace length equals step
-- count (loop iterations = skeleton steps). Chain (all kernel):
--   C139 trace_length_eq: (emitTrace).length = (steps).length (engine iters);
--   C162 steps_length_eq: (steps).length = ecount (this file);
--   C161 ecount_eq: ecount = (d+1)/2 = ceil(d/2) from sdepth.
-- Hence engine counts satisfy e_B = ceil(d^B/2), e_A = ceil(d^A/2).
-- Corollaries (pure arithmetic, closing the 8AC-SYNCED/AROOT links):
-- e_B <= d^B (each StepEv consumes >= 1 path link), e_A >= d^A/2,
-- synced overflow bound (divergence forces A-trivial single step),
-- shallow single-finish (depth <= 2 finishes in <= 1 event).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

inductive SStep where
  | zig : SStep
  | ll : SStep
  | rr : SStep
  | lr : SStep
  | rl : SStep
  deriving DecidableEq, Repr

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

def ecount (x : Nat) : STree → Nat
  | .leaf => 0
  | .node k l r =>
    if (x == k) = true then 0
    else if x < k then match l with
      | .leaf => 0
      | .node p ll lr =>
        if (x == p) = true then 1
        else if x < p then ecount x ll + 1
        else ecount x lr + 1
    else match r with
      | .leaf => 0
      | .node p rl rr =>
        if (x == p) = true then 1
        else if p < x then ecount x rr + 1
        else ecount x rl + 1

-- LOOP CORRESPONDENCE: step-trace length equals step count (engine loop
-- iterations are skeleton steps; skeleton shape mirrors C139 exactly).
theorem steps_length_eq (x : Nat) (t : STree) :
    (steps x t).length = ecount x t := by
  refine (steps.induct x (fun t => (steps x t).length = ecount x t)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · simp [steps, ecount]
  · intro a a_1 a_2 h
    cases a_1 <;> cases a_2 <;>
      simp [steps, ecount, h]
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp [steps, ecount, h1, h2]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp [steps, ecount, h1, h2, h3]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [steps, ecount, h1, h2, h3, h4, ih]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [steps, ecount, h1, h2, h3, h4, ih]
  · intro a a_1 h1 h2
    cases a_1 <;>
      simp [steps, ecount, h1, h2]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3
    cases a_1 <;>
      simp [steps, ecount, h1, h2, h3]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [steps, ecount, h1, h2, h3, h4, ih]
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih
    cases a_1 <;>
      simp [steps, ecount, h1, h2, h3, h4, ih]

-- ENGINE-COUNT DEPTH LINKS: with e = (d+1)/2 (C161+C162), each StepEv
-- consumes >= 1 path link (e_B <= d^B); A-events cover half A-depth.
theorem eb_le_depth (d : Nat) : (d + 1) / 2 ≤ d := by omega

theorem ea_ge_half (d : Nat) : d / 2 ≤ (d + 1) / 2 := by omega

-- SYNCED OVERFLOW (8AC-SYNCED core): synced depths (d^B <= d^A + 2) force
-- overflow <= 1, and none when A is nontrivial (d^A >= 1).
theorem sync_overflow_le (dA dB : Nat) (hsync : dB ≤ dA + 2) :
    (dB + 1) / 2 ≤ 3 * ((dA + 1) / 2) + 1 := by omega

theorem sync_nondivergent (dA dB : Nat) (hsync : dB ≤ dA + 2)
    (hm : 1 ≤ (dA + 1) / 2) : (dB + 1) / 2 ≤ 3 * ((dA + 1) / 2) := by omega

-- SHALLOW SINGLE-FINISH (8AC-AROOT Lemma C): depth <= 2 finishes in <= 1
-- event, exactly 1 iff the depth is nontrivial.
theorem shallow_single (d : Nat) (h : d ≤ 2) : (d + 1) / 2 ≤ 1 := by omega

theorem shallow_exact (d : Nat) (h1 : 1 ≤ d) (h2 : d ≤ 2) :
    (d + 1) / 2 = 1 := by omega
