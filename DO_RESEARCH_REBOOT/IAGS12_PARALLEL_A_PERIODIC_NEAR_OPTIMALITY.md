# IAGS 1.2 — Parallel Route A: periodic near-optimality transfer

Date: 2026-11-10, Asia/Karachi.

**Final verdict: BENCHMARK PROVED**, relative to Chmel et al., arXiv:2607.18498v1, Theorem 1. The new source-to-theorem bridge is an all-source symbolic proof by the author of this report. It is not independent or formal certification of that proof or of the external paper.

For every original finite admissible exactly paired-closed source W on its complete fixed physical population X, put n=|X|. There is an absolute C such that

\[
Q_B(W)\le Cg(n)A(W),\qquad
R_{\rm irr}(W)\le Cg(n)A(W).
\]

Here g is defined for every nonnegative integer in Section 2 and has asymptotic order \(\log\log n(\log\log\log n)^2\). One valid symbolic constant is \(C=3C_0/2\), where C_0 is the absolute constant in the audited external theorem with that choice of g. The proof actually gives the sharper interface (7.4) below.

This establishes a size-dependent ceiling. No absolute coefficient for URCD, no Dynamic Optimality conclusion, and no improvement removing a logarithmic factor is established. This report executes Route A only and stops here.

## 1. Scope and current-source audit

The current complete RESEARCH_RULES, RG01, RG04, G0, and D1–D5 files were read, including the inserted D5 directive at the beginning of the current D4 file and the dated D4 mathematical body that follows it. The original Pair Access and ND35 physical S/SET specifications, current Route 04 and Route 02 linear-incidence reports, and original PIVOT2 cycle-to-prefix documentation were read directly. Their current byte pins are in Section 13. The inserted historical directives are source/provenance material, not authorization to execute their stages.

The four research gates, fixed before the proof, are as follows.

1. **Smaller obligation:** prove the size-dependent theorem using an existing external competitiveness theorem. The uniform-in-size source-work bound is not a premise or an objective silently substituted for this one.
2. **Concrete mechanism:** remove only B identity accesses from a mathematical comparison sequence, schedule the full chronological A rotation stream as paid root-BST restructuring, and apply the external theorem once to an arbitrarily long repetition of one fixed closed period.
3. **Bounded scope:** one cost-model bridge, one periodic limit, the specified static adversarial controls, and a dependency audit of the external factor. No new source engine, experiment, enumeration, solver, replay, subagent, or other research stage is used.
4. **Upward effect:** replace the absence of an audited full-source near-optimality bridge by a proved \(O(g(n))\) ceiling. This does not delete the missing absolute source-work bound. Route 04 Section 9 already sketches a size-dependent comparison; that sketch is not assumed as a theorem here. The active-access accounting and complete-tail construction below supply the explicit bridge requested in this task.

The original model is retained literally. A splays every KEEP and DELETE target; B splays every KEEP target and freezes on DELETE. All requests are to present keys. DELETE removes an occurrence from B's request history, never a physical key. X is finite and fixed, with arbitrary full physical hangers and private A vertices. A and B return to their respective identical complete labelled initial trees after W. Their two initial trees need not equal each other. Reachability from a legal diagonal is retained, but its prefix is outside all costs in this report.

With original edge depths,

\[
A=\sum_t\lceil\delta^A_t/2\rceil,\qquad
Q_B=\sum_{t\ {\rm KEEP}}\lfloor\delta^B_t/2\rfloor.
\tag{1.1}
\]

An A double is one StepEv and two real rotations; a terminal zig is one StepEv and one real rotation. Its virtual companion is not physical work. Write R_A,R_B for real rotation counts, V_A for A terminal-zig virtual units, and Z_B for real B terminal zigs. Thus

\[
R_A=2A-V_A\le2A,\qquad R_B=2Q_B+Z_B.
\tag{1.2}
\]

The original SET accounting remains separate. With P_A,N_A the positive/negative real A counts and B_i the number of B doubles with i decreasing real bits,

\[
D_B=P_A-N_A=B_1+2B_2+Z_1,
\qquad Z_1=Z_B.
\tag{1.3}
\]

This follows from actual A SET changes, nonpositive B SET changes at the post-A target-rooted tree, and complete paired closure. The terminal-zig term is essential. D_B is neither Q_B nor R_B. Equations (1.2) and the KEEP-gap bound proved in Section 6 are the cost bridges used in the main argument; (1.3) is preserved without being substituted for them.

At inherited scope, G0–D5 retain their symbolic verification qualifications. In particular,

\[
R_{\rm irr}\le R_{\rm branch}\le U_{\rm int}\le Q_B,
\quad Q_B\le(32+\Lambda)A+R_{\rm irr}
\tag{1.4}
\]

are not treated as independently certified new results. The main Q_B benchmark below does not require the second inequality, a regeneration matching, or the D5 scan theorem.

## 2. Exact external Theorem 1 statement

Primary dependency: Petr Chmel, Bernhard Haeupler, Richard Hladík, Michal Koucký, Antti Roeyskoe, Václav Rozhoň, Ondřej Sladký, and Robert E. Tarjan, *Splay trees are almost dynamically optimal*, arXiv:2607.18498v1, submitted July 20, 2026. This is the identified primary preprint; no journal-refereeing status is inferred from the word “published” in the request.

