-- WP-6 PIVOT-VINE: universal vine-pair B<=A kernel (shapes + counting only).
--
-- Vine-pair closed walks satisfy B<=A for every n (human assembly in
-- audits/PIVOT_VINE_UNIVERSAL.md; finite base n<=7 by pair-graph BF).
-- This kernel certifies the reusable pieces, which are pure shape facts
-- (no key geometry, no BST hypotheses, no splay loop):
--   (V) vine definition + subtree closure;
--   (R) double rotations branch chains: zigzag always; zigzig when the
--       rising key carries a child (code order: grandparent-first; zigzag
--       uses positional subtree rotations matching the pointer engine);
--   (C) twin-bit counting: any closed walk whose edges are classified
--       (0,0)/(1,0)/(0,1)/(1,1) with the twin-flip table below has
--       total B-A <= 0. Walks are threaded-bit consistent by construction
--       (okChain): each edge's pre-bit equals the running bit.
-- Human audit assembles V1 (n>=5: vine-preserving splay has depth<=1,
-- multi-step case analysis) + classification application. The n<=4
-- zigzig-mirror exceptions (extreme depth-2/3) are handled by finite check.
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

-- Positional zigzag doubles matching the pointer engine (subtree rotation
-- at p first, then root rotation at g).
def zagLR : STree → STree
  | .node g (.node p c (.node x b a)) d =>
    rotR (.node g (rotL (.node p c (.node x b a))) d)
  | t => t

def zagRL : STree → STree
  | .node g d (.node p (.node x a b) c) =>
    rotL (.node g d (rotR (.node p (.node x a b) c)))
  | t => t

-- A vine (chain): every node has at most one (non-leaf) child.
def isVine : STree → Prop
  | .leaf => True
  | .node _ l r => (l = .leaf ∨ r = .leaf) ∧ isVine l ∧ isVine r

theorem vine_sub_l (k : Nat) (l r : STree) (h : isVine (.node k l r)) :
    isVine l := by
  simp only [isVine] at h
  exact h.2.1

theorem vine_sub_r (k : Nat) (l r : STree) (h : isVine (.node k l r)) :
    isVine r := by
  simp only [isVine] at h
  exact h.2.2

theorem vine_either (k : Nat) (l r : STree) (h : isVine (.node k l r)) :
    l = .leaf ∨ r = .leaf := by
  simp only [isVine] at h
  exact h.1

-- Sanity: concrete vines and non-vines.
example : isVine (.node 3 (.node 2 (.node 1 .leaf .leaf) .leaf) .leaf) := by
  simp only [isVine]
  simp

example : ¬ isVine (.node 3 (.node 1 .leaf .leaf) (.node 4 .leaf .leaf)) := by
  simp only [isVine]
  simp

-- LL zigzig (code order: rotR grandparent, then rotR parent).
-- Post: x rises with kept a and gained P'. Branches unless leaf.
theorem vine_LL_branch (g p x : Nat) (a b c d : STree)
    (h : a ≠ .leaf ∨ b ≠ .leaf) :
    ¬ isVine (rotR (rotR (.node g (.node p (.node x a b) c) d))) := by
  have e : rotR (rotR (.node g (.node p (.node x a b) c) d))
      = .node x a (.node p b (.node g c d)) := rfl
  rw [e]
  intro hv
  simp only [isVine] at hv
  cases h with
  | inl ha =>
    cases hv.1 with
    | inl h1 => exact ha h1
    | inr h2 => simp at h2
  | inr hb =>
    have hpv : ¬ isVine (.node p b (.node g c d)) := by
      intro hp2
      simp only [isVine] at hp2
      cases hp2.1 with
      | inl h1 => exact hb h1
      | inr h2 => simp at h2
    exact hpv hv.2.2

