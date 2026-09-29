-- WP-6 STEP AR-17/18/19: Stage-B fresh-channel pigeonholes (Layer B arithmetic).
--
-- Exact Nat lemmas behind FRESH-CAP (E1-CAP instance) and DILUTION-ZERO.
-- f = fresh slots (|E1| case (a); pristine-|E4| case (b)); eB = B-StepEvs of the
-- demanding KEEP; used = in-access picks already landed on fresh (Layer A proves
-- used <= eB - 1 before the eB-th event; fresh loads come only from in-access
-- picks: E1 via E2/E4-earlier + E3-same-access; pristine-E4 via run-interior
-- x-only + creation-at-setup). f >= 1 for every demanding KEEP (FRESH-CHANNEL).
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0
-- (repo WP-1/WP-2 precedent; lakefile untouched).

-- WP-6 STEP AR-17: FRESH-CAP-2 (a sub-cap-3 slot remains).
theorem freshcap_two (f eB used : Nat) (hF : 1 ≤ f) (h : used ≤ eB - 1)
    (hB : eB ≤ 3 * f) : used < 3 * f := by
  omega

-- WP-6 STEP AR-18: FRESH-CAP-1 (a sub-cap-2 slot remains).
theorem freshcap_one (f eB used : Nat) (hF : 1 ≤ f) (h : used ≤ eB - 1)
    (hB : eB ≤ 2 * f) : used < 2 * f := by
  omega

-- WP-6 STEP AR-19: DILUTION-ZERO (a zero slot remains).
theorem dilution_zero (f eB used : Nat) (hF : 1 ≤ f) (h : used ≤ eB - 1)
    (hB : eB ≤ f) : used < f := by
  omega
