# CL-01 Push-Aware Block Accounting (status: requirement stated, not derived)

Per-rotation facts (proved, scoped): x -1, p +1, S-subtree +1/node, only
x/p change size. Macro gap: pushes reattach subtrees rigidly (depths jump
by construction, not rotation); B-validity/gap-match/normalization
constrain endpoints, not paths. A block law needs: entry push inventory
(which subtrees detach/reattach on 0->1) + deep-region push bounds +
exit restoration accounting. None derivable from stored features (pushes
unlogged; envs lack push traces). DATA REQUIREMENT for any future block
law: replay-level push logs paired with abstract endpoints. Until then,
block-level bounds are OPEN; rotation-only bounds must not be substituted
(SR-02 correction stands).
