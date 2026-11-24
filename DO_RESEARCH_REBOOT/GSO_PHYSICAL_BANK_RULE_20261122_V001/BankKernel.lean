import Std

namespace PhysicalBank

theorem greatestByRank {α : Type} [DecidableEq α]
    (f : α → α) (R : α → α → Prop) (rank : α → Nat)
    (refl : ∀ a, R a a)
    (trans : ∀ a b c, R a b → R b c → R a c)
    (mono : ∀ a b, R a b → R (f a) (f b))
    (rankDrop : ∀ a b, R a b → a ≠ b → rank a < rank b) :
    ∀ b, R (f b) b →
      ∃ c, f c = c ∧ R c b ∧ ∀ d, f d = d → R d b → R d c := by
  have descend : ∀ n, ∀ b, rank b = n → R (f b) b →
      ∃ c, f c = c ∧ R c b ∧ ∀ d, f d = d → R d b → R d c := by
    intro n
    refine Nat.strongRecOn n ?_
    intro n ih b hb hdown
    by_cases hfix : f b = b
    · exact ⟨b, hfix, refl b, fun d _ hdb => hdb⟩
    · have hrank := rankDrop (f b) b hdown hfix
      rw [hb] at hrank
      have hnext : R (f (f b)) (f b) := mono (f b) b hdown
      obtain ⟨c, hc, hcb, hgreat⟩ := ih (rank (f b)) hrank (f b) rfl hnext
      refine ⟨c, hc, trans c (f b) b hcb hdown, ?_⟩
      intro d hd hdb
      apply hgreat d hd
      have hfd := mono d b hdb
      simpa only [hd] using hfd
  intro b hdown
  exact descend (rank b) b rfl hdown

theorem creditConservation (before after issued paid : Int)
    (balance : after-before=issued-paid) :
    paid+after=issued+before := by omega

theorem closedBudget (Q paid initial final issued A K H : Int)
    (allPaid : Q=paid) (conservation : paid+final=issued+initial)
    (seam : final=initial) (issue : issued ≤8*(H*A)+H*K)
    (hH : 0≤H) (gap : K≤A) : Q≤9*(H*A) := by
  have hmul : H*K≤H*A := Int.mul_le_mul_of_nonneg_left gap hH
  omega

theorem coarseningLoss (a b anew bnew retired : Int)
    (stationary : 2*a+b=1+anew+bnew+retired)
    (priority : anew≤retired) :
    2*anew+bnew≤2*a+b-1 := by omega

theorem sumUnitDrops (mass : Nat → Int)
    (step : ∀ n, mass (n+1)≤mass n-1) :
    ∀ n, mass n≤mass 0-(n:Int) := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
    have h := step n
    have hn : ((n+1:Nat):Int)=(n:Int)+1 := by omega
    rw [hn]
    omega

theorem truncatedDrops (mass : Nat → Int) (N : Nat)
    (initial : mass 0≤(N:Int))
    (step : ∀ n, mass (n+1)≤max (mass n-1) 0) :
    ∀ n, mass n≤max ((N:Int)-(n:Int)) 0 := by
  intro n
  induction n with
  | zero => omega
  | succ n ih =>
    have h := step n
    have hn : ((n+1:Nat):Int)=(n:Int)+1 := by omega
    rw [hn]
    omega

theorem profileExhausted (mass : Nat → Int) (H : Nat)
    (initial : mass 0≤3*(H:Int))
    (nonnegative : ∀ n, 0≤mass n)
    (step : ∀ n, mass (n+1)≤max (mass n-1) 0) :
    mass (3*H)=0 := by
  have hcast : ((3*H:Nat):Int)=3*(H:Int) := by omega
  have hi : mass 0≤((3*H:Nat):Int) := by omega
  have h := truncatedDrops mass (3*H) hi step (3*H)
  have hn := nonnegative (3*H)
  omega

theorem sumPrefixDrops (mass : Nat → Int) (T : Nat)
    (step : ∀ n, n<T → mass (n+1)≤mass n-1) :
    ∀ n, n≤T → mass n≤mass 0-(n:Int) := by
  intro n
  induction n with
  | zero => intro _; omega
  | succ n ih =>
    intro hn
    have hnt : n<T := by omega
    have h := step n hnt
    have hp := ih (by omega)
    have hcast : ((n+1:Nat):Int)=(n:Int)+1 := by omega
    rw [hcast]
    omega

theorem dryPacketCannotPay (mass : Nat → Int) (H : Nat)
    (initial : mass 0≤3*(H:Int))
    (nonnegative : 0≤mass (3*H+1))
    (allFundedDrops : ∀ n, n<3*H+1 → mass (n+1)≤mass n-1) : False := by
  have h := sumPrefixDrops mass (3*H+1) allFundedDrops (3*H+1) (by omega)
  have hcast : ((3*H+1:Nat):Int)=3*(H:Int)+1 := by omega
  rw [hcast] at h
  omega

#print axioms greatestByRank
#print axioms creditConservation
#print axioms closedBudget
#print axioms coarseningLoss
#print axioms profileExhausted
#print axioms dryPacketCannotPay

end PhysicalBank
