-- WP-6 STEPS C141M (positional program): kernel matching theory, greedy part.
-- (C-numbering: Lean-density track; vault id C144 to avoid clash.)
--
-- Self-contained (repo convention: no imports). Cap-3 bipartite matching
-- with an explicit greedy rule: bevs processed in order, each taking the
-- first eligible site with load < 3. Loads threaded as functions (no global
-- counting needed: maximality needs only local ledger facts). Proved:
-- loads stay within cap; placements land on neighbors; unprocessed indices
-- stay empty; single steps preserve other indices and never decrease loads;
-- GREEDY MAXIMALITY: every unplaced bev has all neighbors full (the kernel
-- core of 8AC-STUCK-SIB: stuck ⟹ all-nonempty-tiers full; E1-sibling
-- specialization is Layer A (eligibility scoping, build_tagged + 8AC-TO)).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- Assignment update (bev j placed on site i) and load update.
def mupd (M : Nat → Option Nat) (j i : Nat) : Nat → Option Nat :=
  fun j' => if j' = j then some i else M j'

def upd (L : Nat → Nat) (i : Nat) : Nat → Nat :=
  fun j => if j = i then L i + 1 else L j

theorem mupd_self (M : Nat → Option Nat) (j i : Nat) :
    mupd M j i j = some i := by
  simp [mupd]

theorem mupd_ne (M : Nat → Option Nat) (j i j' : Nat) (h : j' ≠ j) :
    mupd M j i j' = M j' := by
  simp [mupd, h]

theorem upd_self (L : Nat → Nat) (i : Nat) : upd L i i = L i + 1 := by
  simp [upd]

theorem upd_ne (L : Nat → Nat) (i j : Nat) (h : j ≠ i) :
    upd L i j = L j := by
  simp [upd, h]

theorem upd_ge (L : Nat → Nat) (i j : Nat) : L j ≤ upd L i j := by
  by_cases h : j = i
  · subst h; simp [upd]
  · have h2 : upd L i j = L j := by simp [upd, h]
    omega

-- One placement step over an explicit neighbor list (structural, clean
-- equations): first neighbor with load < 3, else unchanged.
def placeIn (M : Nat → Option Nat) (L : Nat → Nat) (j : Nat) :
    List Nat → (Nat → Option Nat) × (Nat → Nat)
  | [] => (M, L)
  | i :: is => if L i < 3 then (mupd M j i, upd L i) else placeIn M L j is

def place (adj : Nat → List Nat) (st : (Nat → Option Nat) × (Nat → Nat))
    (k : Nat) : (Nat → Option Nat) × (Nat → Nat) :=
  placeIn st.1 st.2 k (adj k)

-- Loads stay within cap (induction on the neighbor list).
theorem placeIn_bound (M : Nat → Option Nat) (L : Nat → Nat) (j : Nat)
    (l : List Nat) (hL : ∀ s, L s ≤ 3) (s : Nat) :
    (placeIn M L j l).2 s ≤ 3 := by
  induction l with
  | nil => simp only [placeIn]; exact hL s
  | cons i is ih =>
    simp only [placeIn]
    by_cases h : L i < 3
    · rw [if_pos h]; show upd L i s ≤ 3
      by_cases h2 : s = i
      · subst h2; rw [upd_self]; omega
      · rw [upd_ne _ _ _ h2]; exact hL s
    · rw [if_neg h]; exact ih

-- Placement outcome: either untouched, or placed on a listed neighbor
-- that had room.
theorem placeIn_outcome (M : Nat → Option Nat) (L : Nat → Nat) (j : Nat)
    (l : List Nat) :
    (placeIn M L j l).1 j = M j ∨
    ∃ i, i ∈ l ∧ (placeIn M L j l).1 j = some i ∧ L i < 3 := by
  induction l with
  | nil => exact Or.inl rfl
  | cons i is ih =>
    simp only [placeIn]
    by_cases h : L i < 3
    · rw [if_pos h]
      refine Or.inr ⟨i, List.mem_cons.mpr (Or.inl rfl), ?_, h⟩
      simp only []; exact mupd_self _ _ _
    · rw [if_neg h]
      cases ih with
      | inl hkeep => exact Or.inl hkeep
      | inr hget =>
        obtain ⟨i', hm, heq, hlt⟩ := hget
        exact Or.inr ⟨i', List.mem_cons.mpr (Or.inr hm), heq, hlt⟩

-- If some listed neighbor has room, placement puts j somewhere.
theorem placeIn_some (M : Nat → Option Nat) (L : Nat → Nat) (j : Nat)
    (l : List Nat) (h : ∃ i, i ∈ l ∧ L i < 3) :
    ∃ i, (placeIn M L j l).1 j = some i := by
  induction l with
  | nil => simp at h
  | cons i is ih =>
    simp only [placeIn]
    by_cases h2 : L i < 3
    · rw [if_pos h2]
      exact ⟨i, by simp only []; exact mupd_self _ _ _⟩
    · rw [if_neg h2]
      obtain ⟨i', hm, hlt⟩ := h
      simp at hm
      cases hm with
      | inl heq =>
        rw [heq] at hlt
        exact absurd hlt h2
      | inr hmem => exact ih ⟨i', hmem, hlt⟩

