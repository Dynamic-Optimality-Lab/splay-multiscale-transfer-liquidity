# PIVOT-14 U4-Core attempt: closed-component capacity (injection) — full record

Verdict: **U4 still OPEN.** The gap is now distilled to ONE inequality family
with three new universal lemmas proved toward it, a complete minimal-X
structural theory locating the exact obstruction shape, and 600+ adversarial
tests (0 failures). No laps as objects; everything on `Z/mZ`.

## 1. New universal lemmas (PROVED)

**L1 (DELETE-setup).** The setup of every starved overflow (KEEP x, `a=0`,
`q≥1`) is always DELETE. Proof: setup `s` with `s=KEEP x` roots `x` in B;
quiet interval `(s,t)` (U2) holds only x-accesses; B there is frozen except
x-KEEPs (which root x); `t` (first x-KEEP at/after `s`, else `t` rooted)
would have `q=0`, contra. Hence `s=DELETE`: `q_s=0`, `a_s≥1`, so its `2a_s`
credits are DEDICATED pure slack (zero self-demand, and DELETEs build
nothing so `s` is never anyone's creator). Census: 42/42 setups DELETE,
0 violations.

**L2 (setup-injectivity over starved B-active).** No two starved B-active
accesses (overflows with `q≥1`, or builders that rotated with `d_B≥1`)
share a setup. Proof: sharers share the setup's key (setup keyed by accessor
key); same-key case dies by B-rooting (earlier KEEP roots B, quiet forces
later rooted, `d_B=0`, contra B-activity); the `k=1` (single-occurrence)
degenerate case dies by dethrone-or-frozen. Census: 0 sharing violations
(69 cycles); namer bounds confirmed: ≤1 starved-KEEP + ≤1 non-starved per
setup (non-starved sharing twice dies because the earlier (dA>0) arrival
supersedes).

**L3 (non-starved depth-extremality, arithmetic).** Non-starved overflow
(`a≥1`, `eps≥1`) needs `q≥2a+1`, i.e. `d_B ≥ 4a+1` with `d_A ≤ 2a` —
B-near-max-depth with A-minimal simultaneously. At `n=6`: impossible
(`q≤2<3`); at `n≤8`: `eps≤1` and only `(a,q)=(1,3)` with `(dA,dB)∈{1,2}×
{6,7}`. So non-starved residuals are tiny and extremal-shaped.

## 2. Minimal-X structural theory (the obstruction, exactly)

Assume Hall fails; take minimal deficient `X` (`|N(X)|=|X|−1`). Then:
(i) NO private neighbors (else a smaller deficient set) — every pool is
shared by ≥2 X-doubles. (ii) Starved setup pools are disjoint from ALL
other pools (DELETE setups host no doubles and build nothing), so each
starved X-double forces its setup to be shared with EXACTLY one
non-starved X-double (H3 + L2 leave no other sharer) — the "dance"
configuration `s(DELETE) < D_j(starved KEEP) < u(dethroner) < D'(nonst
KEEP)`, dynamically coherent, with tight pools needed for `|N|=|X|−1`.
(iii) Dual restatement: failure ⟺ extreme pool-concentration (few pools
touching many doubles), quantified by H4 fan-in (`O(dB)`) + L2 namer
bounds. No contradiction is derivable — the dance is coherent — so U4
needs either a new dynamical invariant killing the dance, or full Hall
with dynamics. This is the precise open core.

## 3. Why the dance never fires (evidence, not proof)

- Dance setups: 6/66 cycles, NEVER tight (always slack), charge never fails.
- Era-correlation (conjectured mechanism): starved B-depth `D(t)` vs setup
  A-depth `dA(s)`: `D ≤ 2·dA(s)+2` holds 53/53 (max slack 1); strong form
  `Σq_starved ≤ Σ2a_setup` holds 69/69 (margins −5/−6); per-starved
  `q/(2a_s) ≤ 0.5` (51 rows); single-builder 50/51 with key-spread ≤2
  mostly (builders key-near ⟹ shared key-intervals ⟹ correlated A/B
  motion — the candidate proof route via BST path-bracketing geometry).
- Typical load is tiny: each starved self-pays via setup (margin 2–6×);
  non-starved self-pay locally; extremal residuals ≤1.
- BUT the correlation is likely TYPICAL-case (shared gross builder count
  + cancellation), not deterministic: adversarial A-cancellation with
  B-accumulation is dynamically coherent. So it cannot close U4
  deterministically. The ≤1-bubble cascade it would leave still needs
  global room (bubbles conserve, never die locally — shown). Global Hall
  is UNAVOIDABLE; no canonical routing closes U4. This negative result
  (ruling out all local routes) is itself banked guidance.

## 4. Extremal probes (all hold; mechanism never fails)

- `(1,3)` extremal engineered at n=7,8 (dA=1, dB=6,7; 12+18 legs);
  BFS-closed 8/8 cycles each with steady-state `(1,3)`: ALL lap2-full
  (WQ −37..−73, slack abundant).
- Deep-starved (`q≥3`): 0 in 73 closed cycles n=7,8.
- Non-starved overflow: 0 in 73 closed cycles (extremal TYPE exists
  transiently only); 22/22 extremal pre-states never recur (transient
  collapse to shallow attractors) — rarity, not impossibility (BFS
  closes them fine).
- Bubble-concentration (shared fat dethroner + many starved): setups turn
  out per-key-adjacent (mutual dethrone makes shared setups impossible),
  so concentration can't even be constructed — injectivity (L2) actively
  defends.
- Siege + bred + hunt + walk + cannon + cross: 600+ non-vacuous
  match-full, 0 failures, 0 with `Q_B>2A`. §26 classification never
  triggered.

## 5. Status and exact next attacks

U4 OPEN. What would close it, in order of promise:
(i) Key-interval bracketing geometry ⇒ deterministic era-correlation
(`D ≤ 2·dA(s)+2`) ⇒ starved residuals ≤ setup + ≤1-bubbles ⇒ Hall for
bubbles via dethroner/builder pools (still needs a global room lemma —
hardest sub-step, stated).
(ii) A recurrence-based invariant killing fully-shared tight clusters
(minimal-X dance) — needs new dynamics, not counting.
(iii) Full structural Hall via cluster-closure + B-depth conservation
(tried: rotation counting collapses to tautology `Z=Σz`; not viable).
Lean: U1 kernel stands green; U2/U3/H/L1–L3 paper-complete (Lean gap:
block/access model + L1/L2 — ~150 lines, deferred since U4 open).
DO chain unchanged (conditional on U4 + C.ZIG assembly).

## 6. Files

- `scripts/wp6_danger.py` (n=6: non-starved overflow IMPOSSIBLE — depth
  arithmetic, consistent), `wp6_extremal.py`, `wp6_close.py`
  (BFS-close via on-demand trans BFS), `wp6_bubble.py`, `wp6_loop.py`,
  `wp6_siege.py`, `wp6_breed.py` (all PIVOT-14).
- Artifacts `overflow/danger.json`, `extremal.json`, `extremal_closed.json`,
  `siege.json`, `breed_n*.json`, `walk_n*.json`, `hunt_n6.json`,
  `analysis.json`.
