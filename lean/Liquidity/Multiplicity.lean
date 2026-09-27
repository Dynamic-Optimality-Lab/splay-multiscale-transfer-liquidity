-- WP-2 STEP 63: LIQ0-02 Layer B — multiplicity algebra, machine-checked.
-- Covers the event-class map (ROOT 0 / ZIG 1 / doubles 2) and trace-sum composition.
-- Full splay-trace equality (sum = depth) is Layer A + differential evidence (ACT-10).
inductive EvClass where
  | root : EvClass
  | zig : EvClass
  | dbl : EvClass
deriving DecidableEq, Repr

def mu : EvClass → Nat
  | EvClass.root => 0
  | EvClass.zig => 1
  | EvClass.dbl => 2

def traceSum : List EvClass → Nat
  | [] => 0
  | e :: t => mu e + traceSum t

theorem mu_root : mu EvClass.root = 0 := rfl

theorem mu_zig : mu EvClass.zig = 1 := rfl

theorem evclass_exhaustion (e : EvClass) :
    e = EvClass.root ∨ e = EvClass.zig ∨ e = EvClass.dbl := by
  cases e with
  | root => simp
  | zig => simp
  | dbl => simp

theorem traceSum_append (r s : List EvClass) :
    traceSum (r ++ s) = traceSum r + traceSum s := by
  induction r with
  | nil => simp [traceSum]
  | cons e t ih => simp [traceSum, ih, Nat.add_assoc, Nat.add_comm (mu e), Nat.add_assoc]
