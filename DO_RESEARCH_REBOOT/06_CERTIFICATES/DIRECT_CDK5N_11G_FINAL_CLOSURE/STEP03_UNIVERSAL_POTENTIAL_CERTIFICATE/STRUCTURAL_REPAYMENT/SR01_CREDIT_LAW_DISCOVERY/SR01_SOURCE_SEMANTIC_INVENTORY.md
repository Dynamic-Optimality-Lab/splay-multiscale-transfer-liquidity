# SR-01 Source Semantic Inventory (from frozen code, not summaries)

Rotation (`single_rot`/`b_single_rot`): one child-x rotation moves (kind,ref)
pairs rigidly. Depth effects per rotation: x −1, parent p +1, p's other
subtree S +1 per node (rigid), middle subtree 0, rest 0. Net B-mass change
ΔD = +|S| ≥ 0. Size effects: ONLY x (grows) and p (shrinks) change subtree
size; all other ranks frozen per rotation. Event weight a = ceil(d/2),
d ∈ 0..4; H = Σa (≤5 events A-side; B-side up to 9 pairs). Edge weight
w = 2H−q (low, H≤2), w = 6−q (contracted high via OM+MO-0 midpoint).
Genuine KEEP moves x to both roots (A-shadow root + B-root agree post-edge;
verified on killers: 3→4, 0→5). q = floor(dB(x)/2), dB = pre-depth of x.
Negative ⟺ q > 2H (deep-B + shallow-A). ssertify pins witness via
AModel/BModel path constraints (why symbolic source-pinned queries stall:
witness freedom too large).
