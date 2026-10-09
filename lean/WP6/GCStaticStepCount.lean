-- WP-6 STEPS C161 (positional program): skeleton step count.
-- (Lean-density track; vault id C161.)
--
-- Self-contained (repo convention: no imports). Step-count correspondence,
-- skeleton side: `ecount` emits one per recursion level (mirroring splay's
-- control exactly); proved equal to ceil(depth/2) via functional induction
-- with exact depth-descent facts. Ingredients: sdepth one-level descent
-- (existential form, no Nat subtraction), zig/double delivery as base cases,
-- omega for the (d+1)/2 arithmetic. Engine side (loop iterations) + the
-- identification e_B/e_A = eloop counts queued (C162); with it, the 8AC-SYNCED
-- links (e_B <= d^B, e_A >= d^A/2, single-finish) become kernel facts.
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

-- Step count: one per recursion level (mirrors splay control exactly).
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

-- STEP COUNT: steps equal ceil(depth/2). The loop-StepEv correspondence
-- target (C162 identifies these counts with engine e_B/e_A).
theorem ecount_eq (x : Nat) (t : STree) :
    ∀ d : Nat, sdepth t x = some d → ecount x t = (d + 1) / 2 := by
  refine (ecount.induct x (fun t => ∀ d : Nat,
    sdepth t x = some d → ecount x t = (d + 1) / 2)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · intro d h
    simp only [ecount] at h ⊢
    cases h
  · intro a a_1 a_2 h d hd
    have hxa : x = a := (beq_iff_eq).mp h
    simp only [hxa] at h hd ⊢
    have hs := sdepth_self a a_1 a_2
    rw [hs] at hd
    have hdd : d = 0 := Eq.symm (Option.some_inj.mp hd)
    subst hdd
    cases a_1 <;> cases a_2
    all_goals simp only [ecount, if_pos h]
    all_goals omega
  · intro a a_1 h1 h2 d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_pos h2]
       simp [sdepth, h1, h2] at hd)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       obtain ⟨dm, hdm, rfl⟩ := sdepth_downL a _ _ x _ hne h2 hd
       have hdm0 : dm = 0 := by
          simp [sdepth, h3] at hdm
          omega
       omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       obtain ⟨dm, hdm, rfl⟩ := sdepth_downL a _ _ x _ hne h2 hd
       have hne2 : x ≠ a_2 := fun he => h3 ((beq_iff_eq).mpr he)
       obtain ⟨d1, hd1, rfl⟩ := sdepth_downL a_2 _ _ x _ hne2 h4 hdm
       have heq := ih d1 hd1
       rw [heq]
       omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       obtain ⟨dm, hdm, rfl⟩ := sdepth_downL a _ _ x _ hne h2 hd
       have hne2 : x ≠ a_2 := fun he => h3 ((beq_iff_eq).mpr he)
       have hlt : a_2 < x := by omega
       obtain ⟨d1, hd1, rfl⟩ := sdepth_downR a_2 _ _ x _ hne2 hlt hdm
       have heq := ih d1 hd1
       rw [heq]
       omega)
  · intro a a_1 h1 h2 d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_neg h2]; simp [sdepth, h1, h2] at hd)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       have hlt2 : a < x := by omega
       obtain ⟨dm, hdm, rfl⟩ := sdepth_downR a _ _ x _ hne hlt2 hd
       have hdm0 : dm = 0 := by
          simp [sdepth, h3] at hdm
          omega
       omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       have hlt2 : a < x := by omega
       obtain ⟨dm, hdm, rfl⟩ := sdepth_downR a _ _ x _ hne hlt2 hd
       have hne2 : x ≠ a_2 := fun he => h3 ((beq_iff_eq).mpr he)
       obtain ⟨d1, hd1, rfl⟩ := sdepth_downR a_2 _ _ x _ hne2 h4 hdm
       have heq := ih d1 hd1
       rw [heq]
       omega)
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih d hd
    cases a_1 <;> simp only [ecount] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       have hlt2 : a < x := by omega
       obtain ⟨dm, hdm, rfl⟩ := sdepth_downR a _ _ x _ hne hlt2 hd
       have hne2 : x ≠ a_2 := fun he => h3 ((beq_iff_eq).mpr he)
       have hlt4 : x < a_2 := by omega
       obtain ⟨d1, hd1, rfl⟩ := sdepth_downL a_2 _ _ x _ hne2 hlt4 hdm
       have heq := ih d1 hd1
       rw [heq]
       omega)