-- RR zigzig mirror (code order: rotL grandparent, then rotL parent).
theorem vine_RR_branch (g p x : Nat) (d c b a : STree)
    (h : b ≠ .leaf ∨ a ≠ .leaf) :
    ¬ isVine (rotL (rotL (.node g d (.node p c (.node x b a))))) := by
  have e : rotL (rotL (.node g d (.node p c (.node x b a))))
      = .node x (.node p (.node g d c) b) a := rfl
  rw [e]
  intro hv
  simp only [isVine] at hv
  cases h with
  | inl hb =>
    have hpv : ¬ isVine (.node p (.node g d c) b) := by
      intro hp2
      simp only [isVine] at hp2
      cases hp2.1 with
      | inl h1 => simp at h1
      | inr h2 => exact hb h2
    exact hpv hv.2.1
  | inr ha =>
    cases hv.1 with
    | inl h1 => simp at h1
    | inr h2 => exact ha h2

-- LR zigzag: rising key gains two non-leaf subtrees unconditionally.
theorem vine_LR_branch (g p x : Nat) (c b a d : STree) :
    ¬ isVine (zagLR (.node g (.node p c (.node x b a)) d)) := by
  have e : zagLR (.node g (.node p c (.node x b a)) d)
      = .node x (.node p c b) (.node g a d) := rfl
  rw [e]
  intro hv
  simp only [isVine] at hv
  cases hv.1 with
  | inl h1 => simp at h1
  | inr h2 => simp at h2

-- RL zigzag mirror.
theorem vine_RL_branch (g p x : Nat) (d a b c : STree) :
    ¬ isVine (zagRL (.node g d (.node p (.node x a b) c))) := by
  have e : zagRL (.node g d (.node p (.node x a b) c))
      = .node x (.node g d a) (.node p b c) := rfl
  rw [e]
  intro hv
  simp only [isVine] at hv
  cases hv.1 with
  | inl h1 => simp at h1
  | inr h2 => simp at h2

-- Twin-bit counting core: a closed classified walk has nonpositive B-A.
-- Edges carry (A-cost, B-cost) in {0,1}^2 plus pre/post twin bits where
-- TRUE means twin-rooted (both roots equal) and FALSE means roots differ.
-- (Application mapping: real differ-bit tau = [rooA != rooB] is the
-- negation of the Lean bit.) The flip table is exactly the vine-edge
-- classification: (0,1) twin-roots (F->T); (0,0) is a self-loop;
-- (1,1) never exits twin-ness (never T->F); (1,0) is unrestricted.
structure VEdge where
  a : Nat
  b : Nat
  pre : Bool
  post : Bool

def edgeOk (e : VEdge) : Prop :=
  (e.a = 0 ∧ e.b = 0 ∧ e.pre = e.post) ∨
  (e.a = 1 ∧ e.b = 0) ∨
  (e.a = 0 ∧ e.b = 1 ∧ e.pre = false ∧ e.post = true) ∨
  (e.a = 1 ∧ e.b = 1 ∧ ¬ (e.pre = true ∧ e.post = false))

def is01 (e : VEdge) : Bool := e.a == 0 && e.b == 1
def is10 (e : VEdge) : Bool := e.a == 1 && e.b == 0

-- Threaded-bit consistency: each edge's pre-bit equals the running bit.
def okChain : Bool → List VEdge → Prop
  | _, [] => True
  | pre, e :: es => e.pre = pre ∧ okChain e.post es

-- One pass: total weight, up-flips, down-flips, threading the bit.
def scan : Bool → List VEdge → Int × Nat × Nat
  | _, [] => (0, 0, 0)
  | pre, e :: es =>
    (((e.b : Int) - (e.a : Int) + (scan e.post es).1,
      (if !pre && e.post then 1 else 0) + (scan e.post es).2.1,
      (if pre && !e.post then 1 else 0) + (scan e.post es).2.2))

def endBit : Bool → List VEdge → Bool
  | pre, [] => pre
  | _, e :: es => endBit e.post es

theorem scan_cons_w (pre : Bool) (e : VEdge) (es : List VEdge) :
    (scan pre (e :: es)).1 = (e.b : Int) - (e.a : Int) + (scan e.post es).1 :=
  rfl

theorem scan_cons_u (pre : Bool) (e : VEdge) (es : List VEdge) :
    (scan pre (e :: es)).2.1
      = (if !pre && e.post then 1 else 0) + (scan e.post es).2.1 := rfl

