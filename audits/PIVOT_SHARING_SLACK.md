# PIVOT-18: SHARING_EXCESS → SLACK injection (attempt + verdict)

## A. Frozen definitions (code-exact)

Pool(e) = `2a_e` A-credits of access e (disjoint; empty iff `a_e=0`,
excluded). Namer: double D with edge to e (local iff e=t(D); setup iff
e=s(t(D)) exists; creator iff e=c(D)). Complete naming (code): every
double touches ALL credits of named accesses (no pool cherry-picking).
fanin(e) = #{X-doubles naming e} (double-granularity). Baseline: first
namer (canonical earliest). Excess-share units: non-baseline namers
(`k_e−1` per pool). Headroom/slack: `room(t)−|X_t|`,
`room(t)=Σ_{t-pools}cap`. GAP = EXCESS−SLACKS identity verified
(double-counting). Minimal: gap exactly 1, sole-naming-empty (members
sole-name only 0-pools; all fat pools shared). Zero-fat: all creators
starved (0-credit, vacuous pools).

## B–D. Units + enable

Excess unit E=(pool e, extra namer D). Slack unit S=(access t, headroom
index ≤ room(t)−|X_t|). enable(E): creator-edge → latest establishment
(ORIGIN, U1); setup-edge → latest arrival (U2-form, L1 DELETE);
local-edge → own access (no event — co-located; local excess = 2nd+
doubles same access). Classification: ENABLE-K (KEEP built/rebuilt),
ENABLE-D (DELETE/arrival), ENABLE-REBIRTH (post-consumption rebuild).
All structural (existing machinery).

## E–G. Per-class analysis (setup / creator / injectivity)

Setup-pool excess (nonst co-namer beyond starved baseline): enable =
arrival-order (no event — absence of superseding arrival). Slack must
come from setup headroom (`2a_s−q_t`, era-margin) — UNPROVED (needs
era). Creator excess (fan-in beyond baseline): enable = building splay
(B-rotations + A-work `2a_c`). Slack = creator headroom (`2a_c−q_c`,
negative if overflowing (then demand, not supply — chains onward)).
Per-enable `Excess(e)≤Slack(e)`: setup needs `1 ≤ 2a_s−q_t` (era-margin,
unproved); creator needs `fanin−1 ≤ 2a_c−q_c` (concentration vs room,
unproved — H4 bounds fanin, L3 bounds residuals, no joint bound).
Injectivity fails at both (shared margins / popular pools).

## Correction banked during attempt

Complete naming OVER-counts for per-pool injection (each demand names
2–3 pools; tight pools match WITHOUT headroom — baseline covers one
demand IN capacity). Correct excess notion is RESIDUALS (post-locals:
starved-full + nonst `(q−2a)⁺`), not namings-beyond-baseline. Residual
injection (residuals → external slack) is the right theorem — and hits
the same wall (below). Canonical locals-first is SUFFICIENT but its
success needs era + concentration control (unproved).

## H. Verdict: SHARING_EXCESS ≤ SLACKS OPEN

Injection unbuilt. Two precise blockers (both necessary):
(i) era (`q_starved ≤ 2a_setup`, setup-covers-own) — unproved
(cancellation wall: gross correlates, nets decouple; coherent
adversarial cancellation; greedy/census 0 violations but no proof);
(ii) residual-concentration bound (extremal leftovers (L3-capped, rare)
don't overwhelm fat pools (H4-fanin) — coherent joint-marginal corner,
0 observations in 900+ tests). Either alone does not close U4
(era leaves nonst-residuals; concentration needs era-margins).
Per-access room FINITE (150/150, 0 violations). Long-splice n=6,7
(maxlen 93/86): full, 0 room violations.

## I–L. E0 / U4 / COARSE-DOUBLE: OPEN (compositions ready; unrefuted;
§26/§38/§44 never fired — no witness in 900+ tests including extremal
(1,3)×8 closed, deep-starved 0/73, dance 6/66 never tight, shape-hunt
133 zeros, room-hunt 150 zeros, long-splice 45 zeros)

ONE missing statement (unchanged in kind, sharpened): E0-dance
unrealizability — equivalently, era + residual-concentration jointly
(statements (i)+(ii) above; neither implied by the other; both needed).
Lean: U1 kernel green; block-model + E0 gap stands (~150–200 lines).
DO chain conditional (C.ZIG-V1V3 + PIVOT-2-excision mechanical).
