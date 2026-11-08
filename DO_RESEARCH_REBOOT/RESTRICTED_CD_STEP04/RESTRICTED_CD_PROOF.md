# Restricted Coarse-Double: Step04 proof

## Imported theorems at unchanged scope

11F gives, for each original `W in W_5^9`, a finite fully closed two-sort walk
`P in G_AF` with

\[
w(P)\le 2A(W)-Q_B(W). \tag{F}
\]

The whole word, including DELETEs, nongenuine KEEPs and zero-cost operations,
is covered by its macro partition. A macro of A-cost H and B-credit q has weight
`2H-q` for H<=2, or `6-q<=2H-q` for H>=3. Thus the direction of (F) is an upper
bound on the abstract weight. T266 is used per macro, not as a global word-size
restriction. Exact paired-tree closure gives identical full abstract endpoints.

Step01 froze `G_star=G_AF`, without a reachability filter. The sealed XFER21
certificate gives one fixed ordinary debt D in[0,2], using the original current
public state only, with

\[
\Phi(O)=-D(O)-5\chi_8(O.b),\qquad
\Phi(M)=-5\chi_8(M.b),\qquad
\chi_8(b)=[b.kr[8]=0\land b.rr[8]=19].
\]

It proves, for every original edge of every original admissible sector,

\[
w(u,v)\ge\Phi(v)-\Phi(u). \tag{E}
\]

Use the actual sealed D, including the XFER19 parent and 4359 completion clauses.
No proof-only lower bound for D is substituted for the function.

## Step03: every original closed walk is nonnegative

For clarity, the two-sort arithmetic of (E) is as follows. LOW conserves chi8,
and the completed signed debt inequality is `w+D(v)-D(u)>=0`. For OM with chi8
unchanged, `w>=2` and `DeltaPhi=D(u)<=2`. For an entering OM, `w>=-3` and
`DeltaPhi=-5+D(u)<=-3`. A leaving OM is impossible. MO has weight0, unchanged
chi8 and `DeltaPhi=-D(v)<=0`. MM has no edge. The HIGH h=0 correction remains
actualdepth0, declareddepth18, q9, weight-3 and is covered by the entering case.
These source facts are the already audited universal M3 premises, not claims
inferred from a finite table of signatures.

Induction on the number of edges yields, for every finite original walk,

\[
\sum_{i=0}^{n-1} w(v_i,v_{i+1})
\ge\sum_{i=0}^{n-1}(\Phi(v_{i+1})-\Phi(v_i))
=\Phi(v_n)-\Phi(v_0).
\]

The zero-edge case is equality. The induction step adds the next edge and
cancels the same full shared vertex's potential. A full closed walk has
`v_n=v_0`, hence weight>=0. This includes LOW-only (M1), HIGH-only (M2) and
mixed (M3) walks, arbitrary repetitions and either sort at the chosen seam.
Equal potentials do not identify unequal vertices. In particular, lo/hi,
unused raw coordinates and the full midpoint remain shared. A debt is never
evaluated on a midpoint, and private inventories are not concatenated.
Therefore `NonNegCycles(G_star)` holds on precisely the frozen full graph.

## Step04: composition

Fix an arbitrary original `W in W_5^9`. Choose the one closed image walk P
whose existence (F) supplies. Every edge of P belongs to G_star by the Step01
coverage theorem. The preceding universal sign theorem applies to this P:

\[
0\le w(P)\le2A(W)-Q_B(W).
\]

Consequently `2A(W)-Q_B(W)>=0`, equivalently

\[
\boxed{\forall W\in\mathcal W_5^9,\quad Q_B(W)\le2A(W).}
\]

The argument uses `forall W exists P` and `forall closed P, w(P)>=0`; it never
reverses either quantifier or demands one private realization for an entire
abstract walk. Since W was arbitrary, the conclusion has the full frozen
domain, all126 masks and arbitrary admissible fringe/signatures. There is no
remaining mandatory premise in this composition.

This proves Restricted CD at the exact 11G target. It does not expand the
number of genuine KEEP keys, prove unrestricted Coarse-Double, or complete the
remaining implications to Dynamic Optimality. Bank25 remains25. Publication
of this proof requires the separate composition audit and resource seal.