theorem scan_cons_d (pre : Bool) (e : VEdge) (es : List VEdge) :
    (scan pre (e :: es)).2.2
      = (if pre && !e.post then 1 else 0) + (scan e.post es).2.2 := rfl

theorem endBit_cons (e : VEdge) (es : List VEdge) (pre : Bool) :
    endBit pre (e :: es) = endBit e.post es := rfl

-- Collapse a concrete boolean if-pair by casing both bits.
theorem collapse_if (u v : Bool) (x y : Nat) :
    (if !u && v then x else y) = match u, v with
      | false, true => x | _, _ => y := by
  cases u <;> cases v <;> rfl

theorem collapse_ifd (u v : Bool) (x y : Nat) :
    (if u && !v then x else y) = match u, v with
      | true, false => x | _, _ => y := by
  cases u <;> cases v <;> rfl

-- Telescope: up-flips minus down-flips equals end-bit minus start-bit.
theorem scan_telescope (es : List VEdge) : ∀ pre : Bool,
    ((scan pre es).2.1 : Int) - ((scan pre es).2.2 : Int)
      = (if endBit pre es then (1 : Int) else 0)
        - (if pre then 1 else 0) := by
  induction es with
  | nil =>
    intro pre
    simp only [scan, endBit]
    cases pre <;> simp <;> omega
  | cons e es ih =>
    intro pre
    rw [scan_cons_u, scan_cons_d, endBit_cons]
    have h := ih e.post
    by_cases hpre : pre = true <;> by_cases hpost : e.post = true <;>
      simp_all <;> omega

-- Closed walks balance flips.
theorem scan_closed (pre : Bool) (es : List VEdge)
    (hcl : endBit pre es = pre) :
    (scan pre es).2.1 = (scan pre es).2.2 := by
  have h := scan_telescope es pre
  rw [hcl] at h
  by_cases hpre : pre = true <;> simp_all <;> omega

theorem is01_iff (e : VEdge) : is01 e = true ↔ e.a = 0 ∧ e.b = 1 := by
  simp only [is01]
  cases e with
  | mk a b pre post =>
    simp only
    constructor
    · intro h
      simp at h
      obtain ⟨ha, hb⟩ := h
      exact ⟨by omega, by omega⟩
    · intro h
      obtain ⟨ha, hb⟩ := h
      simp [ha, hb]

theorem is10_iff (e : VEdge) : is10 e = true ↔ e.a = 1 ∧ e.b = 0 := by
  simp only [is10]
  cases e with
  | mk a b pre post =>
    simp only
    constructor
    · intro h
      simp at h
      obtain ⟨ha, hb⟩ := h
      exact ⟨by omega, by omega⟩
    · intro h
      obtain ⟨ha, hb⟩ := h
      simp [ha, hb]

-- (0,1)-edges inject into up-flips.
theorem count01_le (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) (hc : okChain pre es) :
    (es.filter is01).length ≤ (scan pre es).2.1 := by
  induction es generalizing pre with
  | nil => simp [scan]
  | cons e es ih =>
    have he := h e (by simp)
    obtain ⟨hpc, hcc⟩ := hc
    have ihr := ih e.post (fun e' hm => h e' (by simp [hm])) hcc
    simp only [edgeOk] at he
    by_cases hty : (is01 e = true)
    · simp only [List.filter_cons]
      rw [if_pos hty, List.length_cons, scan_cons_u]
      cases he with
      | inl h00 =>
        obtain ⟨ha0, hb0, -⟩ := h00
        have hty' := (is01_iff e).mp hty
        obtain ⟨ha, hb⟩ := hty'
        omega
      | inr hr =>
        cases hr with
        | inl h10 =>
          obtain ⟨ha1, -⟩ := h10
          have hty' := (is01_iff e).mp hty
          obtain ⟨ha, hb⟩ := hty'
          omega
        | inr hr2 =>
          cases hr2 with
          | inl h01 =>
            obtain ⟨-, -, hpre, hpost⟩ := h01
            have hpre2 : pre = false := hpc ▸ hpre
            have hif : ((!pre && e.post) = true) := by simp [hpre2, hpost]
            rw [if_pos hif]
            omega
          | inr h11 =>
            obtain ⟨ha1, -⟩ := h11
            have hty' := (is01_iff e).mp hty
            obtain ⟨ha, hb⟩ := hty'
            omega
    · simp only [List.filter_cons]
      rw [if_neg hty, scan_cons_u]
      exact Nat.le_trans ihr (Nat.le_add_left _ _)

