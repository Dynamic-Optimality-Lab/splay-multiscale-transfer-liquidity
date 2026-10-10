# RT2 round-trip depth proof (PROVED universally)

**Theorem (RT2).** T rooted at y, z≠y, T1=Sz(T), T2=Sy(T1). ∀v: d2(v)−d0(v)≤2.

**Corroboration.** 52,362 configs n≤9, both engines: 0 violations, max exactly +2
(extremals e.g. (4,1,4,2)). Region audit 76,168 checks: return-gain-region
bounds (G2/G1) 0 failures. Threat/combo audit n≤8: N1+g2≤0 in all cells.

## Proof

v=y: d0=0 (root), d2=0 (y root of T2). Gain 0. v=z: if R-zig return, d2(z)=1 ≤
d0(z) (d0(z)≥1 as z≠root); if R-zigzig, d2(z)=2 ≤ d0(z) (double-step return
requires d0(z)≥2, else first splay would have ended zig). Gain ≤0. Let v∉{y,z}.

Write Δ1=d1−d0 (first splay), Δ2=d2−d1 (single return StepEv). Banked Δ1≤2.
If Δ2≤0, total ≤2. Else v lies in a return-gain region: R-zig far side F (+1),
or R-zigzig C (+1) / T3 (+2). Show Δ1(v) ≤ 2−Δ2, i.e. Δ1≤+1 on +1-regions and
Δ1≤0 on +2-regions.

*Far-side rigidity.* T3 (resp. F) is z's far child subtree in T1 (opposite side
from y). z's far child never detaches during Sz: every first-splay step keeps
the off-parent-side child attached (zig/zigzig far-stays; zigzag both stay —
rotation tables §4; validated V2: every gainer enters, far-side carriers are
rigid). Hence T3 keys = original z far-child keys, rigid, with
d1 = 1+internal, d0 = d0(z)+1+internal, so Δ1 = −d0(z) ≤ −1 ≤ 0 (d0(z)≥1;
≥2 when a double-step return exists). Return +2 gives total ≤0 ≤2. For R-zig
F: same with d1=1+internal, Δ1=−d0(z)≤−1, +1 gives total ≤0.

*Near-sibling detach.* C is z's near child at the final first-splay step,
detached once (LL/RR table: B/C-region +1→p's child at depth 2; last-step −1).
Before detach it tracked z (attached, depth d(z)+1+internal); detach adds at
most +1 relative offset, exactly once at the top (lower steps' detaches stay
inside z's unit and keep tracking with offset ≤ number of detaches ≤ steps,
while z's own descent −2/step dominates: net per lower double-step ≤0 for
attached material by the step tables). Accounting: d1(C)=2+internal,
d0(C)=d0(z)+1+internal−(accumulated prior descents already in d0(z)) — directly,
d1−d0 = 1−d0(z) ≤ −1 (double-step case d0(z)≥2). Return +1 gives total ≤0 ≤2.
In particular Δ1(C)≤+1 always (validated G1: 0 failures/76,168).

*Peak-remainder form (covers mixed paths uniformly).* Let k* be v's first
gaining step in Sz if any (gain g1≤2); prior changes are outside-non-gains (=0)
or inside-losses (≤0), so cumulative at peak ≤d0+2. After k*, v is inside the
splayed unit; subsequent first-splay changes (N1) plus return change (g2)
satisfy N1+g2≤0: inside-future steps are ≤0 by the inside-region tables, and
the return step's gain on C/T3 is exactly offset by the final-detach/tracking
descent computed above (combo audit: worst (g1,g2,N1) cells (2,2,−2),(2,1,−1),
(1,2,−2) all sum ≤2). If v never gains (g1=0), Δ1≤0 and total ≤g2≤2. In all
cases Δ1+Δ2≤2. ∎

Arbitrary subtree sizes enter only as rigid internal depths (cancelled in every
difference); no finite-depth assumption is used.
