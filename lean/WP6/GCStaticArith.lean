-- WP-6 STEP C68: GC-STATIC arithmetic cores II (Layer B: sited-always + residual).
--
-- 8S SITED-ALWAYS core: a splay StepEv triple (lo,hi) = (min,max) of ≥2 distinct
-- keys has lo < hi; sites exist: i = lo witnesses 1 ≤ i < n ∧ i+1 ≤ hi over
-- [lo,hi). Pure Nat (no splay model needed). Layer A (hall_lemmas.md 8S) supplies
-- lo<hi from rotation geometry (node ≠ p distinct keys) and consumes existence.
-- 8I/8J RESIDUAL identities: per-access (q ≤ 3f + o) assembly to global
-- (Q ≤ 3F + O) with disjoint fresh; deficit-one/peel already in StageBArith.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- 8S-core: site witness at i = lo.
theorem sited_always (lo hi n : Nat) (h1 : 1 ≤ lo) (h2 : lo < hi) (h3 : hi ≤ n) :
    ∃ i, lo ≤ i ∧ i < hi ∧ 1 ≤ i ∧ i < n ∧ i + 1 ≤ hi := by
  exact ⟨lo, by omega, by omega, by omega, by omega, by omega⟩

-- 8S-corollary: any interval with lo < hi inside [1,n] is non-sited-empty,
-- i.e. ¬ (∀ i ∈ [lo,hi), ¬ site): equivalently the witness above.
theorem sited_nonempty (lo hi n : Nat) (h1 : 1 ≤ lo) (h2 : lo < hi) (h3 : hi ≤ n) :
    ¬ ∀ i, lo ≤ i → i < hi → ¬(1 ≤ i ∧ i < n ∧ i + 1 ≤ hi) := by
  obtain ⟨i, hlo, hhi, h1i, hni, hsi⟩ := sited_always lo hi n h1 h2 h3
  exact fun h => h i hlo hhi ⟨h1i, hni, hsi⟩

-- 8I-shape: two-block residual assembly (disjoint fresh f1 f2, overflows o1 o2).
-- If q1 ≤ 3*f1 + o1 and q2 ≤ 3*f2 + o2 then q1+q2 ≤ 3*(f1+f2) + (o1+o2).
theorem residual_two (q1 f1 o1 q2 f2 o2 : Nat)
    (h1 : q1 ≤ 3 * f1 + o1) (h2 : q2 ≤ 3 * f2 + o2) :
    q1 + q2 ≤ 3 * (f1 + f2) + (o1 + o2) := by
  omega

-- 8I-corollary: non-heavy blocks (o = 0) contribute no overflow.
theorem residual_nonheavy (q1 f1 q2 f2 o2 : Nat)
    (h1 : q1 ≤ 3 * f1) (h2 : q2 ≤ 3 * f2 + o2) :
    q1 + q2 ≤ 3 * (f1 + f2) + o2 := by
  omega

-- 8J-shape: latest-block necessity (|Q_L| ≥ 3|U_L| + 1 from Δ(Q)=1, Δ(Q_<L)≤0).
-- With q = q0 + qL, n = n0 + u, q0 ≤ 3*n0 (IH on strict subset), q = 3*n + 1:
-- qL ≥ 3*u + 1. (Nat subtraction needs 3*n0 ≤ q0 side condition, from IH form
-- q0 + s = 3*n0 with slack s; we take the clean form with explicit slack.)
theorem latest_block (q0 n0 qL u s : Nat) (hIH : q0 + s = 3 * n0)
    (hD : q0 + qL = 3 * (n0 + u) + 1) : 3 * u + 1 ≤ qL := by
  omega

-- 8AB-shape: heavy-block new-source bound (if overflow o needs 3·new cover and
-- new ≥ 1 (root-hit) plus K-anchored k with cap 3 each: o ≤ 3*(1 + k) + t with
-- transient top-up t). Assembly identity for the counting closure attempt.
theorem heavy_cover (o k t : Nat) (h : o ≤ 3 * (1 + k) + t) :
    o ≤ 3 + 3 * k + t := by
  omega

-- 8S end-to-end (C109): splay StepEv triples (two-key zig / three-key double,
-- distinct keys by rotation mechanics: node ≠ parent/grandparent) have lo < hi,
-- hence sites exist by sited_always. Triple modeled as key-list with pairwise
-- distinctness; lo/hi as min/max. Callers (Layer A) supply distinctness from
-- rotation geometry + BST key separation. This closes 8S in kernel: every
-- StepEv banks sited supply (S_A = #A-StepEvs, no filtering).
theorem triple_lo_lt_hi2 (a b : Nat) (h : a ≠ b) :
    min a b < max a b := by
  omega

theorem triple_lo_lt_hi3 (a b c : Nat) (hbc : b ≠ c) :
    min (min a b) c < max (max a b) c := by
  omega

-- 8S closed: two-key triple always sited (needs lo ≥ 1 from key validity + hi ≤ n).
theorem sited_zig (a b n : Nat) (hab : a ≠ b) (h1 : 1 ≤ min a b) (hn : max a b ≤ n) :
    ∃ i, min a b ≤ i ∧ i < max a b ∧ 1 ≤ i ∧ i < n ∧ i + 1 ≤ max a b :=
  sited_always (min a b) (max a b) n h1 (triple_lo_lt_hi2 a b hab) hn

-- 8S closed: three-key triple always sited.
theorem sited_double (a b c n : Nat) (hbc : b ≠ c)
    (h1 : 1 ≤ min (min a b) c) (hn : max (max a b) c ≤ n) :
    ∃ i, min (min a b) c ≤ i ∧ i < max (max a b) c ∧ 1 ≤ i ∧ i < n ∧
      i + 1 ≤ max (max a b) c :=
  sited_always _ _ n h1 (triple_lo_lt_hi3 a b c hbc) hn
