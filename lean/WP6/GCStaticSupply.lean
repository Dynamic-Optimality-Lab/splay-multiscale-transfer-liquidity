-- WP-6 STEPS C136 (positional program): event-supply accounting.
--
-- Self-contained (repo convention: no imports). Models the engine's site
-- enumeration `_sites(lo,hi,x,nkeys)` (legacy_embedding.py lines 156-161)
-- as a computable count and proves the per-event supply floor: a valid
-- emission interval (1 ≤ lo < hi ≤ n) banks at least one site. Lifting over
-- an event trace: total supply is at least the number of events (each StepEv
-- banks supply — the counting face of 8S/SITED-ALWAYS, feeding S_A).
-- Combined with C133 (valid emission carries sites existentially), this is
-- the quantitative form: valid emission carries COUNTED supply.
-- Loop-lifted agreement (engine loop iterations to skeleton steps over full
-- traces with parent navigation) queued.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- `_sites` count model: i ∈ [lo,hi) with 1 ≤ i, i < n, i+1 ≤ hi.
-- (Engine builds the list; only its length matters here.)
def sites_count (lo hi n : Nat) : Nat :=
  ((List.range' lo (hi - lo)).filter
    (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi))).length

-- PER-EVENT SUPPLY FLOOR: a valid interval banks ≥ 1 site (witness i = lo).
theorem sites_ge_one (lo hi n : Nat) (h1 : 1 ≤ lo) (h2 : lo < hi)
    (h3 : hi ≤ n) : 1 ≤ sites_count lo hi n := by
  have hmem : lo ∈ List.range' lo (hi - lo) :=
    List.mem_range'.mpr ⟨0, by omega, rfl⟩
  have hP : 1 ≤ lo ∧ lo < n ∧ lo + 1 ≤ hi := ⟨h1, by omega, by omega⟩
  have hpred : (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi)) lo = true :=
    decide_eq_true hP
  have hfm : lo ∈ (List.range' lo (hi - lo)).filter
      (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi)) :=
    List.mem_filter.mpr ⟨hmem, hpred⟩
  simp only [sites_count]
  cases hfl : (List.range' lo (hi - lo)).filter
      (fun i => decide (1 ≤ i ∧ i < n ∧ i + 1 ≤ hi)) with
  | nil => rw [hfl] at hfm; simp at hfm
  | cons hd tl => simp only [sites_count, hfl, List.length]; omega

-- TRACE SUPPLY: total sites across an event list cover the event count.
theorem trace_supply (evs : List (Nat × Nat)) (n : Nat)
    (h : ∀ e ∈ evs, 1 ≤ e.1 ∧ e.1 < e.2 ∧ e.2 ≤ n) :
    evs.length ≤ (evs.map (fun e => sites_count e.1 e.2 n)).sum := by
  induction evs with
  | nil => simp
  | cons e rest ih =>
    simp only [List.length_cons, List.map_cons, List.sum_cons]
    have he : 1 ≤ e.1 ∧ e.1 < e.2 ∧ e.2 ≤ n :=
      h e (List.mem_cons.mpr (Or.inl rfl))
    obtain ⟨he1, he2, he3⟩ := he
    have h1 : 1 ≤ sites_count e.1 e.2 n := sites_ge_one _ _ _ he1 he2 he3
    have ihr : rest.length ≤ (rest.map (fun e => sites_count e.1 e.2 n)).sum :=
      ih (fun e' hm => h e' (List.mem_cons.mpr (Or.inr hm)))
    omega
