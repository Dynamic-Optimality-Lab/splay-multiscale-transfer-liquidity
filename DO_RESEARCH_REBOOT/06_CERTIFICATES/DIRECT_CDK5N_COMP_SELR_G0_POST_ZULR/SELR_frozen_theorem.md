# SELR frozen theorem H1–H6 (from §6; immutable for this run)

Intervals I_j (accesses after preceding KEEP through current KEEP):
c_j=1[x_j≠x_{j-1}], H_j=Σa, w_j=q_j−2c_j, R_j=2(H_j−c_j), C_K=Σc.
E={j:c=1,q=3,H=1} (traditional exception slots).
U={j:w>0,¬K,¬P} (untyped positive intervals).
H1: admissible reachable exactly closed pair-walk; exactly five distinct
genuine KEEP keys; complete marked B-ancestor core nine at every cyclic
state; arbitrary ambient size/length. H2: E={e} UNIQUE bare exception
(c=1,q=3,H=1; w=1,R=0). H3: maximal cyclic successor run after e with
c=1,H=1,q≤2 has length t_e∈{0,1} (short creditless relay; maximal run
computed completely). H4: U={e,p} with p≠e, c_p=1, q_p=3, H_p≥2 (distinct
unit-debt donor; ¬K_p, ¬P_p; w_p=1, R_p≥2; same p every clause).
H5: ∀j∉{e,p}: w>0 ⇒ (K∨P) (retained for payment-completeness auditing).
H6: Q≤2A (conclusion only; no aggregate premise). Strict K: d_A≥3 (H alone
insufficient). Strict P: immediately preceding DELETE(y≠x) with a≥1 both,
same interval. SHA of this file pinned in terminal status (frozen text).
