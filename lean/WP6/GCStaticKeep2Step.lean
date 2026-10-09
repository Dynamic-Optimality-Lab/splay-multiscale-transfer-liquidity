-- WP-6 STEP C185 (positional program): tree H1/Q/R3 layer + grounded z-exactness.
--
-- Self-contained (repo convention: no imports). Splay skeleton + ecount
-- mirror the banked kernel (GCStaticLoop/History/StepCount: same arms).
-- New layer: exact per-key residuals and H1/Q/R3 over finite key lists,
-- matching `scripts/wp6_keepres.py`/`wp6_keep2step.py` semantics with
-- ecount as the exact StepEv count (kernel ecount_eq C161: ecount = ceil
-- of depth; present-domain locked so every listed key is present).
-- Proved: root splay is identity (splay_at_root, same proof as banked);
-- ecount at a self-root is 0; fold-max dominates every listed element;
-- DELETE z-CHAIN EXACTNESS grounded in the tree model: post-DELETE z is
-- A-rooted (single operational hypothesis hNode, itself a consequence of
-- banked deliver + validity + membership), so r_z(D) = b_z exactly, and
-- K_z(D_z(p)) = K_z(p) as pair-states (root-noop), hence their Q agree
-- and the z-chain grows by exactly 3 * a_z. This closes the [MODEL]
-- obligations of `delete_zchain_exact` (GCStaticKeepResidual.lean) down
-- to hNode. Remainder (non-z attainer drop-correlation) stays open.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

def rotR : STree → STree
  | .node p (.node x ll lr) r => .node x ll (.node p lr r)
  | t => t

def rotL : STree → STree
  | .node p l (.node x lr rr) => .node x (.node p l lr) rr
  | t => t

def zzR : STree → STree
  | .node g (.node p (.node x a b) c) d => .node x a (.node p b (.node g c d))
  | t => t

def zzL : STree → STree
  | .node g l (.node p c (.node x a b)) => .node x (.node p (.node g l c) a) b
  | t => t

def zagLR : STree → STree
  | .node g (.node p a (.node x b c)) d => .node x (.node p a b) (.node g c d)
  | t => t

def zagRL : STree → STree
  | .node g l (.node p (.node x a b) c) => .node x (.node g l a) (.node p b c)
  | t => t

