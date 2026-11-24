# IAGS 1.2 — G0 quantitative baseline

Date: 2026-11-09, Asia/Karachi.

## Authorized scope — BEFORE

This prompt executes G0 ONLY, the first gate of the user's IAGS 1.2 protocol. D1, D2, D3, P1, V1 and P2 are not executed. No RG-05 is executed.

The immutable target is

\[
\exists K<\infty\quad\forall W\in\mathcal W_{\rm adm}:
U_{\rm int}(W)\le K A(W).
\]

Keep the inherited relation \(U_{\rm int}\le Q_B\le6A+U_{\rm int}\) at its existing verification qualifications. This gate neither reproves that reduction nor derives an unrestricted bound.

The exact G0 obligation is to construct source-defined first-hit cohorts and prove
\(U_{\rm int}=H+E\), \(H\le K_B\le A\), and the equivalence of a universal excess bound with the original interior-demand bound. This is explicitly an accounting reduction. Replacing the missing bound by an equivalent excess bound is not recorded as new quantitative proof advancement.

The concrete mechanism is RG-04 Section 3.2's chosen physical output and first inside KEEP, followed by RG-01 Section 6.3's disjoint cyclic A-gap witnesses. RG-04's overall BLOCKED verdict is preserved: its proved output/first-hit statements are imported, not its unresolved global work assignment.

All source and prior research files remain read-only. Only this new report is written under DO_RESEARCH_REBOOT. Allowed work here is static source reading, symbolic proof and manuscript verification. No source query, semantic replay, experiment, enumeration, solver, potential, external search, resource-cap change, historical payment change or subagent is used.

## 1. Frozen definitions and proven inputs

Let W be ANY finite original admissible exactly paired-closed source on its complete physical labelled key population X. Every request is to a present key. A performs ordinary bottom-up splay on KEEP and DELETE; B performs it on KEEP only. DELETE removes no key. The complete A and B trees each return to their original labelled states; their states at the chosen cyclic cut need not equal one another. A legal reaching prefix is excluded from W's costs.

Keep the original carrier S and SET-label convention \(J_S\), arbitrary private A ancestors, full physical B hangers, all actual helpers, real rotation IDs and virtual zig companions. In particular, the original carrier facts give M subset S, S ancestor-closed in B, and every KEEP path operand in S. No projection into a smaller physical tree is performed.

Write \(\mathcal U_{\rm int}(W)\) for the COMPLETE inherited class of original B doubles d which:

* have both original B SET changes equal to zero;
* have original proper whole-grandparent frame \(F_d\) excluding both carrier extremes;
* have \(F_d\) absent in A at every actual snapshot of the original full window \(\Pi_d=(\kappa_d,t_d^A]\).

Its cardinality is \(U_{\rm int}(W)\). If S is empty or there is no possible B double, the class is empty. It is not restricted by owner vacancy, producer silence, creator type, retirement side or prior payment. Whole-frame membership continues to use \(F_d\), not the selected output label below.

