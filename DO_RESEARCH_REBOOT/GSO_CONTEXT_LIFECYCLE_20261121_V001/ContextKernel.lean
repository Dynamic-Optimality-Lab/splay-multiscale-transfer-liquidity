import Std

namespace GSOContext

inductive Tree (α : Type) where
  | empty
  | node (left : Tree α) (key : α) (right : Tree α)

def right : Tree α → Tree α
  | .node (.node l p h) g r => .node l p (.node h g r)
  | t => t

def left : Tree α → Tree α
  | .node l g (.node h p r) => .node (.node l g h) p r
  | t => t

theorem fullLL (A B C D : Tree α) (x p g : α) :
    right (right (.node (.node (.node A x B) p C) g D)) =
    .node A x (.node B p (.node C g D)) := by rfl

theorem fullRR (A B C D : Tree α) (g p x : α) :
    left (left (.node A g (.node B p (.node C x D)))) =
    .node (.node (.node A g B) p C) x D := by rfl

theorem identicalPrefix (p a q before after : Int) (hp : 0 ≤ p)
    (h : 2*q + after - before ≤ 3*a) :
    2*(p+q) + after - before ≤ 3*(p+a) := by omega

def sum (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n+1 => sum f n + f n

theorem telescope (a q φ : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → 2*q i + φ (i+1) ≤ 3*a i + φ i) :
    2*sum q n + φ n ≤ 3*sum a n + φ 0 := by
  induction n with
  | zero => simp [sum]
  | succ n ih =>
      have hp := ih (fun i hi => h i (Nat.lt_trans hi (Nat.lt_succ_self n)))
      have hn := h n (Nat.lt_succ_self n)
      simp only [sum]
      omega

theorem closedBound (a q φ : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → 2*q i + φ (i+1) ≤ 3*a i + φ i)
    (closed : φ n = φ 0) : 2*sum q n ≤ 3*sum a n := by
  have ht := telescope a q φ n h
  omega

theorem equalValueObstruction (F : Nat → Int) (core C : Nat) :
    (C+2 : Int) + F core - F core > (C : Int) := by omega

#print axioms fullLL
#print axioms fullRR
#print axioms identicalPrefix
#print axioms closedBound
#print axioms equalValueObstruction

end GSOContext
