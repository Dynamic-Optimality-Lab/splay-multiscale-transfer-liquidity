-- WP-6 PIVOT-14: abstract cyclic genealogy kernel (U1/U2/U3 + quiet/disjoint).
--
-- Certifies the DESCENT LOGIC and interconnect of audits/PIVOT_UNIVERSALIZE_U1U4.md
-- on an abstract cyclic access model. Splay facts enter ONLY as hypotheses
-- (no new axioms). All binders are explicit (no section-variable reliance).
-- The mechanical verification that real splay logs satisfy the hypotheses is
-- AUTHOR (paper sections B/D); same-key block disjointness is AUTHOR (paper H);
-- U4 (closed-component capacity) is NOT in this file.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

def accessRank (nn r : Nat) : Nat := r / nn

-- Downward search: latest rank strictly below hi satisfying test, checking
-- hi-1, hi-2, ... (fuel many). Returns the GREATEST satisfying rank.
def latestBelowAux : (Nat → Bool) → Nat → Nat → Option Nat
  | _, _, 0 => none
  | test, hi, f + 1 =>
    if hi = 0 then none
    else if test (hi - 1) then some (hi - 1)
    else latestBelowAux test (hi - 1) f

theorem lbA_zero (test : Nat → Bool) (hi : Nat) :
    latestBelowAux test hi 0 = none := rfl

theorem lbA_succ (test : Nat → Bool) (hi f : Nat) :
    latestBelowAux test hi (f + 1) =
      (if hi = 0 then none
       else if test (hi - 1) then some (hi - 1)
       else latestBelowAux test (hi - 1) f) := rfl

theorem latestBelow_lt (test : Nat → Bool) (hi f r : Nat)
    (h : latestBelowAux test hi f = some r) : r < hi := by
  induction f generalizing hi with
  | zero => rw [lbA_zero] at h; simp at h
  | succ f ih =>
    rw [lbA_succ] at h
    by_cases hz : hi = 0
    · rw [if_pos hz] at h; simp at h
    · rw [if_neg hz] at h
      by_cases ht : test (hi - 1)
      · rw [if_pos ht] at h
        simp at h
        omega
      · rw [if_neg ht] at h
        have := ih (hi - 1) h
        omega

theorem latestBelow_max (test : Nat → Bool) (hi f r : Nat)
    (h : latestBelowAux test hi f = some r) :
    ∀ r', r < r' → r' < hi → test r' = false := by
  induction f generalizing hi with
  | zero => rw [lbA_zero] at h; simp at h
  | succ f ih =>
    intro r' hr1 hr2
    rw [lbA_succ] at h
    by_cases hz : hi = 0
    · rw [if_pos hz] at h; simp at h
    · rw [if_neg hz] at h
      by_cases ht : test (hi - 1)
      · rw [if_pos ht] at h
        simp at h
        omega
      · rw [if_neg ht] at h
        by_cases heq : r' = hi - 1
        · cases htb : test (hi - 1) with
          | true => rw [htb] at ht; simp at ht
          | false => rw [heq]; exact htb
        · exact ih (hi - 1) h r' (by omega) (by omega)

theorem latestBelow_mem (test : Nat → Bool) (hi f r : Nat)
    (h : latestBelowAux test hi f = some r) : test r = true := by
  induction f generalizing hi with
  | zero => rw [lbA_zero] at h; simp at h
  | succ f ih =>
    rw [lbA_succ] at h
    by_cases hz : hi = 0
    · rw [if_pos hz] at h; simp at h
    · rw [if_neg hz] at h
      by_cases ht : test (hi - 1)
      · rw [if_pos ht] at h
        simp at h
        subst h
        exact ht
      · rw [if_neg ht] at h; exact ih (hi - 1) h

