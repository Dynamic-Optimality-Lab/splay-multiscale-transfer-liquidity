# What exact B repayment imposes, and what relaxing it can repair

The completion architecture has not been refuted for arbitrary terminal functions. The bounded cancellation audit is consistent. There is, however, a source-exact reason that weakening B equality alone cannot rescue the previous antichain terminal values.

## Quantifiers and source operations

Let A,B be finite nonempty BSTs on the same ordered key set, r=root(A), C_r(B)=S_r B, and Q_r(B)=floor(d_B(r)/2). Here S is the pinned bottom-up source splay, including the actual parent-first same-side doubles. Present-key completion puts r at the root and is idempotent. Q counts source doubles; depths count edges. Empty-tree conventions are irrelevant to the nonempty counterexample.

During DELETE x only A changes. Its cost is a=ceil(d_A(x)/2); physical B stays fixed and actual q=z=0. A simulated B completion in a potential evaluation is not a physical DELETE operation.

## Exact normal form: proved for all sizes

For any finite real-valued pair function Phi, define its equal-root boundary Theta(A,C)=Phi(A,C) when root(A)=root(C). Exact root-conditioned repayment means

    Phi(A,C_r(B))-Phi(A,B)=-Q_r(B).

Rearrangement gives, necessarily,

    Phi(A,B)=Theta(A,C_r(B))+Q_r(B).                 (1)

Conversely, every function of form (1) has that exact B law: after completion the terminal pair is unchanged, and the new Q is zero. This equivalence assumes no diagonal normalization, reflection symmetry, positivity, matching formula, scalar summary, or regularity of Theta. It characterizes exact equality itself.

## Weak normal form: the omitted freedom is nonnegative slack

The sufficient source theorem asks only

    Phi(A,C_r(B))-Phi(A,B)<=-Q_r(B).

It is equivalent to

    Phi(A,B)=Theta(A,C_r(B))+Q_r(B)+H(A,B),          (2)
    H(A,B)>=0,   H(A,C)=0 whenever roots agree.

To prove necessity, define H as the difference between Phi and the first two terms. The B inequality makes H nonnegative, while equal roots make it zero. To prove sufficiency, a B access changes (2) by exactly -Q_r(B)-H(A,B), which is at most -Q_r(B). This is a direct characterization, not a construction of an unknown successful H or a replacement open premise.

Thus exact equality sets H identically zero. Extra B repayment is precisely the allowed off-terminal slack. Slack may affect DELETE through its difference at the two actual pairs; its sign alone does not prove DELETE.

## The arbitrary-Theta contradiction test

For DELETE x let A'=S_x A, U=(A,C_r(B)), V=(A',C_x(B)). Under exact equality, the required DELETE bound becomes

    Theta(V)-Theta(U)<=2a+Q_r(B)-Q_x(B).            (3)

Every source edge has a determined integer right-hand side. On a closed directed sequence of terminal pairs, the Theta terms cancel. A negative total would refute every Theta in (1). Different B preimages can label successive edges in this projected sequence; they are not free physical B changes in a source walk. A projected contradiction would require its own full provenance and would not automatically be a CD counterexample.

The frozen seven-key minor has no such negative cycle; see [EB02](EB02_FROZEN_MINOR_AND_CERTIFICATE.md). No all-size consistency or no-go theorem follows from that finite result.

## Same source family: weak B cannot rescue the old terminal boundary

Use the complete parity-comb construction and interval proof in [RB01](../route_c_root_step_refutation_20261031_v001/RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md). For n=2m+1>=7,

    A_n=1(empty,n(M_n,empty)), B=R_n,
    T_n=n(1(empty,M_n),empty), V_n=S_n R_n.

The middle M_n has odd right spine 3,5,...,n-2, preceding even singleton left children, and final even leaf n-1. DELETE n is a single root zig, a=1. Source roots agree, Q_source=0; destination completion has Q=m. The proved terminal antichain values are

    K(A_n,R_n)=K(T_n,V_n)=n-3.

Now allow ANY pair potential obeying the weaker B inequality, but retain K as its equal-root boundary. At the source H=0, so Phi(A_n,R_n)=n-3. At the actual destination, the B inequality forces

    Phi(T_n,R_n)>=Phi(T_n,V_n)+m=n-3+m.

Consequently Delta_DELETE Phi>=m>2. No choice of nonnegative off-terminal H can repair this boundary. The same cancellation excludes every equal-root boundary f_n(K) for a finite scalar function f_n, even with arbitrary extra B repayment. This is a direct consequence of the existing witness, not a new terminal proposal or fit.

For n=7, M=3(2,5(4,6)), the two K values are 4, and the destination lower bound is 7. The source is reachable from the R7 diagonal by the existing DELETE prefix 4,7,3,5,7,1; B remains R7. The independent pointer verifier checks the prefix and the two terminal values by an active-right-interval chain upper bound and an attaining endpoint edge.

More generally, for arbitrary Theta the same weak-B/DELETE combination necessarily requires

    Theta(T_n,V_n)-Theta(A_n,R_n)
        <=2-m-H(T_n,R_n)<=2-m=-(n-5)/2.            (4)

The unbounded terminal drop is therefore required even after equality is relaxed. Arbitrary terminal functions are allowed to supply it. In the finite minor the certificate assigns the seven-key source terminal 0 and destination terminal -1, satisfying this particular demand. Those finite certificate numbers are not a proposed all-size potential.

## Scope

The exact and weak normal-form equivalences are PROVED—UNIVERSAL on finite nonempty same-key pairs. All extensions with equal-root boundary K or f_n(K) satisfying both source bounds are REFUTED—EXACT by this existing family. The arbitrary-Theta root-completion architecture, generic Step 3, and Universal Coarse-Double remain OPEN. This audit discharges no original CD obligation and introduces no new assumption for that theorem.
