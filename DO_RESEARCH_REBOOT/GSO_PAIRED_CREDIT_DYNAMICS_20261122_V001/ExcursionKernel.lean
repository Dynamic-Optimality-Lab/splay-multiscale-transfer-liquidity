import Std

namespace OriginalCreditExcursion

def Stock (m : Nat) := Fin m → Int
def Le {m : Nat} (a b : Stock m) : Prop := ∀ i, a i≤b i

def iterate {m : Nat} (F : Stock m → Stock m) : Nat → Stock m → Stock m
  | 0, x => x
  | n+1, x => F (iterate F n x)

theorem pointwise_trans {m : Nat} {a b c : Stock m} (ab : Le a b) (bc : Le b c) : Le a c := by
  intro i
  have h1 := ab i
  have h2 := bc i
  omega

theorem greater_period_map_dominates_closed_balance {m : Nat}
    (F G : Stock m → Stock m) (fixed upper : Stock m)
    (initial : Le fixed upper) (closed : F fixed=fixed)
    (dominates : ∀ x, Le (F x) (G x))
    (monotone : ∀ a b, Le a b → Le (G a) (G b)) :
    ∀ n, Le fixed (iterate G n upper) := by
  intro n
  induction n with
  | zero => exact initial
  | succ n ih =>
    have low : Le fixed (G fixed) := by simpa [closed] using dominates fixed
    have high := monotone fixed (iterate G n upper) ih
    exact pointwise_trans low high

theorem augmented_greatest_seam_dominates {m : Nat}
    (F G : Stock m → Stock m) (base top augmented : Stock m) (steps : Nat)
    (baseBox : Le base top) (baseClosed : F base=base)
    (periodDomination : ∀ x, Le (F x) (G x))
    (periodMonotone : ∀ a b, Le a b → Le (G a) (G b))
    (constructedSeam : augmented=iterate G steps top) : Le base augmented := by
  rw [constructedSeam]
  exact greater_period_map_dominates_closed_balance F G base top baseBox baseClosed periodDomination periodMonotone steps

theorem physical_A_reset_adds_no_negative_credit (before H : Int)
    (box : before≤H) : before≤H := box

theorem persistent_A_supply_is_nondecreasing (before cap supply : Int)
    (box : before≤cap) (nonnegative : 0≤supply) :
    before≤min cap (before+supply) := by omega

theorem every_pooling_coordinate_is_monotone (mass larger H q offset : Int)
    (entry : mass≤larger) :
    min H (max 0 (mass-q-offset))≤min H (max 0 (larger-q-offset)) := by omega

theorem original_unpaid_cost_is_antitone (mass larger q : Int) (entry : mass≤larger) :
    max 0 (q-larger)≤max 0 (q-mass) := by omega

theorem coupled_global_reserve_is_monotone (mass larger G higher q : Int)
    (localEntry : mass≤larger) (globalEntry : G≤higher) :
    max 0 (G-max 0 (q-mass))≤max 0 (higher-max 0 (q-larger)) := by omega

def total (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n+1 => total f n+f n

theorem sum_matched_original_B_once (base augmented : Nat → Int)
    (pointwiseUnpaid : ∀ i, augmented i≤base i) :
    ∀ n, total augmented n≤total base n := by
  intro n
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have step := pointwiseUnpaid n
    simp only [total]
    omega

theorem inherited_global_issuance (H oldA extraA oldBudget extraBudget : Int)
    (base : oldBudget≤9*H*oldA) (added : extraBudget≤9*H*extraA) :
    oldBudget+extraBudget≤9*H*(oldA+extraA) := by
  rw [Int.mul_add]
  omega

theorem same_constant_lifts_from_loop_erased_sources (Q Ared A C : Int)
    (costReduction : Ared≤A) (nonnegativeConstant : 0≤C)
    (reducedBound : Q≤C*Ared) : Q≤C*A := by
  have comparison := Int.mul_le_mul_of_nonneg_left costReduction nonnegativeConstant
  omega

theorem unpaid_bound_lifts_from_loop_erased_sources (Ored O Ared A K : Int)
    (unpaidReduction : O≤Ored) (costReduction : Ared≤A)
    (nonnegativeConstant : 0≤K) (reducedBound : Ored≤K*Ared) : O≤K*A := by
  have comparison := Int.mul_le_mul_of_nonneg_left costReduction nonnegativeConstant
  omega

#print axioms greater_period_map_dominates_closed_balance
#print axioms augmented_greatest_seam_dominates
#print axioms persistent_A_supply_is_nondecreasing
#print axioms every_pooling_coordinate_is_monotone
#print axioms original_unpaid_cost_is_antitone
#print axioms coupled_global_reserve_is_monotone
#print axioms sum_matched_original_B_once
#print axioms inherited_global_issuance
#print axioms same_constant_lifts_from_loop_erased_sources
#print axioms unpaid_bound_lifts_from_loop_erased_sources

end OriginalCreditExcursion
