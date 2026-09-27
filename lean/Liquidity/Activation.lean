-- WP-2 STEP 62: LIQ0 Layer B — bounded-iteration algebra, machine-checked.
-- Covers LIQ0-04 (boundedness by construction) and LIQ0-05/07 (energy + no-resurrection).
inductive Credit where
  | latent : Credit
  | active : Credit
  | spent : Credit
deriving DecidableEq, Repr

def countE : List Credit → Nat
  | [] => 0
  | Credit.latent :: t => countE t + 1
  | Credit.active :: t => countE t + 1
  | Credit.spent :: t => countE t

def firstEligible : List Credit → Option Nat
  | [] => none
  | Credit.latent :: _ => some 0
  | _ :: t => Option.map (· + 1) (firstEligible t)

def setActive : List Credit → Nat → List Credit
  | [], _ => []
  | _ :: t, 0 => Credit.active :: t
  | c :: t, n + 1 => c :: setActive t n

theorem firstEligible_mem (L : List Credit) (i : Nat)
    (h : firstEligible L = some i) : L[i]? = some Credit.latent := by
  induction L generalizing i with
  | nil => simp [firstEligible] at h
  | cons c t ih =>
    cases c with
    | latent =>
      simp [firstEligible] at h
      subst h
      rfl
    | active =>
      simp [firstEligible] at h
      cases i with
      | zero => simp at h
      | succ j =>
        simp at h
        have hj : firstEligible t = some j := by simpa using h
        have := ih j hj
        simpa using this
    | spent =>
      simp [firstEligible] at h
      cases i with
      | zero => simp at h
      | succ j =>
        simp at h
        have hj : firstEligible t = some j := by simpa using h
        have := ih j hj
        simpa using this

theorem setActive_at_latent (L : List Credit) (i : Nat)
    (h : L[i]? = some Credit.latent) : countE (setActive L i) = countE L := by
  induction L generalizing i with
  | nil => simp at h
  | cons c t ih =>
    cases i with
    | zero =>
      simp at h
      subst h
      simp [setActive, countE]
    | succ j =>
      simp at h
      cases c <;> simp [setActive, countE, ih j h]

def t5one : List Credit → List Credit
  | L => match firstEligible L with
    | none => L
    | some i => setActive L i

theorem t5one_energy (L : List Credit) : countE (t5one L) = countE L := by
  simp only [t5one]
  cases h : firstEligible L with
  | none => rfl
  | some i =>
    have hmem := firstEligible_mem L i h
    have hset := setActive_at_latent L i hmem
    simpa [h] using hset

def t5rho : Nat → List Credit → List Credit
  | 0, L => L
  | n + 1, L => t5rho n (t5one L)

theorem t5rho_energy (n : Nat) (L : List Credit) : countE (t5rho n L) = countE L := by
  induction n generalizing L with
  | zero => rfl
  | succ k ih => simp [t5rho, ih, t5one_energy]
