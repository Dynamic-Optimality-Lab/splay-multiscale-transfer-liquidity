-- WP-2 STEP 64: preservation Layer B — support list invariance, machine-checked.
-- Covers LIQ0-06/07 at operator level (type-field-only mutation, LATENT-gated).
inductive CType where
  | latent : CType
  | active : CType
  | spent : CType
deriving DecidableEq, Repr

structure Cred where
  ty : CType
  sup : Nat
deriving DecidableEq, Repr

def supports : List Cred → List Nat
  | [] => []
  | c :: t => c.sup :: supports t

def activateFirst : List Cred → List Cred
  | [] => []
  | ⟨CType.latent, s⟩ :: t => ⟨CType.active, s⟩ :: t
  | c :: t => c :: activateFirst t

theorem supports_preserved (L : List Cred) : supports (activateFirst L) = supports L := by
  induction L with
  | nil => rfl
  | cons c t ih =>
    obtain ⟨ty, sup⟩ := c
    cases ty with
    | latent => simp [activateFirst, supports]
    | active => simp [activateFirst, supports, ih]
    | spent => simp [activateFirst, supports, ih]

def countSpent : List Cred → Nat
  | [] => 0
  | ⟨CType.spent, _⟩ :: t => countSpent t + 1
  | _ :: t => countSpent t

theorem spent_never_decreases_aux (L : List Cred) :
    countSpent (activateFirst L) = countSpent L := by
  induction L with
  | nil => rfl
  | cons c t ih =>
    obtain ⟨ty, sup⟩ := c
    cases ty with
    | latent => simp [activateFirst, countSpent]
    | active => simp [activateFirst, countSpent, ih]
    | spent => simp [activateFirst, countSpent, ih]
