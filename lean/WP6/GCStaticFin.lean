-- WP-6 STEPS C151 (positional program): finite-set toolkit, part 1.
-- (Lean-density track; vault id C151.)
--
-- Self-contained (repo convention: no imports). Minimal finite-set theory
-- over Nat-lists for the Hall assembly (C152): dedup construction with
-- membership/nodup/size laws; neighbor sets; degrees and minimum degree;
-- local erase lemmas (core lacks them). Everything by structural induction
-- with the established simp/omega idioms.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- Dedup (keep last occurrence; members unchanged).
def dedup : List Nat → List Nat
  | [] => []
  | x :: xs => if x ∈ xs then dedup xs else x :: dedup xs

theorem mem_dedup (x : Nat) (l : List Nat) : x ∈ dedup l ↔ x ∈ l := by
  induction l with
  | nil => simp only [dedup]
  | cons y ys ih =>
    simp only [dedup]
    by_cases h : y ∈ ys
    · rw [if_pos h]
      constructor
      · intro hm
        exact List.mem_cons.mpr (Or.inr ((ih.mp) hm))
      · intro hm
        obtain rfl | hmem := List.mem_cons.mp hm
        · exact ih.mpr h
        · exact ih.mpr hmem
    · rw [if_neg h]
      constructor
      · intro hm
        obtain rfl | hmem := List.mem_cons.mp hm
        · exact List.mem_cons.mpr (Or.inl rfl)
        · exact List.mem_cons.mpr (Or.inr (ih.mp hmem))
      · intro hm
        obtain rfl | hmem := List.mem_cons.mp hm
        · exact List.mem_cons.mpr (Or.inl rfl)
        · exact List.mem_cons.mpr (Or.inr (ih.mpr hmem))

theorem nodup_dedup (l : List Nat) : (dedup l).Nodup := by
  induction l with
  | nil => simp [dedup]
  | cons y ys ih =>
    simp only [dedup]
    by_cases h : y ∈ ys
    · rw [if_pos h]; exact ih
    · rw [if_neg h]
      simp only [List.nodup_cons, mem_dedup]
      exact ⟨h, ih⟩

theorem length_dedup_le (l : List Nat) : (dedup l).length ≤ l.length := by
  induction l with
  | nil => exact Nat.zero_le 0
  | cons y ys ih =>
    simp only [dedup]
    by_cases h : y ∈ ys
    · rw [if_pos h]
      simp only [List.length] at ih ⊢
      omega
    · rw [if_neg h]
      simp only [List.length] at ih ⊢
      omega

-- Neighbor sets (distinct adjacent A identities), explicit recursion.
def rawNb (adj : Nat → List Nat) : List Nat → List Nat
  | [] => []
  | b :: bs => adj b ++ rawNb adj bs

def neighbors (adj : Nat → List Nat) (Q : List Nat) : List Nat :=
  dedup (rawNb adj Q)