For an original KEEP t, put
\(k_t=\mathbf1[\text{B's splay at t is nontrivial}]\), and
\(K_B=\sum_t k_t\).
The exact A cost is the number of nonzero original A StepEv:
\(A(W)=\sum_t\lceil\operatorname{depth}_A(x_t)/2\rceil\).
A double StepEv costs one despite having two real rotations. A terminal zig costs one and has only one real rotation, bit 0. A virtual companion is not an event available to the accounting.

The imported results are:

| Proven input | Exact scope used here |
| --- | --- |
| RG-01 Sections 5.1-5.3 | Original costs, real IDs, k_t and complete history-dependent U_int |
| RG-04 Sections 2.1a and 3.2 | Literal chosen output for every neutral double, outside-access rigidity and first-hit necessity |
| RG-01 Section 6.3 | One real A StepEv in each nontrivial cyclic KEEP gap, with distinct StepEv across gaps |
| Regeneration continuation Section 1 | Inherited \(U_{\rm int}\le Q_B\le6A+U_{\rm int}\), unchanged qualification |

The first-hit and cyclic gap arguments are given explicitly below so that G0's own dependency and counting audit can be read without assuming a global RG-04 certificate.

## 2. Define h(d) using the actual chosen output

### 2.1 One deterministic output for every demand

Take \(d=(t,j)\in\mathcal U_{\rm int}(W)\) and its original pre-double path \(g\to p\to x_t\). Define the output birth bit

\[
\nu_d=
\begin{cases}
B(t,j,0),&d\text{ is RR or LL},\\
B(t,j,1),&d\text{ is LR or RL}.
\end{cases}
\tag{2.1}
\]

Let \(O_d\) be the COMPLETE physical subtree rooted at the old grandparent g just after that bit, and put \(J_d=V(O_d)\cap S\), where V(O_d) is its complete physical key set. This is its actual S-descendant label.

These are exactly RG-04's chosen outputs: first SS output for RR/LL and second output for LR/RL. In each literal formula g is demoted, and its new subtree excludes the actual producer target \(x_t\). The S label \(J_d\) is nonempty because it contains g, and proper because it excludes \(x_t\in S\). Its relevant producing bit is neutral. All its physical hangers and internal edges remain part of \(O_d\).

For SS, the second bit preserves this whole rooted output. All remaining steps of the producer access have the same target \(x_t\notin J_d\), so they preserve it as well. Later accesses with KEEP targets outside \(J_d\) preserve the full rooted subtree, although they may transport its incoming edge. DELETEs leave B unchanged.

This output is different from the whole frame \(F_d\) and its historical creator \(\Gamma_d\). Its original identifier is \((\nu_d,g,O_d,J_d)\); neither \(\Gamma_d\) nor an incoming-edge reattachment is substituted for its birth.

### 2.2 Existence and uniqueness of the cyclic first hit

Define \(h(d)\) to be the FIRST subsequent original KEEP occurrence, in cyclic causal order after \(\nu_d\), whose target belongs to \(J_d\).

It exists. Otherwise outside-access rigidity would preserve the complete rooted output at g around an entire period. But immediately before \(\nu_d\), g's subtree contains the producer target \(x_t\); immediately after it, \(O_d\) excludes that target. Exact complete B closure returns the tree at this same pre-birth phase to the same physical state. Persistence of \(O_d\) all the way to that phase would contradict that change at g. Thus a KEEP inside \(J_d\) must occur before the birth phase is reached again.

The finite original cyclic order makes the FIRST such occurrence unique. The current producer cannot be that hit, because its target lies outside \(J_d\). A causal wrap selects an existing original operation ID in W, not a new copy or a prefix operation.

Every KEEP target lies in S, so testing membership in \(J_d\) tests whether that actual physical target is in \(O_d\). No unvisited physical hanger is discarded from the subtree.

Immediately before the B phase at \(h(d)\), \(O_d\) is still intact and proper. The immediately preceding KEEP target is outside \(J_d\): between its birth and its first hit all KEEP targets are outside, and the producer itself is outside. Hence B's current root is outside \(J_d\), whereas the new target is inside. Therefore

\[
k_{h(d)}=1.
\tag{2.2}
\]

The proper label \(J_d\) is removed by the end of this first inside splay. G0 needs the unique first-hit occurrence, not a guessed primitive retirement bit inside it.

### 2.3 Scope of the output history

The history from \(\nu_d\) to the start of the B phase at \(h(d)\) follows one original rooted output through outside accesses and possible incoming-edge transfers. An exact physical edge run may end earlier at a reattachment; that does not terminate or recreate the output.

Different births, roots, labels or output histories are NOT presumed to have different first hits. Different demands may share structure or have nested outputs; repeated uses of a key retain their different original operation IDs. G0 imposes no collision classification or cost beyond one occupied first-hit cohort.

## 3. Cohorts, unique counting and the exact identity

Index by original KEEP OCCURRENCES, not by target key. For each such h define

\[
\mathcal C_h=\{d\in\mathcal U_{\rm int}(W):h(d)=h\}.
\tag{3.1}
\]

Because h(d) is a total single-valued source-defined function, these sets form a disjoint partition of the complete original demand class. A demand is counted exactly once even when its output history wraps around the cyclic seam.

Let
\(\mathcal H(W)=\{h:\mathcal C_h\ne\varnothing\}\), and define

\[
H(W)=|\mathcal H(W)|,\qquad
E(W)=\sum_{h\in\mathcal H(W)}(|\mathcal C_h|-1).
\tag{3.2}
\]

Empty sums are zero. Every summand is a nonnegative integer. Then

\[
\begin{aligned}
U_{\rm int}(W)
&=\sum_{h\in\mathcal H(W)}|\mathcal C_h|\\
&=\sum_{h\in\mathcal H(W)}[1+(|\mathcal C_h|-1)]\\
&=H(W)+E(W).
\end{aligned}
\tag{3.3}
\]

No arbitrary representative needs to be selected from a cohort to obtain this identity. E is a collision count, not a new inventory of physical resources or an A-work payment.

## 4. One actual cyclic A-gap witness per occupied cohort

### 4.1 From occupied cohorts to nontrivial B accesses

Equation (2.2) proves \(\mathcal H(W)\subseteq\{h:k_h=1\}\). Distinct cohort indices are distinct original KEEP occurrences. Thus

\[
H(W)\le K_B(W).
\tag{4.1}
\]

This uses ALL occupied cohorts. It does not count a B access once per demand.

### 4.2 Exact A cost and global multiplicity one

For every nontrivial original B KEEP h, let \(h^-\) be its immediately preceding KEEP in the complete cyclic word, including any identity KEEP. Let y be that preceding target and x the current target.

B ended \(h^-\) rooted at y and freezes on all intervening DELETEs. Nontriviality at h therefore gives \(x\ne y\). A is rooted at y after the A phase of \(h^-\) and at x after the A phase of h.

Consider the actual A events AFTER the post-A boundary of \(h^-\) through the post-A boundary of h. They include every intervening DELETE/helper and the A phase at h. This gap has a nonzero A StepEv because its root changes from y to x.

Let \(F(h)\) be the FIRST such nonzero original A StepEv in that gap. Its bit-0 rotation \(r(h)\) is real, even if the StepEv is a terminal zig. Each \(F(h)\) contributes exactly one to A(W).

Consecutive cyclic KEEP gaps partition the ORIGINAL A StepEv occurrences. Therefore \(h\mapsto F(h)\) is injective on nontrivial B KEEPs, and in particular on occupied cohorts. No physical StepEv or its real bit 0 is counted twice. This proves

\[
\boxed{H(W)\le K_B(W)\le A(W).}
\tag{4.2}
\]

The coefficient is ONE in the original StepEv cost. It is not obtained by treating the two real bits of a double as two cost-one A units.

### 4.3 Seam, zero operations and private helpers

A gap may cross the period boundary. Exact paired closure makes its A and B history consistent across that seam; original IDs on both sides are included once. No new resource is issued at the cut and no reaching-prefix work is used.

A current KEEP can have zero A cost although B is nontrivial. Its witness can lie in an earlier DELETE/helper in the SAME KEEP gap. A root-repeat KEEP remains in the cyclic list even when it contributes no B rotations.

Private promoted A keys, arbitrary A ancestry and full B hangers do not change the root-gap argument. An actual helper StepEv is retained rather than replaced by a projected event. Terminal zigs use only their real bit; B terminal zigs count as nontrivial accesses but not as neutral double demands.

If there is no KEEP, U_int=H=E=K_B=0. If there is exactly one KEEP occurrence, paired B closure makes it a root repeat, so again there is no first-hit cohort. If \(A(W)=0\), (4.2) gives \(K_B=0\); the total first-hit map then forces \(\mathcal U_{\rm int}=\varnothing\), so H=E=U_int=0. Empty words, zero-event periods and carriers too small for a double cause no exceptions.

## 5. Baseline theorem and uniform coefficient equivalence

For EVERY original admissible paired-closed W, (3.3), nonnegativity and (4.2) give

\[
\boxed{
U_{\rm int}=H+E,\qquad
H\le K_B\le A,\qquad
E\le U_{\rm int}\le A+E.
}
\tag{5.1}
\]

The universal quantifiers and constants are exact:

* If some absolute finite \(K_U\ge0\) satisfies \(U_{\rm int}(W)\le K_U A(W)\) for ALL admissible W, then \(E(W)\le K_U A(W)\) for ALL such W.
* If some absolute finite \(K_E\ge0\) satisfies \(E(W)\le K_E A(W)\) for ALL admissible W, then \(U_{\rm int}(W)\le(1+K_E)A(W)\) for ALL such W.

Thus

\[
\boxed{
[\exists K_U<\infty\ \forall W:\ U_{\rm int}\le K_U A]
\ \Longleftrightarrow\
[\exists K_E<\infty\ \forall W:\ E\le K_E A].
}
\tag{5.2}
\]

The conversion from an excess coefficient to an interior-demand coefficient adds at most ONE. All constants are independent of physical population, source length, cohort size, genealogy depth and helper count. The zero-cost case was proved before any ratio is formed.

For \(A(W)>0\), an equivalent diagnostic statement is

\[
0\le\frac{U_{\rm int}(W)}{A(W)}
      -\frac{E(W)}{A(W)}
=\frac{H(W)}{A(W)}\le1.
\tag{5.3}
\]

Consequently a genuine admissible family has unbounded U_int/A if and only if its E/A is unbounded. No such family or finite universal coefficient is constructed here.

## 6. Proof-relevance audit and surviving debt

The explicit part discharged is one occupied-cohort count H, with a globally injective map into actual cost-one A StepEv. The collision excess E contains all additional demand multiplicity sharing those first-hit cohorts.

The same A witness \(F(h)\) is NOT credited once per member of \(\mathcal C_h\). Its demonstrated load is one per COHORT. Treating it as one fresh unit per demand would reinstate RG-04's refuted shared-first-hit rule.

The remaining quantitative assertion is precisely

\[
\exists K_E<\infty\quad\forall W\in\mathcal W_{\rm adm}:
E(W)\le K_E A(W).
\tag{6.1}
\]

It is equivalent to the original unresolved bound. E is not declared a smaller solved class, a funded resource, a new potential or independent progress on that bound. No collision mechanism is classified, and no D1 quantitative interface or D2 theorem is invented in this gate.

The inherited relation \(U_{\rm int}\le Q_B\le6A+U_{\rm int}\) remains unchanged. It supplies no upper bound on E without the missing uniform source-work theorem. Later P1/V1/P2 calculations and downstream Dynamic Optimality certification are not performed.

| Required proof-debt field | G0 record |
| --- | --- |
| Proven inputs | Exact source/cost/U definitions; RG-04's chosen physical output and first hit; RG-01's cyclic gap witness; inherited scalar relation with original qualifications |
| New theorem | For every admissible W, (5.1) and the coefficient equivalence (5.2), with the actual total map h(d) and disjoint cohort partition |
| Quantitative effect | H<=K_B<=A with per-A-StepEv load ONE; E<=U_int<=A+E; coefficient conversion K_E to 1+K_E |
| Surviving residual | All collision excess E; no universal K_E is established |
| Global overlap | PROVED for one witness per occupied cohort; no bound on per-demand reuse within/across output histories is asserted |
| Source counterexample | None needed for these universal baseline identities; prior exact failures remain intact and are not recast as refutations of URCD |
| Dependency status | G0's total first-hit map, unique counting, cyclic A-gap count and coefficient equivalence discharged; D1 and all later obligations unexecuted |
| Verification level | Same-agent symbolic source proof and manuscript checks; not independent or formal certification |
| Main theorem effect | Accounting reduction/diagnostic only; the missing universal linear bound remains OPEN |

PRG checks at G0's stated scope: mathematical identities are source-derived; the numerical bound on H has an actual independent A-cost interface; global multiplicity and the cyclic seam are proved; the dependency chain is acyclic; arbitrary collisions remain allowed; the constants 1 are absolute. These facts certify the baseline, not a discovery sufficient for D2. No adversarial family is excluded to obtain them.

## 7. RESULT, AFTER and stop

**G0: PASS — universal baseline at the same-agent symbolic verification level.**

Every original demand belongs to one source-defined cohort, every occupied cohort's first hit is nontrivial, and distinct cohort witnesses use distinct original A StepEv over the complete cyclic source. The required identities and universal coefficient equivalence are proved.

AFTER: the baseline construction and its noncollision obligations are closed. The original quantitative theorem remains open through (6.1). Net effect is the protocol's explicitly requested accounting reduction; no new bound on E has been proved.

The next gate named by the protocol is D1, source-derived collision discovery, whose proof advancement would require its own quantitative interface. G0 PASS does not authorize executing it in this prompt. Stop here.

## 8. Sources, preservation and verification

The exact frozen inputs, including the current user's protocol, are linked below. Every SHA-256 matched a static post-write recheck.

| Read-only input | SHA-256 |
| --- | --- |
| [RESEARCH_RULES.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RESEARCH_RULES.md>) | `c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc` |
| [RG01_PRIMITIVE_ACCOUNTING.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md>) | `f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa` |
| [RG04_GLOBAL_REGENERATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG04_GLOBAL_REGENERATION.md>) | `52072e0c9a5214cf16b7bf44e3efb09df102e91e939bf3186b2e280b0763832b` |
| [UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md>) | `50e90e4471b1f794ba58f848f44522dc71ac74685ed9f81e09593cfb11e871d0` |
| [Pasted text.txt](<C:/Users/Saif malik/.codex/attachments/11bb4ee0-2d66-4b2a-8d16-4b24c42c8eb8/Pasted text.txt>) | `8388f5175c28f516303b3a768df27e271ef937ac7564f201cea6c79e0770677d` |

Verification consisted of symbolic review of the four output choices, first-hit existence/nontriviality, cyclic StepEv injectivity, empty/zero-cost cases and the coefficient implications, followed by exact manuscript read-back modulo whitespace. There was no source execution, finite sample proof, solver or independent-agent audit.

The read-back matched the constructed manuscript. Tracked Git diff remained empty; the preexisting untracked entries remained in place, with only this new G0 report added. HEAD remains 6d532b2c795c0778f57d8023b23b5fedfc48b010. Original source periods, physical IDs, owner maps, caps and previous artifacts are unchanged.

Final gate verdict: G0 PASS, same-agent symbolic. The universal E/A bound and URCD remain unproved. D1 and all later gates are unexecuted.
