-- WP-6 STEPS C165 (positional program): history ledger, twin case + windows.
--
-- Self-contained (repo convention: no imports). A history is a list of
-- accesses (KEEP? : Bool, key). Both trees evolve by the splay skeleton
-- (KEEP: both trees; DELETE: A only — twin-symmetry breaking); per-access
-- counts come from `ecount` (C161: one step per recursion level); the ledger
-- posts +3 per A-step and charges 1 per B-step on KEEP (Int ledger, exact).
-- Accesses apply only when present (sdepth-some gate; absent accesses are
-- engine no-ops). Proved: TWIN case (all-KEEP from twins keeps twins, so
-- e_A = e_B per access, so Phi is monotone nondecreasing, so Phi >= 0);
-- DELETE rule (banks 3*e_A, spends 0); conditional diverged step (with an
-- explicit window funder hypothesis: the OPEN deep-free-rarity link).
-- Engine identification (ecount-steps = engine StepEvs) rides the AUTHOR
-- simulation bridge (C133/C134); the counting kernel here is exact.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

def sdepth : STree → Nat → Option Nat
  | .leaf, _ => none
  | .node k l r, x =>
    if x == k then some 0
    else if x < k then Option.map (· + 1) (sdepth l x)
    else Option.map (· + 1) (sdepth r x)

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

-- Presence gate: absent accesses are engine no-ops (tree unchanged, 0 count).
def accEA (x : Nat) (t : STree) : Nat :=
  match sdepth t x with
  | none => 0
  | some _ => ecount x t

def applyA (x : Nat) (t : STree) : STree :=
  match sdepth t x with
  | none => t
  | some _ => splay x t

-- One access: A always splays (gated); B splays on KEEP only.
def stepAB (A B : STree) : Bool × Nat → STree × STree × Nat × Nat
  | (true, x) =>
    (applyA x A, applyA x B, accEA x A, accEA x B)
  | (false, x) =>
    (applyA x A, B, accEA x A, 0)

-- History ledger (Int, exact): +3 per A-step, -1 per B-step.
def runPhi (A B : STree) (Phi : Int) : List (Bool × Nat) → STree × STree × Int
  | [] => (A, B, Phi)
  | acc :: rest =>
    let (A', B', eA, eB) := stepAB A B acc
    runPhi A' B' (Phi + 3 * (eA : Int) - (eB : Int)) rest

-- TWIN STEP: same deterministic splay on equal trees stays equal, with
-- equal counts (congruence only).
theorem twin_step (A B : STree) (x : Nat) (htw : A = B) :
    stepAB A B (true, x) =
      (applyA x B, applyA x B, accEA x B, accEA x B) := by
  simp only [stepAB]
  rw [htw]

-- DELETE RULE: B untouched, banks 3*e_A, spends 0.
theorem delete_step (A B : STree) (x : Nat) :
    stepAB A B (false, x) = (applyA x A, B, accEA x A, 0) := by
  simp only [stepAB]