theorem mem_rawNb (adj : Nat → List Nat) (Q : List Nat) (x : Nat) :
    x ∈ rawNb adj Q ↔ ∃ b, b ∈ Q ∧ x ∈ adj b := by
  induction Q with
  | nil => simp [rawNb]
  | cons b bs ih =>
    simp only [rawNb, List.mem_append]
    constructor
    · intro hm
      cases hm with
      | inl h => exact ⟨b, List.mem_cons.mpr (Or.inl rfl), h⟩
      | inr h =>
        obtain ⟨b', hbm, hbx⟩ := (ih.mp h)
        exact ⟨b', List.mem_cons.mpr (Or.inr hbm), hbx⟩
    · intro hm
      obtain ⟨b', hbm, hbx⟩ := hm
      simp only [List.mem_cons] at hbm
      cases hbm with
      | inl heq => subst b'; exact Or.inl hbx
      | inr hmem => exact Or.inr ((ih.mpr ⟨b', hmem, hbx⟩))

theorem mem_neighbors (adj : Nat → List Nat) (Q : List Nat) (x : Nat) :
    x ∈ neighbors adj Q ↔ ∃ b, b ∈ Q ∧ x ∈ adj b := by
  simp only [neighbors, mem_dedup]
  exact mem_rawNb adj Q x

-- Degrees and minimum degree.
def degree (adj : Nat → List Nat) (Q : List Nat) (a : Nat) : Nat :=
  (Q.filter (fun b => decide (a ∈ adj b))).length

def mindeg (deg : Nat → Nat) : List Nat → Nat
  | [] => 0
  | a :: as => Nat.min (deg a) (mindeg deg as)

theorem mindeg_le_mem (deg : Nat → Nat) (l : List Nat) (a : Nat)
    (h : a ∈ l) : mindeg deg l ≤ deg a := by
  induction l with
  | nil => simp at h
  | cons b bs ih =>
    simp only [List.mem_cons] at h
    simp only [mindeg]
    cases h with
    | inl heq => rw [heq]; exact Nat.min_le_left _ _
    | inr hmem => exact Nat.le_trans (Nat.min_le_right _ _) (ih hmem)

-- Removing listed elements (filter out members of R).
def sdiff (Q R : List Nat) : List Nat :=
  Q.filter (fun b => !decide (b ∈ R))

theorem mem_sdiff (Q R : List Nat) (x : Nat) :
    x ∈ sdiff Q R ↔ x ∈ Q ∧ x ∉ R := by
  simp only [sdiff, List.mem_filter]
  constructor
  · intro hm
    obtain ⟨hmQ, hpred⟩ := hm
    refine ⟨hmQ, ?_⟩
    intro hcon
    simp [hcon] at hpred
  · intro hm
    obtain ⟨hmQ, hnm⟩ := hm
    refine ⟨hmQ, ?_⟩
    by_cases h : x ∈ R
    · exact absurd h hnm
    · simp [h]

theorem sdiff_nodup (Q R : List Nat) (h : Q.Nodup) : (sdiff Q R).Nodup := by
  simp only [sdiff]
  exact List.Sublist.nodup List.filter_sublist h

theorem sdiff_length_le (Q R : List Nat) : (sdiff Q R).length ≤ Q.length := by
  simp only [sdiff]
  exact List.Sublist.length_le List.filter_sublist

-- Local erase membership (core lacks it): kept elements are exactly the
-- non-erased members.
theorem erase_mem_of_ne_mem (x a : Nat) (l : List Nat)
    (hne : x ≠ a) (hm : x ∈ l) : x ∈ l.erase a := by
  induction l with
  | nil => simp at hm
  | cons y ys ih =>
    simp only [List.erase]
    cases h2 : y == a with
    | true =>
      have hya : y = a := (beq_iff_eq).mp h2
      simp only [List.mem_cons] at hm
      cases hm with
      | inl heq =>
        have hxa : x = a := heq.trans hya
        exact absurd hxa hne
      | inr hmem => exact hmem
    | false =>
      simp only [List.mem_cons] at hm ⊢
      cases hm with
      | inl heq => exact Or.inl heq
      | inr hmem => exact Or.inr (ih hmem)

-- Removing listed elements (filter out members of R).

-- Subset cardinality (Nodup + membership containment).
theorem subset_length_aux (l₁ : List Nat) : ∀ (l₂ : List Nat),
    l₁.Nodup → (∀ x ∈ l₁, x ∈ l₂) → l₁.length ≤ l₂.length := by
  induction l₁ with
  | nil => intro l₂ _ _; exact Nat.zero_le _
  | cons a as ih =>
    intro l₂ hnd hsub
    simp only [List.nodup_cons] at hnd
    obtain ⟨hna, hndas⟩ := hnd
    have ha2 : a ∈ l₂ := hsub a (List.mem_cons.mpr (Or.inl rfl))
    have hsube : ∀ x ∈ as, x ∈ l₂.erase a := by
      intro x hx
      have hmem : x ∈ l₂ := hsub x (List.mem_cons.mpr (Or.inr hx))
      have hne : x ≠ a := by
        intro he
        have hx2 : a ∈ as := by rw [he] at hx; exact hx
        exact hna hx2
      exact erase_mem_of_ne_mem x a l₂ hne hmem
    have h1 := ih (l₂.erase a) hndas hsube
    have h2 : (l₂.erase a).length + 1 = l₂.length := by
      rw [List.length_erase, if_pos ha2]
      have hp := List.length_pos_of_mem ha2
      omega
    simp only [List.length]
    omega

theorem subset_length (l₁ l₂ : List Nat) (hnd : l₁.Nodup)
    (hsub : ∀ x ∈ l₁, x ∈ l₂) : l₁.length ≤ l₂.length :=
  subset_length_aux l₁ l₂ hnd hsub

-- Strict version with an excluded witness.
theorem length_strict (l₁ l₂ : List Nat) (a : Nat)
    (hsub : ∀ x ∈ l₁, x ∈ l₂) (hmem : a ∈ l₂) (hnmem : a ∉ l₁)
    (hnd1 : l₁.Nodup) : l₁.length + 1 ≤ l₂.length := by
  have hsube : ∀ x ∈ l₁, x ∈ l₂.erase a := by
    intro x hx
    have hmem2 : x ∈ l₂ := hsub x hx
    have hne : x ≠ a := by
      intro he
      have hx2 : a ∈ l₁ := by rw [he] at hx; exact hx
      exact hnmem hx2
    exact erase_mem_of_ne_mem x a l₂ hne hmem2
  have h1 := subset_length l₁ (l₂.erase a) hnd1 hsube
  have h2 : (l₂.erase a).length + 1 = l₂.length := by
    rw [List.length_erase, if_pos hmem]
    have hp := List.length_pos_of_mem hmem
    omega
  omega

