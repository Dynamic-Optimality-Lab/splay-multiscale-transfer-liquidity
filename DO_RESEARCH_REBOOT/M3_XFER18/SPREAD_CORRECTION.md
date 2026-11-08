# Correction before accepting the spread theorem

The first audit FAILED at Z_core_8. SPREAD_REPAYMENT.md and the initial
PRE_EXECUTION proposal are NOT accepted as written. The failed script,
log, exit and CPU charge remain immutable. Its preceding Z_core_4 and
Z_core_6 identities passed and will be reused, not rerun.

The proposed V was a wrong depth-three splay result. The correct V is

 V=8(2(0(E,1),7(5(3(E,4),6),E)),E).

It still has A root8,L6,LL2, but now mark6 has B depth4 and weight0.
An additional one-credit class W, with no alpha guard, has root6 and

 W=6(2(0(E,1),5(3(E,4),E)),8(7,E)).

The correct ordered augmentation is floor1_U, floor1_W, floor1_V,
then cap2_Z, with actual opposite classes at every stage.

W's only marked zero exit is4, whose exact core output is

 4(2(0(E,1),3),6(5,8(7,E))).

All marks there have depth<=3, so the E1 floor pays it. Other marked
W exits are positive. At a fresh V source only2/6 are eligible marked
H1 targets by the unchanged A ordering/G proof. Target2 has price2;
target6 has price0 and its exact B output is W. Thus W's prior credit
pays V's zero exit. The one-credit LOW rule of SPREAD_REPAYMENT.md
now proves all three floor operations. The Z exits and helper proof
are otherwise unchanged: Z->4 is E1, Z->6 is U, Z->8 is corrected V.
All three +1 obligations are repaid. All Z-source LOW rows hold.

The old target-value proof also needs correction: the erroneous
root8/left7 V cannot justify c(T)<=1. Instead access4 has price1
and output C4=4(2(0(E,1),3),5(E,7(6,8))). Prove psi(C4)=0 directly
by inverting the last core splay operation, uniformly over every
possible negative incoming core tree. This is a constructor proof,
not a psi bank lookup or test on selected predecessor trees.

For even negative depths6/8 the final operation is a pair. Its four
possible orientations have uniquely determined processed target
subtrees, obtained from the displayed C4:

* LL: X=4(2(0(E,1),3),E), with five nodes;
* RR: X=4(3,5(E,7(6,8))), with six nodes;
* LR/RL: X=4(3,E), with two nodes.

Remaining depth is4/6. The depth6 remainder needs seven nodes, so
all depth8 cases are impossible immediately. For depth6, the mixed
cases are impossible. LL's remaining four edges would use every node
and go strictly right0,1,2,3,4; its unique paired output has left
child1, rather than C4's processed left child2. Alternatively invert
its next pair: the only structurally possible RR pair leaves a
processed target with fewer than three nodes. The RR case X has
only four possible next pairs: LL leaves4(3,E), mixed leaves4(E,E),
and RR is structurally absent because3 has no left child. Every
remaining depth2 would require three nodes. Hence it too is impossible.

For odd negative depth7 the last operation is a zig. The two possible
processed target subtrees have six/five nodes, while remaining depth6
requires seven. Both are impossible. Thus NO negative incoming core
access can produce C4. The already complete negative-edge recurrence
gives psi(C4)=0. Apply this same inverse-word proof to the actual
opposite constructors as well; do not reflect psi labels or witnesses.

Consequently c(T)<=1+psi(C4)=1, while every marked T depth<=3 gives
c(T)>=1. The saved psi(T)=0 and old-guard exclusions from the first
manuscript then give D_term(T)=1. The saved original zero reset is
indeed a current 2->1 failure, now repaired at Z to2. This conclusion
is accepted only if the NEW independent inverse-word and corrected
constructor audit passes. No completed original control is replayed.

The remainder of SPREAD_REPAYMENT.md applies with these substitutions.
Neither manuscript asserts complete Step4. Continue with the other
marked-source zero families under the user's persistent instruction.
