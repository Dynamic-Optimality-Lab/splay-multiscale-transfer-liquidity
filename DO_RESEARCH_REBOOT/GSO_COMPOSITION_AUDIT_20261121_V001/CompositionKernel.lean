import Std

namespace GSOComposition

theorem compose (Q A localQ localA E carry L D B : Int)
    (cover : Q ≤ localQ + E)
    (localBound : 2*localQ ≤ 3*localA + carry)
    (reuse : localA ≤ L*A)
    (overhead : E ≤ D*A)
    (boundary : carry ≤ B*A) :
    2*Q ≤ (3*L+2*D+B)*A := by
  have h : 2*Q ≤ 3*(L*A)+2*(D*A)+B*A := by omega
  simpa [Int.add_mul, Int.mul_assoc] using h

theorem residualSandwich (Q I E K A : Int)
    (split : Q = I+E) (nonneg : 0 ≤ I)
    (internal : I ≤ 2*K) (gap : K ≤ A) :
    E ≤ Q ∧ Q ≤ E+2*A := by omega

inductive Shape3 where
  | vineR | middle | vineL | hookR | hookL
  deriving DecidableEq

inductive Key3 where
  | one | two | three

open Shape3 Key3

def splay3 : Shape3 → Key3 → Shape3
  | vineR, one | middle, one | vineL, one => vineR
  | vineR, two | middle, two | vineL, two => middle
  | vineR, three | middle, three | vineL, three => vineL
  | hookR, one | hookL, one => hookR
  | hookR, two | hookL, two => middle
  | hookR, three | hookL, three => hookL

def inClosedSet (s : Shape3) : Prop :=
  s = vineR ∨ s = middle ∨ s = vineL

theorem stepClosed (s : Shape3) (key : Key3) (h : inClosedSet s) :
    inClosedSet (splay3 s key) := by
  cases s <;> cases key <;> simp_all [inClosedSet, splay3]

def run (s : Shape3) : List Key3 → Shape3
  | [] => s
  | key::rest => run (splay3 s key) rest

theorem runClosed (s : Shape3) (keys : List Key3) (h : inClosedSet s) :
    inClosedSet (run s keys) := by
  induction keys generalizing s with
  | nil => simpa [run] using h
  | cons key rest ih =>
      exact ih (splay3 s key) (stepClosed s key h)

theorem noLocalSplayHistory (keys : List Key3) :
    run vineR keys ≠ hookL := by
  have h := runClosed vineR keys (by simp [inClosedSet])
  intro heq
  rw [heq] at h
  simp [inClosedSet] at h

#print axioms compose
#print axioms residualSandwich
#print axioms stepClosed
#print axioms noLocalSplayHistory

end GSOComposition
