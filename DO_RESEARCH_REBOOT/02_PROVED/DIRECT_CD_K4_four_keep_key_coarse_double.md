# DIRECT-CD-K4: Coarse-Double for four KEEP keys (PROVED · CDK4-A)

**Status: PROVED.** Marked-core compression (K4-L1 + pruning + ≤7 reduction),
complete 68,876-case one-bit certificate, closed-cycle telescoping, and the
four-key class implication — all universally quantified. Combined with RT2-A:
|supp(KEEP)| ≤ 4 ⇒ Q_B ≤ 2A. Five-key alphabets, universal Coarse-Double, and
Dynamic Optimality remain OPEN. No E/S conjectures, AJ–AS packets, potentials
beyond the frozen one-bit η, or compactness used.

## K4-L1 (PROVED)

Marked splays never grow the ancestor core; unmarked splays add ≤2 (single
rotation ≤+1, 0 when the pivot subtree is marked; first mark-acquiring StepEv
carries the whole ≤+2 budget since the marked unit then stays marked).

## Reduction (PROVED)

Growing-visited-set induction: 1 → ≤3 → ≤5 → ≤7 across first appearances;
revisits/DELETEs never grow; exact closure transfers the bound to every cyclic
B-state (rotation argument covers arbitrary KEEP ordering).

## Finite certificate (PROVED)

68,876 reduced transitions (all shapes × marked 4-sets × marked accesses,
n=4..7), both engines in exact agreement, 0 violations; 1,280 positive raw
weights at n=7 all paid by η-drops.

## Consequence (PROVED)

Q_B ≤ 2C_K (telescoping η) ≤ 2C_X (subsequence contraction) ≤ 2A (per-change
StepEv charging) for |supp(KEEP)|=4; with RT2-A, for ≤4.

## Novelty

Gate-0 witness (19/10/−28, support {1,3,5,7}) lies outside every AJ–AS domain
(all recognizers REJECT); no banked theorem discharged the four-key class.
26AM Outcome B and all other statuses untouched.
