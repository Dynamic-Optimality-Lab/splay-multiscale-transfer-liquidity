# 26AS-L1 universal proof: straddling splay pair conservation (PROVED)

**Theorem (26AS-L1).** For every finite BST B, distinct present keys r<y<s,
with B'=S_y(B) by authoritative bottom-up splay:
d_{B'}(r)+d_{B'}(s) ≤ d_B(r)+d_B(s)+2.

**Status: PROVED** — rotation-case tables + entering-step composition.
Corroboration: 18136 exhaustive triples (n≤7, both engines, 0 violations, max
exactly +2); region-table audit (5448 steps: single-side V1✓, enter V2✓,
max-gain V4✓); threat probes consistent. Finite data corroborates; proof below
is self-contained.

## 1. Per-step region tables (unit top at depth D; verified against source
## `wp6_eventflow.py:111-182` rotation cases)

Zig-L (y left child of root p): y−1; A=y.left −1; T=y.right 0; p+1;
R(p)=p.right +1 (rigid). Gainers {p,R(p)}, all keys >y.
Zig-R (mirror): y−1; A'''=y.left 0; B''=y.right −1; p+1; L(p)+1. Gainers <y.
ZigZig-LL (y,p,g left-line): y−2; A−2; B=y.right −1; p 0; C=p.right +1;
g+2; T3=g.right +2. Gainers {C,g,T3}, keys: C: p<C<g with y<p so C>y; g>y;
T3>y. All >y.
ZigZig-RR (mirror): y−2; A'=y.left −1; B'=y.right −2; p 0; C'=p.left +1;
g+2; T3'=g.left +2. Gainers <y.
ZigZag-RL (y right of p, p left of g): y−2; T1=y.left −1; T3=y.right −1;
T0=p.left 0; p 0; g+1; T4=g.right +1. Gainers {g,T4}, keys >y (y<g; T4>g>y).
ZigZag-LR (mirror): y−2; A_y=y.left −1; B_y=y.right −1; C_y=p.right 0;
p 0; g+1 (<y); D_y=g.left +1 (<y). Gainers {g,D_y}, keys <y.

Consequences used (each read directly off the tables):
(T1) Every step's gaining regions (change>0) are y-monochromatic: LL/RL/
zig-L gain only keys>y (S-steps); RR/LR/zig-R only keys<y (R-steps). No step
gains for both r and s. (V1 audit: 0 violations.)
(T2) Every gaining region ends inside y's subtree (under y after the step:
C under g; g under p; T3 under g; T4 under g; p/side under y). (V2: 0 bad.)
(T3) Regions strictly inside y's subtree (y's descendants, excluding y)
change by ≤0 in every step; the s-side (keys>y) inside regions are exactly
{B(−1),B'(−2),T3(−1),B_y(−1),B''(−1),T(0→−1 corrected: T=y.right in zig-L is
0? — see note} — NOTE: zig-L far side T (y's right) is 0, and T0/T0''-beside
are 0 but OUTSIDE (sibling subtrees). For s (keys>y) strictly inside: every
case gives ≤−1 EXCEPT zig-L-far-T which gives 0. In all cases ≤0. (V3 flags
are exactly these ≤0 cases: 0-changes, never positive.)
(T4) Max single-node single-step gain is +2 (LL/RR outer). (V4 ✓.)
(T5) Outside-y's-subtree non-gaining regions change by exactly 0
(above-untouched; p-as-p in zigzig/zigzag; beside-0 T0/T0''). All other
outside regions are gaining (hence entering, T2).

## 2. Entering-step composition

Each of r,s gains at most once: a gain puts it inside y's subtree (T2), and
later steps give inside nodes ≤0 (T3), so no second gain is possible. Let
g_r,g_s ∈ {0}∪[1,2] be the single gains (T4; 0 if never), N_r,N_s ≤0 the
remaining changes (outside-non-gain =0 by T5; inside-later ≤0 by T3).
If either is 0, total ≤2. Else both ≥1 with gain steps k_r≠k_s (T1: no
dual-gain step). WLOG k_s<k_r (mirror symmetric):
- Before k_r: r outside-non-gain (=0; r cannot have entered, else k_r
  couldn't gain) so R_before=0; S_before ≤ g_s (gain + inside-later ≤0).
- Step k_r (R-step, r gains): s is inside (entered at k_s, membership
  preserved by rigid/transfer moves). s>y forces B-side inside regions:
  RR→B'(−2), LR→B_y(−1), zig-R→B''(−1). Step sums: +2−2=0, +1−1=0, +1−1=0.
- After k_r: both inside, all changes ≤0.
Total ≤ 0+g_s+0+0 ≤ 2. Mirror case ≤ g_r ≤ 2. ∎

## 3. Remarks

The bound is tight (extremals e.g. n=5 splay-3 r=1 s=5: s transiently +2 via
LL-outer, canceled −2 by the following RR-carry, r +2 as final outer
grandparent). The proof corrects two subtle table entries found during
verification (zig far-side 0 not −1; RL-T0 beside-0 not +1); both corrections
are incorporated above and confirmed by the audits.
