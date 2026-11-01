# A single root change refutes normalized root envelopes

Root restriction preserves B repayment but leaves an unbounded DELETE increase. The obstruction is analytic in n and applies to every internal middle-tree shape.

## One source family and one legal DELETE

For any n>=6 let M be any ordered BST on keys 2 through n-1. Put

    A = 1(empty, n(M,empty)),
    B = 2(leaf 1, right vine on 3 through n),
    A_d = S_n A = n(1(empty,M),empty).

DELETE n is one primitive A zig: d_A(n)=1, a=1 and q=0, so its allowed increase is 2. In B, d_B(1)=1, d_B(n)=n-2, and every depth is at most n-2. The M keys retain their A depths in this zig.

For raw G the only changed weights are at keys 1 and n. Therefore the exact increase is

    G(A_d,B)-G(A,B) = (1-r)(n-3) = 7(n-3)/8.

This already exceeds two at n=6. Any additive repair Psi=G+R satisfying this DELETE must therefore have

    R(A_d,B)-R(A,B) <= 2-7(n-3)/8.                       (1)

Thus a correction with a uniformly bounded oscillation in A cannot repair G. A B-only additive gauge cancels on DELETE. Inequality (1) is a necessary condition, not a construction of R.

## The root-pinned envelope

Every source candidate T in L has root 1. Its root contribution to G is one; all other weights sum to less than 1/3. Nonnegative metric penalties cannot increase a score. Hence

    L(A,B) <= 1+(n-2)/3.

At the destination, T=A_d is allowed, and its penalty is zero. Its root contribution alone is n-2. Consequently

    L(A_d,B) >= n-2,
    Delta_DELETE L >= ell(n) := (2/3)(n-2)-1 = (2n-7)/3.  (2)

For every n>=7, ell(n)>2. This proves an unbounded family of actual DELETE violations, without evaluating L on larger finite graphs. The saved six-key metric certificate gives the additional exact boundary violation Delta L=21/8>2 at n=6; it is stronger than the loose analytic lower bound ell(6)=5/3.

## The normalized envelope class excluded by the same bounds

Let C(A,T,B)>=0 be any finite penalty with C(A,A,B)=0. Replace rho by C in either

    F_max(A,B)=max_{root(T)=root(A)} [G(T,B)-C(A,T,B)],
    F_min(A,B)=min_{root(T)=root(A)} [G(T,B)+C(A,T,B)].

For F_max, the source upper bound uses C>=0, and the destination lower bound uses the self-term. For F_min, every destination term has at least its root contribution, while the source self-term is an upper bound. Both functions consequently obey the same two endpoint bounds used in (2), and both fail DELETE for n>=7. No property of a metric, B independence, or fixed coefficient is required for this corollary. Extended penalties may also be allowed if the expressions are well-defined and the zero self-term remains available.

More generally, the same source family rejects any F lying in the band

    d_B(root(A)) <= F(A,B) <= d_B(root(A))+(max_y d_B(y))/3,

even after adding a B-only gauge. Adding a joint correction whose oscillation over A at fixed B is bounded by an absolute K only weakens (2) to ell(n)-K, which still exceeds two for sufficiently large n.

This does not rule out all root-aligned potentials. A correction whose changes grow with n, a state-dependent combination, or a function outside this root-depth band need not satisfy these endpoint estimates. None is constructed here.

## Admissibility from a diagonal and closure

Theorem 3.4 of [Levy and Tarjan](https://arxiv.org/html/1907.06310v3#S3) guarantees a present-key splay sequence between any two same-key BSTs with n>=4. Starting at any diagonal (T0,T0), a common KEEP sequence first reaches (B,B); a DELETE sequence then changes A from B to the displayed A while B stays fixed. The tested DELETE is therefore reachable from the prescribed diagonal. A DELETE sequence from A_d back to B and a common KEEP sequence from B to T0 close the walk exactly.

Only this reachability theorem is used, not its cost constant or a node-depth convention. The counterexample refutes a potential inequality on a genuine source edge. It does not assert that the entire closed walk violates Coarse-Double. The fixed n=6 word in AL04 establishes its own reachability and closure directly through both source engines.
