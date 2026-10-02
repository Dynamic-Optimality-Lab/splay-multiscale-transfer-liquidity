-- WP-6 STEPS C132 (positional program): conditional root delivery.
--
-- Self-contained (repo convention: no imports; STree/splay/validity frame
-- restated from GCStaticLoop/GCStaticValid). Root-key delivery: on a BST-valid
-- tree, splaying a member brings it to the root. Proof by functional induction
-- (splay.induct, refine with explicit motive): root/zig cases deliver
-- directly; double cases route membership through search correctness into the
-- recursive call, invert the delivered root key to a shape, and discharge the
-- fixup condition; off-route cases (empty-side search) are vacuous by bounds.
-- With C130 (key safety) this certifies the skeleton: no keys lost, accessed
-- member key at root. Simulation relation with the pointer engine queued.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

inductive STree where
  | leaf : STree
  | node : Nat → STree → STree → STree
  deriving DecidableEq, Repr

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

def rootKey : STree → Option Nat
  | .leaf => none
  | .node k _ _ => some k

-- Bound-membership routing.
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

-- Search correctness on valid trees.
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

-- Validity decomposition (children and grandchildren).
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

-- Delivered root key inverts to a shape.
theorem rootKey_some (s : STree) (x : Nat) (h : rootKey s = some x) :
    ∃ l r, s = .node x l r := by
  cases s with
  | leaf => simp only [rootKey] at h; exact Option.noConfusion h
  | node k l r =>
    simp only [rootKey] at h
    cases h
    exact ⟨l, r, rfl⟩

-- CONDITIONAL ROOT DELIVERY: valid + member ⟹ splayed key at root.
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
