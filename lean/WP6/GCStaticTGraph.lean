-- WP-6 STEPS C154 (positional program): time-indexed matching core.
-- (Lean-density track; vault id C154.)
--
-- Self-contained (repo convention: no imports). Multi-session matching
-- theory in kernel: time-indexed bipartite graphs (bev/site access levels,
-- eligibility arrow, E1 same-access completeness) with the latest-block
-- decomposition (QL/QQ partition, new-source UL, E1L-inside-UL) and the 8J
-- necessity (|QL| >= 3|UL| + 1 from minimality + induction slack). This pins
-- the EXACT shape of the zone argument's first step in kernel; the
-- old-abundance content (HOLE-1/HOLE-IND) remains the open obligation.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- Dedup with membership law.
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

-- Neighbor sets with membership law.
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

-- Partition counting: filter and complement cover exactly.
theorem filter_count_add (l : List Nat) (p : Nat → Bool) :
    (l.filter p).length + (l.filter (fun x => !p x)).length = l.length := by
  induction l with
  | nil => simp only [List.filter, List.length]
  | cons y ys ih =>
    simp only [List.filter]
    by_cases h : p y = true
    · simp [h]
      omega
    · simp [h]
      omega

-- Latest-block split (QL at access L, QQ earlier via complement) and
-- new sources UL (neighbors at L minus earlier neighborhoods).
def QL (BQ : List Nat) (bacc : Nat → Nat) (L : Nat) : List Nat :=
  BQ.filter (fun b => decide (bacc b = L))

def QQ (BQ : List Nat) (bacc : Nat → Nat) (L : Nat) : List Nat :=
  BQ.filter (fun b => !decide (bacc b = L))

def UL (adj : Nat → List Nat) (BQ : List Nat) (bacc : Nat → Nat)
    (L : Nat) : List Nat :=
  (neighbors adj BQ).filter
    (fun a => !decide (a ∈ neighbors adj (QQ BQ bacc L)))

theorem QLQQ_add (BQ : List Nat) (bacc : Nat → Nat) (L : Nat) :
    (QL BQ bacc L).length + (QQ BQ bacc L).length = BQ.length :=
  filter_count_add BQ _

theorem BQsplit (BQ : List Nat) (bacc : Nat → Nat) (L : Nat)
    (b : Nat) (hb : b ∈ BQ) : b ∈ QL BQ bacc L ∨ b ∈ QQ BQ bacc L := by
  simp only [QL, QQ, List.mem_filter]
  by_cases h : bacc b = L
  · exact Or.inl ⟨hb, decide_eq_true h⟩
  · exact Or.inr ⟨hb, by simp [h]⟩

theorem Nunion (adj : Nat → List Nat) (BQ : List Nat) (bacc : Nat → Nat)
    (L : Nat) (x : Nat) :
    x ∈ neighbors adj BQ ↔
      x ∈ neighbors adj (QL BQ bacc L) ∨ x ∈ neighbors adj (QQ BQ bacc L) := by
  constructor
  · intro hx
    obtain ⟨b, hbm, hbx⟩ := (mem_neighbors adj BQ x).mp hx
    cases BQsplit BQ bacc L b hbm with
    | inl hL => exact Or.inl ((mem_neighbors adj _ x).mpr ⟨b, hL, hbx⟩)
    | inr hR => exact Or.inr ((mem_neighbors adj _ x).mpr ⟨b, hR, hbx⟩)
  · intro hx
    cases hx with
    | inl hL =>
      obtain ⟨b, hbm, hbx⟩ := (mem_neighbors adj _ x).mp hL
      have hbQ : b ∈ BQ := (List.mem_filter.mp hbm).1
      exact (mem_neighbors adj BQ x).mpr ⟨b, hbQ, hbx⟩
    | inr hR =>
      obtain ⟨b, hbm, hbx⟩ := (mem_neighbors adj _ x).mp hR
      have hbQ : b ∈ BQ := (List.mem_filter.mp hbm).1
      exact (mem_neighbors adj BQ x).mpr ⟨b, hbQ, hbx⟩

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

-- Local erase membership (kept elements are non-erased members).
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

-- Equal members + both Nodup gives equal length.
theorem length_eq_of_mem_eq (l₁ l₂ : List Nat) (h1 : l₁.Nodup)
    (h2 : l₂.Nodup) (h : ∀ x, x ∈ l₁ ↔ x ∈ l₂) :
    l₁.length = l₂.length := by
  have g1 := subset_length l₁ l₂ h1 (fun x hx => (h x).mp hx)
  have g2 := subset_length l₂ l₁ h2 (fun x hx => (h x).mpr hx)
  omega

-- Latest-block split: QL (access L) and QQ (earlier, via complement).
-- QQ as complement keeps counting exact; members satisfy acc < L via Emax.
-- New sources at L: neighbors minus earlier neighborhoods.
-- E1 axioms (Layer A: build_tagged construction):
--   arrow: edges point backward-or-same (8AC-TO);
--   E1same: E1(L) plotted at L; E1nb: E1(L) complete to access-L bevs;
--   Emax: L latest; Lmem: L achieved.

theorem neighbors_mono (adj : Nat → List Nat) (Q₁ Q₂ : List Nat)
    (h : ∀ b ∈ Q₁, b ∈ Q₂) (x : Nat) (hx : x ∈ neighbors adj Q₁) :
    x ∈ neighbors adj Q₂ := by
  obtain ⟨b, hbm, hbx⟩ := (mem_neighbors adj Q₁ x).mp hx
  exact (mem_neighbors adj Q₂ x).mpr ⟨b, h _ hbm, hbx⟩