-- TWIN HISTORIES: all-KEEP from twins keeps twins and Phi monotone
-- nondecreasing (per-access net 3e - e = 2e >= 0). Hence Phi >= 0 from 0.
theorem twin_run (A B : STree) (Phi : Int) (H : List (Bool × Nat))
    (htw : A = B) (hk : ∀ a ∈ H, a.1 = true) :
    (runPhi A B Phi H).1 = (runPhi A B Phi H).2.1 ∧
      Phi ≤ (runPhi A B Phi H).2.2 := by
  induction H generalizing A B Phi with
  | nil =>
    simp only [runPhi]
    exact ⟨htw, Int.le_refl _⟩
  | cons hd tl ih =>
    obtain ⟨keep, x⟩ := hd
    have hk0 : keep = true := hk _ (List.Mem.head _)
    have hkrest : ∀ a ∈ tl, a.1 = true :=
      fun a ha => hk a (List.Mem.tail _ ha)
    subst hk0
    simp only [runPhi, stepAB]
    have htw' : applyA x A = applyA x B := by rw [htw]
    have he : accEA x A = accEA x B := by rw [htw]
    refine ⟨(ih _ _ _ htw' hkrest).1, ?_⟩
    have hnet : Phi ≤ Phi + 3 * (accEA x A : Int) - (accEA x B : Int) := by
      omega
    exact Int.le_trans hnet (ih _ _ _ htw' hkrest).2

-- CONDITIONAL DIVERGED STEP: with an explicit window funder hypothesis
-- (Phi_r + window net covers the burst overflow — the OPEN deep-free
-- rarity link), the burst preserves nonnegativity. Pins the exact gap.
theorem diverged_step_cond (Phi : Int) (S W eA eB : Nat)
    (h : (eB : Int) - 3 * (eA : Int) ≤ Phi + 3 * (S : Int) - (W : Int)) :
    0 ≤ Phi + 3 * (S : Int) - (W : Int) + 3 * (eA : Int) - (eB : Int) := by
  omega

theorem sdepth_self (k : Nat) (l r : STree) :
    sdepth (.node k l r) k = some 0 := by
  unfold sdepth
  cases h : (k == k) with
  | true => rfl
  | false =>
    have t : (k == k) = true := (beq_iff_eq).mpr rfl
    rw [t] at h
    exact Bool.noConfusion h

-- One-level descent, existential form (no Nat subtraction).
theorem sdepth_downL (k : Nat) (l r : STree) (x d : Nat)
    (hne : x ≠ k) (hlt : x < k)
    (h : sdepth (.node k l r) x = some d) :
    ∃ d', sdepth l x = some d' ∧ d = d' + 1 := by
  cases hsl : sdepth l x with
  | none =>
    simp [sdepth, beq_iff_eq, hne, hlt, hsl] at h
  | some d' =>
    refine ⟨d', rfl, ?_⟩
    simp [sdepth, beq_iff_eq, hne, hlt, hsl] at h
    omega

theorem sdepth_downR (k : Nat) (l r : STree) (x d : Nat)
    (hne : x ≠ k) (hlt : k < x)
    (h : sdepth (.node k l r) x = some d) :
    ∃ d', sdepth r x = some d' ∧ d = d' + 1 := by
  have h2 : ¬ x < k := by omega
  cases hsl : sdepth r x with
  | none =>
    simp [sdepth, beq_iff_eq, hne, h2, hsl] at h
  | some d' =>
    refine ⟨d', rfl, ?_⟩
    simp [sdepth, beq_iff_eq, hne, h2, hsl] at h
    omega

-- ARRIVAL BANKING: reaching depth >= 1 forces at least one skeleton step
-- (hence >= 3 banked supply at cap-3). Every genuine root arrival banks.
theorem ecount_pos (x : Nat) (t : STree) (d : Nat)
    (hd : sdepth t x = some d) (hd1 : 1 ≤ d) : 1 ≤ ecount x t := by
  cases t with
  | leaf =>
    simp [sdepth] at hd
  | node k l r =>
    cases hkb : (x == k) with
    | true =>
      have hxa : x = k := (beq_iff_eq).mp hkb
      rw [hxa] at hd
      rw [sdepth_self k l r] at hd
      have h0 : (0 : Nat) = d := Option.some_inj.mp hd
      omega
    | false =>
      have hne : x ≠ k := ne_of_beq_false hkb
      have h1 : ¬((x == k) = true) := by simp [hkb]
      by_cases hlt : x < k
      · obtain ⟨dm, hdm, rfl⟩ := sdepth_downL k l r x d hne hlt hd
        cases l with
        | leaf =>
          cases hdm
        | node p ll lr =>
          unfold ecount
          dsimp only
          rw [if_neg h1, if_pos hlt]
          by_cases h3 : ((x == p) = true)
          · rw [if_pos h3]; omega
          · rw [if_neg h3]
            by_cases h4 : x < p
            · rw [if_pos h4]; omega
            · rw [if_neg h4]; omega
      · have hlt2 : k < x := by omega
        obtain ⟨dm, hdm, rfl⟩ := sdepth_downR k l r x d hne hlt2 hd
        cases r with
        | leaf =>
          cases hdm
        | node p rl rr =>
          unfold ecount
          dsimp only
          rw [if_neg h1, if_neg hlt]
          by_cases h3 : ((x == p) = true)
          · rw [if_pos h3]; omega
          · rw [if_neg h3]
            by_cases h4 : p < x
            · rw [if_pos h4]; omega
            · rw [if_neg h4]; omega

-- RUN-CANONICAL FRAME (C174): runs (maximal same-key blocks) partition
-- history disjointly; needs AND S_A both live at run starts (RUN-NEED).
-- Three exact shape kernels around the open remainder
-- (div-runs deficit vs surplus-runs cover):
-- (i) run-start banking: off-root arrival forces >= 1 skeleton step.
theorem runstart_bank (x : Nat) (t : STree) (d : Nat)
    (hd : sdepth t x = some d) (hd1 : 1 ≤ d) : 1 ≤ accEA x t := by
  have he : 1 ≤ ecount x t := ecount_pos x t d hd hd1
  simp only [accEA]
  rw [hd]
  exact he

-- (ii) genesis-run surplus: twin depths (dA = dB) make need vanish
-- (need = max(d+1-2(d+1),0) = 0), so the run banks without spending.
theorem genesis_run_surplus (d : Nat) :
    (d + 1) - 2 * (d + 1) ≤ 6 * ((d + 1) / 2) := by
  omega

-- (iii) synced-run cap: synced depths (dB <= dA+2) leave deficit <= 1
-- (only the (0,1)-boundary charges, covered by Lemma B buffer).
theorem synced_run_le1 (dA dB : Nat) (h : dB ≤ dA + 2) :
    (dB - 2 * dA - 1) - 6 * ((dA + 1) / 2) ≤ 1 := by
  omega
