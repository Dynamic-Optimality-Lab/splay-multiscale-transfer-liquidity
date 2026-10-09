# PIVOT-23: universal dual from BF certificates — twin-max falsified, obstruction banked

(Todo items 1–3 completed via mined artifacts + targeted probes above;
item 4 partially: synthesis attempted and falsified; universal proof +
Lean remain open. This audit records the exact outcome per §§42–44.)

## A. Certificate integrity (verified, hashed)

bf7/8/9.json feasible (3/4/7 passes; V=184041/2044900/23639044).
bf7/8/9.pkl potentials {0..−3}/{0..−4}, 78–79% zeros. howard7 μ*=0/1.
Verifiers GREEN independently (2.6M/32.7M/425.5M inequalities, fresh
trans). BF potential = canonical maximal feasible = −max-prefix-W.

## B–E. Canonical/tight/derivative findings

Super-source dist pointwise-maximal (gauge-fixed). Tight 12.68% edges;
94% nodes 1–2 tight successors (near-functional policy). Battery:
DELETE recharge +2, overflow drain −1, self-loop hold (capacity 3–4).
D(e) takes 2–7 values per (mode,dA,dB) — locality dead. Root-pair does
NOT determine Phi (all 49 multi-valued; prior 0/49 was a scoping bug
caught by histogram). Differ-pairs {0,−1} only; twin all values.
Left-subpair alone 99.2% (151/19415 need right info); neither
projection suffices alone (B 401/429, A 429/429 multi).

## F–I. Twin-max candidate REFUTED (80,560/2,576,574 violations)

`Phi=−[rA==rB]−max(0,(maxD_B−2)//2)`: K-under 96% ((0,1)×18370,
(0,2)×25750, (0,3)×2108, (1,2)×21320, (1,3)×9716), K-over 4%
(over-recharge), DELETE zero. Minimal violator: KEEP x=1, roots
(1,5)→(1,1), maxB 4→3, (dA,dB)=(0,3): twin pays +1, max-destruction
recharges −1 (4→3 second-takes-over), net 0 < w=+1.
Mechanism: max-preserved caps drop at twin-only +1 (covers q=1);
max-touched recharges or small-drops (vine-consecutive covers q≤2
tightly); q≥3 needs setup-era (cancellation wall). n=8/9 validation
skipped (dead at n=7).

## J–K. KEEP/DELETE transition status

DELETE holds for twin-family (twin-change ≥ −2a always; B frozen).
KEEP fails exactly as above. No universal proof (needs max-dynamics
control + setup-era, both walled).

## L–M. Telescope + verdict

No universal dual (twin-max dead; recursive/interface program open:
left-99.2% + 151 right-B vine/branch bits untested for sufficiency;
additivity refuted (residual −3..+2); offsets unbounded; max-depth
inverse; counts unbounded). **COARSE-DOUBLE OPEN** (n≤9 BF-certified;
universal dual open). ONE atomic obstruction (§42): max-term
recharge-vs-drop dilemma — preserved caps +1 (q=1 only), touched
recharges-or-underpays, q≥3 needs setup-era wall; no max-form covers
all (preserved-vs-destroyed contradiction). Lean: U1/descent green;
dual gap stands (block+E0+dual ~200 lines). DO conditional.
Zero kills (candidate refuted; theorems untouched).
