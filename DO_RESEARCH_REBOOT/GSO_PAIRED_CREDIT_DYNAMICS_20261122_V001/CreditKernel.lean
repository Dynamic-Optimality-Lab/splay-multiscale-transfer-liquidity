import Std

namespace PairedCredit

inductive Tree where
  | leaf
  | node (left right : Tree)

def size : Tree → Nat
  | .leaf => 0
  | .node l r => size l+size r+1

theorem physical_RR_alias (a b c d : Tree)
    (outer : size a=size d) (inner : size b=size c) :
    size (Tree.node c d)=size (Tree.node a b) ∧
    size (Tree.node b (Tree.node c d))=size (Tree.node (Tree.node a b) c) := by
  simp only [size] at *
  omega

theorem all_cardinality_weights_cancel (w : Nat → Int) (a b c d : Tree)
    (outer : size a=size d) (inner : size b=size c) :
    w (size (Tree.node c d))+w (size (Tree.node b (Tree.node c d)))-
    w (size (Tree.node a b))-w (size (Tree.node (Tree.node a b) c))=0 := by
  obtain ⟨h1,h2⟩ := physical_RR_alias a b c d outer inner
  rw [h1,h2]
  omega

def First (c P : Int) : Prop := (1)*c + (-16)*P + (9)*1 = 0
def Second (S P j : Int) : Prop := (1)*S + (-16)*P + (16)*j + (12)*1 = 0

theorem learned_initialization : First 7 1 ∧ Second 4 1 0 := by
  simp [First, Second]

theorem learned_joint_preservation (c P S j : Int)
    (h1 : First c P) (h2 : Second S P j) :
    First (2*c+9) (2*P) ∧ Second (S+c-7) (2*P) (j+1) := by
  unfold First Second at *
  omega

theorem physical_support_identity (q S P N : Int)
    (h : Second S P q) (support : N=16*(q+1)+1+S) : N=16*P+5 := by
  unfold Second at h
  omega

def power : Nat → Int
  | 0 => 1
  | n+1 => 2*power n

theorem power_is_two_pow (n : Nat) : power n=(2:Int)^n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [power, ih, Int.pow_succ, Int.mul_comm]

theorem positive_padding (c P S j : Int)
    (hc : 7≤c) (hP : 1≤P) (hS : 4≤S) (hj : 0≤j) :
    7≤2*c+9 ∧ 1≤2*P ∧ 4≤S+c-7 ∧ 0≤j+1 := by omega

theorem bounded_signed_A_issuance (old new M : Int)
    (ho : -M≤old) (_ho' : old≤M) (_hn : -M≤new) (hn' : new≤M) :
    new-old≤2*M := by omega

theorem signed_size_energy_cannot_pay_all_bursts (C M : Int) (u v : Int → Int)
    (hC : 0≤C) (hM : 0≤M)
    (lowerU : ∀ q, -M≤u q) (lowerV : ∀ q, -M≤v q) :
    ¬ (∀ q : Int, 1≤q → q+1+u q+v q≤C) := by
  intro all
  have bad := all (C+2*M+1) (by omega)
  have hu := lowerU (C+2*M+1)
  have hv := lowerV (C+2*M+1)
  omega

theorem nonnegative_size_energy_cannot_pay_all_bursts (q C u v : Int)
    (large : C<q+1) (hu : 0≤u) (hv : 0≤v) :
    ¬ (q+1+u+v≤C) := by omega

theorem memory_or_shape_must_supply (q C M decrease u v : Int)
    (hu : -M≤u) (hv : -M≤v)
    (paid : q+1+u+v-decrease≤C) : q+1-C-2*M≤decrease := by omega

theorem supply_preserves_required_credit (G need next s cap : Int)
    (entry : need≤G) (recurrence : next-s≤need) (capacity : next≤cap) :
    next≤min cap (G+s) := by omega

theorem demand_preserves_required_credit (G next d : Int)
    (entry : d+next≤G) (nonnegative : 0≤next) :
    d≤G ∧ next≤G-d := by omega

theorem clipped_credit_monotone (g h cap s : Int) (entry : g≤h) :
    min cap (g+s)≤min cap (h+s) := by omega

theorem closed_balance_has_no_free_spend (start finish issued paid : Int)
    (conservation : finish-start=issued-paid) (closed : finish=start) :
    paid=issued := by omega

theorem bounded_unpaid_cost_is_permitted (Q paid unpaid issued A K : Int)
    (cost : Q=paid+unpaid) (cyclic : paid=issued)
    (actualA : issued≤4*A) (residual : unpaid≤K*A) :
    Q≤(4+K)*A := by
  rw [Int.add_mul]
  omega

def capacity (r : Int) : Int := max (max (8*r) (12*r-4)) (max (14*r-12) (15*r-28))

theorem exact_H_capacity_bounds (r : Int) (hr : 2≤r) :
    8*r≤capacity r ∧ 12*r-4≤capacity r ∧
    14*r-12≤capacity r ∧ 15*r-28≤capacity r ∧ capacity r≤15*r := by
  unfold capacity
  omega

theorem complete_critical_credit (r : Int) (hr : 2≤r) :
    0≤capacity r-8*r ∧
    min (capacity r) (capacity r-8*r+4)-4*r=capacity r-12*r+4 ∧
    0≤capacity r-12*r+4 ∧
    min (capacity r) (capacity r-12*r+4+8)-2*r=capacity r-14*r+12 ∧
    0≤capacity r-14*r+12 ∧
    min (capacity r) (capacity r-14*r+12+16)-r=capacity r-15*r+28 ∧
    0≤capacity r-15*r+28 := by
  have bounds := exact_H_capacity_bounds r hr
  omega

theorem descending_restoration_refills (r : Int) (hr : 2≤r) :
    min (capacity r) (capacity r-15*r+28+4*(16*r-7))=capacity r := by
  have bounds := exact_H_capacity_bounds r hr
  omega

theorem arbitrary_forward_step (cap G q : Int)
    (buffer : cap-4≤G) (box : G≤cap) (cost : 0≤q) (costBound : q≤4)
    (room : 4≤cap) :
    q≤min cap (G+4) ∧ cap-4≤min cap (G+4)-q ∧ min cap (G+4)-q≤cap := by omega

theorem cyclic_reverse_restoration_refills (r G : Int) (hr : 2≤r) (entry : 0≤G) :
    min (capacity r) (G+4*(16*r))=capacity r := by
  have bounds := exact_H_capacity_bounds r hr
  omega

theorem first_burst_requires_past_credit (r before after issued : Int)
    (noCurrentA : issued=0) (conservation : after-before=issued-8*r)
    (funded : 0≤after) : 8*r≤before := by omega

#print axioms physical_RR_alias
#print axioms all_cardinality_weights_cancel
#print axioms learned_joint_preservation
#print axioms physical_support_identity
#print axioms power_is_two_pow
#print axioms signed_size_energy_cannot_pay_all_bursts
#print axioms memory_or_shape_must_supply
#print axioms supply_preserves_required_credit
#print axioms closed_balance_has_no_free_spend
#print axioms bounded_unpaid_cost_is_permitted
#print axioms complete_critical_credit
#print axioms descending_restoration_refills
#print axioms arbitrary_forward_step
#print axioms cyclic_reverse_restoration_refills

end PairedCredit