-- Other indices are never touched by a placement step.
theorem placeIn_preserve (M : Nat → Option Nat) (L : Nat → Nat) (k : Nat)
    (l : List Nat) (j : Nat) (hjk : j ≠ k) :
    (placeIn M L k l).1 j = M j := by
  induction l with
  | nil => rfl
  | cons i is ih =>
    simp only [placeIn]
    by_cases h2 : L i < 3
    · rw [if_pos h2]; exact mupd_ne _ _ _ _ hjk
    · rw [if_neg h2]; exact ih

-- Loads never decrease through a placement step.
theorem placeIn_mono (M : Nat → Option Nat) (L : Nat → Nat) (j : Nat)
    (l : List Nat) (s : Nat) : L s ≤ (placeIn M L j l).2 s := by
  induction l with
  | nil => exact Nat.le_refl _
  | cons i is ih =>
    simp only [placeIn]
    by_cases h2 : L i < 3
    · rw [if_pos h2]; show L s ≤ upd L i s; exact upd_ge _ _ _
    · rw [if_neg h2]; exact ih

-- Chronological greedy run: bev B processed from the state after bevs < B.
-- Structural on fuel (clean equations, traceLen idiom).
def runGreedy (adj : Nat → List Nat) : Nat → (Nat → Option Nat) × (Nat → Nat)
  | 0 => ((fun _ => none), (fun _ => 0))
  | B + 1 => place adj (runGreedy adj B) B

-- GREEDY MAXIMALITY (kernel core of 8AC-STUCK-SIB): cap respected, future
-- indices empty, and every unplaced processed bev has all neighbors full.
theorem greedy_maximal (adj : Nat → List Nat) (B : Nat) :
    (∀ s, (runGreedy adj B).2 s ≤ 3) ∧
    (∀ j, j < B → (runGreedy adj B).1 j = none →
      ∀ i, i ∈ adj j → 3 ≤ (runGreedy adj B).2 i) ∧
    (∀ j, B ≤ j → (runGreedy adj B).1 j = none) := by
  induction B with
  | zero =>
    refine ⟨?_, ?_, ?_⟩
    · intro s; exact Nat.zero_le 3
    · intro j hj _ _ _; omega
    · intro j _; rfl
  | succ B ih =>
    obtain ⟨hbound, hmax, hunproc⟩ := ih
    refine ⟨?_, ?_, ?_⟩
    · intro s
      simp only [runGreedy, place]
      exact placeIn_bound _ _ _ _ (fun s => hbound s) s
    · intro j hj hnone i hi
      simp only [runGreedy, place] at hnone ⊢
      by_cases heq : j = B
      · subst j
        by_cases hex : ∃ i', i' ∈ adj B ∧ (runGreedy adj B).2 i' < 3
        · obtain ⟨i', hi', hlt⟩ := hex
          have hplaced := placeIn_some (runGreedy adj B).1
            (runGreedy adj B).2 B (adj B) ⟨i', hi', hlt⟩
          obtain ⟨i'', heq2⟩ := hplaced
          rw [heq2] at hnone
          simp at hnone
        · have hfull : ∀ i', i' ∈ adj B → 3 ≤ (runGreedy adj B).2 i' := by
            intro i' hi'
            by_cases hlt : (runGreedy adj B).2 i' < 3
            · exact absurd ⟨i', hi', hlt⟩ hex
            · omega
          have hmono : (runGreedy adj B).2 i ≤
              (placeIn (runGreedy adj B).1 (runGreedy adj B).2 B (adj B)).2 i :=
            placeIn_mono _ _ _ _ i
          have hfi := hfull i hi
          omega
      · have hne : j ≠ B := heq
        have hkeep : (placeIn (runGreedy adj B).1 (runGreedy adj B).2 B
            (adj B)).1 j = (runGreedy adj B).1 j :=
          placeIn_preserve _ _ _ _ _ hne
        rw [hkeep] at hnone
        have hfull := hmax j (by omega) hnone i hi
        have hmono : (runGreedy adj B).2 i ≤
            (placeIn (runGreedy adj B).1 (runGreedy adj B).2 B (adj B)).2 i :=
          placeIn_mono _ _ _ _ i
        omega
    · intro j hj
      simp only [runGreedy, place]
      have hne : j ≠ B := by omega
      have hkeep : (placeIn (runGreedy adj B).1 (runGreedy adj B).2 B
          (adj B)).1 j = (runGreedy adj B).1 j :=
        placeIn_preserve _ _ _ _ _ hne
      rw [hkeep]
      exact hunproc j (by omega)
