-- WP-6 STEPS C170 (positional program): Terminal C service-vs-D6 kernel.
--
-- Self-contained (repo convention: no imports). Terminal C establishes the
-- exact logical position of DIRECT-D6 (D <= 6*S_A) relative to service
-- (paid == need every present KEEP, i.e. MSTL-14P discharge success):
--   (i)   D6-def identity: D - 6*S_A = 2*(E_B - 3*S_A) - slack, with
--         slack >= 0 per access (D2 banked: need <= 2*e_B; DELETE terms
--         cancel exactly). Hence DIRECT-D6 <=> GC-def <= slack/2.
--   (ii)  service => D6 (D6 NECESSARY): conservation (injected = pool +
--         spent, all >= 0) + injection 6 per sited Aev + spent = D under
--         paid==need give 6*S_A = pool + D >= D. Pure arithmetic.
--   (iii) NO-WEAKER-SUBSTITUTE: any X with (D6 => X) and (X => service)
--         satisfies (X => D6) by transitivity with (ii); so no strictly
--         weaker sufficient obligation exists. Propositional closure.
-- Consequence: D6 is the UNIQUE minimal cumulative obligation (necessary;
-- sufficient together with the banked activation machinery C4). The bypass
-- hope (a weaker X implying service) is REFUTED as a matter of logic.
-- Proving D6 remains load-bearing (same wall: D6 <=> GC-def <= slack/2).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- (i) Slack identity: sum of per-access (2*e_B - need) equals 2*E_B - D
-- (exact list distributivity; DELETE terms absent on both sides since
-- DELETE contributes no need and no B-events).
theorem slack_identity (eBs needs : List Nat) (h : eBs.length = needs.length) :
    ((eBs.zip needs).map (fun p => 2 * (p.1 : Int) - (p.2 : Int))).sum
      = 2 * (eBs.map Nat.cast).sum - (needs.map Nat.cast).sum := by
  induction eBs generalizing needs with
  | nil =>
    cases needs with
    | nil =>
      simp
    | cons nd nds =>
      simp at h
  | cons eb ebs ih =>
    cases needs with
    | nil =>
      simp at h
    | cons nd nds =>
      have hlen : ebs.length = nds.length := by
        simp only [List.length] at h
        omega
      have hih := ih nds hlen
      simp only [List.zip, List.zipWith, List.map_cons, List.sum_cons]
        at hih ⊢
      omega

-- Slack is nonnegative under the banked D2 per-access bound
-- (need <= 2*e_B; AR-05). Hence D6-def <= 2*GC-def always.
theorem slack_nonneg (pairs : List (Nat × Nat))
    (hD2 : ∀ p ∈ pairs, p.2 ≤ 2 * p.1) :
    0 ≤ (pairs.map (fun p => 2 * (p.1 : Int) - (p.2 : Int))).sum := by
  induction pairs with
  | nil =>
    simp
  | cons hd tl ih =>
    simp only [List.map_cons, List.sum_cons]
    have h1 : hd.2 ≤ 2 * hd.1 := hD2 _ (List.Mem.head _)
    have h2 : ∀ p ∈ tl, p.2 ≤ 2 * p.1 :=
      fun p hp => hD2 p (List.Mem.tail _ hp)
    have h3 := ih h2
    omega

-- Banked route in kernel: GC counting + slack gives D6.
theorem d6_of_gc (D EB SA slack : Int)
    (hid : D - 6 * SA = 2 * (EB - 3 * SA) - slack)
    (hGC : EB - 3 * SA ≤ 0) (hslack : 0 ≤ slack) :
    D - 6 * SA ≤ 0 := by
  omega

-- (ii) Service implies D6. Abstract ledger: injected I (= 6 per sited
-- Aev), pool P (>= 0: LATENT+ACTIVE), spent S (= D under paid==need).
-- Conservation I = P + S gives D = S <= I = 6*S_A.
theorem service_implies_D6 (SA D I P S : Nat)
    (hInj : I = 6 * SA) (hCons : I = P + S) (hPaid : S = D) :
    D ≤ 6 * SA := by
  omega

-- (iii) No strictly-weaker sufficient obligation. If X is weaker than D6
-- (D6 => X) and X suffices for service (X => Svc), then with (ii)
-- (Svc => D6) we get X => D6: X is equivalent, not strictly weaker.
theorem no_weaker_substitute (D6 X Svc : Prop)
    (_hW : D6 → X) (hS : X → Svc) (hN : Svc → D6) : X → D6 := by
  exact fun x => hN (hS x)

-- D6-MICRO: a synced (0,1) step charges at most 1 (e_A = 0 forces dA = 0;
-- e_B = 1 forces dB in {1,2}; need = dB - 1 <= 1). Buffer >= 1 covers it
-- (Lemma B AUTHOR banking; finite buf01_min 13 on the GC pool).
theorem d6_micro01_charge (dA dB : Nat)
    (_hA : (dA + 1) / 2 = 0) (hB : (dB + 1) / 2 = 1) : dB - 1 ≤ 1 := by
  omega

-- FIRST-VIOLATION GEOMETRY: a KEEP step with dB <= 5*dA + 1 + B cannot
-- cross a D6-buffer of B (contrapositive: first crossing needs
-- dB > 5*dA + 1 + B -- extreme divergence, same node as GC's 3*dA).
-- need is Nat-truncated (max(dB-2*dA-1,0)); e_A = (dA+1)/2 exact.
theorem d6_no_first_violation (dA dB B : Nat) (h : dB ≤ 5 * dA + 1 + B) :
    dB - 2 * dA - 1 ≤ 6 * ((dA + 1) / 2) + B := by
  omega

-- SLACK STRUCTURE: per-access D2-slack (2*e_B - need, Int exact) is
-- quantified by depth shape. Positive need leaves >= 2*dA+1 slack;
-- need-free accesses leave >= dB slack (their full depth credit).
theorem slack_of_needpos (dA dB : Nat) (h : 2 * dA + 1 < dB) :
    2 * dA + 1 ≤ 2 * ((dB + 1) / 2 : Nat) - (dB - 2 * dA - 1 : Nat) := by
  omega

theorem slack_ge_depth (dB : Nat) : dB ≤ 2 * ((dB + 1) / 2 : Nat) := by
  omega

-- ISOLATED RATE HYPOTHESIS: the single open premise for DIRECT-D6.
-- With GC-deficit bounded by half the slack pool, D6 follows from the
-- deficit identity. Everything else in this file is kernel-closed
-- around it.
theorem d6_of_rate (D EB SA slack : Int)
    (hid : D - 6 * SA = 2 * (EB - 3 * SA) - slack)
    (hrate : EB - 3 * SA ≤ slack / 2) :
    D - 6 * SA ≤ 0 := by
  omega
