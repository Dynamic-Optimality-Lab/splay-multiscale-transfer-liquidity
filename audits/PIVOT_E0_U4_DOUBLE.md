# PIVOT-17: E0 unrealizability → U4 → Coarse-Double → DO chain

## A. Authoritative E0 predicate (code-accurate, complete naming)

Eligibility (`wp6_overflow.charge`): double `D` at access `t` ↔ ALL credits
of `t` (local) + ALL of creator-acc(`D`) + ALL of setup-acc(`t`) (complete
bipartite per named access — members name ALL their pools, no pool
cherry-picking). Pools = per-access credit sets (`2a_e`), disjoint across
accesses. `N(X)` = credits of named accesses `P(X)`; `|N(X)|=Σ_{P(X)}2a_e`.
Zero-fat E0 (minimal deficient `X` = starved-`t` doubles + nonst-`t'`
doubles, shared setup `s`, all creators starved (0-credit pools)):
`|N|=2a_s+2a'`, `|X|=q_t+q'`, deficiency ⟺
**`(q_t−2a_s)+(q'−2a')=1`**. Fat form: `−Σ_C2a_c` (distinct fat creators).
Verified against code (local-first order irrelevant to existence).

## B. Bridge reverified (+ sole-naming-empty refinement)

Minimal deficient ⇒ `|N|=|X|−1` + no privates (else smaller deficient;
sole-locally-paid exclusion proved). NEW refinement: members sole-name
ONLY empty pools (sole-named fat pool with cap `c` makes removal grow gap
by `c−1≥1`, so minimality forces sole-named caps = 0 and gap exactly 1).
Hence every FAT pool in play is shared ≥2 — the dance + local/fan-in
sharing is forced, not assumed. Bridge holds; U1–U3 untouched.

## C–D. Equations

Zero-fat: `(q_t−2a_s)+(q'−2a')=1` ( demanda minus named pools, E0 §E).
Fat: same `−Σ_C2a_c` (fat creators raise the bar to deficits ≥3+;
minimal (easiest) obstruction is zero-fat).

## E. Residual splits

`(r_s,r_u)` with `r_s+r_u=1`: `(1,0)` (starved over by 1 (era-boundary
`D≈2d+2`) + nonst tight) / `(0,1)` (nonst over by 1 (extremal `(1,3)`-style)
+ starved covered) / negatives compensate (one side surplus, other over
more). Bounds: `q=⌊d_B/2⌋`, `a=⌈d_A/2⌉`; starved `r_s=q_t−2a_s` (era-capped
empirically); nonst needs L3-extremality (`d_B≥4a+1`) when positive.

## F. Depth/parity

E0 ⇒ `q_t+q'` odd (2a even). No parity contradiction available (shared
setup/creator geometry imposes no mod-2 relation on `q_t,q'` — falsified
by inspection: parities independent across the dance (observed both)).
Mod-4 via `⌊d_B/2⌋`: no invariant (zig parity free). E0-A (arithmetic
contradiction): DEAD — equation always solvable in integers.

## G–J. Normal forms (DELETE / quiet / starved-KEEP / sharer)

DELETE `s`: A `z→root`, B frozen (asymmetry free). Quiet `(s,t)`:
DELETE-`z` noops only; B frozen; `t` first-KEEP (`D` = pre-`s` built).
Starved `t`: `(A-root,B-deep)→(root,root)` convergence; `q_t` from
pre-`s` stack. Sharer `t'`: first `z` after dethroner `u`; `D'` rebuilt
post-`t` by starved-KEEPs (A-noop) + DELETEs (A-only) — divergence engine
precise. Non-starved disparity needs extremal rebuild (L3). All
banked/coherent; no contradiction.

## K. Creator/rebirth accounting

Consumed edges destroyed; rebuilders are KEEPs (A-work included);
in-epoch builders (U1); disjoint setup blocks (H2). Creation inventory:
each residual needs a distinct latest builder-edge (H4); saturated
creators (zero-fat: starved, 0 credits) still BUILD (rotations) while
contributing nothing — the `+1` excess is exactly unbuilt-by-credit work.
No inventory contradiction (starved builders are free labor with private
DELETE-setups (ineligible 2-hop)). E0-C (inventory): DEAD as stated.

## L. Skeleton

Minimal E0: `a_s=1, q_t=2, a'=1, q'=3`, zero-fat-creators, shared setup
(`(0,2)+(1,3)`). Support: dance key + ~10 builders/setups + dethroner
(key-near). No contraction theorem (depths need multiplicities;
locality unproved). Parametric path-length form collapses to E0 itself
(tautological — E0-D/E/F routes dead for same reason).

## M. Contradiction OR witness: NEITHER (new structural lens instead)

Gap decomposition (exact): `GAP(X)=|X|−|N(X)|=SHARING-EXCESS−SLACKS` with
`EXCESS=Σ_{P(X)}2a_e(fanin_T(e)−1)≥0`,
`SLACKS=Σ_{T}(room(t)−|X_t|)≥Σ(room−q)≥0` (per-access room).
Deficiency ⟺ EXCESS > SLACKS. Per-access room banked FINITE (150/150
cycles, 0 violations — every access's doubles fit named pools).
Complete naming removes pool cherry-picking; sole-naming-empty removes
fat privates. What remains is EXACTLY sharing-multiplicity vs local
headroom — i.e. E0/dance. No contradiction derived (sharing coherent);
no witness found (shape-hunt 133 + room-hunt 150 + all prior: 0).
E0-G (gap `F≤0-or-≥2`): no gap theorem (F=1 realizable in integers;
dynamics unruled).

## N. E0_UNREALIZABLE: OPEN

## O. U4: OPEN (needs N)

## P. total_overflow ≤ total_slack: OPEN (850+ green)

## Q. COARSE-DOUBLE Q_B ≤ 2A: OPEN (composition ready; unrefuted)

## R. Post-Double chain (precise status)

C.ZIG (`Z_B≤A`): AUTHOR-banked, V1–V3 mechanical assembly OPEN (verify:
`lean/WP6/` has no Z_B file; hall 8AC-CDOUBLE records same). ⇒ `B≤3A`
CONDITIONAL. PIVOT-2 (`E_B≤3S_A+g` via cycle-excision): assembly status
per `audits/` (list lemmas — NOT re-verified this run; record as
mechanical obligation). Translation `LT≤7LT+2g`: parametric banked
(`translation kernel-green LT(Y)≤(2C+1)LT(X)+2g` per prior summary).
Levy–Tarjan ⇒ DO: banked conditional (eventual+repeatable+coercible).
MATHEMATICAL DISCOVERY: open at E0/U4. FULL KERNEL ASSEMBLY: open at
E0/U4 + C.ZIG-V1V3 + PIVOT-2-excision. No DO claimed.
