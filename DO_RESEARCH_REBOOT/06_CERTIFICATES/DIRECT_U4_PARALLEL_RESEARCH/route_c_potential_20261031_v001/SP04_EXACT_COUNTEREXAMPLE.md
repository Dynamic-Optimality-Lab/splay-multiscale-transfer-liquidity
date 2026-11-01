# Exact source countercertificate for the explicit candidate

Use keys1..6. Let M be the median-recursive BST on2..5 (root4,left3 with left2,right5), and

    A = 1(empty,6(M,empty)),
    B = 2(1,3(empty,4(empty,5(empty,6)))).

KEEP1 leaves A unchanged and makes B the right vine1..6. It has a0,q0,z1.

Exact function evaluation gives

    Psi(source)=405/128,
    Psi(destination)=16625/4096,
    increase=3665/4096 >0.

Thus the whole-access signed inequality fails. The raw G DELETE6 comparison increases by21/8, exceeding its budget2, whereas Psi's DELETE budget is already guaranteed analytically.

The evaluation enumerates exactly132 SINGLE-tree BSTs and660 directed primitive-rotation arcs. It does not fit any potential label or scan a larger Pair Access graph. There are no free parameters. Distances are proved exact by actual predecessor paths plus1-Lipschitz inequalities on every rotation edge. The independent verifier rebuilds those edges from the pointer source and recomputes all264 source/destination expression values.

The failed edge occurs inside this complete original closed word, starting both trees at B:

    D1 D4 D6 D1 K1 D2 D5 D1 D3 D1 K2

The certificate includes every source/destination tree, source event trace and cost. Total A=15,Q_B=0,Z_B=2, with exact paired closure. It is not a Coarse-Double counterexample; it is a counterexample to the frozen candidate. No B zig or weight-zero operation was erased.

Files: explicit_potential_countercertificate.json contains all states, all formula terms, complete metric certificate, maximizing trees, failed edge and closed word. independent_audit.json verifies these without importing the candidate evaluator. The all-n proof is in SP03; this fixed evaluation is an independent control, not its universality argument.
