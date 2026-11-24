import Std

namespace ConservativeTransport

theorem targetRise (H t fresh other next : Int)
    (_hH : 1<=H) (ht : 0<=t) (bound : t<=H)
    (hf : 2<=fresh) (ho : 0<=other)
    (rule : next=min H (max 0 (t+fresh+other-1))) :
    min H (t+1)<=next := by omega

theorem persistentOne (H fresh other persistent : Int)
    (hH : 1<=H) (hf : 2<=fresh) (ho : 0<=other)
    (rule : persistent=min H (max 0 (H+fresh+other-1-H))) :
    1<=persistent := by omega

theorem warmBound (stock : Nat -> Int) (H : Int)
    (hH : 1<=H) (h0 : 0<=stock 0)
    (step : forall n, min H (stock n+1)<=stock (n+1)) :
    forall n : Nat, min H (n:Int)<=stock n := by
  intro n
  induction n with
  | zero => omega
  | succ n ih =>
    have h := step n
    have cast : ((n+1:Nat):Int)=(n:Int)+1 := by omega
    rw [cast]
    omega

theorem warmed (stock : Nat -> Int) (H : Nat)
    (hH : 1<=H) (h0 : 0<=stock 0)
    (cap : forall n, stock n<=(H:Int))
    (step : forall n, min (H:Int) (stock n+1)<=stock (n+1)) :
    stock H=(H:Int) := by
  have hi : 1<=(H:Int) := by omega
  have lower := warmBound stock (H:Int) hi h0 step H
  have upper := cap H
  omega

theorem noProfileLeak (H persistent leftRoot retired : Int)
    (hp : persistent=H) (hl : leftRoot=H) (hr : retired=H-1) :
    2*persistent+leftRoot=3*H /\ persistent-retired=1 := by omega

theorem packetStep (H t other q next : Int)
    (_cap : t<=H) (fed : q<=t+other)
    (rule : next=min H (max 0 (t+other-q))) :
    H-next=max 0 (H-t+q-other) := by omega

theorem packetGuard (H t other q : Int) :
    H-t+q-other<=H <-> q<=t+other := by omega

#print axioms targetRise
#print axioms persistentOne
#print axioms warmBound
#print axioms warmed
#print axioms noProfileLeak
#print axioms packetStep
#print axioms packetGuard

end ConservativeTransport
