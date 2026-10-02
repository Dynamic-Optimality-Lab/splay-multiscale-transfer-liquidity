-- WP-6 STEPS C145 (positional program): augmenting-path flip, set improvement.
-- (Lean-density track; vault id C145.)
--
-- Self-contained (repo convention: no imports). Berge improvement direction,
-- set form: flipping an alternating path (reassign each path bev to its
-- path site) matches strictly more bevs — the previously unmatched head
-- becomes matched, all previously matched bevs stay matched. No counting
-- needed (pointwise status + Nodup paths); cap-side validity stays with the
-- threaded loads (C144) and the meta-argument (8AC-BERGE, C116 hall_lemmas).
-- With C144 (greedy maximality: stuck ⟹ all-neighbors-full), this is the
-- kernel matching-theory pair: stuck points are either fixable (augmentable,
-- strictly improvable here) or witness violators.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- Assignment update (bev j placed on site i).
def mupd (M : Nat → Option Nat) (j i : Nat) : Nat → Option Nat :=
  fun j' => if j' = j then some i else M j'

theorem mupd_self (M : Nat → Option Nat) (j i : Nat) :
    mupd M j i j = some i := by
  simp [mupd]

theorem mupd_ne (M : Nat → Option Nat) (j i j' : Nat) (h : j' ≠ j) :
    mupd M j i j' = M j' := by
  simp [mupd, h]

-- Path flip: reassign each listed (bev, site) pair in order.
def pathflip (M : Nat → Option Nat) : List (Nat × Nat) → Nat → Option Nat
  | [] => M
  | (b, a) :: es => pathflip (mupd M b a) es

-- Off-path bevs keep their status.
theorem flip_offpath (M : Nat → Option Nat) (edges : List (Nat × Nat))
    (j : Nat) (h : j ∉ edges.map Prod.fst) :
    pathflip M edges j = M j := by
  induction edges generalizing M with
  | nil => rfl
  | cons e es ih =>
    obtain ⟨b', a'⟩ := e
    simp only [pathflip]
    have hmem : b' ∈ ((b', a') :: es).map Prod.fst :=
      List.mem_cons.mpr (Or.inl rfl)
    have h1 : j ≠ b' := by
      intro he
      subst he
      exact h hmem
    have h2 : j ∉ es.map Prod.fst :=
      fun hc => h (List.mem_cons.mpr (Or.inr hc))
    have hih := ih (mupd M b' a') h2
    rw [hih]
    exact mupd_ne _ _ _ _ h1

-- Listed bevs (distinct) get their listed sites.
theorem flip_set (M : Nat → Option Nat) (edges : List (Nat × Nat))
    (hnd : List.Nodup (edges.map Prod.fst)) (b a : Nat)
    (hmem : (b, a) ∈ edges) : pathflip M edges b = some a := by
  induction edges generalizing M with
  | nil => simp at hmem
  | cons e es ih =>
    obtain ⟨b', a'⟩ := e
    simp only [pathflip]
    simp only [List.mem_cons] at hmem
    simp only [List.map_cons, List.nodup_cons] at hnd
    obtain ⟨hnd1, hnd2⟩ := hnd
    obtain h | h := hmem
    · have hba : b = b' ∧ a = a' := by
        simp only [Prod.mk.injEq] at h
        exact h
      obtain ⟨hb, ha⟩ := hba
      rw [hb, ha]
      have hfp : pathflip (mupd M b' a') es b' = mupd M b' a' b' :=
        flip_offpath _ _ _ hnd1
      rw [hfp]
      exact mupd_self _ _ _
    · exact ih _ hnd2 h

-- BERGE IMPROVEMENT (set form): flipping a distinct-bev alternating path
-- whose head was unmatched matches strictly more bevs — the head becomes
-- matched, every previously matched bev stays matched.
theorem flip_improve (M : Nat → Option Nat) (edges : List (Nat × Nat))
    (hnd : List.Nodup (edges.map Prod.fst)) (b₀ a₀ : Nat)
    (hmem0 : (b₀, a₀) ∈ edges) :
    (pathflip M edges b₀ ≠ none) ∧
    (∀ j, M j ≠ none → pathflip M edges j ≠ none) := by
  refine ⟨?_, ?_⟩
  · have h1 := flip_set M edges hnd b₀ a₀ hmem0
    rw [h1]
    simp
  · intro j hj
    by_cases hmem : j ∈ edges.map Prod.fst
    · obtain ⟨p, hpm, hfst⟩ := List.mem_map.mp hmem
      obtain ⟨b', a'⟩ := p
      have hjb : j = b' := Eq.symm hfst
      subst j
      have hset := flip_set M edges hnd b' a' hpm
      rw [hset]
      simp
    · have hoff := flip_offpath M edges j hmem
      rw [hoff]
      exact hj
