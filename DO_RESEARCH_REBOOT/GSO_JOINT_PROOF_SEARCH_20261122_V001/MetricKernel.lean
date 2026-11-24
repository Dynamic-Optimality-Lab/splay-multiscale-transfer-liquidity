import Std

namespace PhysicalMetric

inductive Tree where
  | leaf
  | node (left right : Tree)

def size : Tree → Nat
  | .leaf => 0
  | .node l r => size l + size r + 1

def ls : Tree → Nat
  | .leaf => 0
  | .node l _ => ls l + 1

inductive Rotation : Tree → Tree → Prop where
  | left (a b c : Tree) : Rotation (.node a (.node b c)) (.node (.node a b) c)
  | right (a b c : Tree) : Rotation (.node (.node a b) c) (.node a (.node b c))
  | belowLeft {a b : Tree} (c : Tree) : Rotation a b → Rotation (.node a c) (.node b c)
  | belowRight {a b : Tree} (c : Tree) : Rotation a b → Rotation (.node c a) (.node c b)

theorem spine_le_size (t : Tree) : ls t ≤ size t := by
  induction t with
  | leaf => simp [ls, size]
  | node l r il _ => simp only [ls, size]; omega

theorem rotation_preserves_size {a b : Tree} (h : Rotation a b) : size a=size b := by
  induction h with
  | left a b c => simp only [size]; omega
  | right a b c => simp only [size]; omega
  | belowLeft c _ ih => simp only [size]; omega
  | belowRight c _ ih => simp only [size]; omega

theorem one_rotation_spine_upper {a b : Tree} (h : Rotation a b) : ls b≤ls a+1 := by
  induction h with
  | left a b c => simp only [ls]; omega
  | right a b c => simp only [ls]; omega
  | belowLeft c _ ih => simp only [ls]; omega
  | belowRight c _ _ => simp only [ls]; omega

inductive Path : Nat → Tree → Tree → Prop where
  | refl (t : Tree) : Path 0 t t
  | cons {n : Nat} {a b c : Tree} : Rotation a b → Path n b c → Path (n+1) a c

theorem path_spine_upper {n : Nat} {a b : Tree} (h : Path n a b) : ls b≤ls a+n := by
  induction h with
  | refl t => omega
  | cons step _ ih =>
    have bound := one_rotation_spine_upper step
    omega

theorem geodesic_lower_bound {n : Nat} {a b : Tree}
    (h : Path n a b) (sameSize : size b=size a) (vine : ls b=size b) :
    size a-ls a≤n := by
  have bound := path_spine_upper h
  omega

theorem next_flattening_rotation (t : Tree) (h : ls t<size t) :
    ∃ u, Rotation t u ∧ ls u=ls t+1 ∧ size u=size t := by
  induction t with
  | leaf => simp [ls, size] at h
  | node l r il _ =>
    cases r with
    | leaf =>
      have smaller : ls l<size l := by simpa [ls, size] using h
      obtain ⟨u, step, grow, same⟩ := il smaller
      refine ⟨Tree.node u Tree.leaf, Rotation.belowLeft Tree.leaf step, ?_, ?_⟩
      · simp only [ls]; omega
      · simp only [size]; omega
    | node b c =>
      refine ⟨Tree.node (Tree.node l b) c, Rotation.left l b c, ?_, ?_⟩
      · simp only [ls]
      · simp only [size]; omega

theorem exact_flattening (d : Nat) :
    ∀ t, size t-ls t=d → ∃ u, Path d t u ∧ size u=size t ∧ ls u=size u := by
  induction d with
  | zero =>
    intro t gap
    refine ⟨t, Path.refl t, rfl, ?_⟩
    have bound := spine_le_size t
    omega
  | succ d ih =>
    intro t gap
    have small : ls t<size t := by omega
    obtain ⟨u, step, grow, same⟩ := next_flattening_rotation t small
    have rank : size u-ls u=d := by omega
    obtain ⟨v, rest, sizev, vine⟩ := ih u rank
    exact ⟨v, Path.cons step rest, sizev.trans same, vine⟩

theorem arbitrary_metric_values_cancel (f : Nat → Int) (N : Nat) :
    f (N-3)-f (N-3)=0 := by omega

theorem flat_original_fragment_rejects_trial (q C start finish : Int)
    (equalDescriptorValue : start=finish)
    (claimedFragment : q+1+finish-start≤14*C)
    (large : 14*C<q+1) : False := by omega

theorem no_integer_universal_fragment_bound (C : Int) (hC : 0≤C) :
    ¬ (∀ q : Int, 1≤q → q+1≤14*C) := by
  intro all
  have chosen := all (14*C+1) (by omega)
  omega

theorem bank_or_shape_must_supply_deficit (q C drop : Int)
    (accounted : q+1-drop≤14*C) : q+1-14*C≤drop := by omega

#print axioms one_rotation_spine_upper
#print axioms next_flattening_rotation
#print axioms exact_flattening
#print axioms geodesic_lower_bound
#print axioms flat_original_fragment_rejects_trial
#print axioms no_integer_universal_fragment_bound
#print axioms bank_or_shape_must_supply_deficit

end PhysicalMetric
