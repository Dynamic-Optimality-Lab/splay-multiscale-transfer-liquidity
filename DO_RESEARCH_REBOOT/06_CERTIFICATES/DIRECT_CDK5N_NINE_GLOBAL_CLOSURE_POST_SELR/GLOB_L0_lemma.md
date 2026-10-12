# L0 — Shallow-A / Deep-B Disparity at Every Positive-Excess Interval (§6)

## Statement

Let I_j be source-valid with H_j=1, c_j=1, q_j∈{3,4}. Let u=x_{j-1},
v=x_j, P = pair state after preceding KEEP. Then:
L0.1 Both roots are u at P. L0.2 Exactly one access in I_j has A-cost 1;
rest 0. L0.3 That occurrence accesses v at A-depth ∈{1,2}; before it every
access targets root u (A unchanged); after it every access targets root v.
Hence d_A^P(v)∈{1,2}. L0.4 B frozen until terminal KEEP, so
q_j=floor(d_B^P(v)/2): E3 ⇒ d_B^P(v)∈{6,7}; E4 ⇒ =8. L0.5 g_P(v)≥4 (E3),
≥6 (E4).

## Proof (from engines + arithmetic)

a=ceil(d/2)≥0 integer; Σa=1 ⇒ exactly one a=1, rest 0 (L0.2 counting).
a=1 ⇔ d∈{1,2}. Root access (d=0) has empty splay frames ⇒ tree unchanged
(splay.py _descend/_rebuild; wp6 cross-checked); non-root present-key
splay moves key to root (rebuild roots cur at x; absent ⇒ ReplayError,
excluded by source-validity). Preceding KEEP(u) splayed u to both roots,
and P immediately follows ⇒ L0.1. Before the nonzero event, every access
has a=0 ⇒ targets current root; root starts u and zero-cost accesses
don't move it ⇒ all target u, A state ≡ P up to the event. The event
accesses some y at depth 1–2 and moves root to y. After it, all accesses
a=0 ⇒ target current root; root is y until end; terminal KEEP targets v
⇒ y=v; all post accesses target v (L0.3). Hence depth at event = d_A^P(v)
∈{1,2}. Nonzero may be DELETE(v) (observed 4/670 corpus E3) or KEEP(v);
if DELETE(y),y≠v, root becomes y≠v yet terminal needs v at root with
a=0 — contradiction; so y=v either way. B: DELETEs leave Bp unchanged
(replay.py: Bp touched iff KEEP); interior accesses are DELETEs (KEEPs
cut intervals) ⇒ B at terminal ≡ P ⇒ q=floor(d_B^P(v)/2) (L0.4 depths).
Core-nine ⇒ d_B≤8 for genuine v; q=3 ⇒ 6–7; q=4 ⇒ 8 (8 is max). Gap
g=d_B−d_A: E3 ≥6−2=4; E4 ≥8−2=6 (L0.5). No global inequality, no bank
theorem, no matching assumed. ∎

## Empirical verification

670 E3 + 0 E4 intervals (SELR-IN/OUT + 384-word corpus): roots ok 670/670;
one-nz 670/670 (incl. 4 nonzero-on-DELETE, all targeting v); P-depths
1–2; B-depths 6–7; gaps ≥4; B-frozen prefixes verified state-equal.
Script: tmp_L0check.py + tmp_L0full.py (0 fails). E4 clause vacuous on
corpus (no source-valid E4 observed; universal statement retained).