theorem Nsplit_length (adj : Nat → List Nat) (BQ : List Nat)
    (bacc : Nat → Nat) (L : Nat) :
    (neighbors adj BQ).length =
      (neighbors adj (QQ BQ bacc L)).length +
      (UL adj BQ bacc L).length := by
  have hQQsub : ∀ b ∈ QQ BQ bacc L, b ∈ BQ := by
    intro b hb
    simp only [QQ, List.mem_filter] at hb
    exact hb.1
  have hF : (((neighbors adj BQ).filter
      (fun a => decide (a ∈ neighbors adj (QQ BQ bacc L)))).length) =
      (neighbors adj (QQ BQ bacc L)).length := by
    have hsub : (((neighbors adj BQ).filter
        (fun a => decide (a ∈ neighbors adj (QQ BQ bacc L)))).Sublist
        (neighbors adj BQ)) := List.filter_sublist
    have hnf : (((neighbors adj BQ).filter
        (fun a => decide (a ∈ neighbors adj (QQ BQ bacc L)))).Nodup) :=
      hsub.nodup (nodup_dedup _)
    have hndQQ : (neighbors adj (QQ BQ bacc L)).Nodup := nodup_dedup _
    have hiff : ∀ x, x ∈ ((neighbors adj BQ).filter
        (fun a => decide (a ∈ neighbors adj (QQ BQ bacc L)))) ↔
        x ∈ neighbors adj (QQ BQ bacc L) := by
      intro x
      constructor
      · intro hx
        simp only [List.mem_filter] at hx
        exact of_decide_eq_true hx.2
      · intro hx
        have hmem : x ∈ neighbors adj BQ :=
          neighbors_mono adj (QQ BQ bacc L) BQ hQQsub x hx
        simp only [List.mem_filter]
        exact ⟨hmem, decide_eq_true hx⟩
    have g1 := subset_length _ _ hnf
      (fun x hx => (hiff x).mp hx)
    have g2 := subset_length _ _ hndQQ
      (fun x hx => (hiff x).mpr hx)
    omega
  have hC := filter_count_add (neighbors adj BQ)
    (fun a => decide (a ∈ neighbors adj (QQ BQ bacc L)))
  simp only [UL] at hC ⊢
  omega

-- E1(L) sits inside the new sources UL (pristine + arrow + latest):
-- E1 reaches the latest block (completeness, needs a latest bev) and
-- cannot reach earlier blocks (arrow would point forward).
theorem E1L_sub_UL (BQ : List Nat) (bacc sacc : Nat → Nat)
    (adj : Nat → List Nat) (E1L : List Nat) (L : Nat)
    (arrow : ∀ b ∈ BQ, ∀ a ∈ adj b, sacc a ≤ bacc b)
    (E1same : ∀ a ∈ E1L, sacc a = L)
    (E1nb : ∀ a ∈ E1L, ∀ b ∈ BQ, bacc b = L → a ∈ adj b)
    (Emax : ∀ b ∈ BQ, bacc b ≤ L)
    (hmemL : ∃ b ∈ BQ, bacc b = L) :
    ∀ a ∈ E1L, a ∈ UL adj BQ bacc L := by
  obtain ⟨b₀, hb₀Q, hb₀L⟩ := hmemL
  have hb₀QL : b₀ ∈ QL BQ bacc L :=
    List.mem_filter.mpr ⟨hb₀Q, decide_eq_true hb₀L⟩
  intro a ha
  have hNB : a ∈ neighbors adj BQ := by
    have hQL : a ∈ neighbors adj (QL BQ bacc L) := by
      have hadj : a ∈ adj b₀ := E1nb a ha b₀ hb₀Q hb₀L
      exact (mem_neighbors adj _ a).mpr ⟨b₀, hb₀QL, hadj⟩
    have hsub : ∀ b ∈ QL BQ bacc L, b ∈ BQ := by
      intro b hb
      simp only [QL, List.mem_filter] at hb
      exact hb.1
    exact neighbors_mono adj _ BQ hsub a hQL
  have hnew : a ∉ neighbors adj (QQ BQ bacc L) := by
    intro hc
    obtain ⟨b', hbm', hab'⟩ := (mem_neighbors adj _ a).mp hc
    have hle1 : L ≤ bacc b' := by
      have h1 : sacc a = L := E1same a ha
      have h2 : sacc a ≤ bacc b' := arrow b' ((List.mem_filter.mp hbm').1) a hab'
      omega
    have hle2 : bacc b' ≤ L := Emax b' ((List.mem_filter.mp hbm').1)
    have hne : bacc b' ≠ L := by
      have h3 : (!decide (bacc b' = L)) = true :=
        (List.mem_filter.mp hbm').2
      intro heq
      simp [heq] at h3
    omega
  simp only [UL, List.mem_filter]
  exact ⟨hNB, by simpa using hnew⟩

-- 8J ARITHMETIC (latest-block necessity, pure counting).
theorem eightJ (q q0 qL n n0 u s : Nat)
    (hQ : q = q0 + qL) (hN : n = n0 + u)
    (hIH : q0 + s = 3 * n0) (hD : q = 3 * n + 1) :
    3 * u + 1 ≤ qL := by
  omega
