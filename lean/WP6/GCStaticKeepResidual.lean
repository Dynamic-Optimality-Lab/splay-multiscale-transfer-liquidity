-- WP-6 STEP C183-2 (positional program): KEEP-RESIDUAL epoch-induction scaffold.
--
-- Self-contained (repo convention: no imports). Finite campaign C183-2
-- (scripts/wp6_keepres.py + beam/deepdiv/walk48) leaves three survivors and
-- two refutations:
--   REFUTED: PREPEND-2 (unbounded linear saving n/4-1 on vines; splay
--     non-monotonicity), ROOT-COLLAPSE both forms (same-root +1 n=32;
--     post-KEEP reachable +1). H2 = max(H1,Q) must be carried, never collapsed.
--   SURVIVORS (finite-held, zero kills): H2-IDENTITY (DEL2 branch redundant),
--     DELETE-H2 (H2(D_z) <= H2 + 3*a_z), KEEP-RESIDUAL reach (Q_x <= Phi).
-- This file kernelizes the exact arithmetic those survivors buy:
--   (i)    H2-identity is a COROLLARY of BD1 (8AC-BD1): on a DELETE state
--          B is frozen, so DEL2(z) = H1(D_z) - 3*a_z <= H1 by BD1.
--   (ii)   DELETE step preserves Phi >= H2 from DELETE-H2 alone.
--   (iii)  KEEP step: KEEP-RESIDUAL bounds the one-step lookahead H1(K_x);
--          with the KEEP-2STEP hypothesis (two-step lookahead bound at the
--          post-state) the full Phi >= H2 invariant is preserved.
--   (iv)   Phi >= H2 gives GC (Phi >= 0) since H2 >= 0.
-- OPEN premises (explicit hypotheses, finite-held C183-2, NOT proved here):
-- delete_h2, keep_res, keep2. Together with BD1-ride-induction (deferred,
-- 8AC-BD1) they imply the epoch invariant; KEEP-2STEP is the remaining
-- rate-adjacent gap. Conditional scaffold, not a proof claim.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- (i) BD1 per-key corollary: DEL2(z) = hz - 3a <= H1 from BD1 hz <= H1 + 3a.
theorem del2_le_h1_of_bd1 (hz a H1 : Int)
    (hBD1 : hz ≤ H1 + 3 * a) : hz - 3 * a ≤ H1 := by
  omega

-- H2-identity: DEL2max <= H1 forces max(max H1 Q) DEL2max = max H1 Q.
theorem h2_identity_of_bd1 (H1 Q del2max : Int)
    (hdel : del2max ≤ H1) : max (max H1 Q) del2max = max H1 Q := by
  omega

-- H2 is nonnegative from H1 >= 0 (H1 = max(0, ...) by definition).
theorem h2_nonneg (H1 Q : Int) (hH1 : 0 ≤ H1) : 0 ≤ max H1 Q := by
  omega

