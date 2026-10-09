-- WP-6 STEPS C163 (positional program): micro-coupling kernel core.
--
-- Self-contained (repo convention: no imports). Micro-coupling is the
-- synced-trivial branch of prefix-GC: synced depths (d^B <= d^A + 2) give
-- overflow <= 1 (C162 sync_overflow_le); overflow 0 is free (slack
-- nondecreasing); overflow 1 is exactly the (0,1) splash, which consumes
-- exactly 1 from a buffer >= 1 (buffer supplied by Lemma B banking,
-- 8AC-AROOT; finite micro.json: buffer >= 13 before all 689 (0,1)
-- splashes). Proved: the case disjunction + both step facts (pure Nat
-- arithmetic; counts are (d+1)/2 by C161+C162). Composition (prose):
-- synced step preserves prefix-GC given Lemma B buffer on (0,1) steps.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- MICRO-COUPLING DISJUNCTION: synced depths leave overflow <= 0 or the
-- exact (0,1) splash (e_A = 0 and e_B = 1, witnessed via (d+1)/2 counts).
theorem micro_couple (dA dB : Nat) (hsync : dB ≤ dA + 2) :
    (dB + 1) / 2 ≤ 3 * ((dA + 1) / 2) ∨
      ((dA + 1) / 2 = 0 ∧ (dB + 1) / 2 = 1) := by
  omega

-- COVERED STEP: overflow <= 0 never decreases the buffer.
theorem micro_step_zero (Phi eA eB : Nat) (h : eB ≤ 3 * eA) :
    Phi ≤ Phi + 3 * eA - eB := by
  omega

-- (0,1) STEP: from buffer >= 1 consumes exactly one (no Nat floor).
theorem micro_step_one (Phi : Nat) (h : 1 ≤ Phi) :
    Phi + 3 * 0 - 1 + 1 = Phi := by
  omega
