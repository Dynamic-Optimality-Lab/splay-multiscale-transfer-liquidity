# DIRECT-CDK5-LOW: five-key submaximal-core Coarse-Double (PROVED · CDK5L-A)

**Status: PROVED.** Nine-node upper bound + closed-core conservation + exact
142,385-edge / 28,477-vertex finite certificate (0/1 potential, 0 violations,
independently verified) + telescoping + banked A-charging ⇒ Q_B≤2A for five
KEEP keys with core ≤8 throughout. Strictly new coverage certified. Nine-node
class, K≥6, universal Coarse-Double, DO remain OPEN.

## Geometry (PROVED)

K4-L1/pruning (banked, arbitrary M) ⇒ 1+4·2=9 universal bound (tight:
nine-node witness attains 9 everywhere) ⇒ fixed-M closed cycles conserve core
size (nonincreasing cyclic ⇒ constant) ⇒ label swaps handled by full
shape×subset enumeration (no fixed-key assumption; compression canonical).

## Certificate (PROVED)

Raw 449,615 (210/3960/45045/400400) → 28,477 valid-core vertices → 142,385
edges (54,670 size-drops, all verified; invalid-state omission sound: real
projections visit valid cores only — leaf-marked ⟺ ancestor-closed). SPFA
longest-path potentials in {0,1}: every edge w+Δη≤0. Independent tuple-engine
re-derivation: vertex set, all edges, all inequalities PASS. Both engines
agreed on all 449,615 raw transitions during generation.

## Theorem (PROVED)

Projection + telescoping: Q_B≤2C_K; banked C_K≤C_X≤A: **Q_B≤2A** on CDK5-LOW
(arbitrary n/length/order/DELETEs/prefix). With CDK4-A + RT2-A: all classes
through ≤4 keys plus five-key ≤8-core banked.

## Novelty

Five-key witness (19/9/−29, core ≤7, all recognizers REJECT, outside every
prior domain) + nine-node obstruction (core 9, Q−2C_K=+2) proving the boundary
load-bearing. No prior result altered.