-- Down-flips inject into (1,0)-edges (other types never flip down).
theorem count10_le (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) (hc : okChain pre es) :
    (scan pre es).2.2 ≤ (es.filter is10).length := by
  induction es generalizing pre with
  | nil => simp [scan]
  | cons e es ih =>
    have he := h e (by simp)
    obtain ⟨hpc, hcc⟩ := hc
    have ihr := ih e.post (fun e' hm => h e' (by simp [hm])) hcc
    simp only [edgeOk] at he
    by_cases hty : (is10 e = true)
    · simp only [List.filter_cons]
      rw [if_pos hty, List.length_cons, scan_cons_d]
      have hif : (if pre && !e.post then (1 : Nat) else 0) ≤ 1 := by
        split <;> omega
      have := Nat.add_le_add_right ihr 1
      omega
    · simp only [List.filter_cons]
      rw [if_neg hty, scan_cons_d]
      cases he with
      | inl h00 =>
        obtain ⟨ha0, hb0, hpp⟩ := h00
        have hif : ¬ ((pre && !e.post) = true) := by
          rw [hpc.symm, hpp]
          by_cases hpost : e.post = true <;> simp_all
        rw [if_neg hif]
        omega
      | inr hr =>
        cases hr with
        | inl h10 =>
          obtain ⟨ha1, hb1⟩ := h10
          have hcontra : (is10 e = true) := (is10_iff e).mpr ⟨ha1, hb1⟩
          simp [hcontra] at hty
        | inr hr2 =>
          cases hr2 with
          | inl h01 =>
            obtain ⟨ha0, hb0, hpre, hpost⟩ := h01
            have hpre2 : pre = false := hpc ▸ hpre
            have hif : ¬ ((pre && !e.post) = true) := by
              simp [hpre2]
            rw [if_neg hif]
            omega
          | inr h11 =>
            obtain ⟨ha1, hb1, hnn⟩ := h11
            have hif : ¬ ((pre && !e.post) = true) := by
              rw [hpc.symm]
              by_cases hepre : e.pre = true <;>
                by_cases hpost : e.post = true <;> simp_all
            rw [if_neg hif]
            omega