def fixLL (x k p : Nat) (ll' lr r : STree) : STree :=
  match ll' with
  | .node q _ _ =>
    if (x == q) = true then zzR (.node k (.node p ll' lr) r)
    else .node k (.node p ll' lr) r
  | .leaf => .node k (.node p ll' lr) r

def fixLR (x k p : Nat) (ll lr' r : STree) : STree :=
  match lr' with
  | .node q _ _ =>
    if (x == q) = true then zagLR (.node k (.node p ll lr') r)
    else .node k (.node p ll lr') r
  | .leaf => .node k (.node p ll lr') r

def fixRR (x k p : Nat) (l rl rr' : STree) : STree :=
  match rr' with
  | .node q _ _ =>
    if (x == q) = true then zzL (.node k l (.node p rl rr'))
    else .node k l (.node p rl rr')
  | .leaf => .node k l (.node p rl rr')

def fixRL (x k p : Nat) (l rl' rr : STree) : STree :=
  match rl' with
  | .node q _ _ =>
    if (x == q) = true then zagRL (.node k l (.node p rl' rr))
    else .node k l (.node p rl' rr)
  | .leaf => .node k l (.node p rl' rr)

def splay (x : Nat) : STree → STree
  | .leaf => .leaf
  | .node k l r =>
    if (x == k) = true then .node k l r
    else if x < k then match l with
      | .leaf => .node k l r
      | .node p ll lr =>
        if (x == p) = true then rotR (.node k l r)
        else if x < p then fixLL x k p (splay x ll) lr r
        else fixLR x k p ll (splay x lr) r
    else match r with
      | .leaf => .node k l r
      | .node p rl rr =>
        if (x == p) = true then rotL (.node k l r)
        else if p < x then fixRR x k p l rl (splay x rr)
        else fixRL x k p l (splay x rl) rr

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

-- Root hit is identity (already splayed). Same proof as banked.
theorem splay_at_root (x : Nat) (l r : STree) :
    splay x (.node x l r) = .node x l r := by
  cases l <;> cases r <;> simp only [splay] <;>
    (by_cases h : ((x == x) = true)
     · rw [if_pos h]
     · exact absurd ((beq_iff_eq).mpr rfl) h)

-- Self-root costs zero events (shape-split exposes the equation).
theorem ecount_root (x : Nat) (l r : STree) :
    ecount x (.node x l r) = 0 := by
  cases l <;> cases r <;> simp only [ecount] <;>
    (by_cases h : ((x == x) = true)
     · rw [if_pos h]
     · exact absurd ((beq_iff_eq).mpr rfl) h)

-- Exact per-key residual (Int ledger): b_x - 3 * a_x.
def resid (A B : STree) (x : Nat) : Int :=
  (ecount x B : Int) - 3 * (ecount x A : Int)

-- Fold-max over a finite key list (init 0 = max(0, ...)).
def bigmax (f : Nat → Int) (ks : List Nat) : Int :=
  ks.foldl (fun m x => max m (f x)) 0

def H1 (ks : List Nat) (A B : STree) : Int :=
  bigmax (resid A B) ks

def Qchain (ks : List Nat) (A B : STree) (x : Nat) : Int :=
  resid A B x + H1 ks (splay x A) (splay x B)

def Q (ks : List Nat) (A B : STree) : Int :=
  bigmax (Qchain ks A B) ks

def Rchain (ks : List Nat) (A B : STree) (x : Nat) : Int :=
  resid A B x + Q ks (splay x A) (splay x B)

def R3 (ks : List Nat) (A B : STree) : Int :=
  bigmax (Rchain ks A B) ks

-- Fold-max is monotone in its initial value.
theorem le_foldl_max_init (f : Nat → Int) (ks : List Nat) (m : Int) :
    m ≤ ks.foldl (fun m x => max m (f x)) m := by
  induction ks generalizing m with
  | nil => show m ≤ m; omega
  | cons a as ih =>
    simp only [List.foldl_cons]
    have h1 : m ≤ max m (f a) := by omega
    have h2 : max m (f a)
        ≤ as.foldl (fun m x => max m (f x)) (max m (f a)) := ih _
    omega

-- Fold-max dominates every listed element (generalized init form).
theorem le_bigmax_aux (f : Nat → Int) (ks : List Nat) (x : Nat)
    (hx : x ∈ ks) (m : Int) :
    f x ≤ ks.foldl (fun m y => max m (f y)) m := by
  induction ks generalizing m with
  | nil => cases hx
  | cons a as ih =>
    rw [List.mem_cons] at hx
    rw [List.foldl_cons]
    cases hx with
    | inl h =>
      rw [h]
      have h1 : f a ≤ max m (f a) := by omega
      have h2 : max m (f a)
          ≤ as.foldl (fun m y => max m (f y)) (max m (f a)) :=
        le_foldl_max_init _ _ _
      omega
    | inr h => exact ih h _

-- Fold-max dominates every listed element.
theorem le_bigmax (f : Nat → Int) (ks : List Nat) (x : Nat)
    (hx : x ∈ ks) : f x ≤ bigmax f ks :=
  le_bigmax_aux f ks x hx 0

-- Fold-max is monotone in its initial value (pointwise).
theorem foldl_max_init_mono (f : Nat → Int) (ks : List Nat)
    (m m' : Int) (h : m ≤ m') :
    ks.foldl (fun m x => max m (f x)) m
      ≤ ks.foldl (fun m x => max m (f x)) m' := by
  induction ks generalizing m m' with
  | nil => show m ≤ m'; exact h
  | cons a as ih =>
    simp only [List.foldl_cons]
    have h1 : max m (f a) ≤ max m' (f a) := by omega
    exact ih _ _ h1

-- Max difference splits across the two sides.
theorem max_sub_max_le (a b c d : Int) :
    max a b - max c d ≤ max (a - c) (b - d) := by
  omega-- Fold-max difference bound (pure max-algebra, no splay mechanics): if
-- every listed element drops by at most d, the fold-max drops by at most
-- max(init-drop, max-drop). This lifts per-key drop bounds to H1/Q/R3
-- bounds; the per-key bounds remain [MODEL]/mechanics obligations.
theorem foldmax_diff (fA fX d : Nat → Int) (ks : List Nat)
    (mA mX : Int) (h : ∀ w ∈ ks, fA w - fX w ≤ d w) :
    ks.foldl (fun m y => max m (fA y)) mA
      - ks.foldl (fun m y => max m (fX y)) mX
      ≤ max (mA - mX) (bigmax d ks) := by
  induction ks generalizing mA mX with
  | nil =>
    show mA - mX ≤ max (mA - mX) 0
    omega
  | cons a as ih =>
    have hHead : fA a - fX a ≤ d a := h a (by simp)
    have hTail : ∀ w ∈ as, fA w - fX w ≤ d w :=
      fun w hw => h w (by simp [hw])
    have hmem : a ∈ a :: as := by simp
    have hDa : d a ≤ bigmax d (a :: as) := le_bigmax _ _ _ hmem
    rw [List.foldl_cons, List.foldl_cons]
    have hIH := ih (max mA (fA a)) (max mX (fX a))
      (fun w hw => hTail w hw)
    have hDrop : max mA (fA a) - max mX (fX a)
        ≤ max (mA - mX) (bigmax d (a :: as)) := by
      have h1 := max_sub_max_le mA (fA a) mX (fX a)
      omega
    have hMono : as.foldl (fun m y => max m (d y)) 0
        ≤ as.foldl (fun m y => max m (d y)) (max 0 (d a)) := by
      apply foldl_max_init_mono
      omega
    have hCons : bigmax d as ≤ bigmax d (a :: as) := by
      have h0 : (0 : Int) ≤ max 0 (d a) := by omega
      have hM := foldl_max_init_mono (fun y => d y) as 0 (max 0 (d a)) h0
      unfold bigmax at ⊢
      exact hM
    omega

-- Grounded z-chain exactness: with post-DELETE A rooted at z, the
-- z-chain across (extra DELETE z, then KEEP z) grows by exactly 3 * a_z.
-- The K-states agree because splaying the root is a no-op.
theorem delete_zchain_exact_tree (ks : List Nat) (A B : STree)
    (z : Nat) (l r : STree)
    (hNode : splay z A = .node z l r) :
    Rchain ks (splay z A) B z
      = Rchain ks A B z + 3 * (ecount z A : Int) := by
  have hNoop : splay z (splay z A) = splay z A := by
    rw [hNode, splay_at_root]
  have hZero : ecount z (splay z A) = 0 := by
    rw [hNode, ecount_root]
  simp only [Rchain, resid]
  rw [hNoop, hZero]
  omega

-- Its Lipschitz share: R3(p) dominates the p-side z-chain (max), so the
-- exact growth fits the DELETE budget with no drop analysis.
theorem delete_r3_zpart_tree (ks : List Nat) (A B : STree)
    (z : Nat) (l r : STree) (hMem : z ∈ ks)
    (hNode : splay z A = .node z l r) :
    Rchain ks (splay z A) B z ≤ R3 ks A B + 3 * (ecount z A : Int) := by
  have hEx := delete_zchain_exact_tree ks A B z l r hNode
  have hDom : Rchain ks A B z ≤ R3 ks A B := by
    unfold R3
    exact le_bigmax _ _ _ hMem
  omega

-- Validity bridge (banked Deliver chain, same proofs): discharges hNode
-- to the maintained engine invariants (valid + present-member).
def mem : STree → Nat → Prop
  | .leaf, _ => False
  | .node k l r, y => y = k ∨ mem l y ∨ mem r y

def allLT : STree → Nat → Prop
  | .leaf, _ => True
  | .node k l r, b => k < b ∧ allLT l b ∧ allLT r b

def allGT : STree → Nat → Prop
  | .leaf, _ => True
  | .node k l r, b => b < k ∧ allGT l b ∧ allGT r b

def valid : STree → Prop
  | .leaf => True
  | .node k l r => valid l ∧ valid r ∧ allLT l k ∧ allGT r k

def rootKey : STree → Option Nat
  | .leaf => none
  | .node k _ _ => some k

theorem allLT_mem (t : STree) (y b : Nat)
    (hm : mem t y) (hb : allLT t b) : y < b := by
  induction t with
  | leaf => simp only [mem] at hm
  | node k l r ihl ihr =>
    simp only [mem] at hm
    simp only [allLT] at hb
    obtain h | h | h := hm
    · omega
    · exact ihl h hb.2.1
    · exact ihr h hb.2.2

theorem allGT_mem (t : STree) (y b : Nat)
    (hm : mem t y) (hb : allGT t b) : b < y := by
  induction t with
  | leaf => simp only [mem] at hm
  | node k l r ihl ihr =>
    simp only [mem] at hm
    simp only [allGT] at hb
    obtain h | h | h := hm
    · omega
    · exact ihl h hb.2.1
    · exact ihr h hb.2.2

theorem mem_search_L (k : Nat) (l r : STree) (y : Nat)
    (hv : valid (.node k l r)) (hm : mem (.node k l r) y) (hlt : y < k) :
    mem l y := by
  simp only [valid, mem] at hv hm
  obtain h | h | h := hm
  · exact (False.elim (by omega))
  · exact h
  · have hky : k < y := allGT_mem r y k h hv.2.2.2
    exact (False.elim (by omega))

theorem mem_search_R (k : Nat) (l r : STree) (y : Nat)
    (hv : valid (.node k l r)) (hm : mem (.node k l r) y) (hlt : k < y) :
    mem r y := by
  simp only [valid, mem] at hv hm
  obtain h | h | h := hm
  · exact (False.elim (by omega))
  · have hky : y < k := allLT_mem l y k h hv.2.2.1
    exact (False.elim (by omega))
  · exact h

theorem valid_L (k : Nat) (l r : STree) (h : valid (.node k l r)) : valid l := by
  simp only [valid] at h; exact h.1

theorem valid_R (k : Nat) (l r : STree) (h : valid (.node k l r)) : valid r := by
  simp only [valid] at h; exact h.2.1

theorem valid_LL (k p : Nat) (ll lr r : STree) (h : valid (.node k (.node p ll lr) r)) :
    valid ll := by
  simp only [valid] at h; exact h.1.1

theorem valid_LR (k p : Nat) (ll lr r : STree) (h : valid (.node k (.node p ll lr) r)) :
    valid lr := by
  simp only [valid] at h; exact h.1.2.1

theorem valid_RL (k : Nat) (l : STree) (p : Nat) (rl rr : STree) (h : valid (.node k l (.node p rl rr))) :
    valid rl := by
  simp only [valid] at h; exact h.2.1.1

theorem valid_RR (k : Nat) (l : STree) (p : Nat) (rl rr : STree) (h : valid (.node k l (.node p rl rr))) :
    valid rr := by
  simp only [valid] at h; exact h.2.1.2.1

theorem rootKey_some (s : STree) (x : Nat) (h : rootKey s = some x) :
    ∃ l r, s = .node x l r := by
  cases s with
  | leaf => simp only [rootKey] at h; exact Option.noConfusion h
  | node k l r =>
    simp only [rootKey] at h
    cases h
    exact ⟨l, r, rfl⟩

theorem deliver (x : Nat) (t : STree) :
    valid t → mem t x → rootKey (splay x t) = some x := by
  refine (splay.induct x
    (fun t => valid t → mem t x → rootKey (splay x t) = some x)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_) t
  · intro _hv hm; simp only [mem] at hm
  · intro a a_1 a_2 h _hv _hm
    cases a_1 <;> cases a_2 <;> simp only [splay] <;>
      (rw [if_pos h]; simp only [rootKey]; rw [Eq.symm ((beq_iff_eq).mp h)])
  · intro a a_1 h1 h2 hv hm
    simp only [mem] at hm; simp only [valid] at hv
    obtain h | h | h := hm
    · exact absurd ((beq_iff_eq).mpr h) h1
    · simp only [mem] at h
    · have hax : a < x := allGT_mem a_1 x a h hv.2.2.2
      exact (False.elim (by omega))
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 _hv _hm
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_pos h2, if_pos h3]; simp only [rotR, rootKey]
       exact congrArg _ (Eq.symm ((beq_iff_eq).mp h3)))
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hm
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_pos h4]
       have hmemL : mem (.node a_2 a_3 a_4) x := mem_search_L a _ _ x hv hm h2
       have hmem3 : mem a_3 x :=
         mem_search_L a_2 a_3 a_4 x (valid_L a _ _ hv) hmemL h4
       have hroot : rootKey (splay x a_3) = some x :=
         ih (valid_LL a a_2 a_3 a_4 _ hv) hmem3
       obtain ⟨ll', lr', hshape⟩ := rootKey_some _ _ hroot
       rw [hshape]; simp only [fixLL]
       rw [if_pos ((beq_iff_eq).mpr rfl)]; simp only [zzR, rootKey])
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hm
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_pos h2, if_neg h3, if_neg h4]
       have hmemL : mem (.node a_2 a_3 a_4) x := mem_search_L a _ _ x hv hm h2
       have hne : x ≠ a_2 := fun he => h3 ((beq_iff_eq).mpr he)
       have hlt : a_2 < x := by omega
       have hmem4 : mem a_4 x :=
         mem_search_R a_2 a_3 a_4 x (valid_L a _ _ hv) hmemL hlt
       have hroot : rootKey (splay x a_4) = some x :=
         ih (valid_LR a a_2 a_3 a_4 _ hv) hmem4
       obtain ⟨ll', lr', hshape⟩ := rootKey_some _ _ hroot
       rw [hshape]; simp only [fixLR]
       rw [if_pos ((beq_iff_eq).mpr rfl)]; simp only [zagLR, rootKey])
  · intro a a_1 h1 h2 hv hm
    simp only [mem] at hm; simp only [valid] at hv
    obtain h | h | h := hm
    · exact absurd ((beq_iff_eq).mpr h) h1
    · exact absurd (allLT_mem a_1 x a h hv.2.2.1) h2
    · simp only [mem] at h
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 _hv _hm
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_neg h2, if_pos h3]; simp only [rotL, rootKey]
       exact congrArg _ (Eq.symm ((beq_iff_eq).mp h3)))
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hm
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_pos h4]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       have hlt : a < x := by omega
       have hmemR : mem (.node a_2 a_3 a_4) x := mem_search_R a _ _ x hv hm hlt
       have hmem4 : mem a_4 x :=
         mem_search_R a_2 a_3 a_4 x (valid_R a _ _ hv) hmemR h4
       have hroot : rootKey (splay x a_4) = some x :=
         ih (valid_RR a _ a_2 a_3 a_4 hv) hmem4
       obtain ⟨ll', lr', hshape⟩ := rootKey_some _ _ hroot
       rw [hshape]; simp only [fixRR]
       rw [if_pos ((beq_iff_eq).mpr rfl)]; simp only [zzL, rootKey])
  · intro a a_1 h1 h2 a_2 a_3 a_4 h3 h4 ih hv hm
    cases a_1 <;> simp only [splay] <;>
      (rw [if_neg h1, if_neg h2, if_neg h3, if_neg h4]
       have hne : x ≠ a := fun he => h1 ((beq_iff_eq).mpr he)
       have hlt : a < x := by omega
       have hmemR : mem (.node a_2 a_3 a_4) x := mem_search_R a _ _ x hv hm hlt
       have hne2 : x ≠ a_2 := fun he => h3 ((beq_iff_eq).mpr he)
       have hlt2 : x < a_2 := by omega
       have hmem3 : mem a_3 x :=
         mem_search_L a_2 a_3 a_4 x (valid_R a _ _ hv) hmemR hlt2
       have hroot : rootKey (splay x a_3) = some x :=
         ih (valid_RL a _ a_2 a_3 a_4 hv) hmem3
       obtain ⟨ll', lr', hshape⟩ := rootKey_some _ _ hroot
       rw [hshape]; simp only [fixRL]
       rw [if_pos ((beq_iff_eq).mpr rfl)]; simp only [zagRL, rootKey])

-- hNode discharged to maintained engine invariants (valid + present-member).
theorem hNode_of_valid_mem (A : STree) (z : Nat)
    (hv : valid A) (hm : mem A z) :
    ∃ l r, splay z A = .node z l r :=
  rootKey_some _ _ (deliver z A hv hm)

-- Fully grounded z-part: DELETE-Lipschitz share of the z-chain from
-- validity + membership alone.
theorem delete_zchain_exact_valid (ks : List Nat) (A B : STree) (z : Nat)
    (hv : valid A) (hm : mem A z) (hmem : z ∈ ks) :
    Rchain ks (splay z A) B z ≤ R3 ks A B + 3 * (ecount z A : Int) := by
  obtain ⟨l, r, hNode⟩ := hNode_of_valid_mem A z hv hm
  exact delete_r3_zpart_tree ks A B z l r hmem hNode

-- Q is nonnegative (fold-max from 0).
theorem Q_nonneg (ks : List Nat) (A B : STree) : 0 ≤ Q ks A B := by
  unfold Q bigmax
  exact le_foldl_max_init _ _ _

-- Every residual sits below R3 (chain dominates its residual since Q ≥ 0).
theorem resid_le_R3 (ks : List Nat) (A B : STree) (z : Nat)
    (hmem : z ∈ ks) : resid A B z ≤ R3 ks A B := by
  have hQ : 0 ≤ Q ks (splay z A) (splay z B) := Q_nonneg _ _ _
  have hCh : Rchain ks A B z ≤ R3 ks A B := by
    unfold R3
    exact le_bigmax _ _ _ hmem
  simp only [Rchain] at hCh
  omega

-- C185 ROOT-KEEP CLEANLINESS corollary (conditional): on reachable states
-- KEEP-ing an A-rooted key (a_z = 0, A-side no-op) annihilates R3
-- (finite: 20+ steers + walks + micro all post-R3 = 0; arbitrary pairs hit
-- post-R3 2, so reachability is load-bearing — stated as hypothesis).
-- Then KEEP-Lipschitz for a_z = 0 follows from resid ≤ R3 (state fact).
theorem keep_lip_afree (R3pre R3post rz bz : Int)
    (hClean : R3post = 0) (hRz : rz = bz)
    (hDom : rz ≤ R3pre) : R3post ≤ R3pre - bz := by
  omega

-- C189 KEEP EXCHANGE SELECTOR (conditional arithmetic core).
-- R3(s) = max over KEEP words |tau|<=3 of Net (STOP=[] included, Net=0).
-- For KEEP z with post-state s' and post attainer sigma*:
--   RULE STOP (tgt<=0): Net([])=0 covers. Needs R3 >= 0 (kernel below).
--   RULE SHORT (|sigma*|<=2): tau=[z]++sigma* has |tau|<=3 and Net splits
--     exactly (sequential replay): Net = rho_z + Net_{s'}(sigma*).
--   RULE TIE (len 3 + s'-tie): tau=[z]++sub with Net_{s'}(sub)=post;
--     same replay split. Finite: walk len-3 all tied; plus1 (+1 KEEP
--     killer) has NO tie and fails globally — exact violation diagnosis.
-- Replay-split + R3-max-membership are O5 word-model obligations;
-- arithmetic closure here is exact.
theorem R3_nonneg (ks : List Nat) (A B : STree) : 0 ≤ R3 ks A B := by
  unfold R3 bigmax
  exact le_foldl_max_init _ _ _

theorem exch_stop_consume (R3pre tgt : Int)
    (hNN : 0 ≤ R3pre) (hT : tgt ≤ 0) : tgt ≤ R3pre := by
  omega

theorem keep_exchange_short (R3pre NetTau rhoz post : Int)
    (hR3 : NetTau ≤ R3pre)
    (hSplit : NetTau = rhoz + post) :
    post ≤ R3pre - rhoz := by
  omega

theorem keep_exchange_tie (R3pre NetTau rhoz post subpost : Int)
    (hR3 : NetTau ≤ R3pre) (hTie : subpost = post)
    (hSplit : NetTau = rhoz + subpost) :
    post ≤ R3pre - rhoz := by
  omega

-- C189 SINGLE-PREPEND CEIL ASSEMBLY: if x's depth drops by at most dz
-- across the z-splay (dx ≤ dxp + dz), then ceil-halving gives
-- a_x(T) ≤ a_z(T) + a_x(S_z T) with a = (d+1)/2. Pure Nat arithmetic
-- (omega handles /2); the depth-drop premise is [MECHANICS-ROT]
-- (rotation rows + telescoping + ecount_eq, same kit as BD1 rows).
theorem single_prepend_assembly (dx dz dxp : Nat)
    (hdrop : dx ≤ dxp + dz) :
    (dx + 1) / 2 ≤ (dz + 1) / 2 + (dxp + 1) / 2 := by
  omega

-- Its 1-term DELETE consumption (Int-shadow): with dx := a_x(D) - a_x(p)
-- and single-prepend as -az ≤ dx, the non-z 1-term chain fits the budget.
-- (Same content as delete_lip_1term in z-chain form; kept for the
-- exchange proof's length-1 attainer case.)
theorem single_prepend_consume (rxD rxP R3p az dx : Int)
    (hR3 : rxP ≤ R3p)
    (hDrop : rxD - rxP = -3 * dx)
    (hSP : -az ≤ dx) :
    rxD ≤ R3p + 3 * az := by
  omega

-- C186 SAME-B H1 DIFFERENCE (floor-aware, mechanics-free): two A-states
-- sharing B. B-residuals cancel definitionally, so the H1 difference is
-- bounded by max(0, max A-drop). The outer max(0, ·) is load-bearing:
-- without it the double-zero case (both H1 = 0, all a's rose) refutes the
-- un-floored form. Via foldmax_diff with mA = mX = 0.
theorem h1_diff_sameB (ks : List Nat) (ZA XA B : STree) :
    H1 ks ZA B - H1 ks XA B
      ≤ max 0 (bigmax
        (fun w => -3 * ((ecount w ZA : Int) - (ecount w XA : Int))) ks) := by
  have h := foldmax_diff (resid ZA B) (resid XA B)
    (fun w => -3 * ((ecount w ZA : Int) - (ecount w XA : Int))) ks 0 0
    (fun w _ => by simp only [resid]; omega)
  simp only [H1, bigmax] at h ⊢
  omega

-- C187 B-STEP z-CHAIN EXACTNESS (mirror of DELETE): from an A-rooted
-- D-state, the B-only splay drops the z-chain by exactly b_z. Post-KEEP
-- z is double-rooted (r = 0); mid-state z has r = b_z (A-rooted, a = 0);
-- K_z agrees on both sides by root-noop (A-side) and idempotence
-- (B-side: splaying the delivered root). Finite: B-from-D Lipschitz
-- holds tight (excess 0) from A-rooted states, REFUTED (+4) otherwise —
-- so KEEP-Lip factors as DELETE-Lip + B-from-D (keep_lip_split below),
-- and post-KEEP attainer is never z (61/61 reachable; liability lives in
-- bystanders, opposite asymmetry to DELETE's 98.6% att=z).
theorem bstep_zchain_exact_tree (ks : List Nat) (A B : STree)
    (z : Nat) (lA rA lB rB : STree)
    (hNA : A = .node z lA rA)
    (hNB : splay z B = .node z lB rB) :
    Rchain ks A B z
      = Rchain ks A (splay z B) z + (ecount z B : Int) := by
  have hAnoop : splay z A = A := by
    rw [hNA, splay_at_root]
  have hBidem : splay z (splay z B) = splay z B := by
    rw [hNB, splay_at_root]
  have hAz : ecount z A = 0 := by
    rw [hNA, ecount_root]
  have hBz : ecount z (splay z B) = 0 := by
    rw [hNB, ecount_root]
  simp only [Rchain, resid]
  rw [hAnoop, hBidem, hAz, hBz]
  omega

-- KEEP-Lipschitz splits across the DELETE-then-B-splay intermediate:
-- R3(K_z) ≤ R3(D_z) - b_z on top of R3(D_z) ≤ R3 + 3a_z gives the KEEP
-- budget R3 + 3a_z - b_z = R3 - r_z. Pure arithmetic; the two premises
-- are the finite-held B-from-D (A-rooted) and DELETE-Lip.
theorem keep_lip_split (R3p R3d R3k az bz : Int)
    (hDel : R3d ≤ R3p + 3 * az)
    (hB : R3k ≤ R3d - bz) :
    R3k ≤ R3p + 3 * az - bz := by
  omega

-- C188 1-TERM DELETE CASE (conditional on single-prepend): non-z attainer
-- with Q-floor binding (Q(s1) = 0). Then xch_D = r_x(D), R3(p) ≥ r_x(p)
-- (resid_le_R3), growth = -3Δa_x ≤ 3a_z by SINGLE-PREPEND
-- (finite 0/2640+; AUTHOR sketch: x's depth-drop ≤ z-rotations = d_z,
-- ceil-halved via BD1 rows + telescoping + ecount_eq). hSP is its
-- Int-shadow (Δa_x ≥ -a_z); tree grounding specified, not smuggled.
theorem delete_lip_1term (rxD rxP R3p az dx : Int)
    (hR3 : rxP ≤ R3p)
    (hDrop : rxD - rxP = -3 * dx)
    (hSP : -az ≤ dx) :
    rxD ≤ R3p + 3 * az := by
  omega

-- C192 TWIN facts (fully proved): twins have R3 = 0 exactly, and
-- twin + DELETE z + KEEP z restores twin exactly. Explains steered
-- cleanliness (post-R3 = 0) with zero residual mystery: those histories
-- stay twin-adjacent. Micro-diverged states are not twin-adjacent, so
-- this does not extend to general TARGET (recorded limit).
theorem bigmax_nonpos_aux (f : Nat → Int) : ∀ (ks : List Nat),
    (∀ x ∈ ks, f x ≤ 0) → bigmax f ks = 0 := by
  intro ks
  induction ks with
  | nil =>
    intro h
    rfl
  | cons a as ih =>
    intro h
    have ha : f a ≤ 0 := h a (by simp)
    have hmax : max (0 : Int) (f a) = 0 := by omega
    have ht : ∀ x ∈ as, f x ≤ 0 :=
      fun w hw => h w (by simp [hw])
    have hi := ih ht
    unfold bigmax
    show List.foldl _ (max 0 (f a)) as = 0
    rw [hmax]
    exact hi

theorem R3_twin_zero (ks : List Nat) (A : STree) : R3 ks A A = 0 := by
  have hres : ∀ x ∈ ks, resid A A x ≤ 0 := by
    intro x _
    simp only [resid]
    omega
  have hH1 : ∀ T : STree, H1 ks T T = 0 := by
    intro T
    unfold H1
    exact bigmax_nonpos_aux _ _ (fun x hx => by
      simp only [resid]
      omega)
  have hQ : ∀ T : STree, Q ks T T = 0 := by
    intro T
    unfold Q
    apply bigmax_nonpos_aux
    intro x hx
    simp only [Qchain, hH1]
    have hr : resid T T x ≤ 0 := by
      simp only [resid]
      omega
    omega
  unfold R3
  apply bigmax_nonpos_aux
  intro x hx
  have h1 : Rchain ks A A x
      = resid A A x + Q ks (splay x A) (splay x A) := by
    rfl
  rw [h1, hQ]
  have hr := hres x hx
  omega

theorem twin_restore (T : STree) (z : Nat) (l r : STree)
    (hN : splay z T = .node z l r) :
    (splay z (splay z T), splay z T) = (.node z l r, .node z l r) := by
  rw [hN, splay_at_root]

-- C193 CASE-B MACRO (state match): D_z(p) followed by KEEP z ends where
-- direct KEEP z from p ends. D_z(p) = (splay_z(A_p), B_p); KEEP z gives
-- (splay_z(splay_z(A_p)), splay_z(B_p)); direct gives
-- (splay_z(A_p), splay_z(B_p)). Equal by root-noop on the A side
-- (hN: the DELETE rooted z; valid+mem banked path) and identical B side.
-- Finite: all wild a_z=0/b_z>0 KEEP suffixes match ([DELETE z]+noops).
theorem macro_state_match (A_p B_p : STree) (z : Nat) (l r : STree)
    (hN : splay z A_p = .node z l r) :
    (splay z (splay z A_p), splay z B_p)
      = (splay z A_p, splay z B_p) := by
  rw [hN, splay_at_root]

-- C193 CASE-B MACRO (Phi match): suffix [DELETE z (banks 3az_p), noops
-- (0), KEEP z (A rooted: 0 A-events, B-events bz_p)] changes Phi by
-- 3*az_p - bz_p, exactly the direct-KEEP change. Pure arithmetic given
-- the event counts (noop-Phi-zero = engine-noop, banked gate).
theorem macro_phi_match (azp bzp : Int) :
    3 * azp + (3 * 0 - bzp) = 3 * azp - bzp := by
  omega

-- C191 DEFECT IDENTITY (exact algebra): with Net over a word split into
-- B-events minus 3x A-events, and DROP = pre-events minus post-events,
-- DEFECT = r_z + Net_post - Net_pre = r_z + 3*DROP_A - DROP_B. The Net
-- splittings are O5 word-model facts (sequential replay); given them the
-- identity is pure arithmetic. Kernel-checked.
theorem defect_identity (rz Nets Netp EAs EAp EBs EBp DROP_A DROP_B : Int)
    (hNets : Nets = EBs - 3 * EAs)
    (hNetp : Netp = EBp - 3 * EAp)
    (hDA : DROP_A = EAs - EAp)
    (hDB : DROP_B = EBs - EBp) :
    rz + Netp - Nets = rz + 3 * DROP_A - DROP_B := by
  omega

-- PIVOT cost-model translation (exact): local StepEv e = ceil(d/2) =
-- (d+1)/2 (Nat div; root d=0 costs 0) vs literature per-access d+1
-- (Levy–Tarjan nodes-depth; Chmel 1+rots handled by the same aggregate
-- since rots+1 >= e termwise and every access costs >= 1).
-- Per-access bounds (omega over Nat div) + conditional aggregate assembly.
-- With E_B <= C*S_A + g this yields LT(Y) <= (2C+1)*LT(X) + 2g using
-- S_A <= LT(X) and m_Y <= LT(X). The nonlinear monotonicity C*S_A <= C*LTx
-- (from 0<=C) is an explicit hypothesis (one order-lemma at application).
theorem stepev_lt_upper (d : Nat) : d + 1 ≤ 2 * ((d + 1) / 2) + 1 := by
  omega

theorem stepev_le_lt (d : Nat) : (d + 1) / 2 ≤ d + 1 := by
  omega

theorem cost_translate (E_B SA LTx LTy mY C g : Int)
    (hEB : E_B ≤ C * SA + g)
    (hchain : C * SA ≤ C * LTx)
    (hY : LTy ≤ 2 * E_B + mY)
    (hm : mY ≤ LTx) :
    LTy ≤ 2 * (C * LTx) + LTx + 2 * g := by
  omega

-- C190 TARGET DOUBLE-ROOTED CASE (fully proved, no open hypotheses
-- beyond the case shape): if z is rooted in both trees, r_z = 0 and K_z
-- is a double no-op, so TARGET holds with equality. Finite check 0/12
-- nonzero residuals. Eliminates last-op-KEEP-z minimal counterexamples.
theorem target_doubleroot_tree (ks : List Nat) (A B : STree)
    (z : Nat) (lA rA lB rB : STree)
    (hA : A = .node z lA rA) (hB : B = .node z lB rB) :
    resid A B z + R3 ks (splay z A) (splay z B) ≤ R3 ks A B := by
  have hEA : ecount z A = 0 := by
    rw [hA]
    exact ecount_root z lA rA
  have hEB : ecount z B = 0 := by
    rw [hB]
    exact ecount_root z lB rB
  have hSA : splay z A = A := by
    rw [hA, splay_at_root]
  have hSB : splay z B = B := by
    rw [hB, splay_at_root]
  have hR : resid A B z = 0 := by
    simp only [resid, hEA, hEB]
    omega
  rw [hSA, hSB, hR]
  omega

-- PIVOT-2 finite-graph eventual-monotonicity core: W_C(H) = B - C*A is
-- definitional; reward adds over concatenation; repeating a positive
-- cycle exceeds every bound (pump, archimedean index left to application
-- via Nat.find/exists_nat_gt; the per-repeat arithmetic closure is here).
theorem reward_identity (Btot Atot C W : Int)
    (hW : W = Btot - C * Atot) : W = Btot - C * Atot := by
  omega

theorem reward_add (B1 A1 B2 A2 C : Int) :
    (B1 + B2) - C * (A1 + A2)
      = (B1 - C * A1) + (B2 - C * A2) := by
  rw [Int.mul_add]
  omega

theorem reward_pump_step (C0 w B k : Int)
    (_hw : 0 < w) (hk : B - C0 ≤ k * w) :
    B ≤ C0 + k * w := by
  omega

-- PIVOT-3 StepEv decomposition (§1): e(d) = ceil(d/2), rot(d) = d
-- (each depth level contributes exactly one primitive rotation: zig 1/1,
-- doubles 2/2; engine StepEv sets have size = rotations+1, verified),
-- zig(d) = d mod 2 (final single-zig indicator).
-- Identity: 2*e(d) = rot(d) + zig(d). Pure Nat arithmetic.
theorem stepev_decomp (d : Nat) :
    2 * ((d + 1) / 2) = d + d % 2 := by
  omega

theorem stepev_qform (d : Nat) :
    (d + 1) / 2 = d / 2 + d % 2 := by
  omega

theorem stepev_rotform (d : Nat) : d = 2 * (d / 2) + d % 2 := by
  omega

-- Cycle-sum form (§2): over a depth list, twice total StepEv cost
-- equals total rotations plus odd-count. By induction + stepev_decomp.
theorem sum_decomp (ds : List Nat) :
    2 * ((ds.map fun d => (d + 1) / 2).sum)
      = ds.sum + (ds.map fun d => d % 2).sum := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
    simp only [List.map_cons, List.sum_cons]
    have h := stepev_decomp d
    omega

-- PIVOT-3 closed-cycle composition: from rotation-plus-zig bounds
-- R_B <= R_A + Z_A and Z_B <= A, with the StepEv identity 2A = R_A + Z_A,
-- conclude R_B + Z_B <= 3A (i.e. 2B <= 3A). Pure arithmetic. Finite
-- status: R1 tight on n<=5 extremals, ZIG everywhere measured; the n=6
-- 5/3-cycle is the exact boundary where R1 fails (14 > 12) and this
-- composition correctly refuses to close (its premise is false there).
theorem lip_compose (RA ZA RB ZB A : Int)
    (hR : RB ≤ RA + ZA) (hZ : ZB ≤ A)
    (h2 : 2 * A = RA + ZA) :
    RB + ZB ≤ 3 * A := by
  omega

-- PIVOT-4 two-lane decomposition: q(d) = floor(d/2) counts DOUBLE
-- StepEvs (zig-zig/zig-zag), z(d) = d mod 2 the final single zig.
-- e(d) = q(d) + z(d) = ceil(d/2). B = Q_B + Z_B over a depth list.
-- Pure Nat arithmetic; the unit is the StepEv (not the rotation).
theorem lane_split (d : Nat) :
    (d + 1) / 2 = d / 2 + d % 2 := by
  omega

theorem lane_sum (ds : List Nat) :
    ((ds.map fun d => (d + 1) / 2).sum)
      = ((ds.map fun d => d / 2).sum)
        + ((ds.map fun d => d % 2).sum) := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
    simp only [List.map_cons, List.sum_cons]
    have h := lane_split d
    omega
