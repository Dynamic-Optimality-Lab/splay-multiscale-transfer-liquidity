# Support erasure: exact closed outputs, with the signed gap retained

Let gamma be any original reachable fully closed Pair Access walk with nonempty
genuine support M=G, |M|=r. For z in M, change every KEEP of z inside the period
to DELETE, retaining every request and every other mode. The A history and its
period cost A(gamma) are unchanged. B's one-period transformation F_z is the
composition of the remaining ordinary splays on the same finite ordered keys.

Start from the original reachable paired start, reached using the original
prefix. Repeating this changed period is itself a legal Pair Access history.
At every period boundary A returns to its original full tree. Because the set
of B trees is finite, F_z has, along this history, a preperiod u_z and period
p_z>=1. After the preperiod, p_z repetitions form an original fully closed,
reachable auxiliary pair walk with genuine support at most r-1. Its A cost is
p_z A(gamma). No original endpoint equality for B is assumed after one erased
period; recurrence is precisely what supplies it.

All z can be synchronized without new graph coordinates: choose u at least
all u_z and L a common multiple of all p_z. At boundary u the separately
defined auxiliary histories all have their original A tree; each B_z returns
after L more periods. Each auxiliary pair is independently diagonally
reachable through its own changed-mode history. Their private B states are
not identified, and no joint-state graph is constructed or enumerated.

Let Q_z be B's charge over those L auxiliary periods and set qbar_z=Q_z/L.
The original repeated period has A_L=L A and Q_L=L Q. Define

    R=2A-Q,
    R_z=2A-qbar_z,
    Delta_z=Q-qbar_z.

Then the exact signed identity is

    R=R_z-Delta_z.

CD(r-1), if available, implies R_z>=0. It supplies no bound on Delta_z.
In particular, the unqualified claim that some erased key preserves or
increases B charge is false. The following is a source-term proof over an
arbitrary-fringe family, not a finite replay.

Choose y<p<z with arbitrary valid BST hangers A,B,C,D in the four inorder gaps.
Write

    T_R=y(A,p(B,z(C,D))),
    T_L=z(p(y(A,B),C),D).

The original parent-first RR double gives S_z(T_R)=T_L. The parent-first LL
double gives S_y(T_L)=T_R, with every hanger restored at its original gap.
Starting from the diagonal (T_R,T_R), the period Kz,Ky is fully closed and
has A=2,Q=2. Both accesses have original depth2 and are genuine.

Erase z: B remains rooted at y and every retained KEEP is a root identity, so
its recurrent B charge is0. Erase y: after the first Kz, B stays rooted at z
and every remaining Kz is a root identity, again giving recurrent charge0.
Hence qbar_y=qbar_z=0 and Delta_y=Delta_z=2>0 for arbitrary hanger populations.
The residual identity reads R=2, R_y=R_z=4, Delta=2; CD is satisfied.

This refutes an UNQUALIFIED B-charge-monotone erasure rule, not a specialized
r>=6 lifting theorem and not CD. A correct signed reduction must control the
marginal Delta using actual independently available credit/slack. Merely
asserting R_z>=Delta_z would be the original conclusion again, since their
difference is exactly R. No such assertion is promoted here.

Thus the auxiliary-domain/closure subbridge is proved for arbitrary support;
the quantitative signed repayment subbridge remains OPEN. CD(5) alone cannot
settle it. No finite tests, new source evaluations, or row replays were used.
