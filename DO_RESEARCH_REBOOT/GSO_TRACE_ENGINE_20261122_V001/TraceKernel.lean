import Std

namespace GSOTrace

theorem exchangeConserves (lo hi : Int) : (hi+lo)-(lo+hi)=0 := by omega

theorem ledgerStep (paid bank issued initial dp db di : Int)
    (invariant : paid+bank-issued=initial)
    (conservation : dp+db=di) :
    (paid+dp)+(bank+db)-(issued+di)=initial := by omega

theorem closedLedger (Q bank issued initial c A d K : Int)
    (invariant : Q+bank-issued=initial)
    (seam : bank=initial) (budget : issued ≤ c*A+d*K) :
    Q ≤ c*A+d*K := by omega

theorem originalConstant (Q A K c d : Int) (hd : 0 ≤ d)
    (bound : Q ≤ c*A+d*K) (gap : K ≤ A) : Q ≤ (c+d)*A := by
  have h : d*K ≤ d*A := Int.mul_le_mul_of_nonneg_left gap hd
  rw [Int.add_mul]
  omega

theorem pumpObstruction (q c d R delta : Int)
    (lower : -(10*R) ≤ delta) (large : c+d+10*R < q+1) :
    ¬ (q+1+delta ≤ c+d) := by omega

#print axioms exchangeConserves
#print axioms ledgerStep
#print axioms closedLedger
#print axioms originalConstant
#print axioms pumpObstruction

end GSOTrace
