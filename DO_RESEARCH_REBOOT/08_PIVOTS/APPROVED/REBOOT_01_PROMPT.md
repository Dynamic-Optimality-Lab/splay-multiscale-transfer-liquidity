PIVOT ID: REBOOT-01
TITLE: Equal-signature SAME-CHILD sibling erasure

ORIGINAL PIPELINE NODE: SAME-CHILD -> ROW-DIAMETER -> COARSE-DOUBLE Q_B<=2A -> B<=3A -> cycle-to-prefix -> eventual monotonicity -> Dynamic Optimality.

EXACT THEOREM:
For every finite valid BST B=[p,T,S], every distinct u,v in T at equal edge-depth d in B whose top-fringe fold coefficients f_u,f_v are equal, and every single globally shared real assignment j(tau),rho(c), prove D_J(B;u,v)=D_J([p,T,None];u,v). Prove the right-child mirror. Prove that odd d gives f_u=f_v=1. Here tau=(slot,lambda,depth(z)-depth(y),depth(y)), J_y=sum_(z!=y) j(tau_yz)+rho(c_y), and H_y=-R_static(B,y)+4(|B|-subsize_B(y))+J_y. D_J=H_u-H_v.

WHY THIS IS STRICTLY SMALLER:
Eliminates arbitrary sibling structure/depth for a geometric subclass, leaving the base width and other pair classes open.

WHY ONE-SESSION COMPLETION IS PLAUSIBLE:
One exact cancellation using the source's path-only fold and full coefficient multisets.

PREVIOUSLY PROVED PREMISES:
Definitions in scripts/wp6_staticR.py, wp6_lambda.py, wp6_j4shared.py. Include elementary proofs of the path partition and R=c+sum lambda directly from those definitions.

UNVERIFIED FACTS TO CHECK FIRST:
Old atom coefficients and root tokens must remain fixed; a new sibling key must have slot F_(d-1); odd-depth top fold coefficient must be 1; the mirror must be valid. Any failure is NO-GO.

SOURCE FILES:
Read-only paths relative to repository root: scripts/wp6_staticR.py; scripts/wp6_lambda.py; scripts/wp6_j4shared.py; scripts/wp6_context.py; scripts/wp6_context2.py; scripts/wp6_twins.py.
Repository: C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2.
HEAD: 88f344d34b155f6cdc0fc4dae9bf0490d0677e1f. The tree is dirty; bind source bytes by SHA-256, not HEAD alone.

MATHEMATICAL ATTACK:
For B0=[p,T,None], prove H_y(B)-H_y(B0)=(4-f_y)|S|+sum_(z in S) j(F_(d_y-1),f_y,d_B(z)-d_y,d_y). The root charge and all old atom occurrences cancel. Subtract the two rows. Equal d,f makes every remaining coefficient zero. Prove the odd-depth corollary by showing the original terminal fringe coefficient 1 remains last in each Tmap step. Prove the mirror explicitly from LL/RR and LR/RL exchange.

NONVACUITY:
Use p=80, balanced T on keys 10,20,30,40,50,60,70; u=10,v=30 (ambient depth 3), arbitrary S above 80. Give arbitrary-depth and reflected families.

SUCCESS CONDITION:
Complete quantified proof and exact coefficient verification. Delete the independent sibling variable for the qualifying SAME-CHILD class. Do not claim |D|<=2 or global J existence.

FAILURE CONDITION:
Exact valid in-domain tree with nonzero complete difference form, an omitted coefficient, or invalid mirror. Record the failure and stop the route.

PROOF VALIDATION:
Check signs, repeated-atom multiplicities, root terms, empty S, arbitrary depth, shared variables, and both orientations. Finite tests support the written universal proof; they do not establish it.

FILESYSTEM RULE:
Every write only under DO_RESEARCH_REBOOT/. Existing source, configuration, tests, Git state, and dependencies are read-only. Use python -B and AST extraction of pure functions; do not run source entry points that write into artifacts/.

STOP RULE:
At most this one theorem. No new UG/existence/compatibility system. After completion reassess the remaining original graph before approving another pivot.

REQUIRED ARTIFACTS:
02_PROVED/REBOOT_01_SIBLING_ERASURE.md; 10_EXPERIMENTS/verify_reboot.py; 10_EXPERIMENTS/verification_results.json; 08_PIVOTS/COMPLETED/REBOOT_01_ADVANCEMENT.md. The pre-execution approval is REBOOT_01_APPROVAL.md beside this prompt.