The full primary [HTML](https://arxiv.org/html/2607.18498v1) was inspected at Section 2.1, Theorem 1, Sections 5.1–5.6, Appendix B, and the normal-form proof in Appendix C.4. Relevant statements were cross-checked in the repository's existing 68-page PDF: model on PDF pages 3–4, Theorem 1 on page 13, pairing statements on pages 37, 39, 45–47, completed proof on pages 46–48, and Appendix B on pages 58–59. The PDF's page numbers here count its first page as 1. No paper or source was altered.

In mathematical form, the original theorem says: for a fixed ordered n-key universe and any finite access sequence \(\sigma=(x_1,\ldots,x_L)\) in it, splaying from an arbitrary initial configuration satisfies

\[
\operatorname{cost}_{\rm splay}(\sigma)
=O\!\left((\operatorname{cost}(T^{\rm OPT}_\sigma,\sigma)+n)
\log\log n\,\log^2\log\log n\right).
\tag{2.1}
\]

The cost is the paper's root-BST cost. Section 2.1 explicitly permits OPT to choose its initial configuration and gives no control over the initial splay configuration. Theorem 1 includes the additive n; it is not restricted to long sequences. Discussions of competitiveness for sufficiently long sequences do not remove that term from the finite-sequence theorem. The paper explains that arbitrary initial splay trees can require linear initial work even on one access.

For an everywhere-defined version, set

\[
\bar n=\max\{16,n\},\qquad
g(n)=\log_2\log_2\bar n\,
\bigl(1+\log_2\log_2\log_2\bar n\bigr)^2.
\tag{2.2}
\]

This is positive, finite, and nondecreasing for every integer n>=0, with g(n)>=2, and has the required asymptotic order. After enlarging one absolute constant to cover the finitely many small sizes, (2.1) yields the audited interface

\[
\operatorname{cost}_{\rm splay}(\sigma)
\le C_0g(n)\bigl(\operatorname{OPT}_{\rm root}(\sigma)+n\bigr).
\tag{2.3}
\]

C_0 is symbolic and absolute; no numerical constant is claimed. For small positive n, the elementary bound \(\operatorname{cost}_{\rm splay}\le nL\), together with \(\operatorname{OPT}_{\rm root}\ge L\), justifies such enlargement. For n=0 only the empty sequence is legal and both costs are zero.

## 3. Root-BST cost-model comparison

The decisive model clauses are [Section 2.1](https://arxiv.org/html/2607.18498v1#S2.SS1) and [Appendix B](https://arxiv.org/html/2607.18498v1#A2). Appendix B describes paid arbitrary rotations before the unit-charge access, which must then find the target at the root.

| Audit question | Primary-text answer and consequence |
| --- | --- |
| Initial splay tree arbitrary? | Yes. Use the actual complete B tree at W's cut. It need not resemble A. |
| Comparator initial tree selectable? | Yes. OPT minimizes over initial configurations as well as executions. Starting a candidate at the original A tree is therefore legal. |
| Operations during one access? | Any finite sequence of ordinary rotations on the fixed universe, ending with the requested key at the root; each rotation is charged. |
| Arbitrary rotations before bringing the target to the root? | Yes. They need not be rotations of the current requested target or its ancestors. There is no root-pointer travel charge in this root model. |
| Full key population fixed? | Yes. The theorem concerns accesses within one n-node universe. Order-preserving relabelling of X by [n] is harmless; removing physical keys is not part of this application. |
| Initialization allowance? | The stated bound contains n inside the factor C_0g(n). It is paid once for the whole input sequence. |
| Sequence length restriction? | No minimum length in Theorem 1 with its additive term. The theorem's constants do not depend on L. |
| Root access with no rotations? | Costs one. This charge survives for every retained access and cannot be discarded as initialization. |

Appendix B, Lemma 37, gives standard-to-root cost at most twice standard cost, and equality of the two costs for an execution already valid in the root model. No factor from that equivalence is needed here: the comparator is constructed directly in the root model. The original StepEv convention and the external root convention are connected explicitly rather than identified.

In particular, original A DELETEs can supply rotations during a later retained comparator request without being declared extra comparator requests. The comparator pays those rotations. It does not execute them for free between charged requests.

## 4. Original B active-access extraction

In the original chronological word let

\[
t_1<\cdots<t_k
\]

be exactly the KEEP occurrences at which B performs at least one real rotation. Define

\[
\sigma_B(W)=(x_{t_1},\ldots,x_{t_k}),\qquad k=K_B(W).
\tag{4.1}
\]

The starting tree for splaying this sequence is the actual B_0. Removing a DELETE from this comparison has no B effect because its B phase was identity. Removing a root-only B KEEP has no effect because ordinary bottom-up splay on a root performs no rotations and changes no pointer.

Induct on original operations. Before the next retained KEEP, the extracted execution and the original B have identical complete labelled trees: omitted operations left B unchanged, and the preceding retained operation was served by the same deterministic splay. At this KEEP, their full search path, ordered double/zig steps, and successive complete trees therefore agree. This proves the invariant for the next operation.

Consequently every original B rotation, including terminal zigs, occurs in the extracted execution in its original order. There are no extra B rotations. Original source IDs remain attached to the corresponding rotations; the mathematical comparison sequence does not edit the archived source word or its A execution. Thus exactly

\[
\operatorname{cost}_{B}(\sigma_B(W))=R_B(W)+K_B(W)
=2Q_B(W)+Z_B(W)+K_B(W).
\tag{4.2}
\]

All A work at an omitted KEEP remains in the A rotation stream used below. This includes positive A cost caused by helpers since B last accessed that root. The extraction introduces no term proportional to the total number of omitted requests.

## 5. Legal A-derived offline comparator

Assume k>0; k=0 is handled separately. Fix m>=1 and consider the chronological original A execution on W^m, starting at its actual A_0. Its rotation stream includes every original A rotation in all m periods, in exact order, including every DELETE and every omitted B-root KEEP. No intermediate original A tree is projected.

For each retained request, assign to it all not-yet-simulated original A rotations through the A phase of that request. Perform them as its paid pre-access restructuring. For any retained request except the very last, the resulting tree is precisely the original post-A tree for that occurrence, so its requested key is at the root. Charge the access one. Keep this entire complete A configuration for the next batch.

This schedules all rotations through the final retained KEEP. There remains a final tail: original A rotations after that KEEP through the end of the last copy of W. Discarding that tail would violate the proposed complete-trajectory comparator. Appending it after an already completed final request would also leave the wrong final root in general.

Instead, include that tail among the paid rotations **before completing the final comparator access**. After the tail, the simulated tree is A_0 by exact A closure. Let A_* be the complete original post-A tree at the last retained KEEP in W; its root is the final requested key. Convert A_0 to A_* by at most

\[
J(n)=2\max\{n-1,0\}
\tag{5.1}
\]

additional real rotations, then charge the last access one. All these rotations occur before that comparator access is completed; visiting its target at the root earlier during restructuring does not terminate an access automatically.

Here is a physical proof of the conversion bound. Any nonempty n-key BST can be made into the full right vine using at most n-1 right rotations: scan its right spine, rotating away left children until none remain; each such rotation places an additional vertex on that spine and never removes its existing vertices. Converting the desired tree to the same vine and reversing those rotations gives a second path of length at most n-1. Concatenate the two paths. Every step is a real rotation on X. The empty/one-key cases need none.

The comparator is now legal at every charged access. Every original A rotation in W^m was simulated once in original chronological order; the final conversion is separately paid auxiliary work. Before termination, complete source configurations were maintained at every source snapshot. No subsequent original operation remains after the terminal correction. In particular, rotations after the last retained KEEP of one nonfinal period and before the first retained KEEP of the next are executed together in that next access's batch, with no reset or free restructuring.

Since OPT can choose its initial configuration, this candidate can start at A_0 without an initial conversion. We have proved

\[
\boxed{
\operatorname{OPT}_{\rm root}(\sigma_B(W^m))
\le m\bigl(R_A(W)+K_B(W)\bigr)+J(n).
}
\tag{5.2}
\]

This is one comparator for the full repeated sequence, not m separately initialized comparators. J(n) is independent of W's length, its tail length, and m. If an interface instead prescribed a common initial comparator tree, one physical conversion to A_0 would add at most another J(n), once. The actual theorem does not require that extra term.

There is also an exact periodic comparator if chronological order is understood on the source circle. Start at A_*, process the last-to-first A tail across the seam before the first retained target, and then the other retained batches. One cycle ends at A_* again and costs exactly R_A+K_B. Repeating this rotation schedule proves an exact no-adjustment comparison under that cyclic cut. The main finite proof (5.2) deliberately keeps W^m's original linear chronology and includes every final-tail rotation, so it does not depend on accepting that alternative reindexing.

## 6. Full-period A-cost accounting

To verify K_B<=A with G0's exact definition, list **all** original cyclic KEEP occurrences, including root identities. For a nontrivial B KEEP h, let h^- be the immediately preceding KEEP. If its target is y and h's target is x, then B's root before h is y, because intervening DELETEs freeze B. Nontriviality implies x!=y.

A is rooted at y after h^-'s A phase and at x after h's A phase. The original A interval between those boundaries contains at least one nonzero StepEv. Choose its first such StepEv, whether it occurs in an intervening DELETE or h itself. There is no other KEEP inside this particular gap, since the cyclic list includes every KEEP. Its bit 0 is a real rotation, also for a terminal zig.

The cyclic intervals between successive post-A KEEP boundaries partition original A StepEv occurrences. Distinct nontrivial B KEEPs therefore have distinct selected cost-one StepEv. Exact complete A/B closure validates the interval crossing the seam; no reaching-prefix event is used. Hence

\[
\boxed{K_B\le A.}
\tag{6.1}
\]

Together with the original real/virtual identity,

\[
R_A+K_B=2A-V_A+K_B\le3A.
\tag{6.2}
\]

This proves the requested absolute C_1=3 in

\[
\operatorname{OPT}_{\rm root}(\sigma_B(W^m))
\le3mA(W)+J(n).
\tag{6.3}
\]

Neither a root-only KEEP nor a DELETE is charged an unnecessary comparator access. Both can still incur A rotations, all of which were paid in (5.2). The per-retained-access unit charge is mK_B; it is proportional to m and is controlled by (6.1), not sent to zero with initialization.

If there is no KEEP, then K_B=Q_B=R_B=0. If there is exactly one KEEP in an exactly B-closed word, its target must already be B's initial root, so it is an identity. More generally K_B=0 directly implies Q_B=R_B=0, independently of any positive A-only work. No nonempty comparator is needed for that case.

## 7. Paired-closed repetition and additive-term cancellation

Each complete labelled A tree and B tree returns to its own initial configuration after W. Determinism therefore makes every subsequent copy begin in exactly the same physical pair and reproduce the same depths, real rotations, double/zig partition, and active KEEP indices. Induction on copies proves

\[
A(W^m)=mA(W),\quad R_A(W^m)=mR_A(W),
\quad Q_B(W^m)=mQ_B(W),
\tag{7.1}
\]

and likewise R_B,Z_B,K_B scale by m. It also proves

\[
\sigma_B(W^m)=\sigma_B(W)^m,
\quad \operatorname{cost}_{B}(\sigma_B(W^m))
=m(R_B+K_B).
\tag{7.2}
\]

Only equality of roots would not prove these facts; equality of both complete labelled trees is used. The analytical copies have their own chronological occurrences for counting m periods; they do not lend extra resources to the original one-period ledger.

Apply the external theorem once to this entire sequence, with B starting at its original B_0 and n fixed. From (5.2),

\[
m(R_B+K_B)
\le C_0g(n)\{m(R_A+K_B)+J(n)+n\}.
\tag{7.3}
\]

Divide by m and let m tend to infinity for this fixed W and fixed X. Both J(n)/m and n/m vanish. The multiplier g(n) is fixed in this limit and remains. No other initialization or endpoint term is hidden. Thus

\[
\boxed{R_B+K_B\le C_0g(n)(R_A+K_B).}
\tag{7.4}
\]

We did not send m to infinity while changing X, omit a per-copy tail, or apply the theorem independently to every copy. The reaching prefix is absent from both sides. Arbitrary initial B and freely chosen comparator initial A are precisely the initial-configuration conventions of the primary theorem.

## 8. Quantitative near-URCD theorem or exact failure

Substitute the exact original counts into (7.4):

\[
\boxed{
2Q_B+Z_B+K_B
\le C_0g(n)(2A-V_A+K_B).
}
\tag{8.1}
\]

This is the strongest retained cost interface of the transfer; the following uniform-in-W form deliberately simplifies it:

\[
Q_B\le\frac{C_0g(n)(2A-V_A+K_B)-K_B-Z_B}{2}
\le\frac32C_0g(n)A.
\tag{8.2}
\]

The first inequality distinguishes B doubles from B real rotations and retains the per-access charge on both sides. We may also retain \(R_B\le3C_0g(n)A\). Neither conclusion identifies R_B with Q_B.

If A=0, (6.1) gives K_B=0, hence Q_B=0. This proves the zero case before forming a ratio. Empty X permits only an empty present-key word. For one or two keys there are no B doubles. The smoothed g handles these and every other finite small size; no undefined iterated logarithm is used.

**Full-physical-population theorem:** (8.2) holds for every original admissible W with n=|X|, absolute C=3C_0/2, and only the stated primary external dependency. There is no transfer blockage at the comparator, initialization, or cost-model steps.

### Investigation of replacing |X| by |S|

The B side does have a useful exact restriction, already made explicit in D5 Section 7.2. Since S is ancestor-closed in B and contains every KEEP target, the tree of S vertices uses actual physical edges; an off-S component is an S-free hanger. A B rotation has S operands. Its literal rotation table carries each hanger intact. Induction on rotations proves that the same requests in the ordinary S-vertex tree produce exactly the same S operand paths, real rotation counts, and double/zig choices. This proves B cost invariance under this mathematical comparison. It does not modify W.

It is insufficient to replace n throughout (5.2)–(8.2). A can have private ancestors and private branching vertices separating S keys. Its DELETE helpers can target keys outside S. The supplied facts give no map sending the complete A trajectory to a legal S-key root-BST comparator with O(R_A+K_B) total paid rotations. Deleting private A vertices without specifying that map is an unsupported implication.

A sufficient additional theorem would construct, for every original W and every m, an S-key comparator for the same extracted retained targets with cost at most \(c\,mA(W)+I(S)\), c absolute and I independent of m, while justifying all effects of private A rotations. Together with the B invariance just proved, the same limit would yield O(g(|S|))A. That comparator theorem is not proved here. Consequently **no |S| replacement is claimed**. The elementary inherited bound \(Q_B\le\lfloor(|S|-1)/2\rfloor K_B\) remains available at its original carrier scope; it is a different, linear-in-carrier-size estimate.

## 9. Bound on the original R_irr residual

At D5's unchanged membership and verification scope, each R_irr object is an original adjacent cohort pair, is in R_branch, and the total collision count is at most U_int. Consequently the inherited chain in (1.4) and the newly proved (8.2) give

\[
\boxed{R_{\rm irr}(W)\le\tfrac32C_0g(|X|)A(W).}
\tag{9.1}
\]

For A>0 this is an explicit size-dependent ceiling on the unresolved ratio. It does not establish that a size-independent supremum is finite. It does not pay R_irr by the old D1–D5 event maps, allocate vacant units, change historical owners, or prove their missing regeneration law.

The same argument bounds R_branch and U_int by the right side of (9.1). Proper-subclass membership alone gives no factor improvement. In particular, no extra factor is removed because R_irr has stricter structural predicates than all B doubles. The inherited inequality \(Q_B\le(32+\Lambda)A+R_{\rm irr}\) is compatible with this ceiling but unnecessary to prove the benchmark.

The original cycle-to-prefix documentation was audited for scope only. It requires an absolute cycle coefficient to obtain the source-uniform constant needed by the downstream route. Fixing n makes Cg(n) a coefficient for that fixed state graph; it does not make it universal over sizes. Its multiplication of recurrent A cost cannot be moved into an initial-tree-only additive allowance as sequence length grows. No Dynamic Optimality implication is asserted.

## 10. Full adversarial source audit

This is a static, symbolic consistency audit of the complete supplied constructions. Their historical exact-source calculations retain their same-agent verification level; none was replayed. The universal proof above comes from arbitrary W, rather than from this list. Unknown full-scan costs below remain named actual costs, with every access included.

For compact notation V+ is the full right vine. In W/H families let \(N=2^{p+1}(q+1)+1\), \(x_j=N+1-2^j\) for 0<=j<=p, and \(m_0=x_p\). The exponent m in the proof is unrelated to this last marked key.

| Complete source | Complete word, closure work, and A cost retained | Transfer audit |
| --- | --- | --- |
| Original W_pq | From common V+ on [N]: DELETE 2,...,N; every descending target N,...,m_0, KEEP only x_0,...,x_p; KEEP 1,...,N; KEEP N-1,...,1. Length 3N+2^p-2. \(A=2(N-1)+(2^p-1)+C_{\rm forward}\), with the full actual forward cost, including its first jump. | All preparation DELETE rotations and both closing scans enter R_A. There are K_B=p+2N active KEEPs. The large critical B accesses are not independently closed comparison periods. |
| Complete H_pq | Extend the same descending A sweep through EVERY key to 1, with the same marked KEEPs, then retain both full KEEP scans. Length 4N-2, \(A=R_A=4(N-1)\); both complete trees close to V+. | Again K_B=p+2N. Here (7.4) has comparator density \(4(N-1)+p+2N\), with all reset work retained. Shared first hits and arbitrarily long renewal chains do not affect legality or create extra unit charges. |
| H_(6,1) | The preceding complete H word with N=257, length 1026, A=R_A=1024. Retain the actual growing relay [11,33] to [19,129] and both original incident histories. | K_B=520; the exact periodic comparator density is 1544. No shrinking output-size/rank claim is used. The relay neither violates the benchmark nor supplies a constant-factor strengthening. |
| W_hit | Insert the supplied KEEP a_i after W_pq's entire critical packet, then retain both full closing scans. \(a_i=N+2-2^{p+1}(i+1)\). Length 3N+2^p-1. \(A=2(N-1)+(2^p-1)+\lceil(m_0-a_i)/2\rceil+C_{\rm new\ forward}\). | The added low jump and every later A rotation are paid; K_B=p+2N+1. Persistent obstruction key 1 creates no exception. Its first-hit cost is not charged once per cohort member. |
| W_5 | Complete W_(3,1) with KEEP 5 inserted after its critical packet, then both full closing scans. N=33, length 106, \(A=82+C_{\rm full\ increasing}\). The added jump has depth 21 and cost 11. | K_B=70. Preserve the first LR signs (0,-1) and the edge (10,6,LEFT) returning within the hit with changed descendants and no A between those B bits. Extraction retains both B bits; the comparator never assumes that every B edge rebirth requires a new A access. |
| W_star | D2's complete 235-operation H_(3,1) source with both A-only excursions P and Q and both closing KEEP scans. P: DELETE 1,2; DELETE 1,...,33; DELETE 32, inserted after KEEP 32. Q: DELETE 11,10,1,2; DELETE 1,...,33; DELETE 32,...,1, inserted after the descent reaches 1. \(A=128+75+79=282\). | All 105 helper operations remain in the A rotation stream, with K_B=69. The middle candidate failing its full Pi at A(36,7,1) stays excluded by the original U predicate. No artificial residual adjacency or extra helper access charge is introduced. |
| Repeated 21-key I^r Z | Common full T with T_10=19(-,20(-,21)) and T_i=(2i)(2i-1,T_(i+1)), i=9,...,1. I: DELETE 4,6,...,18; descend 18,16,...,2 keeping only 18,16; KEEP 2,4,...,18; KEEP 16,14,...,2. Z: KEEP 1,...,21; KEEP 20,...,1; KEEP 19; then for k=1,...,9 KEEP 2k,2k-2,...,2. Length 34r+87; \(A=32r+A(Z)\). Full I and Z returns are retained, and S=X=[21] for the complete source. | K_B=19r+87 by counting the successive distinct KEEP targets. R_A=32r+R_A(Z), so the comparator density is \(51r+R_A(Z)+87\). Fixed closing Z is not omitted. New nonleaf births are distinct original occurrences; persistent leaf 7 supplies no new credit. The extraction theorem does not merge different copies' first-hit IDs. |
| Warmed-up paired-closed repeat | Use the actual legal reaching prefix to A=full left vine, B=B_p, excluded from period costs. The period descends EVERY N,...,m_0 keeping exactly the marks, then DELETE m_0+1,...,N. Complete B_p, every gap/low hanger, and complete A return are retained. \(A=R_A=2(2^p-1)\); original S is the marked carrier. | K_B=p+1. The final A-only ascending tail is essential: in (5.2) it crosses into the next retained access, and in the final copy it is followed by the paid terminal conversion. The excluded q-sized preparation wave is never charged again. No changing physical population or support substitution is used. |
| D5 irregular G | From common V+ on [65]: DELETE 2,...,65; descend EVERY 65,...,1 keeping exactly 65,64,62,58,50; KEEP 1,...,31; KEEP 1; KEEP 1,...,65; KEEP 64,...,1. Length 290, \(A=237+C_{\rm close}\), where C_close is the entire final increasing-scan cost. The low reset has depth 30 and costs 15. | K_B=165. In original IDs, KEEP 1 at 161 is followed by root-only KEEP 1 at 162. The latter is omitted from the comparison, with no B rotation lost. The complete later reset and closing work stays in A. The genuine R_irr pair consumed at 132 remains outside D5's long-scan class and is nevertheless covered by (9.1). |

For G, the K_B count is \(5+31+1+64+64=165\); the omitted first KEEP in its final increasing scan contributes no active-access unit. In every source, all real B zigs remain in R_B even when they supply no double to Q_B.

The many-identity-access issue is settled universally, not just by G's one explicit occurrence. For any admissible W, arbitrarily many B-root identity KEEPs would still contribute zero terms to (4.2). Their actual A rotations, if any, remain in R_A. The comparator charges only K_B access units, and K_B<=A was proved on the original cyclic KEEP list including every identity. Thus no uncontrolled |W| or total-KEEP-count term arises. This is a quantified consequence of the extraction proof, not an experimental insertion into any historical word.

These checks preserve complete A/B closing work and distinguish all excluded prefixes from actual periods. The original D1–D5 full-Pi predicates are neither weakened nor needed to prove the Q_B comparison. They are needed when interpreting which original residual objects inherit its upper bound.

## 11. Exact logarithmic-loss dependency analysis

All statements in this section refer to the primary paper's valid normal-form comparison and its auxiliary structures, not to the original physical S labels. In particular a “gap” in the paper is not an original blind gap or a G0 collision layer. No dictionary identifying those objects has been proved.

Write \(c_* = \operatorname{cost}(T^*)\), \(N_*=n+c_*\), p for paid lazy-interval operations, u for unimportant boundary pairings, a for all internal pairings, and h_good for good internal pairings. The paper uses g for the last count; it is renamed here to avoid confusion with (2.2).

### 11.1 Normal form, ranks, and lazy rotation updates

[Theorem 2 and Corollary 3](https://arxiv.org/html/2607.18498v1#S5.SS1) supply a comparator T^* with cost O(OPT), depth O(log n), constant-length ribs, and rotations within constant depth of the root. Its existence is proved in Appendix C; these are properties of a comparison tree, not assumptions on the original A or B. The normal-form slowdown is absolute, not logarithmic.

In Section 5.2.1, each external node's rank is its depth in T^*. A heavy edge leads toward the unique minimum-rank external node in its subtree (Lemma 4, Corollary 5). Definition 6 uses rank differences for heap-parent gaps. Definitions 7–8 split a gap into an interval component and a nonnegative point component q, then contract it to

\[
\lceil1+\log_2(1+q)\rceil,
\qquad
G=\max_t\lceil1+\log_2(2+\operatorname{depth}(T_t^*))\rceil
=O(\log\log n).
\tag{11.1}
\]

This is the origin of the parameter G. Depth normalization improves the bound; it does not make G absolute. A binary tree containing arbitrary n keys cannot have uniformly bounded total depth as n grows. More selectively bounded relevant gaps would require a different lemma; neither paired closure nor an A/B root-return identity supplies it.

[Lemmas 12–15](https://arxiv.org/html/2607.18498v1#S5.SS3) handle comparator rotations. The rank changes occupy five ordered segments. Constant-depth border nodes have O(1) heap ancestors, so one comparator rotation causes O(1) heavy-path junctions, O(1) new bends, O(1) paid lazy operations, and O(1) new lazy intervals. Lazy interval gaps absorb uniform shifts of many ranks without changing existing contracted point gaps. **There is no extra logarithmic multiplier per comparator rotation in these lemmas.**

Exact original paired closure restricts endpoint physical trees. It gives no bound on maximum T^* rank, and does not cancel the positive number of lazy operations induced by its rotations. The source comparator does have ordinary A-splay batches, but Theorem 2 does not promise that this batching survives normalization. Any source-specific use of that property needs a proof through the normal-form simulation or an analysis that safely avoids it.

### 11.2 Boundary lifetimes: the first log G

Lemma 21 gives, for an unbroken lazy interval I, at least \((|I|-6)/2\) internal pairings per splay and at least \((|I|-6)/4\) in each of the first/second pairing groups. Lemma 20 allows only the first relevant splay to encounter a broken interval. Definition 9 classifies an unbroken boundary pairing as unimportant when its loser's interval has size at least \(\kappa G\log G\).

[Lemma 22](https://arxiv.org/html/2607.18498v1#S5.SS4) bounds important boundary pairings with a loser in one lazy interval over that interval's lifetime by O(log G). Physically, an interval in the intermediate size range between a constant and \(\kappa G\log G\) can lose a constant fraction of its children in successive passes while still yielding boundary insertions. There are O(log G) such size scales. Broken and constant-size cases contribute only O(1).

Lemma 23 creates O(1) lazy intervals per splay. Lemma 31 gives \(\ell=O(N_*)\) intervals ever created, including O(n) initialization and O(1) per comparator rotation. Lemmas 24 and 32 then give

\[
p\le u+O(\ell\log G+c_*)
\le u+O(N_*\log G).
\tag{11.2}
\]

Original paired closure does not reduce this interval-lifetime scale count. A fresh interval created next period can repeat the same positive boundary workload. Original first-hit constraints exist, but no bound identifies these auxiliary important pairings with bounded-load original A events. A sufficient improvement for this loss alone would replace the aggregate important-boundary contribution by O(N_*), with a global proof across all intervals and copies; a per-interval assertion inferred merely from source closure is unsupported.

### 11.3 Contracted-gap recharge: the G factor

Lemma 10 says internal pairings never increase a loser's contracted point gap, and a good internal pairing decreases it by at least one. In the lazy-operation table, inserts can give a new element up to O(G) contracted gap. Other listed operations do not increase existing contracted point gaps. The proof counts positive recharge, not net endpoint change.

Using (11.2), [Lemma 33](https://arxiv.org/html/2607.18498v1#S5.SS6) gives

\[
h_{\rm good}\le uG+O(N_*G\log G).
\tag{11.3}
\]

Its initial O(nG) gap stock is included in the second term. The recurrent G factor is the possible recharge per insertion multiplied by the number of insertions. Even if a suitable auxiliary state were periodic, equality of its initial and final sum would make total decreases equal total increases, not make either positive total zero. Periodic physical A/B closure does not even assert periodicity of the paper's lazy-interval representation or normalized comparator.

A sufficient improvement for this mechanism would bound the total positive contracted-gap recharge of source-induced insertions by an absolute multiple of original A work plus a one-time population allowance, with actual global multiplicity. The source supplies no proved such bound. Replacing G by a constant because original labels are intervals confuses two different notions of gap.

### 11.4 Pairing interface: the second log G

[Lemma 25](https://arxiv.org/html/2607.18498v1#S5.SS5) states

\[
a=O\bigl((p+n)G\log G+h_{\rm good}\log G\bigr).
\tag{11.4}
\]

This is the precise pairing-heap-related input proved in the paper through its own interface, abstracted from multi-pass/pure pairing-heap analyses. It is not a black-box assertion that all splay steps are heap delete-min operations. The paper's interface allows ordered growing/shrinking blocks, splitting, matching passes, and integer value changes.

Lemma 26 quantifies interface activity \(\mathcal A_{\rm int}=\sum_{\rm Pass}|M|\) by

\[
\mathcal A_{\rm int}
\le \#\mathrm{Insert}\,O(G)
+\#\mathrm{ValueChange}\,O(\log G).
\tag{11.5}
\]

Lemma 27 chooses

\[
\tau=C_{\rm exempt}
+\left\lceil\log_{1/(1-\gamma)}(4G)\right\rceil
=O(\log G),\qquad
\mathcal A_{\rm insig}\le
\frac{\mathcal A_{\rm int}+\#\mathrm{Insert}}{4G}.
\tag{11.6}
\]

The physical/combinatorial reason is repeated constant-fraction shrinking of a block, including split descendants that inherit pass counts. Up to \(\tau\) significant passes can charge the same value-change history. The u/v-shift terms have this O(log G) overlap; w-shifts telescope with an O(G) allowance per insertion. Lemma 28 gives at most p+n interface insertions; Lemma 29 gives O(h_good+pG) value increases; Lemma 30 gives at most that many value decreases plus nG. These statements yield (11.4).

Closure of original physical trees places no proved constant bound on these significant-pass overlaps. Original A steps occur in ordinary splay batches, but the interface tracks comparator-depth-based ranks after normalization, and its synthetic unit changes also include adjustments for good pairings. No argument relates their multiplicity to the original KEEP gaps. A sufficient improvement here would be a sharper interface charging theorem for the actually induced traces, with constant significant-shift overlap or a summed charge avoiding that overlap. A generic constant replacement is not supplied by Lemma 26.

### 11.5 Absorption and the final factor

Substituting (11.3) into (11.4), and then (11.2), produces

\[
a\le \alpha uG\log G+O(N_*G\log^2G)+O(1).
\tag{11.7}
\]

Lemma 34 sets \(\kappa=\max\{16,32\alpha\}\) and proves

\[
\alpha uG\log G\le a/2,\qquad u\le a.
\tag{11.8}
\]

It uses the many internal pairings in every large unbroken interval, with at most four relevant boundary pairings per such interval per splay. This absorption introduces no new multiplicative asymptotic loss. Its \(G\log G\) threshold explains why important-boundary lifetimes in Lemma 22 still have logarithmically many size scales.

Lemma 35 therefore bounds zig-zigs by \(O(N_*G\log^2G)\). The factors are **one G** from contracted-gap/value recharge and **two log G factors in the combined analysis**, through boundary-lifetime accounting and the pairing interface. They are not an extra factor for each heavy edge or each original source double. With (11.1),

\[
G\log^2G=O\bigl(\log\log n(\log\log\log n)^2\bigr).
\tag{11.9}
\]

### 11.6 Zig-zags, zigs, and initialization

Lemma 18 represents each zig-zig by exactly two pairings, and Lemma 19 gives disjoint first-pairing and second-pairing groups within a splay. These are constant-factor correspondences.

Lemma 17 bounds newly created bends in one splay by O(1) plus its zig-zigs, and bounds removed bends below by its zig-zags. Lemma 13 creates O(1) bends per comparator rotation. Thus Lemma 36 bounds all zig-zags by O(n+c_*+#zig-zigs). It inherits the zig-zig loss, with no additional logarithm. Riblessness and the constant ranks of the access's adjacent null nodes in Corollary 3 are needed for this bend argument; they cannot simply be assumed for the unnormalized original A tree.

The completed Theorem 1 proof charges at most one terminal zig and one unit access cost per request. In this transfer there are mK_B such requests, with K_B<=A. Those are recurrent costs, already controlled. Initial lazy intervals, initial contracted-gap stock, and initial bends give population terms such as O(n), O(nG); they are precisely one-time allowances. Our repeated-source limit removes the resulting additive initialization contribution. Normal-form slowdown remains an absolute constant. None of these observations removes recurrent insertions, important boundary pairings, or significant-pass overlaps.

This identifies the losses without claiming that any one is a lower bound for splay, URCD, or these sources. They are losses of the published analysis as audited.

## 12. Stronger-source-lemma opportunities

The original source provides three additional facts worth distinguishing from proved improvements: the comparator's rotations are batches of ordinary A splays; the complete physical A/B trajectory is periodic; and its active request count has a load-one association to original A StepEv. These prove the transfer. No audited lemma converts them into constant auxiliary rank range, total recharge, or significant-pass overlap after normal-form conversion.

The following are precise **unproved proof obligations**, not additional results or permission to execute another research stage.

| Mechanism | Sufficient stronger lemma and exact remaining source issue |
| --- | --- |
| Important boundary lifetimes | For a specified valid auxiliary representation induced from the A comparator, bound the total important-boundary insertions by c(mA+n), c absolute. One must associate their full interval lifetimes to actual original source work with bounded total load. The generic bound is O((mA+n)log G), and original cohort nesting alone does not identify these intervals. |
| Positive contracted-gap recharge | Bound initial stock plus positive recharge at all induced lazy insertions by c(mA+n), or by c times that quantity plus a controlled unimportant-pairing term. Net zero over a period is insufficient. Each recharge needs a source-derived cause and an all-cohort/all-period overlap proof. |
| Pairing-interface shift overlap | Prove a constant-loss replacement of (11.4) on the induced traces, using an actual restriction on block join times, splits, significant passes, or synthetic value changes. A proof must survive the normal-form simulation. Ordinary A splay batching before that simulation is not the missing theorem. |
| Relevant rank range | A bound on maximum full-tree depth by an absolute constant cannot hold for arbitrary n. A possible useful statement would instead bound the summed charge for large relevant gaps using original A work. This requires a genuine source-to-heavy-path dictionary; no identification with the original output-size rank is justified. |
| Physical key reduction | Supply the S-key A-comparator theorem in Section 8, including private DELETE targets. B hanger invariance alone proves only one side of this proposed improvement. |

A modular sufficiency calculation exposes how strong a constant-factor route would have to be. Put \(M=mA(W)+n+1\). For a specified normal-form/interval construction, suppose source-derived proofs supplied absolute c_p,c_h,c_a>=1 such that

\[
p\le u+c_pM,\qquad
h_{\rm good}\le c_h(u+M),\qquad
a\le c_a(p+h_{\rm good}+n).
\tag{12.1}
\]

The three clauses respectively improve boundary aggregate cost, recharge, and the pairing interface. The original large-interval counting can make

\[
u\le\frac{a}{2c_a(1+c_h)}
\tag{12.2}
\]

by choosing the absolute threshold multiplier kappa sufficiently large: its slot count gives \(a\ge\kappa G\log G\,u/16\), with G>=2. Then (12.1) implies

\[
a\le a/2+c_a(c_p+c_h+1)M,
\quad a\le2c_a(c_p+c_h+1)M.
\tag{12.3}
\]

Important boundary pairings are part of the paid insertion inventory, so p and u would then also be O(M). Lemmas 18, 17, and 13 would bound zig-zigs and zig-zags by O(M); repetition would give an absolute source coefficient. This is a sufficiency calculation only. **None of the three strengthened clauses in (12.1) has been proved for all original sources.** Removing just one published factor would not establish all of them or an absolute coefficient.

The adversarial sources rule out simplistic substitutes. H has arbitrarily long first-hit chains and unbounded sharing of one original A hit. I^r Z reuses persistent physical content across genuinely new nonleaf births. H_(6,1) refutes monotonic decrease of the original chosen-output size. G separates irregular consumption from a later full reset. These facts constrain a proposed dictionary or selector; they are not counterexamples to any specific heavy-path/interface lemma until that dictionary is defined.

Accordingly the external theorem is a rigorous bypass of the regeneration ledger **for the size-dependent ceiling**. The audited proof supplies no established source-specific constant-factor bypass of G0–D5. Promoting the unproved clauses above would reintroduce substantial quantitative work, and is not net advancement toward an absolute URCD theorem.

## 13. Mathematical dependency ledger

| Claim | Exact dependencies | Status in this report |
| --- | --- | --- |
| B active extraction, (4.2) | Ordinary deterministic splay; DELETE and root-request B identities | Proved universally, same-agent symbolic |
| Full A comparator, (5.2) | Paid arbitrary root-BST rotations; freely selected comparator initial tree; real vine conversion | Proved universally, with one terminal J(n) |
| K_B<=A | All original cyclic KEEP gaps, A root transitions, complete paired closure | Reproved at G0's exact definition |
| R_A=2A-V_A | Original StepEv and real/virtual convention | Reconstructed from depths |
| D_B=P_A-N_A=B_1+2B_2+Z_1 | Original physical S/SET signs and full closure | Retained exactly; not used as a cost-model shortcut |
| Period scaling and limit | Complete labelled A and B return, fixed X, one whole-sequence application | Proved; no per-period additive term removed |
| External factor | Chmel et al. v1, Theorem 1, audited model and completed Section 5.6 proof | External mathematical dependency, not independently certified here |
| Q_B benchmark | Previous bridge plus R_B=2Q_B+Z_B | Proved for all original W, C=3C_0/2 |
| R_irr ceiling | Q_B benchmark plus unchanged D5 subset/cardinality chain | Proved relative to the inherited residual definitions and their verification scope |
| Carrier-size substitution | B invariance proved; S-key A comparator missing | Not established |
| Constant coefficient | Source-uniform improvements to recurrent rank/interval/interface charges missing | Open; no claimed improvement |
| Cycle-to-prefix / DO | Original reduction requires an absolute coefficient over all sizes | Audited for scope; no downstream conclusion executed |

The proof graph has no use of URCD, Dynamic Optimality, bounded regeneration congestion, the D5 scan theorem, a new matching premise, or the target size-dependent bound itself to establish its comparator. The near-optimality theorem is the sole external theorem needed for the benchmark. Its normal-form and pairing arguments are inspected dependencies, not separately claimed new certificates.

Current input provenance follows. Paths in this table are relative to the repository root named below. The mathematical source citations in the preceding sections identify their exact section numbers; hashes identify bytes, not proof correctness.

| Read-only current input | SHA-256 |
| --- | --- |
| DO_RESEARCH_REBOOT/RESEARCH_RULES.md | c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc |
| DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md | f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa |
| DO_RESEARCH_REBOOT/RG04_GLOBAL_REGENERATION.md | 52072e0c9a5214cf16b7bf44e3efb09df102e91e939bf3186b2e280b0763832b |
| DO_RESEARCH_REBOOT/IAGS12_G0_QUANTITATIVE_BASELINE.md | 09863af3277745f5ebef956e680feb43a3d1ad4e5c7bb57bb545918c4813523a |
| DO_RESEARCH_REBOOT/IAGS12_D1_COLLISION_PROVENANCE.md | 0aa9cbf3e9cc036af5d4bbdf3ea3acdfcbef9341c856401b74247a615c4f814f |
| DO_RESEARCH_REBOOT/IAGS12_D2_RESIDUAL_REGENERATION_COST.md | 4b1623da997a7c1dbd40073809d198cfd8c850b48edc1db6b42b5655b1808b0e |
| DO_RESEARCH_REBOOT/IAGS12_D3_BLIND_GAP_COMPOSITION.md | 303f270f78d777932040e0e4f9ddd46cdd74f1835bdeaf1ad50f286bba1f02bc |
| DO_RESEARCH_REBOOT/IAGS12_D4_NEUTRAL_RENEWAL.md | f6d0d7d256064a5b456b13befe3d87c042f4b3105c3cf6604ab496139b9d34c2 |
| DO_RESEARCH_REBOOT/IAGS12_D5_BRANCH_RENEWAL_COST.md | 4a3cb7a156618489bf6d51ca51662f49b3fc8297b8fd99ad9086a0f6dc09c905 |
| DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md | 8be55471edfdac31f59d552952c84f8d380bbfa3a7e46b7643d22af766757fd5 |
| DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md | a52487cfe212aa562b91406bb6006d2f9a9469bebcfd4e039d9cd224fc6d677b |
| DO_RESEARCH_REBOOT/ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md | f85354f04eed727e3bdc4c0ddca72c1a6f706885c35721ced525ee52fa26e712 |
| DO_RESEARCH_REBOOT/PARALLEL_ROUTE02_STEP04_LINEAR_INCIDENCE_20261108/STEP04_LINEAR_INCIDENCE_SOURCE_GEOMETRY.md | 77702f3cb914d36a62adb5ba7511c141d92068b52680138997aefc845349e11a |
| DO_RESEARCH_REBOOT/02_PROVED/PIVOT2_CONDITIONAL_REDUCTION.md | bf49cb509c811cc97721fa0c206e146da6a36528a5c6e982498f31be574bd5d3 |
| v03/history/external/papers/L6_chmel_et_al_2026_2607.18498.pdf | 60b3213d9380f9c2d4da2549133d0222960ded8a0956aa10429c569148e7c5e7 |

Repository: C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2. Initial branch coarse-double-branch, HEAD 6d532b2c795c0778f57d8023b23b5fedfc48b010. Preexisting untracked reports and directories are not changes of this task. D6 was not read as a mathematical source. Its initial read-only preservation pin was 57e50e7be5682d1d5a54ae39af8860c8924f8479afdccf9fda4533e585bbdfea; the later check observed 18875b952b9372e5a26423e688b1c12de9828cd6d0758d681fc6d6c0f2939b8f. Other workspace activity also added IAGS12_PARALLEL_B_BOUNDARY_SURCHARGE.md during this task. Neither external change was incorporated, edited, or reverted. In particular, an unchanged-D6 claim would be incorrect; this task itself issued no D6 write.

The primary online version was verified as arXiv v1 of July 20, 2026. The existing PDF was used for statement cross-checks, without asserting a newly downloaded byte identity. Direct primary links: [Theorem 1](https://arxiv.org/html/2607.18498v1#Thmtheorem1), [completed proof](https://arxiv.org/html/2607.18498v1#S5.SS6), [Appendix B](https://arxiv.org/html/2607.18498v1#A2), [normal-form proof](https://arxiv.org/html/2607.18498v1#A3.SS4).

## 14. Verification level and final verdict

Verification consists of same-agent symbolic review and static manuscript/source preservation checks. The principal checks are: B state-by-state extraction; original cyclic A-StepEv injectivity; physical conversion length; full chronological tail simulation; endpoint target legality; one comparator across repetitions; separation of real rotations, StepEv, doubles and per-access charges; fixed-n order of limits; zero and small cases; and the exact source cost/factor algebra. The primary theorem's model and the numbered loss statements were read directly rather than inferred from its abstract.

Only this new Markdown report is written by this task. This task does not modify any original source, D6 file, historical proof, event ID, owner map, test, code, resource cap, branch, commit, or Git history. No new source-engine query, semantic replay, enumeration, solver, experiment, dependency installation, formal-kernel run, or subagent is performed. Notion guide/skill discovery was read-only; this explicitly requested repository artifact is recoverable from the repository and is not duplicated into Notion.

The full report was read back. All 15 SHA-256 input pins in Section 13 matched their actual bytes after the write; the tracked Git diff remained empty and branch/HEAD remained unchanged. All 14 required numbered sections are present and display-math delimiters balance. Two manuscript issues found on readback were corrected in this report alone: a KEEP-gap sentence now states that no other KEEP lies between consecutive KEEP occurrences, and a table row avoids an unescaped vertical bar. The concurrent excluded-file changes described above are preserved and are not claimed as this task's edits or mathematical inputs.

**BENCHMARK PROVED.** The exact new bridge is (5.2), (6.1), (7.3)–(7.4), and (8.1)–(8.2). It gives an all-source size-dependent upper bound with C_1=3, I(X)=2max(|X|-1,0), and C=3C_0/2, conditional only on the stated established external Theorem 1 and the original source definitions. Its R_irr interpretation retains the inherited D5 definition/verification qualification.

**No SUBSTANTIVE IMPROVEMENT verdict:** no source-uniform logarithmic-factor improvement, |S| theorem, absolute URCD coefficient, or Dynamic Optimality theorem is proved. The nonconstant losses are recurrent auxiliary charges isolated in Section 11, not initialization errors that periodic closure removes.

BEFORE: the proposed active-access root-BST transfer and its final tail required an explicit proof. RESULT: the legal complete-trajectory comparator, exact source-cost translation, periodic cancellation, and original residual ceiling are established. AFTER: the universal constant-factor problem remains open; Section 12 identifies unproved stronger source lemmas without assuming them or commencing their investigation. NET ADVANCEMENT: the requested rigorous quantitative benchmark and loss diagnosis, with all original period costs preserved.

**STOP — Route A only.** D6, P1, V1, P2, RG-05, and all other stages are unexecuted.
