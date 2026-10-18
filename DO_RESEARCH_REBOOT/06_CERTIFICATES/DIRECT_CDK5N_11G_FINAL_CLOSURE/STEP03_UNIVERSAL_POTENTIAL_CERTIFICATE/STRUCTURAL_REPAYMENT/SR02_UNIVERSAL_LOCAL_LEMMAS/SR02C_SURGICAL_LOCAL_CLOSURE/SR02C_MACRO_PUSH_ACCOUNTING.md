# SR02C Push-Aware Macro Accounting (code-derived, scope-corrected)

Per-rotation (proved by reading single_rot/b_single_rot): x -1, p +1,
S-subtree +1/node, middle 0, rest 0; only x,p change subtree size (hence
only x,p change rank); DeltaD_rotation = +|S| >= 0. Macro level: B-splay
composes rotations with pushes (splay_B_push outB reattachments) and
gap/boundary normalization; E4-collapse (D 36->24) proves macro drops
exceed rotation-only accounting (pushes/restructuring dominate). THEREFORE:
no per-rotation identity transfers to macros without push accounting;
SR-02's corrected scope stands. Implication for credit laws: macro
rank/depth changes are push-dominated, not rotation-telescoping — any
future law must model pushes or bound them universally (open).