-- Single-path x-line descent with fuel (U1 core), bind-form for rewriting.
def descX (nn : Nat) (est : Nat → Nat → Option Nat) (consumedX : Nat → Nat) :
    Nat → Nat → Nat → Option Nat
  | _, _, 0 => none
  | e, R, f + 1 =>
    (est e R).bind fun r' =>
      if accessRank nn r' = accessRank nn R then
        descX nn est consumedX (consumedX r') r' f
      else some r'

theorem descX_zero (nn : Nat) (est : Nat → Nat → Option Nat)
    (consumedX : Nat → Nat) (e R : Nat) :
    descX nn est consumedX e R 0 = none := rfl

theorem descX_succ (nn : Nat) (est : Nat → Nat → Option Nat)
    (consumedX : Nat → Nat) (e R f : Nat) :
    descX nn est consumedX e R (f + 1) =
      ((est e R).bind fun r' =>
        if accessRank nn r' = accessRank nn R then
          descX nn est consumedX (consumedX r') r' f
        else some r') := rfl

-- Same-access ranks order by seq (needs nn > 0). Manual: substitute the
-- shared quotient so omega sees one nonlinear atom consistently.
theorem sameAcc_seq_lt (nn a b : Nat)
    (hsame : a / nn = b / nn) (hlt : a < b) : a % nn < b % nn := by
  have ha := Nat.div_add_mod a nn
  have hb := Nat.div_add_mod b nn
  rw [hsame] at ha
  omega

-- Soundness: every result lies strictly after epochStart.
theorem descX_sound (nn : Nat)
    (est : Nat → Nat → Option Nat)
    (consumedX : Nat → Nat) (isX : Nat → Bool) (epochStart : Nat)
    (hEx : ∀ e R, isX e = true → epochStart < accessRank nn R →
      ∃ r, est e R = some r ∧
        (accessRank nn r ≠ accessRank nn R → epochStart < accessRank nn r)) :
    ∀ (e R fuel : Nat),
    isX e = true → epochStart < accessRank nn R →
    (∀ e' R', isX e' = true → epochStart < accessRank nn R' →
      isX (consumedX R') = true) →
    ∀ r, descX nn est consumedX e R fuel = some r →
      epochStart < accessRank nn r := by
  intro e R fuel
  induction fuel generalizing e R with
  | zero =>
    intro _ _ _ r h; rw [descX_zero] at h; simp at h
  | succ f ih =>
    intro hx hR hcons r h
    rw [descX_succ] at h
    cases hest : est e R with
    | none => rw [hest, Option.bind_none] at h; simp at h
    | some r' =>
      rw [hest, Option.bind_some] at h
      by_cases hsame : accessRank nn r' = accessRank nn R
      · rw [if_pos hsame] at h
        have hR' : epochStart < accessRank nn r' := hsame ▸ hR
        have hx' : isX (consumedX r') = true := hcons e r' hx hR'
        exact ih (consumedX r') r' hx' hR' hcons r h
      · rw [if_neg hsame] at h
        simp at h; subst h
        obtain ⟨r0, hr0, hprior⟩ := hEx e R hx hR
        have heq : r' = r0 := by
          rw [hr0] at hest; cases hest; rfl
        subst heq
        exact hprior hsame

-- Completeness: fuel nn always suffices.
theorem descX_complete (nn : Nat) (hnn : 0 < nn)
    (est : Nat → Nat → Option Nat)
    (hE1 : ∀ e R r, est e R = some r → r < R)
    (consumedX : Nat → Nat) (isX : Nat → Bool) (epochStart : Nat)
    (hEx : ∀ e R, isX e = true → epochStart < accessRank nn R →
      ∃ r, est e R = some r ∧
        (accessRank nn r ≠ accessRank nn R → epochStart < accessRank nn r)) :
    ∀ (f e R : Nat),
    R % nn + 1 ≤ f →
    isX e = true → epochStart < accessRank nn R →
    (∀ e' R', isX e' = true → epochStart < accessRank nn R' →
      isX (consumedX R') = true) →
    descX nn est consumedX e R f ≠ none := by
  intro f
  induction f with
  | zero =>
    intro e R hle _ _ _ h
    have hmod : R % nn < nn := Nat.mod_lt R hnn
    omega
  | succ f ih =>
    intro e R hle hx hR hcons hnone
    rw [descX_succ] at hnone
    cases hest : est e R with
    | none =>
      rw [hest, Option.bind_none] at hnone
      simp at hnone
      obtain ⟨r0, hr0, _⟩ := hEx e R hx hR
      rw [hest] at hr0; simp at hr0
    | some r' =>
      rw [hest, Option.bind_some] at hnone
      by_cases hsame : accessRank nn r' = accessRank nn R
      · rw [if_pos hsame] at hnone
        have hlt : r' < R := hE1 e R r' hest
        have hseqdec : r' % nn < R % nn := sameAcc_seq_lt nn r' R hsame hlt
        have hR' : epochStart < accessRank nn r' := hsame ▸ hR
        have hx' : isX (consumedX r') = true := hcons e r' hx hR'
        have hle' : r' % nn + 1 ≤ f := by omega
        exact ih (consumedX r') r' hle' hx' hR' hcons hnone
      · rw [if_neg hsame] at hnone
        simp at hnone

-- Every returned rank precedes the query bound.
theorem descX_lt (nn : Nat)
    (est : Nat → Nat → Option Nat)
    (hE1 : ∀ e R r, est e R = some r → r < R)
    (consumedX : Nat → Nat) :
    ∀ (e R fuel c : Nat),
    descX nn est consumedX e R fuel = some c → c < R := by
  intro e R fuel
  induction fuel generalizing e R with
  | zero => intro c h; rw [descX_zero] at h; simp at h
  | succ f ih =>
    intro c h
    rw [descX_succ] at h
    cases hest : est e R with
    | none => rw [hest, Option.bind_none] at h; simp at h
    | some r' =>
      have hlt : r' < R := hE1 e R r' hest
      rw [hest, Option.bind_some] at h
      by_cases hsame : accessRank nn r' = accessRank nn R
      · rw [if_pos hsame] at h
        exact Nat.lt_trans (ih (consumedX r') r' c h) hlt
      · rw [if_neg hsame] at h
        simp at h; subst h; exact hlt

-- U1 packaged: with fuel nn, the x-line yields an in-epoch strictly-prior rank.
theorem cyclic_creator_exists (nn : Nat) (hnn : 0 < nn)
    (est : Nat → Nat → Option Nat)
    (hE1 : ∀ e R r, est e R = some r → r < R)
    (consumedX : Nat → Nat) (isX : Nat → Bool) (epochStart : Nat)
    (hEx : ∀ e R, isX e = true → epochStart < accessRank nn R →
      ∃ r, est e R = some r ∧
        (accessRank nn r ≠ accessRank nn R → epochStart < accessRank nn r))
    (e R : Nat)
    (hx : isX e = true)
    (hR : epochStart < accessRank nn R)
    (hcons : ∀ e' R', isX e' = true → epochStart < accessRank nn R' →
      isX (consumedX R') = true)
    (hseq : R % nn < nn) :
    ∃ c, descX nn est consumedX e R nn = some c ∧
      epochStart < accessRank nn c ∧ c < R := by
  have hmod : R % nn < nn := Nat.mod_lt R hnn
  have hle : R % nn + 1 ≤ nn := by omega
  have hne : descX nn est consumedX e R nn ≠ none :=
    descX_complete nn hnn est hE1 consumedX isX epochStart hEx
      nn e R hle hx hR hcons
  obtain ⟨c, hc⟩ := Option.ne_none_iff_exists.mp hne
  have hc' : descX nn est consumedX e R nn = some c := hc.symm
  exact ⟨c, hc',
    descX_sound nn est consumedX isX epochStart hEx
      e R nn hx hR hcons c hc',
    descX_lt nn est hE1 consumedX e R nn c hc'⟩
