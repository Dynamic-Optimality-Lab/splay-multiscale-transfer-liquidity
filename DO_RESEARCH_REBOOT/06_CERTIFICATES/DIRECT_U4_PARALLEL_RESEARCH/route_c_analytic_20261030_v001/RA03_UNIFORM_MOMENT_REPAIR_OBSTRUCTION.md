# Uniform obstruction to depth moments plus bounded nonlinear repair

**Theorem.** Fix any real alpha, any beta>0 and any finite K. No source potential

    Psi(A,B)=alpha*D_A(A)+beta*D_B(B)+R(A,B)

can satisfy q-2a<=Psi(source)-Psi(destination) on every admissible original transition if D_A,D_B are sums of edge depths and R has oscillation at most K on each n-key state domain, uniformly in n. R may otherwise depend on both full trees, n, labels, nonlinear statistics or hidden joint structure. A size-dependent additive gauge does not matter. Alpha and beta are fixed constants, not functions growing with n.

**Proof.** Apply the R branch of RA02 with m arbitrary. Differentiate its profile in z or w and evaluate at z=w=1. The source core A-depth sum is12 and destination sum11; the fringe's A depths are unchanged. Hence Delta D_A=-1. B's core sum goes15 to9, while every fringe node descends one level. Thus Delta D_B=m-6.

The access has a=1,q=2, so the required inequality is Delta Psi<=0. But

    Delta Psi = -alpha+beta*(m-6)+Delta R
              >= -alpha+beta*(m-6)-K.

Choose an integer m>6+(alpha+K)/beta, with m>=0. Then Delta Psi>0, contradiction. RA02 proves physical admissibility for every such m. This proves the all-size exclusion without any larger fit or sampled tail argument. Reflection gives the same obstruction in the other orientation.

Equivalently, a repair of this positive-B-moment strategy must have a DROP on the zero helper of at least beta*(m-6)-alpha, growing linearly with the fringe size. A fixed range-two joint correction, root/vine bits or any other uniformly bounded correction cannot repair that strategy globally.

**Scope limits.** This excludes the specified moment-plus-bounded-repair architecture. It does not exclude beta<=0, n-dependent moment coefficients, a genuinely unbounded nonlinear correction, a nonlinear histogram potential with no such decomposition, a structural full-tree invariant, or a justified macro potential. It does not refute any CHR/FRC theorem at its certified scope. In particular RA02 contains no negative-weight closed walk.

Historical comparison: depth sums and their fringe-recharge failure were already recorded in PIVOT_CONSTRAINT_GUIDED_DUAL.md and wp6_symtable.py. The new explicit arbitrary-fringe zero-helper family gives a uniform quantitative obstruction covering arbitrary bounded JOINT repair, rather than announcing an old depth-moment idea as a new viable candidate. This is strategic elimination, not a positive CD-U proof leaf.
