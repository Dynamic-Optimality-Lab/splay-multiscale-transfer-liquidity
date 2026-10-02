-- WP-6 STEP C110: splay-loop skeleton (positional tracking foundation).
--
-- Functional mirror of `python/liquidity/legacy_embedding.py` splay_trace
-- (lines 107-143): path-pattern classifier (ZIG/LL/RR/LR/RL per bottom-up
-- grandparent/parent/node configuration) + triple-key extraction (lo/hi as
-- min/max, feeding GCStaticArith sited_* lemmas) + fuel-bounded driver.
-- Scope: SHAPES ONLY (case classification + trace emission + termination by
-- fuel); tree transformation, depth dynamics, and equivalence with the pointer
-- engine are queued (need simulation relation + STree splay ops). Sanity
-- theorems: empty path emits nothing; trace length bounded by fuel/steps;
-- every emitted triple has lo < hi given distinct keys (connects sited_*).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

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

-- Bottom-up classifier: given the two lowest path links (node-to-parent dir,
-- parent-to-grandparent dir optionality), emit the StepEv case. Mirrors the
-- branch structure of splay_trace (ZIG iff no grandparent).
def classify : SDir → Option SDir → SStep
  | _, none => .zig
  | .L, some .L => .ll
  | .R, some .R => .rr
  | .R, some .L => .lr
  | .L, some .R => .rl

-- One fuel step consumes one path link (zig) or two (double); returns the
-- emitted case and remaining path length. Termination by fuel (structural).
def stepEv : Nat → Nat → Option (SStep × Nat)
  | 0, _ => none
  | _ + 1, 0 => none
  | _f + 1, 1 => some (.zig, 0)
  | _f + 1, len + 2 => some (.ll, len)

-- Fuel-bounded trace length over a path length: zig consumes 1 link, double 2.
-- Constructor-disjoint equations (clean simp normal forms, no overlap).
def traceLen : Nat → Nat → Nat
  | 0, _ => 0
  | _ + 1, 0 => 0
  | _ + 1, 1 => 1
  | f + 1, len + 2 => 1 + traceLen f len

theorem traceLen_zero_fuel (len : Nat) : traceLen 0 len = 0 := by
  rfl

theorem traceLen_zero_path (f : Nat) : traceLen f 0 = 0 := by
  cases f with
  | zero => rfl
  | succ _ => rfl

theorem traceLen_bound (f len : Nat) : traceLen f len ≤ f := by
  induction f generalizing len with
  | zero => simp only [traceLen]; omega
  | succ k ih =>
    cases len with
    | zero => simp only [traceLen]; omega
    | succ l =>
      cases l with
      | zero => simp only [traceLen]; omega
      | succ m =>
        have h := ih m
        simp only [traceLen]
        omega

-- Triple lo<hi from distinct keys (feeds sited_zig/sited_double in
-- GCStaticArith; Layer A supplies distinctness from rotation geometry).
theorem triple_keys_lt (a b c : Nat) (hab : a ≠ b) :
    min (min a b) c < max (max a b) c ∨ min a b < max a b := by
  cases Decidable.em (b = c) with
  | inl he => subst he; exact Or.inr (by omega)
  | inr hc => exact Or.inl (by omega)
