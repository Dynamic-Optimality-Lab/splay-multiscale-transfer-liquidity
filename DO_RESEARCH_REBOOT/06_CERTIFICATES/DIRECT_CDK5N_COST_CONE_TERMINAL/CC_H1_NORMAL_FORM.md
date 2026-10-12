# CC_KEEP_BOUNDARY_REDUCTION.md (STEP 04) + CC_H1_NORMAL_FORM.md (STEP 05)

## Normalization

Every closed walk contains a genuine KEEP (five genuine keys ⇒ ≥5 KEEPs).
Rotate to post-KEEP boundary: totals A/Q unchanged (cyclic sum), closure
preserved (same cycle), rotated start reachable (it occurs in the original
execution), no new operations. Post-KEEP invariant: A/B roots both equal
last KEEP target (splay moves accessed key to root; verified 0 violations
on 82 words / all post-KEEP boundaries: CC_BOUNDARY_CHECK.json).

## Interval identity + H=1 normal form

ΣH=A, Σq=Q, Σc=C_K over cyclic intervals (0 violations). H≥c (root-change:
H=0,c=1 would freeze A-root, contradicting different-key KEEP). Core-nine
⇒ q≤4 ⇒ w=2H−q<0 needs H=1,q∈{3,4},c=1 (143/143 negative intervals in
normal form; 0 E4 observed — E4 case covered analytically: same H=1 shape
with d_B=8). H=1 normal form (L0-shape): exactly one nonzero access (Σa=1
over nonnegative integers), targeting v at A-depth 1–2 (a=1 ⟺ d∈{1,2}),
DELETE(v)+KEEP(v)-at-root or terminal KEEP(v); all other DELETEs root
no-ops (frames-empty identity); net A transition = splay_v. No deep
fringe DELETE can be nontrivial inside H=1 (would cost ≥1 more).
E3/E4 intervals thus have EXACT shallow source form; the proof stays
global via weighted cycles (no local repayment assumed).