-- Weight equals (#01) - (#10) on classified walks.
theorem scan_weight (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) :
    (scan pre es).1
      = (((es.filter is01).length : Int)
        - ((es.filter is10).length : Int)) := by
  induction es generalizing pre with
  | nil => simp [scan]
  | cons e es ih =>
    have he := h e (by simp)
    have ihr := ih e.post (fun e' hm => h e' (by simp [hm]))
    simp only [edgeOk] at he
    rw [scan_cons_w]
    simp only [List.filter_cons]
    cases he with
    | inl h00 =>
      obtain ⟨ha0, hb0, -⟩ := h00
      have f01 : ¬ (is01 e = true) := by simp [is01, ha0, hb0]
      have f10 : ¬ (is10 e = true) := by simp [is10, ha0]
      rw [if_neg f01, if_neg f10]
      omega
    | inr hr =>
      cases hr with
      | inl h10 =>
        obtain ⟨ha1, hb1⟩ := h10
        have f01 : ¬ (is01 e = true) := by simp [is01, ha1]
        have f10 : (is10 e = true) := by simp [is10, ha1, hb1]
        rw [if_neg f01, if_pos f10, List.length_cons]
        omega
      | inr hr2 =>
        cases hr2 with
        | inl h01 =>
          obtain ⟨ha0, hb0, -, -⟩ := h01
          have f01 : (is01 e = true) := by simp [is01, ha0, hb0]
          have f10 : ¬ (is10 e = true) := by simp [is10, ha0]
          rw [if_pos f01, if_neg f10, List.length_cons]
          omega
        | inr h11 =>
          obtain ⟨ha1, hb1, -⟩ := h11
          have f01 : ¬ (is01 e = true) := by simp [is01, ha1]
          have f10 : ¬ (is10 e = true) := by simp [is10, hb1]
          rw [if_neg f01, if_neg f10]
          omega

-- Twin-start A-work forcing (T1 edge core): from a twin-bit state, an
-- A-cost-0 classified edge must be a (0,0) self-loop. Hence any
-- non-trivial vine path starting twin does A-work >= 1 on its first edge.
-- (Human assembly: (0,0) vine edges are state self-loops via splay-at-root
-- noop + DELETE-freeze/B-noop, so the path stays put unless it pays A>=1.)
theorem twin_exit_A (e : VEdge) (h : edgeOk e) (ht : e.pre = true)
    (ha : e.a = 0) : e.b = 0 := by
  simp only [edgeOk] at h
  cases h with
  | inl h00 => exact h00.2.1
  | inr hr =>
    cases hr with
    | inl h10 =>
      obtain ⟨ha1, -⟩ := h10
      omega
    | inr hr2 =>
      cases hr2 with
      | inl h01 =>
        obtain ⟨-, -, hpre, -⟩ := h01
        simp [hpre] at ht
      | inr h11 =>
        obtain ⟨ha1, -⟩ := h11
        omega

-- Vine bit-change law (§10 excursion scaffold): along any classified
-- threaded walk, twin-bit drop is bounded by total A-work. In differ-bit
-- form this reads d(end)-d(start) <= A(V). Follows per-edge from the flip
-- table + costs (no splay model needed beyond edgeOk).

def twinVal : Bool → Int
  | true => 1
  | false => 0

def asum : List VEdge → Nat
  | [] => 0
  | e :: es => e.a + asum es

theorem twinVal_le_one (b : Bool) : twinVal b ≤ 1 := by
  cases b <;> simp [twinVal]

theorem twinVal_nonneg (b : Bool) : 0 ≤ twinVal b := by
  cases b <;> simp [twinVal]

-- Per-edge: twin-bit drop across one classified edge is paid by its A-cost.
theorem vine_step_le (e : VEdge) (pre : Bool)
    (h : edgeOk e) (hc : e.pre = pre) :
    twinVal pre - twinVal e.post ≤ (e.a : Int) := by
  simp only [edgeOk] at h
  cases h with
  | inl h00 =>
    obtain ⟨ha0, hb0, hpp⟩ := h00
    have hpre : pre = e.post := by rw [← hc]; exact hpp
    rw [hpre]
    omega
  | inr hr =>
    cases hr with
    | inl h10 =>
      obtain ⟨ha1, -⟩ := h10
      have h1 := twinVal_le_one pre
      have h2 := twinVal_nonneg e.post
      omega
    | inr hr2 =>
      cases hr2 with
      | inl h01 =>
        obtain ⟨ha0, hb0, hpre, hpost⟩ := h01
        have hpre2 : pre = false := hc ▸ hpre
        rw [hpre2, hpost]
        simp only [twinVal]
        omega
      | inr h11 =>
        obtain ⟨ha1, hb1, -⟩ := h11
        have h1 := twinVal_le_one pre
        have h2 := twinVal_nonneg e.post
        omega

-- Telescoped path version.
theorem vine_bit_le_A (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) (hc : okChain pre es) :
    twinVal pre - twinVal (endBit pre es) ≤ (asum es : Int) := by
  induction es generalizing pre with
  | nil => simp [twinVal, asum, endBit]
  | cons e es ih =>
    have he := h e (by simp)
    obtain ⟨hpc, hcc⟩ := hc
    have ihr := ih e.post (fun e' hm => h e' (by simp [hm])) hcc
    have hstep := vine_step_le e pre he hpc
    have hE : endBit pre (e :: es) = endBit e.post es :=
      endBit_cons e es pre
    rw [hE]
    simp only [asum]
    omega

-- W_2 twin-bit path law (§10 companion): on classified threaded walks,
-- total B-2A is bounded by twice the twin-bit rise. In differ-bits this
-- reads W_2(V) <= 2(tau(s)-tau(t)). Holds on all vine-internal edges
-- (n>=5 by V1-costs + root-tracking flips; n<=4 by finite check), hence
-- on all vine-confined paths by telescoping. Finite-exact on excursions
-- n=6,7 (R0-rule); witness-scale (+9) exceeds its +2 range.

def scanW2 : Bool → List VEdge → Int
  | _, [] => 0
  | _, e :: es => ((e.b : Int) - 2 * (e.a : Int)) + scanW2 e.post es

theorem scanW2_cons (e : VEdge) (es : List VEdge) :
    scanW2 pre (e :: es)
      = ((e.b : Int) - 2 * (e.a : Int)) + scanW2 e.post es := rfl

-- Per-edge: B-2A is bounded by twice the twin-bit rise.
theorem vine_W2_step_le (e : VEdge) (pre : Bool)
    (h : edgeOk e) (hc : e.pre = pre) :
    ((e.b : Int) - 2 * (e.a : Int))
      ≤ 2 * ((if e.post then (1 : Int) else 0)
        - (if pre then 1 else 0)) := by
  simp only [edgeOk] at h
  cases h with
  | inl h00 =>
    obtain ⟨ha0, hb0, hpp⟩ := h00
    have hpre : pre = e.post := by rw [← hc]; exact hpp
    rw [hpre, ha0, hb0]
    simp
  | inr hr =>
    cases hr with
    | inl h10 =>
      obtain ⟨ha1, hb1⟩ := h10
      rw [ha1, hb1]
      by_cases hpre : pre = true <;> by_cases hpost : e.post = true <;>
        simp_all <;> omega
    | inr hr2 =>
      cases hr2 with
      | inl h01 =>
        obtain ⟨ha0, hb0, hpre, hpost⟩ := h01
        rw [ha0, hb0]
        by_cases hpre2 : pre = true <;> by_cases hpost2 : e.post = true <;>
          simp_all <;> omega
      | inr h11 =>
        obtain ⟨ha1, hb1, hnn⟩ := h11
        rw [ha1, hb1]
        by_cases hpre : pre = true <;> by_cases hpost : e.post = true <;>
          simp_all <;> omega

-- Telescoped path version.
theorem vine_W2_twin_bound (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) (hc : okChain pre es) :
    scanW2 pre es
      ≤ 2 * ((if endBit pre es then (1 : Int) else 0)
        - (if pre then 1 else 0)) := by
  induction es generalizing pre with
  | nil => simp [scanW2, endBit]
  | cons e es ih =>
    have he := h e (by simp)
    obtain ⟨hpc, hcc⟩ := hc
    have ihr := ih e.post (fun e' hm => h e' (by simp [hm])) hcc
    have hstep := vine_W2_step_le e pre he hpc
    have hE : endBit pre (e :: es) = endBit e.post es :=
      endBit_cons e es pre
    rw [scanW2_cons, hE]
    omega

-- Main counting theorem: closed classified walks have B-A <= 0.
theorem vine_cycle_nonpos (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) (hc : okChain pre es)
    (hcl : endBit pre es = pre) :
    (scan pre es).1 ≤ 0 := by
  have hw := scan_weight pre es h
  have hbal := scan_closed pre es hcl
  have h1 := count01_le pre es h hc
  have h2 := count10_le pre es h hc
  omega

-- Open-path boundary law (§2 excursion scaffold): a vine-confined PATH
-- (not necessarily closed) satisfies W <= twin(end) - twin(start), i.e.
-- B-A <= tau(s) - tau(t) in differ-bit form (tau = negation of Lean bit).
-- Sharp: single (0,1) edges attain equality. Closed walks recover
-- vine_cycle_nonpos (boundary cancels).
theorem vine_path_bound (pre : Bool) (es : List VEdge)
    (h : ∀ e ∈ es, edgeOk e) (hc : okChain pre es) :
    (scan pre es).1
      ≤ (if endBit pre es then (1 : Int) else 0)
        - (if pre then 1 else 0) := by
  have hw := scan_weight pre es h
  have h1 := count01_le pre es h hc
  have h2 := count10_le pre es h hc
  have ht := scan_telescope es pre
  split at ht
  split at ⊢
  all_goals omega
