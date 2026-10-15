# STRICT_B_CORE_VALIDITY.md — A4 (full ordered-rooted-tree validity + reconstruction)

## Repair
Parent/depth vars + exactly-one-claimant (non-root; root zero) + claimant-parent consistency +
depth chains (root 0; par-dep+1; dep-0 unique by chain descent) + gap slots under core + gap
presence derived from sig (nonempty gaps attached distinctly; empty gaps detached with par NULL).
Interval (BST) validity retained. R3: encoding-auxiliary vars only; state space (mu,b,alpha,sigma)
unchanged (same trees representable).

## Why intervals alone were insufficient
Interval containment is BST-necessary but does not imply: single root, one-parent, acyclicity with
sharing, connectedness, duplicate-free children, gap attachment. Counter-shape (rejected
adversarially): two core slots claiming one child (tot==2); detached cycle-free component;
gap slot with two parents. All UNSAT under the repaired predicate.

## Reconstruction (test support)
`reconstruct_B`: core topology + gap blocks from any satisfying assignment; output verified BST
(valid order, connected, S positions, gap spans). Applied to sampled SAT states in verifier.

## Gate A4: REPRODUCED + REPAIRED.
