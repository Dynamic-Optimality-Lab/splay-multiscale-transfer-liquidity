import Std

namespace GSO

inductive Tree (α : Type) where
  | empty
  | node (left : Tree α) (key : α) (right : Tree α)

def inorder : Tree α → List α
  | .empty => []
  | .node l k r => inorder l ++ [k] ++ inorder r

theorem rightRotation (L H R : Tree α) (p g : α) :
    inorder (.node (.node L p H) g R) =
    inorder (.node L p (.node H g R)) := by
  simp [inorder, List.append_assoc]

theorem leftRotation (L H R : Tree α) (g p : α) :
    inorder (.node L g (.node H p R)) =
    inorder (.node (.node L g H) p R) := by
  simp [inorder, List.append_assoc]

theorem LL (A B C D : Tree α) (x p g : α) :
    inorder (.node (.node (.node A x B) p C) g D) =
    inorder (.node A x (.node B p (.node C g D))) := by
  simp [inorder, List.append_assoc]

theorem RR (A B C D : Tree α) (g p x : α) :
    inorder (.node A g (.node B p (.node C x D))) =
    inorder (.node (.node (.node A g B) p C) x D) := by
  simp [inorder, List.append_assoc]

theorem LR (A B C D : Tree α) (p x g : α) :
    inorder (.node (.node A p (.node B x C)) g D) =
    inorder (.node (.node A p B) x (.node C g D)) := by
  simp [inorder, List.append_assoc]

theorem RL (A B C D : Tree α) (g x p : α) :
    inorder (.node A g (.node (.node B x C) p D)) =
    inorder (.node (.node A g B) x (.node C p D)) := by
  simp [inorder, List.append_assoc]

def prefixSum (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n+1 => prefixSum f n + f n

theorem telescope (a q φ : Nat → Int) (C : Int) (n : Nat)
    (h : ∀ i, i < n → q i + φ (i+1) ≤ C * a i + φ i) :
    prefixSum q n + φ n ≤ C * prefixSum a n + φ 0 := by
  induction n with
  | zero => simp [prefixSum]
  | succ n ih =>
      have hp := ih (fun i hi => h i (Nat.lt_trans hi (Nat.lt_succ_self n)))
      have hn := h n (Nat.lt_succ_self n)
      simp only [prefixSum, Int.mul_add]
      omega

theorem closedBudget (a q φ : Nat → Int) (C : Int) (n : Nat)
    (h : ∀ i, i < n → q i + φ (i+1) ≤ C * a i + φ i)
    (closed : φ n = φ 0) : prefixSum q n ≤ C * prefixSum a n := by
  have hb := telescope a q φ C n h
  omega

#print axioms rightRotation
#print axioms LL
#print axioms LR
#print axioms closedBudget

end GSO
