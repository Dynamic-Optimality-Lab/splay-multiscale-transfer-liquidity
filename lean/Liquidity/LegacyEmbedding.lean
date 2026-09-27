-- WP-1 STEP 22: LIQ0-01 Layer B — operator embedding + conservation, machine-checked.
-- Scope: T5 operator algebra over credit lists. Full-trace splay equality is Layer A+C.
inductive Credit where
  | latent : Credit
  | active : Credit
  | spent : Credit
deriving DecidableEq, Repr

def countE : List Credit → Nat
  | [] => 0
  | Credit.latent :: t => countE t + 1
  | Credit.active :: t => countE t + 1
  | Credit.spent :: t => 0 + countE t

def activateFirst : List Credit → List Credit
  | [] => []
  | Credit.latent :: t => Credit.active :: t
  | c :: t => c :: activateFirst t

theorem energy_conserved (L : List Credit) : countE (activateFirst L) = countE L := by
  induction L with
  | nil => rfl
  | cons h t ih =>
    cases h <;> simp [activateFirst, countE, ih]

def t5rho : Nat → List Credit → List Credit
  | 0, L => L
  | n + 1, L => t5rho n (activateFirst L)

theorem t5rho_one (L : List Credit) : t5rho 1 L = activateFirst L := rfl

theorem t5rho_energy (n : Nat) (L : List Credit) : countE (t5rho n L) = countE L := by
  induction n generalizing L with
  | zero => rfl
  | succ k ih => simp [t5rho, ih, energy_conserved]
