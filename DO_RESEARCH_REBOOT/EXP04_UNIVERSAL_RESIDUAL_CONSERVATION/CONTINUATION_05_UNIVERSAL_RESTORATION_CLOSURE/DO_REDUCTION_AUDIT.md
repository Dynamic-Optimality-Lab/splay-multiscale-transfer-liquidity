# Conditional downstream audit (premise not discharged)

No Universal Relaxed Coarse-Double premise has been proved,
so no Dynamic Optimality conclusion is asserted. The following
audit checks what would follow from **any** absolute C in
\(Q_B\le CA\), on all original admissible periods. It is not a
formal or independent-human audit.

## Original Route04 chain

1. In a closed period every genuine B KEEP changes its root
   from the previous KEEP target to a distinct key. Its
   preceding cyclic gap contains real A work, since the two
   A roots at those KEEP endpoints are different. The gaps
   are disjoint. Each KEEP has at most one terminal zig, so
   \(Z_B\le A\), including the zero-work and no-KEEP cases.
   Thus \(B=Q_B+Z_B\le(C+1)A\) on the exact complete cycles.
2. PIVOT-2 excises repeated full pair states in any finite
   present-legal history from a common T0. A removed subwalk
   is a reachable exact closed source, with its measured
   interval costs only; its reward \(B-(C+1)A\) is
   nonpositive under the premise. Splicing the identical
   pair states preserves actual transition legality. A
   simple residual path has at most \(\mathrm{Cat}_n^2-1\)
   edges and edge B cost at most \(\lfloor n/2\rfloor\).
   This gives a finite tree-only prefix overhead g(T0)
   independently of history length. For n≥4 the new
   constructive closure instead gives
   \(g\le468(C+1)(n-1)\). No uniform n-independent additive
   term is assumed or needed. Empty histories and n≤1 are
   immediate.
3. For X and an occurrence subsequence Y with the SAME
   initial T0, tag the complementary occurrences DELETE.
   A executes X, B executes Y. Levy–Tarjan's transition
   tree cost for ordinary bottom-up Splay is depth+1 in
   edge-depth conventions. Thus \(2A\le L(X,T_0)\) and
   \(L(Y,T_0)\le 2B+|Y|\). Since \(|Y|\le L(X,T_0)\),
   \[
   L(Y,T_0)\le(C+2)L(X,T_0)+2g(T_0).
   \]
   This sharper arithmetic implies the earlier conservative
   \(2C+3\) multiplier. These are universal multiplicative
   factors and tree-only startup terms, not statements about
   a mutated BST or a different starting tree.
4. [Levy–Tarjan v3, Theorem 4.3](https://arxiv.org/html/1907.06310v3#S4)
   takes eventual monotonicity exactly in this same-initial
   rooted-hull transition-tree cost model and concludes
   dynamic optimality, \(L(X,T_0)\le c\,\mathrm{OPT}(X,T_0)\)
   with a universal c and no startup term. The original
   bottom-up LL/RR and LR/RL operations match its algorithm.
   Its coercibility/repeatability are external inputs, not
   implications of fixed-size state graph finiteness. The
   paper uses an initial-tree normalization in its optimal
   cost argument; we do not presume \(n\le\mathrm{OPT}\) for
   arbitrary X,T0. Small n≤3 has \(L\le3|X|\le3\mathrm{OPT}\).
   Theorem 3.5 alone would not remove a startup term. Appendix
   A's rotational-model comparison is constant-factor, not
   an equality with StepEv.

## Separate constructive conditional implication

The new physical closure gives a way to audit the startup
issue directly, without relying on that external last arrow.
Work in the same rooted-hull cost model. For a nonempty
optimal execution, let J be the union of its transition-hull
keys over the whole execution. J is ancestor-closed in T0:
if an initial ancestor u of a selected key had never been
selected, its entire hanging component would stay internally
rigid until it is selected; the first hull containing a key
in it must contain u. Thus every initial ancestor of any
member of J is in J. The execution never touches outside
components except by intact reattachment. Restriction to J
preserves its original transition sizes, and \(|J|\le\mathrm{OPT}\).
Splay on X also preserves the initial hull J and has exactly
the same paths as in T0, since every requested key is in J.
This is a proved comparison projection; it does not project
any archived Pi or overflow record.

If \(|J|<4\), Splay has cost at most \(3|X|\).
Otherwise simulate each optimal rooted-hull transformation
by the splay coercion of DIRECT_CD_ALTERNATIVE inside that
hull, with arbitrary hanging components intact. For a hull
of size 1–3, extend it to four keys by actual ancestor-closed
frontier vertices of J, retaining their internal structure
in the desired after-tree. Their original hanging attachment
may move, but their paths stay in the augmented hull. The
four-key table supplies the transition. A simulation word
ends in the actual requested root; if it was empty, append
that one root request. Its A StepEv cost is at most \(156m\)
for an optimal hull of m keys, including the small and
identity cases. The original requests X are now a designated
subsequence of the simulated A word on J.

Run original Pair Access for that supersequence, starting at
the common projected tree. Its B side executes X. Append the
measured exact closure costing at most \(468(|J|-1)\) A.
Under the still-open universal CD premise and C.ZIG,
\[
L(X,T_0)\le 2(C+1)(156\,\mathrm{OPT}+468|J|)+|X|
             \le [1248(C+1)+1]\,\mathrm{OPT}.
\]
All optimal-cost quantities refer to the same original
specified T0. No tree-only startup is absorbed without the
explicit J argument, and no reaching work is miscounted.
This is a conditional derivation, not a new DO theorem.
The first missing hypothesis in both routes is the same
universal closed-source cost bound.