-- (ii) DELETE preservation: Phi' = Phi + 3a (A-events bank, B frozen),
-- H2' <= H2 + 3a (DELETE-H2) keep Phi' >= H2' from Phi >= H2.
theorem delete_preserves (Phi H2 H2' a : Int)
    (hInv : H2 ≤ Phi) (hDel : H2' ≤ H2 + 3 * a) :
    H2' ≤ Phi + 3 * a := by
  omega

-- DELETE preservation in update form (Phi' named).
theorem delete_preserves_upd (Phi H2 H2' Phi' a : Int)
    (hInv : H2 ≤ Phi) (hDel : H2' ≤ H2 + 3 * a)
    (hPhi : Phi' = Phi + 3 * a) : H2' ≤ Phi' := by
  omega

-- (iii) KEEP one-step bound: Q_x = r + H1K with r = b - 3a and Q_x <= Phi
-- (KEEP-RESIDUAL) plus eB = b (C161-162 exact e_B = ceil(d/2)) give
-- H1(K_x) <= Phi + 3a - eB = Phi'.
theorem keep_h1_of_keepres (Qx r H1K b a Phi eB : Int)
    (hQ : Qx = r + H1K) (hr : r = b - 3 * a)
    (hKR : Qx ≤ Phi) (heB : eB = b) :
    H1K ≤ Phi + 3 * a - eB := by
  omega

-- KEEP full preservation from the one-step bound + KEEP-2STEP hypothesis
-- (Q2 <= Phi' at the post-state) + H2-identity at the post-state.
theorem keep_preserves_of_keep2 (Phi a eB H1K Q2 H2' Phi' : Int)
    (hH1 : H1K ≤ Phi + 3 * a - eB)
    (hQ2 : Q2 ≤ Phi + 3 * a - eB)
    (hH2 : H2' = max H1K Q2)
    (hPhi : Phi' = Phi + 3 * a - eB) : H2' ≤ Phi' := by
  omega

-- (iv) GC discharge: the invariant implies Phi >= 0.
theorem gc_of_invariant (Phi H2 : Int)
    (hInv : H2 ≤ Phi) (hNN : 0 ≤ H2) : 0 ≤ Phi := by
  omega

-- (v) C184 §2 EXPANSION identities (mission: must be proved algebraically).
-- Phi_after = Phi - r for a KEEP (banking 3a - eB with eB = b exact).
theorem phi_after_keep (Phi a eB b r Phi' : Int)
    (hr : r = b - 3 * a) (heB : eB = b)
    (hPhi : Phi' = Phi + 3 * a - eB) : Phi' = Phi - r := by
  omega

-- One-term case: Q(s1) = 0 forces KR2 = r - Phi.
theorem kr2_expand_1 (r Q1 Phi KR2 : Int)
    (hQ : Q1 = 0) (hKR : KR2 = r + Q1 - Phi) : KR2 = r - Phi := by
  omega

-- Two-term case: Q(s1) = r_y + H1s2 with H1s2 = 0.
theorem kr2_expand_2 (r ry H1s2 Phi KR2 Q1 : Int)
    (hQ : Q1 = ry + H1s2) (hH : H1s2 = 0)
    (hKR : KR2 = r + Q1 - Phi) : KR2 = r + ry - Phi := by
  omega

-- Three-term case: Q(s1) = r_y + H1s2 with H1s2 = r_z > 0.
theorem kr2_expand_3 (r ry rz Phi KR2 Q1 H1s2 : Int)
    (hQ : Q1 = ry + H1s2) (hH : H1s2 = rz)
    (hKR : KR2 = r + Q1 - Phi) : KR2 = r + ry + rz - Phi := by
  omega

-- (vi) C184 ROOT-NOOP collapse (case (a)): splaying the just-KEPT root x
-- is a no-op (0 events, tree fixed), so r_x(s1) = 0 and Q_x(s1) = H1(s1).
-- If the Q-maximum is attained (or tied) at x, KEEP-2STEP IS KEEP-RESIDUAL.
theorem keep2step_of_attainer (r H1s1 Phi KR2 Q1 : Int)
    (hAtt : Q1 = H1s1)
    (hKR : r + H1s1 ≤ Phi)
    (hKR2 : KR2 = r + Q1 - Phi) : KR2 ≤ 0 := by
  omega

-- (vii) C184 hard-core gap bound (case (b), y ≠ x attainer): with
-- Q1 = r_y + H1s2 and r_y ≤ H1s1 (H1 dominates every key residual),
-- the excess of KR2 over the KEEP-RESIDUAL bound is at most H1(s2).
-- This is the proved "future compression" half; the remaining gap is
-- H1(s2) against historical bank (last-reset nesting, open).
theorem keep2_gap_le_h1s2 (r Q1 H1s1 ry H1s2 Phi KR2 : Int)
    (hQ : Q1 = ry + H1s2) (hDom : ry ≤ H1s1)
    (hKR : r + H1s1 ≤ Phi)
    (hKR2 : KR2 = r + Q1 - Phi) : KR2 ≤ H1s2 := by
  omega

-- (viii) C184 LIPSCHITZ induction steps (conditional skeleton): with R3
-- the worst ≤3-KEEP drain from a state, P(h) : Phi(h) ≥ R3(end(h))
-- propagates across each transition from the one-step Lipschitz bounds.
-- Finite status C184: DELETE-Lip clean everywhere tested (incl. arbitrary
-- pairs); KEEP-Lip clean on all reachable states tested (+1 failure on
-- rare large arbitrary pairs). Both remain explicit hypotheses here.
theorem lip_delete_step (R3p R3d Phi_p Phi_d a : Int)
    (hP : R3p ≤ Phi_p)
    (hLip : R3d ≤ R3p + 3 * a)
    (hPhi : Phi_d = Phi_p + 3 * a) : R3d ≤ Phi_d := by
  omega

theorem lip_keep_step (R3p R3k Phi_p Phi_k r : Int)
    (hP : R3p ≤ Phi_p)
    (hLip : R3k ≤ R3p - r)
    (hPhi : Phi_k = Phi_p - r) : R3k ≤ Phi_k := by
  omega

-- Diagonal base: R3 = 0 on a diagonal (root residual 0, Q = 0).
theorem lip_diag_base (R3diag : Int)
    (hR : R3diag = 0) : R3diag ≤ 0 := by
  omega

-- (ix) C184-3 DELETE z-CHAIN EXACTNESS (conditional arithmetic core).
-- Post-DELETE z is A-rooted (a_z(D) = 0, z just splayed) so r_z(D) = b_z;
-- K_z(D_z(p)) and K_z(p) are the SAME pair-state (splaying the A-root is
-- a no-op with 0 events; B-side is the identical KEEP z), hence their Q
-- values agree; the z-chain x = z therefore grows by exactly 3 * a_z.
-- Model obligations [MODEL] (need splay/tree model: root-noop identity
-- + 0 events, K-state agreement): hRoot, hSame. Finite: R3-attainer is z
-- itself in 98.6% of sampled post-DELETE states (512/525 → 414/420), and
-- every tight DELETE-Lip case observed has attainer z.
theorem delete_zchain_exact (rzD rzP QzD QzP bz az : Int)
    (hRoot : rzD = bz) (hSame : QzD = QzP)
    (hrP : rzP = bz - 3 * az) :
    rzD + QzD = (rzP + QzP) + 3 * az := by
  omega

-- z-part bound: since R3(p) dominates every chain at p (max), the exact
-- z-chain growth gives its Lipschitz share with no drop analysis.
theorem delete_r3_zpart (R3p zchainD zchainP az : Int)
    (hDom : zchainP ≤ R3p)
    (hExact : zchainD = zchainP + 3 * az) :
    zchainD ≤ R3p + 3 * az := by
  omega

