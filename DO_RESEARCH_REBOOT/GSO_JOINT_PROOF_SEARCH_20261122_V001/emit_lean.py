"""Emit a Lean induction certificate using the JOINTLY LEARNED parameters.

The arbitrary-hole substitution and frame proof are structural proof kernels;
the invariant coefficients and bounds substituted into them are learner output.
"""
import sys
import json
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def pattern(t):
    if t[0]=='hole':return '(Pattern.hole '+str(ord(t[1])-ord('A'))+')'
    return '(Pattern.node '+('true' if t[2] else 'false')+' '+pattern(t[3])+' '+pattern(t[4])+')'


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    folder=sys.argv[1] if len(sys.argv)>1 else 'run_005'
    cert=json.loads((HERE/folder/'CONTROL_CERTIFICATE.json').read_text());p=cert['candidate']
    schemas=json.loads((HERE/'PROOF_LANGUAGE.json').read_text())['rotation_schemas']
    case_text=[]
    for row in schemas:
        name=row['case'];term='(graft holes before_'+name+')'
        for path,direction in row['rotations']:
            fn='rotR' if direction=='right' else 'rotL'
            if path=='L':term='(belowLeft '+fn+' '+term+')'
            elif path=='R':term='(belowRight '+fn+' '+term+')'
            else:term='('+fn+' '+term+')'
        case_text.append('def before_'+name+' : Pattern := '+pattern(row['before']))
        case_text.append('theorem physical_'+name+' (holes : Nat -> Plain) : depths '+term+' = ['+str(row['old_root_post_depth'])+'] := by\n  simp [before_'+name+', graft, rotR, rotL, belowLeft, belowRight, depths, depths_embed]')
    path=p['path_invariant'];reserve=p['reserve_invariant']
    path_expr=' + '.join('('+str(a)+')*'+v for a,v in zip(path,['initial','remaining','doubles','zigs']))
    reserve_expr=' + '.join('('+str(a)+')*'+v for a,v in zip(reserve,['target','global','doubles','H','T']))
    text=r'''import Std

namespace JointCertificate

inductive Plain where
  | leaf
  | node (left right : Plain)

inductive Pattern where
  | hole (index : Nat)
  | node (mark : Bool) (left right : Pattern)

def embed : Plain -> Pattern
  | .leaf => .hole 0
  | .node l r => .node false (embed l) (embed r)

def depths : Pattern -> List Nat
  | .hole _ => []
  | .node mark l r =>
      (if mark then [0] else []) ++ (depths l).map Nat.succ ++ (depths r).map Nat.succ

def graft (holes : Nat -> Plain) : Pattern -> Pattern
  | .hole i => embed (holes i)
  | .node m l r => .node m (graft holes l) (graft holes r)

theorem depths_embed (t : Plain) : depths (embed t)=[] := by
  induction t with
  | leaf => rfl
  | node l r il ir => simp [embed, depths, il, ir]

theorem arbitrary_hanging_subtrees (holes : Nat -> Plain) (t : Pattern) :
    depths (graft holes t)=depths t := by
  induction t with
  | hole i => exact depths_embed (holes i)
  | node m l r il ir => simp [graft, depths, il, ir]

def rotR : Pattern -> Pattern
  | .node m (.node c a b) d => .node c a (.node m b d)
  | t => t

def rotL : Pattern -> Pattern
  | .node m a (.node c b d) => .node c (.node m a b) d
  | t => t

def belowLeft (f : Pattern -> Pattern) : Pattern -> Pattern
  | .node m l r => .node m (f l) r
  | t => t

def belowRight (f : Pattern -> Pattern) : Pattern -> Pattern
  | .node m l r => .node m l (f r)
  | t => t

@CASE_DEFS@

inductive RootRun : Nat -> Nat -> Prop where
  | already : RootRun 0 0
  | zig : RootRun 1 1
  | same : RootRun 2 2
  | cross : RootRun 2 1
  | beneath (remaining depth : Nat) (nonterminal : 3<=remaining)
      (tail : RootRun (remaining-2) depth) : RootRun remaining depth

theorem learned_root_bound {remaining depth : Nat}
    (run : RootRun remaining depth) : depth<=@BOUND@ := by
  induction run with
  | already => omega
  | zig => omega
  | same => omega
  | cross => omega
  | beneath remaining depth _ _ ih => exact ih

theorem all_original_frame_lengths (remaining : Nat) :
    Exists (fun depth => RootRun remaining depth) := by
  refine Nat.strongRecOn remaining ?_
  intro remaining ih
  by_cases h0 : remaining=0
  · subst remaining; exact Exists.intro 0 RootRun.already
  by_cases h1 : remaining=1
  · subst remaining; exact Exists.intro 1 RootRun.zig
  by_cases h2 : remaining=2
  · subst remaining; exact Exists.intro 2 RootRun.same
  have smaller : remaining-2<remaining := by omega
  obtain ⟨d, tail⟩ := ih (remaining-2) smaller
  exact Exists.intro d (RootRun.beneath remaining d (by omega) tail)

def badAfter (bad : Bool) : List Bool -> Bool
  | [] => bad
  | reset::rest => badAfter (if reset then false else bad) rest

theorem reset_free_good_stays_good (flags : List Bool) : badAfter false flags=false := by
  induction flags with
  | nil => rfl
  | cons flag rest ih => cases flag <;> simpa [badAfter] using ih

theorem a_genuine_reset_restores_invariant (flags : List Bool) (bad : Bool)
    (resetExists : true ∈ flags) : badAfter bad flags=false := by
  induction flags generalizing bad with
  | nil => simp at resetExists
  | cons flag rest ih =>
    cases flag with
    | false =>
      have tailReset : true ∈ rest := by simpa using resetExists
      simpa [badAfter] using ih bad tailReset
    | true => simpa [badAfter] using reset_free_good_stays_good rest

theorem original_cyclic_entry_is_derived (flags : List Bool) (bad : Bool)
    (resetExists : true ∈ flags) (pairedClosure : badAfter bad flags=bad) : bad=false := by
  have good := a_genuine_reset_restores_invariant flags bad resetExists
  rw [good] at pairedClosure
  exact pairedClosure.symm

def PathI (initial remaining doubles zigs : Int) : Prop := @PATH_EXPR@ = 0

theorem learned_path_initialization (n : Int) : PathI n n 0 0 := by
  unfold PathI; omega

theorem learned_path_double (n r q z : Int) (h : PathI n r q z) :
    PathI n (r-2) (q+1) z := by
  unfold PathI at *; omega

theorem learned_path_zig (n q : Int) (h : PathI n 1 q 0) :
    PathI n 0 q 1 := by
  unfold PathI at *; omega

def ReserveI (target global doubles H T : Int) : Prop := @RESERVE_EXPR@ >= 0

theorem learned_reserve_entry (H T G : Int)
    (hH : 0<=H) (entry : T<=G) : ReserveI H G 0 H T := by
  unfold ReserveI; omega

theorem learned_reserve_double (H T target G q other : Int)
    (_hH : 0<=H) (ht : 0<=target) (cap : target<=H)
    (_hg : 0<=G) (hr : 0<=other)
    (inv : ReserveI target G q H T) :
    ReserveI (min H (target+other-min 1 (target+other)))
      (G-min G (1-min 1 (target+other))) (q+1) H T := by
  unfold ReserveI at *; omega

theorem original_double_including_bank_overflow
    (n r q z target G other : Int)
    (path : PathI n r q z) (bound : n<=@BOUND@) (loop : 2<=r)
    (_nonnegative : 0<=q) (terminalZig : z=0)
    (targetBox : target=0) (globalBox : 0<=G) (otherStock : 0<=other)
    (reserve : ReserveI target G q @H@ @T@) :
    min 1 (target+other) + min G (1-min 1 (target+other))=1 := by
  unfold PathI ReserveI at *; omega

theorem whole_access_original_cost (n q z k : Int)
    (path : PathI n 0 q z) (scope : n<=@BOUND@*k)
    (hz : 0<=z) : q<=k := by
  unfold PathI at *; omega

theorem learned_whole_original_q_energy
    (n r q z target G other : Int)
    (path : PathI n r q z) (bound : n<=@BOUND@) (loop : 2<=r)
    (terminalZig : z=0) (targetBox : target=0)
    (globalBox : 0<=G) (otherStock : 0<=other) (footprintBound : other<=7*@H@)
    (reserve : ReserveI target G q @H@ @T@) :
    1-@WB@*(min 1 (target+other))-@WG@*(min G (1-min 1 (target+other)))<=0 := by
  unfold PathI ReserveI at *; omega

def sumPrefix (f : Nat -> Int) : Nat -> Int
  | 0 => 0
  | n+1 => sumPrefix f n+f n

theorem sum_mono (f g : Nat -> Int) (pointwise : forall n, f n<=g n) :
    forall n, sumPrefix f n<=sumPrefix g n := by
  intro n; induction n with
  | zero => simp [sumPrefix]
  | succ n ih =>
    have h := pointwise n
    simp only [sumPrefix]; omega

theorem original_closed_two_target_cost (q k : Nat -> Int) (n : Nat) (A : Int)
    (originalAccessProof : forall j, q j<=k j)
    (pinnedOriginalGapInterface : sumPrefix k n<=A) : sumPrefix q n<=A := by
  have h := sum_mono q k originalAccessProof n
  omega

theorem conservative_original_q (q bankPaid overflowPaid before after issued : Int)
    (allOriginalCost : q=bankPaid+overflowPaid)
    (physicalConservation : after-before=issued-bankPaid-overflowPaid) :
    q+after-before=issued := by omega

theorem global_reserve_monotone (g g' m m' q : Int)
    (hg : g<=g') (hm : m<=m') :
    max 0 (g-max 0 (q-m))<=max 0 (g'-max 0 (q-m')) := by omega

#print axioms arbitrary_hanging_subtrees
#print axioms learned_root_bound
#print axioms all_original_frame_lengths
#print axioms original_cyclic_entry_is_derived
#print axioms learned_path_double
#print axioms learned_reserve_double
#print axioms original_double_including_bank_overflow
#print axioms original_closed_two_target_cost
#print axioms learned_whole_original_q_energy
#print axioms global_reserve_monotone

end JointCertificate
'''
    for key,value in {'@CASE_DEFS@':'\n\n'.join(case_text),'@BOUND@':str(p['root_bound']),
                      '@PATH_EXPR@':path_expr,'@RESERVE_EXPR@':reserve_expr,
                      '@H@':str(p['bank_capacity']),'@T@':str(p['overflow_ticket']),
                      '@WB@':str(p.get('bank_weight',1)),'@WG@':str(p.get('overflow_weight',1))}.items():text=text.replace(key,value)
    target=HERE/'JointLearnedProof.lean';assert not target.exists();target.write_text(text,encoding='utf-8')
    print({'generated':target.name,'uses_learned_invariants':True,'scope':'two original B targets; unrestricted root OPEN'})


if __name__=='__main__':main()
