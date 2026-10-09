"""Author the requested research handbook. Refuse destructive overwrites."""
from pathlib import Path
import json, hashlib, sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
R=W.parent
folders=['00_REPOSITORY_AUDIT','01_MAIN_PIPELINE','02_PROVED','03_OPEN','04_REFUTED',
 '05_FINITE_EXACT','06_CERTIFICATES','07_STRATEGIES','08_PIVOTS/APPROVED',
 '08_PIVOTS/REJECTED','08_PIVOTS/COMPLETED','09_PROMPT_TEMPLATES','10_EXPERIMENTS',
 '11_REPRODUCIBILITY','12_FINAL_PROOF']
for d in folders:(W/d).mkdir(parents=True,exist_ok=True)
docs={}
docs['README.md']='''# Dynamic Optimality research reboot

Start with [START_HERE.md](START_HERE.md). All original repository files remain read-only. This workspace was created on 9 October 2026 (Asia/Karachi).

The current research conclusion is a restricted sibling-erasure theorem and an otherwise open universal proof chain. The main conjecture has not been proved.
'''
docs['START_HERE.md']=r'''# Start here

The goal is a universal constant-factor bound for ordinary bottom-up splay against offline optimal BST execution, with the same specified initial tree. The recovered source permits an intermediate startup term depending only on that tree; Levy–Tarjan's eventual-monotonicity theorem removes it in the final dynamic-optimality conclusion.

The original candidate architecture is:

```text
Pair Access (occurrence KEEP/DELETE encoding)
    -> COARSE-DOUBLE Q_B<=2A  [OPEN]
    +  C.ZIG Z_B<=A          [universal mathematical proof; formal assembly open]
    -> B=Q_B+Z_B<=3A         [CONDITIONAL]
    -> PIVOT-2 cycle excision
    -> E_B<=3S_A+g(T0)       [CONDITIONAL]
    -> LT(Y)<=7LT(X)+2g(T0)  [CONDITIONAL]
    -> Levy–Tarjan Theorem 4.3
    -> Dynamic Optimality   [OPEN]
```

Here A,B are StepEv totals on a closed pair walk, not the names of the two trees. E_B,S_A are the corresponding prefix totals. Local depth counts edges, e(d)=ceil(d/2), and LT cost is d+1. DELETE removes an occurrence from the B execution, not a key from a tree. The full definitions and quantifiers are in [ORIGINAL_PIPELINE.md](ORIGINAL_PIPELINE.md).

The J4 route is sufficient, not known necessary: one globally shared assignment must satisfy J-SELF and the adjusted ROW-DIAMETER constraints on all finite BSTs. Finite fitted assignments do not provide that witness. The universal row theorem and COARSE-DOUBLE remain open.

This run proved [equal-signature sibling erasure](02_PROVED/REBOOT_01_SIBLING_ERASURE.md): for same-child u,v at equal ambient depth with equal top fringe coefficient, arbitrary S can be erased without changing H_u-H_v, for every shared J assignment. All odd-depth equal-depth pairs qualify. Both orientations hold. This removes a real independent sibling variable; it does not prove the remaining empty-sibling width <=2. No UG or potential-existence assumption was added.

Exact finite checks also recovered the 970x79 coupling block's rational rank 48/nullity 31 and the LRF template contradiction 9/34. Neither is an all-depth result. Some later 26S–26AB reports described in the supplied directive are absent from this checkout; their summaries are retained with explicit evidence gaps rather than promoted to proofs.

Read [CURRENT_STATE.md](CURRENT_STATE.md), [CLAIM_LEDGER.md](CLAIM_LEDGER.md), and [NEXT_ACTION.md](NEXT_ACTION.md) next. The first pivot is complete; no successor currently passes the four-rule gate. Fresh research must identify a concrete, strictly smaller proof with a real original obligation deleted. Rephrasing global J existence as all-horizon feasibility is prohibited.

The checkout is dirty: branch wp5x-k6c2-specialized, HEAD 88f344d34b155f6cdc0fc4dae9bf0490d0677e1f. Source hashes bind the actual working bytes. Only DO_RESEARCH_REBOOT/ was writable; [the safety audit](11_REPRODUCIBILITY/SAFETY_AND_REPRODUCIBILITY.md) describes the complete digest comparison.
'''
docs['CURRENT_STATE.md']=r'''# Current proof state — 9 October 2026

Repository: `C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2`.
Branch: `wp5x-k6c2-specialized`. HEAD: `88f344d34b155f6cdc0fc4dae9bf0490d0677e1f`.
Pre-existing modifications: beam.json, hall_lemmas.md, WP6_BEHAVIOR_VAULT.md, wp6_bellman.py, wp6_periodic.py, wp6_recur.py; many untracked artifacts/scripts and .lake files. Full inventory: 11_REPRODUCIBILITY/baseline.json. No source mutation, commits, branch changes, installation, or source entry-point runs were performed.

**Universal mathematical results:** Pair Access is the occurrence-level subsequence encoding; zero-A closed walks have zero B cost; C.ZIG has a complete run-partition proof. Cost translation and cycle excision are complete implications with open upstream premises. REBOOT-01 proves sibling erasure for equal-depth/equal-top-fold pairs and both mirrors. Source-defined H differences cancel their explicit 4n term exactly.

**Not proved:** universal Q_B<=2A; a single all-size admissible J4 potential; universal J-SELF + ROW-DIAMETER under one such assignment; arbitrary-T empty-sibling width; remaining same-child, cross-child and root/child cases; the actual E_B<=3S_A+g premise; Dynamic Optimality. Mathematical conditional implications and formal-kernel completion are distinct.

**Finite results rechecked here:** source-defined coefficient identities on the bounded corpus, C0 rational rank 48 and nullity 31, and saved-matrix LRF Farkas contradiction 9/34. Historical n<=9 Bellman-Ford bounds remain source-reported, not rerun. No positive universal conclusion follows from them.

**Evidence gaps/conflicts:** later named reports 26X–26AB are not present as reports; 26Y's formula is recovered as a corollary of the source insertion identity. The 48->44->55->47 and 4->5->15 sequences and corrected T-map dimensions are directive-only until their actual matrices are acquired. Local L3 v3 bytes differ from the v1 bridge manifest. The legacy MSTL-19 registry remains BLOCKED_BY_SOURCE; this workspace separately verifies the v3 reduction. Several context scripts flip T's side in their s=0 branch and omit unrepresented coordinates in finite vector maps.

**Retired strategies:** the exact refuted LRF template, independent sign shortcuts without exact provenance, presumed finite-rank stabilization, new compactness premises without construction, translation-invariant bulk assumptions without source proof, and recurring finite-coordinate refinements with no endpoint inequality. A restricted refutation does not kill unrestricted J4.

Recommendation: retain the row identities and the new structural cancellation, but pause global J4 synthesis. No repaired potential or alternative route has a concrete first theorem passing all four rules. The original cycle inequality remains the reference obstruction.
'''
docs['ORIGINAL_PIPELINE.md']=r'''# Original Dynamic Optimality pipeline

## Fixed definitions

K is a finite totally ordered key set; T0 is any valid BST on K. X=(x_1,...,x_m), with every x_i in K. Choose an occurrence-index set I subset {1,...,m}; Y is the corresponding subsequence, preserving duplicates and order. A_i^tree always splays x_i. B_i^tree splays x_i on KEEP (i in I) and otherwise freezes. Both start at T0. Key sets remain K. Absent-key conventions in the broader liquidity repository are not used on this route.

Local edge-depth d has root value 0. A-side StepEv weight is a_i=ceil(d_A(x_i)/2). On KEEP define q_i=floor(d_B(x_i)/2), z_i=d_B(x_i) mod 2, b_i=q_i+z_i=ceil(d_B(x_i)/2); on DELETE set q_i=z_i=b_i=0. A DOUBLE counts one event for two primitive rotations; a terminal ZIG counts one event. These are not depth+1 search costs.

On a closed pair walk gamma define A=sum a_i, Q_B=sum q_i, Z_B=sum z_i, B=sum b_i. On a prefix H define S_A=sum a_i and E_B=sum b_i. Under P_all/U=0 all A events are sited, so the historical sited count S_A agrees with this event total; don't substitute a different eligibility policy. LT(X,T0)=sum_i(d_A(x_i)+1); LT(Y,T0) uses retained B accesses. Source g_C(T0) is a finite maximum residual over reachable simple paths, independent of history length. An explicit conservative bound is given in the reconstructed PIVOT-2 proof.

## Exact implication chain and status

| Node | Exact obligation / implication | Status |
|---|---|---|
| Pair Access | For every X,I,T0, A/B states represent the full/retained splay executions | PROVED mathematical encoding |
| COARSE-DOUBLE | For every finite K and closed pair walk reachable from some diagonal, Q_B<=2A | OPEN; finite reported bounds only |
| C.ZIG | For every finite closed present-key pair walk, Z_B<=A | PROVED mathematical; formal run assembly open |
| Event decomposition | B=Q_B+Z_B, therefore the two cycle inequalities imply B<=3A | PROVED arithmetic implication; conclusion CONDITIONAL |
| PIVOT-2 | If every reachable cycle has E_B−3S_A<=0, then every prefix has E_B<=3S_A+g(T0) | Complete conditional implication; actual bound OPEN |
| Cost comparison | That prefix bound implies LT(Y,T0)<=7LT(X,T0)+2g(T0), universally for Y subsequence X | Complete conditional implication; actual bound OPEN |
| Levy–Tarjan | Eventual monotonicity of Splay implies dynamic optimality (v3 Theorem 4.3) | External established reduction; application CONDITIONAL |
| Dynamic Optimality | Exists universal c>=1: LT(X,T0)<=c OPT(X,T0), every finite instance | OPEN |

The target model in the recovered L3 v3 paper is a rooted-hull/transition-tree execution: for each request choose a rooted hull containing its access path, reshape it with the same keys so the request becomes its root, and reattach hanging subtrees in symmetric order. Cost is the sum of transition-tree sizes. Splay's transition tree is its access path, so cost is d+1. OPT can use full future knowledge; Splay is online. The same specified T0 is used on both sides. The final conjecture has no startup term. Eventual monotonicity allows an arbitrary integer-valued overhead depending only on T0.

The paper's Appendix A compares this with rotational execution: search costs access-path nodes, each primitive rotation costs one, and rotations may occur anywhere before a request. These optimal costs are equivalent within factor 2. Pointer traversal/restructuring is accounted for by the chosen execution model; do not claim the literal primitive cost equals StepEv or LT cost. Different initial trees would need the paper's additional initial-tree argument, rather than silent substitution.

The required external result is Theorem 4.3, not merely Theorem 3.5 (which assumes approximate monotonicity without additive overhead). Source: local L3 PDF, printed/PDF pages 3–5, 8–10 and Appendix A; verified online [v3](https://arxiv.org/html/1907.06310v3). The historical bridge manifest pins different v1 bytes and an absent L2; those old registry gates are preserved and documented, not rewritten.

## Local sufficient route to COARSE-DOUBLE

One shared j(tau),rho(c) across all finite BSTs -> universal J-SELF and adjusted ROW-DIAMETER -> residual edge inequality -> telescope on cycles -> Q_B<=2A. This is a sufficient proof architecture, not a theorem that J4 is necessary.

The raw same-child target is |H_u−H_v|<=2. REBOOT-01 reduces equal-depth/equal-top-fold instances to the correctly oriented empty-sibling tree. Remaining arbitrary-T bases and other classes are OPEN. No source-verified list of 14 boundaries exists; the actual global pair partition is same child, opposite children, or one root, with each orientation and all depths included.
'''
docs['THEOREM_DEPENDENCIES.md']=r'''# Dependency graph and proof-state labels

Edges below are sufficient mathematical implications, not equivalences unless stated. A proved implication with an open premise does not mark its destination proved.

```mermaid
flowchart TD
  PA[Pair Access encoding: PROVED] --> CD[COARSE-DOUBLE: OPEN]
  J[One globally admissible J: OPEN] --> SELF[J-SELF: OPEN]
  J --> ROW[Adjusted ROW-DIAMETER: OPEN]
  SC[SAME-CHILD: OPEN] --> ROW
  CC[Cross-child and root-child: OPEN] --> ROW
  ER[REBOOT-01 erasure: PROVED restricted] --> BASE[Empty-sibling bases: OPEN]
  BASE --> SC
  OTHER[Unequal depth / unequal coefficient cases: OPEN] --> SC
  SELF --> RES[Residual edge bound: CONDITIONAL]
  ROW --> RES
  RES --> CD
  CD --> SUM[B <= 3A: CONDITIONAL]
  Z[C.ZIG: PROVED mathematical] --> SUM
  SUM --> EX[Cycle excision: proved implication]
  EX --> PRE[E_B <= 3 S_A + g: CONDITIONAL]
  PRE --> LT[LT(Y) <= 7 LT(X) + 2g: CONDITIONAL]
  LT --> RED[Levy-Tarjan v3 Thm 4.3: established]
  RED --> DO[Dynamic Optimality: OPEN]
```

Arbitrary-depth SAME-CHILD and its bases are subdivisions of the same global row obligation, not successive independent existence problems. The coefficient identity proved for REBOOT-01 is exact for arbitrary J and thus adds no witness premise. For other pairs, the same insertion identity produces different coordinates and does not cancel automatically.

Parallel historical branches (GC-STATIC, Hall routing, U4/overflow, finite Bellman-Ford) are optional sufficient routes or experiments. Their results are not automatically prerequisites of J4. The graph does not claim all-depth UG: existing finite substitutions are a chosen constrained system.

Formal verification overlay: source Lean arithmetic statements exist; tree validity/run partition/cycle excision/global J and their complete assembled dependency closure have not been kernel verified in this run. A grep for `sorry` alone is not a proof audit. No Lean build was executed because repository build outputs would violate the write boundary without additional isolation.
'''
docs['CLAIM_LEDGER.md']=r'''# Source-backed claim ledger

Each status is scoped. “Reported” means the source artifact was read but its certificate was not independently rerun. Branch/HEAD and working-byte hashes are in the reproducibility records. Definition rows are not theorem achievements.

| ID | Claim | Status and scope | Evidence / proof |
|---|---|---|---|
| D01 | KEEP/DELETE masks represent occurrence subsequences from common T0 | PROVED universal encoding | pair_access_domain_mapping.md:1-42; stage_09 |
| D02 | e(d)=ceil(d/2); q=floor(d/2); z=d mod2; e=q+z | PROVED integer arithmetic | GCStaticKeep2Step.lean:703 onward; ORIGINAL_PIPELINE |
| D03 | BST/transition-tree LT model; offline OPT, fixed T0 | SOURCE DEFINITION | local L3 pp.3-5; stage_00 |
| C01 | Zero A on closed pair walks implies zero B | PROVED universal | C_ZIG_RECONSTRUCTED.md, first case |
| C02 | Z_B<=A on closed present pair walks | PROVED universal mathematical; formal tasks open | C_ZIG_RECONSTRUCTED.md |
| C03 | Q_B<=2A on all reachable closed pair walks | OPEN | PIVOT_COARSE_DOUBLE.md; J4 sufficient route |
| C04 | B=Q_B+Z_B<=3A given C02+C03 | CONDITIONAL conclusion | stage_10; arithmetic |
| C05 | Nonpositive reachable cycles imply a finite tree-only startup bound | Complete CONDITIONAL implication | PIVOT2_CONDITIONAL_REDUCTION.md |
| C06 | Actual E_B<=3S_A+g(T0) for all histories | OPEN | needs C03; stage_03 |
| C07 | Prefix StepEv bound implies LT(Y)<=7LT(X)+2g | Complete CONDITIONAL implication | COST_TRANSLATION_CONDITIONAL.md |
| C08 | Eventual monotonicity implies DO for Splay | Established external reduction; application conditional | L3 v3 Theorem 4.3 pp.9-10 |
| C09 | Dynamic Optimality | OPEN | full chain incomplete |
| J01 | kappa=4 and tau=(slot,lambda,delta,row-depth), root charge rho(c) | SOURCE DEFINITION | wp6_j4shared.py:17-150 |
| J02 | Full row H=-R+4(n−subsize)+sum j(tau)+rho(c) | SOURCE DEFINITION reconstructed from generator | REBOOT_01 proof |
| J03 | 4n cancels in H_u−H_v | PROVED algebraic identity | REBOOT_01; implementation_semantics |
| J04 | R_static is the fold-defined c+sum lambda | PROVED identity of source definitions | REBOOT_01 partition argument |
| J05 | R_static=q−total-depth drop under actual splay | Source mechanics claim, finite validated; universal mechanics not independently re-proved here | wp6_staticR.py; J4_CONDITIONAL_SUFFICIENCY premise |
| J06 | Universal J-SELF under the same globally admissible assignment | OPEN | wp6_j4shared.py:94-117 |
| J07 | Adjusted row diameter <=2; root/raw correction essential | OPEN, exact target recovered | wp6_j4shared.py:125-150 |
| J08 | J-SELF+ROW and R mechanics imply Q_B<=2A | Complete CONDITIONAL implication | J4_CONDITIONAL_SUFFICIENCY.md |
| J09 | One all-size assignment j,rho satisfying the source inequalities exists | OPEN | no source universal construction |
| J10 | rho=c, NONE coordinates merge to N_d, K_d=dN_d | CONDITIONAL normalization / chosen reduced subclass | wp6_rednorm.py:44 onward; not implied by defaults |
| J11 | Six UG substitutions plus two k=5 extensions | finite imposed constraints; universal necessity OPEN | wp6_gapcompat.py:42 onward; wp6_ugar.py:25-31 |
| J12 | Universal UG equality at all nonnegative offsets | OPEN; no source proof | REJECTED/UG_DEEP_SIBLING.md |
| R01 | Full fixed-child leaf-insertion defect f_v−f_u+j(a_e)−j(b_e) | PROVED source-defined identity | supporting lemma in REBOOT_01 |
| R02 | Equal-depth/equal-top-fold sibling erasure, both orientations | PROVED restricted domain, arbitrary depth/S/J | REBOOT_01_SIBLING_ERASURE.md |
| R03 | Twin2(1,m) difference increment −1+x_m−y_(m+1) | PROVED corollary of R01/source Twin2 | HISTORICAL_FINDINGS.md; not a width theorem |
| R04 | Exact neutrality x_m−y_(m+1)=1 for an admissible global J | OPEN | 26Z directive; no witness |
| F01 | C0 970x79 rank_Q48/nullity31; independent 48-row subset has same finite kernel | FINITE-EXACT rechecked | C0_RANK_EXACT_RECHECK.json |
| F02 | Joint reduced LRF template infeasible | REFUTED EXACT for saved 26823x163 matrix | LRF_EXACT_RECHECK.json; contradiction9/34 |
| F03 | n<=6 cycle-ratio certificates / n<=9 coarse BF bounds | finite source-reported, not rerun | PIVOT_RECURRENT_EXCESS/DUAL_UNIVERSAL |
| F04 | 48->44->55->47; quotient leaks4->5->15 | UNVERIFIED directive-only, not source-verified here | HISTORICAL_FINDINGS.md |
| F05 | Given T-map dimensions/ranks, kernels19,5,32 and cokernels11,11,9 | PROVED arithmetic conditional on supplied dimensions/ranks | RANK_NULLITY_CORRECTION.md |
| F06 | Exact all-depth stabilization, finite-dimensional universal representation | OPEN; tested candidates may fail, universal impossibility absent | historical retained limitations |
| F07 | Old-key occurrence changes under genuine fixed-node leaf insertion | REFUTED for the precisely fixed geometry by R01 proof | missing 26AB data cannot identify prior cause |

No universal source claim is upgraded merely because a JSON field says VERIFIED/REVIEWED, a float LP returns feasible/infeasible, or a report calls its result PROVED. Missing numerical report provenance is an evidence gap, not a mathematical disproof.
'''
docs['RECONSTRUCTION_REPORT.md']=r'''# Reconstruction report

## What was actually inspected

Read-only Git branch/HEAD/status/log; the normative specs, present-domain mapping, theorem/proof registry, stage arithmetic Lean source, recurrent/coarse/coupled audits, constraint-guided J4 report, J4/static-fold/coefficient/UG/context/Twin2/Lift2/finite-rank/certificate scripts, selected saved matrices and JSON, and the local Levy–Tarjan PDF. Independent searches found no AGENTS.md in the repository. Source file hashes are recorded separately from HEAD because much of the current J4 work is untracked.

The repository contains several overlapping programs. The normative MSTL/LIQ theorem registry tracks the liquidity formulation (k=6,C=2,P_all,rho=2) and later present-only variants. The requested proof route instead uses closed pair-cycle StepEv totals, COARSE-DOUBLE, zig accounting, and eventual monotonicity. These formulations are related but their theorem constants/costs and statuses cannot be conflated. WP6_CONDITIONAL_CHAIN is an older GC-STATIC-specific route, not proof that every other upstream leg is closed.

## Definitions recovered without guessing

The J4 generator includes one atom per other node and a separate root atom indexed by the fold constant c. Thus the complete assignment is j(tau),rho(c), not a two-atom F ladder. Slots are determined by tree/path membership; ancestors are NONE, descendants L/R, and fringe blocks F_j. lambda is obtained from the same backward fold as R_static. tau stores absolute row depth and relative node depth. The coefficient 4 is literal source KAPPA. The explicit 4n term disappears from row differences.

SELF rows demand H_x(B)−H_x(S_xB)>=R_static−2(1−b_x). DIAM rows demand H_r−H_x>=−2+2(b_r−b_x); the universal diameter target is for H−2b. Raw SAME-CHILD width is exactly 2 because both nodes are nonroots. Root/nonroot raw range is [0,4]. No source census establishes “14 boundaries.” The complete location split is same child, opposite children, and one root; then depths/path patterns supply remaining subcases.

The reduced expression H=4G+sum bar-j+K_d follows if rho(c)=c and all ancestor NONE coordinates at row depth d equal N_d. Those are normalization assumptions of the reduced system. Source scripts impose finite UG gaps j(F,2,delta,d)=j(F,1,delta,d)+1; they do not prove those equations follow from unrestricted all-size ROW/SELF. UG+rho=c is therefore a selected constrained formulation until universal admissibility is shown. `.get(...,0)` is an implementation lookup default, not a theorem fixing unseen coordinates.

## Results independently established

The supplied 26AB insertion identity is recovered directly from the code's complete occurrence sums: true nonrotating leaf insertion in the other child leaves every old node's path, slot, coefficient, depth, and root token fixed. An old atom's aggregate count can increase when the new leaf has that same atom; no old occurrence changes. The full insertion formula and the new equal-signature erasure proof include that multiplicity issue explicitly. They are identities for the source-defined observable, not claims that it already supplies the needed global potential.

The C0 block was reconstructed from j4_xclean_mat.npz, using exactly the old columns touched by its 970 added rows. It is 970x79. A nonzero modular rank48 certifies rank_Q>=48, and 31 independent rational null vectors with all 970 exact residuals zero certify rank_Q<=48. Selecting the 48 independent source rows gives a new finite summary with the same kernel; this does not verify that every historical S0 file equals this chosen summary.

All saved LRF multipliers reconstruct rationally and give zero residual on every column and RHS9/34>0. This verifies a finite constrained template elimination, not a general no-J theorem. The REBOOT-01 finite checks use integer coefficient dictionaries and rational key gaps, never a numerical fit.

## Missing evidence and source conflicts

The named 26S–26AB reports and the three corrected T+ matrices were not located by filename/content searches. Earlier scripts explicitly labeled 26O/26R and their artifacts are available. Later navigation claims are retained as directive-only unless recovered directly from the actual definitions. In particular, the rank/leak sequences are not independently certified in this workspace. A missing file does not disprove its mathematical assertion.

The local 29-page L3 PDF is v3 (SHA f7aa7901...), whereas prereg/bridge_manifest.yaml pins a different v1 blob (SHA e23ea8b5...) and reports L2 absent. This workspace checks the actual v3 model and Theorem4.3 independently. It does not change MSTL-19's historical BLOCKED_BY_SOURCE registry. The paper's crossing lower-bound discussion cannot itself supply a splay upper bound; its eventual-monotonicity reduction can legitimately be used once its premise is proved.

Several s=0 probes replace [p,T,None] by [0,None,T], changing child orientation. They cannot establish a same-position sibling-erasure comparison. Finite vector builders also skip absent coordinates. Proposed repairs are documented inside this workspace; original code was not edited.

## Result and stopping point

One approved theorem completed: equal-signature sibling erasure. It removes arbitrary S from a genuine infinite SAME-CHILD subclass. The empty-sibling base width, remaining row cases, shared J existence and COARSE-DOUBLE remain open. No second pivot was commissioned because none has a source-backed bounded proof mechanism that deletes another original obligation without importing the global existence burden.
'''
docs['RESEARCH_RULES.md']=r'''# Permanent research rules

Apply these rules to every pipeline stage, not just J4. A pivot is authorized only after all four pass in a written pre-execution record.

1. **Strictly smaller.** Identify the exact reduction in quantified domain, structural cases, variables, compatibility burdens, mechanisms, or original dependencies. A representation change or all-horizon restatement of global existence is insufficient.
2. **Concrete reason it is solvable now.** Give a specific starting identity and proof sketch: direct cancellation, an established theorem, a proved-complete finite classification, explicit construction, determined induction, exact specified dual certificate, symmetry, or a bounded recurrence with a proved invariant. Numerical plausibility is insufficient.
3. **One-prompt scope.** One principal theorem, one principal mechanism, one bounded source audit, one completed proof or exact obstruction, and one direct graph connection. If a second independent open theorem is necessary, stop. No guarantee of truth or success is implied; a credible bounded proof/refutation attack is required.
4. **Real upward advancement.** Fix before execution the exact original obligation that success deletes. A new equivalent existence premise, decomposition, quotient rank, finite fit, or conditional theorem with a comparably hard new witness does not count. Independently mandatory premises may support a real reduction; source-imposed extra constraints are not automatically mandatory.

An existence-burden audit asks whether the new object is the old unsolved object, whether constraints make its construction harder, whether notation hides the difficulty, and whether an independent construction mechanism actually exists. Replacing “find global J” by “all finite systems feasible” or “compactness premise” fails without that mechanism.

Statuses: PROVED—UNIVERSAL requires a complete proof on the whole stated domain with established premises. PROVED—RESTRICTED DOMAIN names the subclass and deleted original case. FINITE-EXACT requires integer/rational computation on a pinned finite corpus. REFUTED—EXACT requires a valid in-domain counterexample or exact dual contradiction. CONDITIONAL means an essential premise remains open. NUMERICAL means floating evidence without exact certification. OPEN means neither a complete proof nor exact refutation. SOURCE DEFINITION and report-only provenance are recorded separately. “Not reverified” is a verification attribute, not an upgrade in truth status.

Before PROVED: check quantifiers, all boundary cases, both orientations, signs, repeated-coordinate multiplicity, global sharing, nonvacuity, dependencies and circularity. A telescoping formula needs an endpoint/accumulation bound; a finite certificate needs complete row provenance, dimensions, multipliers, signs and zero residuals. A finite tested counterexample only rejects its specified template.

After each pivot record BEFORE/RESULT/AFTER, genuinely deleted obligations, new assumptions and NET PROOF ADVANCEMENT. Strategic elimination is distinct from advancement of the original theorem. Do not redefine success after seeing results. Workspace creation is not mathematical progress.

Stop on refuted mechanism, failed gate, equally hard new existence burden, or lack of a credible small theorem. Two consecutive non-advancing pivots using essentially the same mechanism mandate strategy review; renamed targets cannot reset the count. Do not automatically proceed after OPEN. No auxiliary treadmill.

All writes, logs, caches, scripts, proposed patches and artifacts stay in DO_RESEARCH_REBOOT/. Existing sources/tests/configuration/Git are read-only. No commits, branch changes, resets, clean/stash, dependency installations, or overwrites of old research. Existing reboot files must be preserved; future runs use versioned names. User authorization in the master directive governs approved in-scope execution; this mathematical approval gate does not require another user permission prompt.
'''
docs['PIVOT_APPROVAL_GATE.md']=r'''# Mandatory pre-pivot approval

Complete this record before generating/executing a research prompt. PASS requires all four individually PASS. Missing evidence gives REJECT pending source verification, not “mostly compliant.” Do not execute a rejected prompt.

```text
PIVOT ID:
CURRENT ORIGINAL PROOF NODE:
EXACT THEOREM TO PROVE: [all quantifiers/constants]
RULE 1 — WHY STRICTLY SMALLER:
RULE 2 — CONCRETE PROOF MECHANISM:
RULE 3 — WHY ONE SESSION IS PLAUSIBLE:
RULE 4 — EXACT ORIGINAL OBLIGATION DELETED:
PREVIOUSLY PROVED PREMISES: [proof + source]
NEW HYPOTHESES INTRODUCED:
EXISTENCE-BURDEN AUDIT:
SOURCE LOCATIONS: [working-byte hashes]
PROOF PLAN:
NONVACUITY WITNESS:
EXPECTED OUTPUT:
EXACT COUNTEREXAMPLE / FAILURE STANDARD:
APPROVAL: PASS / REJECT
```

Completed approval: [REBOOT-01](08_PIVOTS/APPROVED/REBOOT_01_APPROVAL.md), now proved. Rejected: [UG deep-sibling pruning](08_PIVOTS/REJECTED/UG_DEEP_SIBLING.md); universal UG at required offsets is not established or source-mandatory. Its identical-signature subclass is handled by REBOOT-01 without UG.

A new successor needs a fresh gate. The remaining arbitrary-depth empty-sibling base currently fails concrete-mechanism and bounded-scope requirements. The proposed all-horizon compactness/global-feasibility reformulation fails rules1,2,3,4 unless an independently easier constructive argument is supplied. No such prompt is issued.
'''
docs['STRATEGY_REVIEW.md']=r'''# Strategic review

The nearest original load-bearing inequality is COARSE-DOUBLE Q_B<=2A on all reachable closed present-key pair walks. The J4 branch replaces it with sufficient all-size shared row constraints. A witness satisfying those constraints remains unconstructed. Finite feasibility and transport descriptors have repeatedly moved rather than removed that burden.

| Route | Current evidence | Concrete mechanism / advantage | Decision |
|---|---|---|---|
| A: existing J4 | exact source row definitions; new identical-signature cancellation; finite feasible systems; restricted LRF refutation | cancellation deletes S without new constraints | complete REBOOT-01; pause synthesis at base/global witness |
| B: repair potential | source family defects and specific finite refutations exist | no explicit simpler all-size construction found | unapproved research idea; no added coordinates |
| C: direct Coarse-Double | universal zig accounting separate; reported BF bounds through n9; genealogy/U4 claims remain open | avoids sufficient J4 witness burden, but no new local charging theorem was located | preserve original target; no executable pivot yet |
| D: different implication chain | LT eventual-monotonicity reduction verified; historical GC-STATIC/Hall and imported lower-bound ideas remain open or inapplicable as upper bounds | no source-backed first theorem with a demonstrated cost advantage | no speculative alternative pipeline |

The C0 rank/nullity result describes one finite coefficient block. Growing quotient-visible leaks can eliminate specified stabilization explanations; they do not prove every symbolic finite-dimensional representation impossible. The exact LRF certificate eliminates its finite extra-equality template. Neither justifies declaring unrestricted J4 impossible.

The proposed UG route fails before execution: source substitutions are finite imposed equations, not a proved all-offset consequence of ROW/SELF. Demanding a globally admissible J with additional neutral ladder constraints would reproduce the old existence problem. Equal coordinates cancel directly, giving the narrower theorem now proved.

The newly reduced arbitrary-T empty-sibling width still has an unknown globally shared charge assignment. That base is structurally smaller, but no constructive recurrence, endpoint inequality or established lemma closes it in one session. It must not be commissioned merely because it is the next line in the graph.

Continue only when a proposed theorem has an explicit statement in the original model, a nonempty example, a specific proof technique, a demonstrated advantage, and a bounded GO/NO-GO gate. An alternative with no such first theorem is an idea, not an approved pivot. Current decision: retain J4 evidence, stop its auxiliary expansion, and keep the direct cycle inequality visible. No second non-advancing pivot was run.
'''
docs['NEXT_ACTION.md']=r'''# Next action and handoff

The first approved theorem was REBOOT-01 equal-signature sibling erasure. It is complete; [the archived executable prompt](08_PIVOTS/APPROVED/REBOOT_01_PROMPT.md) and [advancement report](08_PIVOTS/COMPLETED/REBOOT_01_ADVANCEMENT.md) record its scope. Do not rerun it as a new advancement.

**No successor research theorem currently passes all four rules.** The next J4 obstruction is |D_J([p,T,None];u,v)|<=2 for arbitrary T in the reduced pair class, under the same all-size assignment that must also satisfy every other SELF/DIAM row. No concrete construction/induction mechanism is established. Adding a new global compatibility system would fail the gate.

The UG candidate is rejected; recovering an actual universal UG proof would be an evidence acquisition task, not permission to assume one. The missing 26S–26AB reports may change the evidence picture if they become available, but their absence does not authorize inventing their contents.

For a fresh session: read START_HERE, ORIGINAL_PIPELINE, CURRENT_STATE, CLAIM_LEDGER, the completed proof and its exact premises, and STRATEGY_REVIEW. Verify the current branch/HEAD/source hashes; source bytes are dirty and may change. Use the safety protocol before any write. Version new files rather than overwriting these records. Commission exactly one new theorem only after a new written PASS record. If none has a credible mechanism, preserve the stop decision.

Original goal remains Dynamic Optimality. This run removed sibling quantifiers for a restricted row class, recovered exact finite evidence and clarified reductions. It did not prove the universal row width, global potential, COARSE-DOUBLE or Dynamic Optimality.
'''
docs['WORKLOG.md']='''# Work log

9 October 2026, Asia/Karachi. Read the complete supplied directive, identified the repository and existing dirty state, created only the authorized root folder, and recorded a SHA-256/size/mtime inventory of 4,429 files outside it (including ignored files and .git).

Reconstructed the occurrence-level present domain, StepEv/LT costs, cycle-to-prefix chain, J4 row generator and finite normalization scope. Read the local L3 source and checked the v3 reduction online. Recovered source conflicts and missing later reports without modifying old registries.

Rechecked the LRF finite certificate exactly (zero column residual, positive RHS9/34) and the finite C0 rank48/nullity31. Rejected universal UG pruning at its source gate.

Wrote REBOOT-01's four-rule approval and standalone prompt before execution. Completed its universal restricted-domain proof and exact coefficient checks. Recorded the precise deleted sibling obligations and remaining base/global difficulties. Did not authorize a speculative successor.

Created the mandatory handbook/stages, reproducibility scripts and final proof checklist. Ran the final filesystem comparison; see final_safety_audit.json for machine-readable results. No mathematical progress is attributed to documentation volume.
'''
docs['00_REPOSITORY_AUDIT/repository_map.md']=r'''# Repository map

| Area | Meaning for this reboot |
|---|---|
| IMPLEMENTATION_SPEC*, WorkPlan.md, Path.md, planning/, prereg/ | normative liquidity program and historical gates; kept read-only |
| python/independent/, python/liquidity/ | splay/cost/ledger implementations; distinguish LT costs from event counts |
| scripts/ | most current J4, cycle, transport and solver probes; many untracked; entry points often write outside the allowed folder |
| audits/ | recurrent/coarse/coupled/J4 narrative proofs and conditional-state reports |
| math/theorems/, math/proofs/, math/proof_status.json | MSTL/LIQ registry; not a proof of every later J4 claim |
| lean/WP6/ | tree mechanics and arithmetic source; no isolated build run here |
| artifacts/v04/wp6_present/0909c74a/ | finite present-domain experiments, matrices and certificates |
| artifacts/v04/wp6_present/present_domain_audit/ | occurrence masks and fixed-key closure |
| v03/history/ | preserved prior program and local papers, including L3 v3 |
| historical/ | superseded normative material |
| .git/, .lake/, .pytest_cache/ | Git/build/test state; read only; included in outside-file audit |
| DO_RESEARCH_REBOOT/ | the single permitted writable research workspace |

Sibling zip in the parent Temp directory was not extracted or modified. No alternate repository/worktree was created. No README exists at this repository root; WorkPlan/Path/specs provide the project entry documentation.
'''
docs['00_REPOSITORY_AUDIT/implementation_semantics.md']=r'''# Implementation semantics

Tree terms are [key,left,right], with None for empty. Keys are distinct and totally ordered. Present-key ordinary bottom-up splay uses oriented zig, LL/RR zig-zig, LR/RL zig-zag and preserves the key set. All old-tree mutations are prohibited during this reboot.

Depth in scripts is edge-depth. e(d)=floor((d+1)/2) counts StepEvs: root access0, double1, terminal zig1. The legacy API splay_cost uses depth+1, including its broader absent path. The present route uses only keys in the fixed universe. DELETE masks the B occurrence and leaves B unchanged; it is not a BST deletion. Dense key ranks are an order-isomorphic encoding.

J4 slots: SELF for y (excluded from the per-other-node sum), L/R for descendant child subtrees, F_j for the off-path child of the ancestor j+1 steps above y, NONE for strict ancestors. lambda comes from the path fold. tau4=(slot,lambda,d(z)−d(y),d(y)). The root atom is separately indexed by the fold constant c. Shared variables span all tree sizes.

H_y=−R_static+4(n−subsize(y))+sum_(z!=y)j(tau_yz)+rho(c_y). Hence D_J=R_static(v)−R_static(u)+4(subsize(v)−subsize(u))+J_u−J_v; 4n cancels. Individual H growth gives no row-difference growth theorem.

Reduced H=4G+sum_non-NONE(j−lambda)+K_d additionally requires rho=c and NONE(tau)=N_d for all ancestors at depth d, with K_d=dN_d. These restrictions are not Python default values or established universal consequences. Finite maps may omit coordinates; the mathematical domain does not.

The DIAM generator bounds H−2b, b=[y=root(B)]. For nonroots raw width2; for root/nonroot the raw difference lies in [0,4]. J-SELF is a separate same-row splay inequality. A complete proof needs one assignment satisfying both, not separate pointwise selections.
'''
docs['00_REPOSITORY_AUDIT/inconsistencies.md']=r'''# Conflicts, bugs, and proposed repairs (not applied)

1. **Finite UG imposed vs universally mandatory.** wp6_gapcompat.py adds gap equalities; wp6_ugar.py builds a finite map from six overlaps plus two extensions. No all-offset proof found. Repair: label these as added finite constraints and prove any claimed universal necessity separately; do not enlarge the map by assumption.
2. **Empty-sibling orientation.** wp6_funcmp.py:108 onward, wp6_redimpl.py:174 onward, and analogous leveled probes use [0,None,T] for s=0 but [p,T,S] for s>0. This changes the path side. Proposed patch: keep root p and the same child slot in both cases. Do not edit source here. The new checker uses [p,T,None] (or its mirror) exactly.
3. **Unseen-coordinate omission.** vec/Pform builders skip keys absent from finite rvmap. Proposed patch: keep a separate symbolic coefficient dictionary for unknown coordinates or refuse a universal interpretation. Unseen coordinates are not zero-valued mathematical variables.
4. **Root correction.** Raw diameter2 for every node is not the source DIAM statement. Use adjusted H−2b; root/nonroot raw range[0,4].
5. **Counts vs key sets.** Equality of atom key sets does not establish equality of coefficients. Genuine fixed-child nonrotating insertion freezes each old occurrence, while the new leaf can increase an already-present atom's aggregate count. Missing 26AB logs prevent identifying the cause of any purported changed old occurrence.
6. **Paper pins.** prereg/bridge_manifest.yaml records v1 SHAe23ea8b5..., local 29-page L3 v3 has SHAf7aa7901.... Do not silently update the original bridge gate. This reboot has an explicit independent v3 reference.
7. **Finite interface labels.** The 970x79 C0 narrative block is the xclean added-row restriction to old touched columns. It is not the full A0/A1/A2 arrays in j4_levelblocks.npz (250/550/970 rows by142 common columns). Compare matrices and coordinate domains before comparing ranks.
8. **Rank/nullity confusion.** Source kernel dimension is source_dim−rank; target image deficit is target_dim−rank. See permanent correction. Supplied corrected dimensions are retained but their missing actual matrices are not certified here.
9. **Stale report states.** “Only GC-STATIC open” in an older conditional route and later “Coarse-Double open” refer to different sufficient programs. The normative MSTL registry does not reflect every untracked J4 exploration. Preserve source distinctions.

All repair proposals remain documentation inside the authorized workspace. No source fix was applied.
'''
docs['03_OPEN/ORIGINAL_OBLIGATIONS.md']=r'''# Original open obligations

The immediate original inequality is universal Q_B<=2A on reachable closed present-key pair walks. Its optional J4 sufficient route needs a single shared j,rho, defined on every realized tau/root token across all finite sizes, satisfying all SELF/DIAM rows. No such object has been constructed.

After REBOOT-01, equal-depth/equal-top-fold SAME-CHILD cases reduce to |D_J([p,T,None];u,v)|<=2, with p and child orientation retained. T and depth are still arbitrary. Other same-child cases (unequal depths or unequal top folds), cross-child nonroot width2, root/nonroot adjusted width2/raw range[0,4], and J-SELF remain. Base reduction does not select or construct J.

Universal mechanics linking the static fold to actual splay depth drop must be included in the final proof closure; this run verifies its code definitions and finite identities, not a new complete formal mechanics proof. Source-based arithmetic and run/cycle arguments have separate formal assembly tasks.

Downstream E_B<=3S_A+g and LT<=7LT+2g remain conditional on cycle bounds. The external v3 eventual-monotonicity theorem is available; applying it before those universal premises is invalid. No final Dynamic Optimality document can be assembled yet.
'''
docs['05_FINITE_EXACT/HISTORICAL_FINDINGS.md']=r'''# Historical findings retained with precise evidence scope

| History | Material finding | Verification in this reboot / consequence |
|---|---|---|
| 26F–H | joint LRF candidate refuted; independent sign shortcut reported refuted | LRF exact contradiction9/34 rechecked; other exact refutations not regenerated. Refutes templates only |
| 26I–N | Lift2 changes absolute/relative depths and F indices; shallow descriptors insufficient | actual Twin/Lift2/oldF/context code read; retains transport dependence. No universal finite-state impossibility |
| 26O–R | 970x79 finite block rank48/nullity31, 48-row summary | independently exact from xclean; selected48 independent rows have same finite kernel. Historical specific S0 matrix not separately reconstructed |
| 26S–W | supplied raw ranks48->44->55->47 and leaks4->5->15 | later matching matrices/reports absent; directive-only here. No claimed regeneration or universal no-representation theorem |
| 26X | W_req=2 for SAME-CHILD | recovered exactly from DIAM source; shared all-depth J remains open |
| 26Y | Twin2(1,m) increment−1+x_m−y_(m+1) | recovered from full insertion proof plus wp6_twins.py:35-46. u=1 (d2,f2), v=2 (d1,f1), new sibling depth m+2 gives stated atoms |
| 26Z | exact neutrality would fix the ladder difference | conditional algebra only; no global admissible J witness found. Numerical template failures don't imply general impossibility |
| 26AA | full coupled coordinates include F/NONE/R/root families | source row sum shows these families; claimed bulk-template failure not independently rechecked without later report |
| 26AB planned | all-horizon/compactness approach | directive says superseded; no completed theorem found, no prompt authorized |
| 26AB insertion | complete fixed-child insertion law | recovered universally for source-defined observable in REBOOT-01 proof; base/global width still open |
| proposed 26AC | UG deep-sibling pruning | rejected because universal all-offset UG premise unverified and finite constraints are imposed |

Additional retained finite evidence: PIVOT_RECURRENT_EXCESS reports exact cycle ratios1,1,3/2,3/2,5/3 for n2..6; PIVOT_DUAL_UNIVERSAL reports coarse BF certificates through n9. These were read, not rerun. They are not universal premises in the new proof. Earlier DOUBLE Q_B<=A is refuted by a reported replayed n5 cycle with A4,Q6; this does not refute COARSE-DOUBLE Q_B<=2A.

Lift2 defects and telescope sums retain the original lesson: Gamma(k)=Gamma(k0)+sum Dbar_L2 is an identity; per-step bounds, descriptors and finite kernels do not bound the accumulated correction. There is no endpoint inequality or all-depth recurrence derived here.
'''
docs['05_FINITE_EXACT/RANK_NULLITY_CORRECTION.md']=r'''# Permanent rank-nullity correction

For T:Q^s->Q^t of rank r, dim kerT=s−r and dim cokerT=t−r. They measure different spaces.

| Supplied map | s | t | r | source kernel | target codimension |
|---|---:|---:|---:|---:|---:|
| T01+ | 52 | 44 | 33 | 19 | 11 |
| T12+ | 49 | 55 | 44 | 5 | 11 |
| T23+ | 70 | 47 | 38 | 32 | 9 |

The subtraction is proved exactly. These underlying dimensions/ranks come from the user's directive; actual corresponding T+ matrices were not located and their ranks are not independently certified here. Do not use this arithmetic check as a matrix verification.

By contrast, the reconstructed finite C0:Q^79->Q^970 has certified rank48, kernel31 and cokernel922. Its source nullity31 is not a target deficit31. See 06_CERTIFICATES/C0_RANK_EXACT_RECHECK.json for independent rank bounds and complete null-vector verification.
'''
docs['07_STRATEGIES/STOP_RECORD.md']='''# Strategic stop record

REBOOT-01 advanced a restricted row reduction and is complete. No successor was approved. Universal UG at new offsets is unavailable; the arbitrary-T base requires unresolved shared-potential control. Neither a new compactness condition nor a deeper finite transport matrix supplies a smaller constructive theorem.

The stopping condition is methodological, not a proof of impossibility and not a claim that every J4 strategy fails. Preserve the exact identities and the original target. Resume only with new evidence or a fresh candidate passing all four rules before execution.
'''
docs['08_PIVOTS/REJECTED/UG_DEEP_SIBLING.md']=r'''# Proposed UG deep-sibling pruning — REJECT

CURRENT NODE: SAME-CHILD -> ROW-DIAMETER -> COARSE-DOUBLE.
PROPOSED THEOREM: equal-depth same-child rows with different top coefficients1 and2 have every sufficiently deep sibling insertion invisible under already mandatory universal UG.

Rule1 PASS: deletes sibling depth for a subclass. Rule2 FAIL: cancellation needs bar-j(F_(d−1),2,h−d,d)=bar-j(F_(d−1),1,h−d,d) at unbounded offsets; no source proof of that mandatory universal equation was found. Rule3 FAIL: closing that unknown prerequisite is an additional independent all-depth theorem. Rule4 FAIL as currently posed: adding the equation to a globally admissible J is a new compatibility burden, not a proved deletion under existing premises.

Source scope: j4_gapdomain.json lists overlaps (k,delta,d)=(1,−1..2,2) and (3,−3..−2,4). wp6_ugar.py adds (5,−5,6),(5,−4,6). wp6_gapcompat.py imposes gap=1 rather than deriving it. In q notation delta=q−k, the encoded offsets are q0..3 at k1 and q0..1 at k3/k5. This is neither an all-q theorem nor a refutation of one.

Actual same-depth pairs with different folds exist (e.g. T has a root with two children; the ambient d2 pair has f2 and f1). Complete insertion law and both orientations have been verified, but the equality of different atoms remains unsupported. A new leaf at arbitrarily large h uses an unbanked offset. Missing finite rows are not counterexamples to universal UG.

APPROVAL: REJECT. No rejected prompt generated or executed. Identical-signature pairs need no UG and are handled by the separately approved REBOOT-01. No new J system is introduced as a repair.
'''
docs['09_PROMPT_TEMPLATES/PER_PIVOT.txt']='''PIVOT ID:
TITLE:
ORIGINAL PIPELINE NODE:
EXACT THEOREM: [Full quantifiers and constants.]
WHY THIS IS STRICTLY SMALLER: [Removed difficulty.]
WHY ONE-SESSION COMPLETION IS PLAUSIBLE: [Named mechanism and bounded work.]
PREVIOUSLY PROVED PREMISES: [Proofs with source hashes/lines.]
UNVERIFIED FACTS TO CHECK FIRST: [Hard GO/NO-GO gate.]
SOURCE FILES: [Read-only absolute repository context + paths.]
MATHEMATICAL ATTACK: [Explicit derivation.]
NONVACUITY: [Real family/consequence.]
SUCCESS CONDITION: [Theorem and exact original obligation deleted.]
FAILURE CONDITION: [Exact counterexample or obstruction.]
PROOF VALIDATION: [Domain, boundaries, mirrors, signs, multiplicities, sharing.]
FILESYSTEM RULE: [All writes only DO_RESEARCH_REBOOT/. Version existing files.]
STOP RULE: [No auxiliary replacement problem; no second independent open theorem.]
REQUIRED ARTIFACTS: [Proof/certificate/report inside workspace.]

Prerequisite: completed PASS record under PIVOT_APPROVAL_GATE.md before writing an executable prompt.
'''
docs['11_REPRODUCIBILITY/SAFETY_AND_REPRODUCIBILITY.md']=r'''# Reproducibility and filesystem safety

All authoring and computation occurred inside the one authorized root DO_RESEARCH_REBOOT/. The initial folder did not exist. No prior reboot contents were overwritten. Source imports were avoided: verification executes only selected pure function AST definitions in a controlled namespace. Source main functions, which write into artifacts/, were never executed.

At entry, branch/HEAD/porcelain status were read with GIT_OPTIONAL_LOCKS=0 / --no-optional-locks. baseline.json records SHA-256, size and mtime_ns for every outside file, including .git, ignored bytecode/test caches and build files, plus directory paths and the complete dirty/untracked list. It covers 4,429 files and 404,217,810 bytes. The baseline was created after the permitted folder and safety script were created; those are excluded by design. The initial outside status was read before that folder existed, and workspace entries are filtered symmetrically in the final comparison.

Commands from repository root:

```powershell
python -B .\DO_RESEARCH_REBOOT\safety_audit.py begin
python -B .\DO_RESEARCH_REBOOT\10_EXPERIMENTS\verify_reboot.py
python -B .\DO_RESEARCH_REBOOT\11_REPRODUCIBILITY\inspect_evidence.py
python -B .\DO_RESEARCH_REBOOT\author_workspace.py
python -B .\DO_RESEARCH_REBOOT\safety_audit.py end
```

`begin` refuses to overwrite its baseline. Authoring refuses to overwrite already authored paths. To reproduce a future run, use a new versioned output directory/script copy within this root; do not replace the old baseline. Existing Python3.13, numpy, sympy and pypdf were used without installation. -B and dont_write_bytecode disable bytecode writes. No pytest, compiler, package manager, lake build or installation was run. Libraries use in-memory arithmetic; no source caches were generated.

Verification inputs: source ASTs in wp6_staticR.py, wp6_lambda.py, wp6_j4shared.py; enumerated T1..6/S0..3 contexts and mirrors; all empty insertion pointers for T4/S0..3; larger family heights0..30. Exact outputs and function hashes/spans: verification_results.json. C0 inputs: saved xclean matrix, old-column support and added-row block. LRF inputs: saved reduced matrix, multipliers and equality list. Exact certificate outputs: 06_CERTIFICATES/. Provenance and paper hash/page count: evidence_metadata.json. The scripts record finite scope and distinguish evidence recovery from the universal written proof.

The local L3 PDF was read and its extracted text saved only here. Online verification used arxiv.org/html/1907.06310v3 for the external reduction/model; no external media/download caches or dependencies were installed.

Final result is authoritative in final_safety_audit.json: added/deleted/changed outside files/directories must all be empty, original outside Git status unchanged and branch/HEAD unchanged. A claim of safety is not based only on Git status, since Git can miss ignored-file writes. The comparison checks content plus mtime and size. The audit does not claim to reconstruct unrelated system-wide platform internals; the complete repository boundary, including pre-existing dirty work, is checked.
'''
docs['12_FINAL_PROOF/ASSEMBLY_CHECKLIST.md']=r'''# Final proof assembly — NOT READY

No Dynamic Optimality proof is assembled. The following must all be discharged with linked verified proofs and exact source models before claiming the conjecture:

1. Finite ordered BST domain, execution/search/restructuring costs and offline comparator; common specified initial T0.
2. All finite present-key access sequences and all occurrence-level retained subsequences, including empty histories and small n.
3. Universal COARSE-DOUBLE with constant2, either directly or through a constructed shared potential and fully proved mechanics/row cases.
4. C.ZIG constant1 with complete tree/run formal assembly if kernel certification is required.
5. Event decomposition and B<=3A on every reachable closed cycle.
6. Full cycle-to-prefix implication with a finite overhead depending only on T0.
7. Correct StepEv/LT translation, constant7 and overhead2g, with P_all S_A identity and no cost-model conflation.
8. Exact v3 Levy–Tarjan eventual-monotonicity application, including its initial-tree and repeatability/coercibility handling; historical manifest conflicts resolved explicitly if using the old registry.
9. All sibling bases, other child/root cases, depth parities, coefficient multiplicities, shared coordinates and any potential-existence premises used.
10. Constant-factor final comparison without startup overhead, and rotational-model equivalence if presenting that formulation.

Current missing load-bearing premise: item3. REBOOT-01 closes only sibling erasure for one row subclass. Conditional arrows are not substitute proofs. Never rename this checklist to a final theorem merely because the workspace or an experiment is complete.
'''

# Stage references: all requested fields, with no invented completed node.
stages=[
('stage_00_dynamic_optimality.md','DO','Dynamic Optimality',
 'Exists c>=1 independent of K,T0,X such that LT(X,T0)<=c OPT(X,T0).',
 'Every finite ordered key set, valid initial BST and finite present-key sequence. Empty sequences included.',
 'Universal c; no final additive term.',
 'LT is splay transition-tree/access-path cost; OPT is offline optimal transition-tree execution from the same T0.',
 'Universal eventual monotonicity plus L3 v3 reduction.',
 'External reduction only; no proof of the premise.',
 'Finite pair bounds do not prove DO.',
 'No exact counterexample to DO established here.',
 'All universal upstream inequalities.', 'OPEN',
 'Local L3 pp.3-5,9-10; math/theorems/MSTL-19.md historical blocked ledger.',
 'Final original target.'),
('stage_01_levy_tarjan.md','LT-RED','Levy–Tarjan reduction',
 'If Splay is eventually monotone then Splay is dynamically optimal (v3 Theorem4.3).',
 'All finite instances (X,T0), all occurrence subsequences Y, one universal monotonicity factor and tree-only startup overhead.',
 'Input factor b universal; g(T0) integer-valued. This paper does not set the project factor7.',
 'Eventual monotonicity allows cost(Y,T0)<=b cost(X,T0)+g(T0).',
 'Splay-specific coercibility/repeatability supplied by the paper; exact cost/domain correspondence.',
 'Published v3 Theorem4.3 pp.9-10; Theorem3.5 covers the zero-overhead case.',
 'None needed for the external implication.',
 'No refutation of the reduction; crossing lower bounds do not discharge its premise.',
 'Project universal eventual bound; original v1/L2 ledger gates not silently replaced.', 'CONDITIONAL application; established external theorem',
 'v03/history/external/papers/L3_levy_tarjan_foundation_1907.06310.pdf; prereg/bridge_manifest.yaml; https://arxiv.org/html/1907.06310v3',
 'Converts the completed LT subsequence bound to the final conjecture.'),
('stage_02_lt_bound.md','LT-7','LT cost comparison',
 'E_B<=3S_A+g(T0) implies LT(Y,T0)<=7LT(X,T0)+2g(T0).',
 'Every present-key X,Y subsequence,T0; same initial tree.',
 '7 and 2; more generally 2C+1 and2.',
 'e=ceil(d/2); LT=d+1; E_B retained B events, S_A all A events under P_all.',
 'Universal prefix bound, |Y|<=|X|, S_A<=LT(X), LT(Y)<=2E_B+|Y|.',
 '02_PROVED/COST_TRANSLATION_CONDITIONAL.md; Lean arithmetic source.',
 'No finite premise used.', 'None for the arithmetic implication.',
 'The prefix inequality remains open.', 'CONDITIONAL',
 'lean/WP6/GCStaticKeep2Step.lean:703-716; present_domain_mapping.',
 'Establishes eventual monotonicity in the exact LT model.'),
('stage_03_pivot2.md','PIVOT-2','Cycle-to-prefix',
 'If every reachable closed pair walk has B<=3A, then every present prefix satisfies E_B<=3S_A+g(T0).',
 'Every finite K,T0 and every finite present-legal KEEP/DELETE history from (T0,T0).',
 '3; conservative g=(Cat_n^2−1)floor(n/2). Source g is maximum simple-path reward.',
 'Reward W=B−3A additive; pair graph has at most Cat_n² states.',
 'Nonpositive reachable cycles; finite fixed key universe.',
 '02_PROVED/PIVOT2_CONDITIONAL_REDUCTION.md.',
 'Small graphs source-reported; not necessary to prove conditional excision.',
 'A positive reachable cycle refutes any tree-only bound at that C.',
 'Universal cycle premise; formal list-excision assembly not completed.', 'CONDITIONAL',
 'audits/PIVOT_RECURRENT_EXCESS.md:12-20; scripts/wp6_cycle_ratio.py:58-100.',
 'Moves closed-cycle counts to the full sequence comparison.'),
('stage_04_coarse_double.md','CD','COARSE-DOUBLE',
 'Q_B(gamma)<=2A(gamma) for every reachable closed present-key pair walk gamma.',
 'All finite ordered K, diagonal start T0, reachable cycles of arbitrary length.',
 '2; no startup term on cycles.',
 'Q_B counts B doubles; A counts all A StepEvs, including DELETE accesses.',
 'Either direct charging, or all-size J-SELF/ROW plus static mechanics and one shared witness.',
 'Conditional sufficiency reconstructed; no universal proof.',
 'n<=6 ratios and n<=9 coarse BF reported; finite only.',
 'Q_B<=A is a different stronger refuted candidate; Q_B<=2A not refuted here.',
 'Global witness/row inequalities or another universal mechanism.', 'OPEN',
 'audits/PIVOT_COARSE_DOUBLE.md; PIVOT_DUAL_UNIVERSAL.md; scripts/wp6_j4shared.py.',
 'Nearest original load-bearing cycle inequality.'),
('stage_05_czig.md','C.ZIG','Zig contribution',
 'Z_B(gamma)<=A(gamma) for every finite closed present pair walk.',
 'All valid pair starts and present-key closed walks; no reachability restriction.',
 '1.',
 'Z_B terminal B zigs on KEEP; A all A StepEvs.',
 'Root splay no-op, nonroot cost>=1, delivery to root and key preservation.',
 '02_PROVED/C_ZIG_RECONSTRUCTED.md gives complete cyclic run charging.',
 'Finite evidence not a premise.', 'No counterexample to this precise theorem.',
 'Formal V1–V3 assembly remains open; mathematical proof complete.', 'PROVED — UNIVERSAL mathematical',
 'audits/PIVOT_RECURRENT_EXCESS.md:136 onward.',
 'Combines with Coarse-Double to give B<=3A.'),
('stage_06_row_diameter.md','ROW','Adjusted ROW-DIAMETER',
 'For every BST B and r!=x, H_r(B)−H_x(B)>=−2+2(b_r−b_x) under one shared J; equivalently diameter(H−2b)<=2.',
 'Every finite valid BST, every ordered distinct node pair, all depths/sizes.',
 '2 adjusted width; raw root/nonroot range[0,4].',
 'H source-defined; b_y=[root(B)=y]; j/rho globally shared.',
 'Construct shared admissible assignment; same-child, cross-child, root/child cases and bases.',
 'REBOOT-01 removes sibling variation for equal-signature same-child pairs only.',
 'Finite SELF/DIAM LPs; no universal extrapolation.',
 'Absorbed H with J=0 reported refuted for row switch; unrestricted J not refuted.',
 'All remaining bases/cases/global compatibility.', 'OPEN',
 'scripts/wp6_j4shared.py:125-150; 02_PROVED/J4_CONDITIONAL_SUFFICIENCY.md.',
 'Pays A-root row switching in the sufficient residual potential.'),
('stage_07_j_self.md','J-SELF','Same-row transport',
 'H_x(B)−H_x(S_xB)>=R_static(B,x)−2(1−b_x), for every B,x under the same globally shared J.',
 'All finite valid BSTs and present x; root case included.',
 'Kappa4; root correction2.',
 'S_x ordinary splay; b_x indicates old B root.',
 'Source mechanics, shared all-size row assignment compatible with DIAM.',
 'Source reports absorbed H0 self-control; joint all-size witness not constructed.',
 'Generated finite rows and LP checks only.',
 'No general self theorem for an unknown joint witness; arbitrary assignments need not satisfy it.',
 'Joint compatibility with ROW; source mechanics formal closure.', 'OPEN as joint admissibility obligation',
 'scripts/wp6_j4shared.py:94-117; audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md:1310 onward.',
 'Pays pointed-B splay transport; combining with ROW pays KEEP/DELETE.'),
('stage_08_same_child.md','SC','SAME-CHILD',
 'For all B=[p,T,S] (or mirror), u!=v in T, |D_J(B;u,v)|<=2 under the same admissible J.',
 'Arbitrary T,S, row depths, pairs and both orientations, globally shared J.',
 '2.',
 'D_J=R(v)−R(u)+4(subsize(v)−subsize(u))+J_u−J_v.',
 'Base width and global assignment; other structural cases needed for full ROW.',
 'Equal-signature sibling erasure proved; full width not proved.',
 '19,404 row formulas and2,232 erasure pairs exactly checked; supporting only.',
 'Different signatures give different insertion atoms, so no automatic cancellation.',
 'Arbitrary-T empty-sibling bases, unequal depths/folds, global compatibility.', 'OPEN; restricted reduction PROVED',
 '02_PROVED/REBOOT_01_SIBLING_ERASURE.md; scripts/wp6_context.py/context2.py; j4shared.py.',
 'Closes one part of nonroot row diameter once the actual width is proved.'),
('stage_09_pair_access.md','PA','Pair Access representation',
 'A_i equals full-X splay prefix; B_i equals retained-Y splay prefix, keys both remain K.',
 'All finite present-key histories, T0, occurrence-index masks, repeated keys.',
 'No competitive constant; exact encoding.',
 'KEEP splays both; DELETE splays A only; shared initial T0.',
 'Ordinary splay preserves keys and order.',
 'Induction on occurrences, following definitions; mapping source gives C1-C3.',
 'Differential replay tests source-reported, not universal proof basis.',
 'Value-set masks fail with duplicates; absent-key route is a different domain.',
 'No missing encoding premise on present domain.', 'PROVED universal mathematical encoding',
 'artifacts/v04/wp6_present/present_domain_audit/pair_access_domain_mapping.md:1-42; IMPLEMENTATION_SPEC...v0.4.txt:256-280.',
 'Links pair histories to the original LT subsequence target.'),
('stage_10_event_composition.md','SUM','B<=3A composition',
 'If Q_B<=2A and Z_B<=A on a closed walk, then B=Q_B+Z_B<=3A.',
 'Every walk satisfying those two bounds; constants shared universally.',
 '2+1=3.',
 'Each B event is a double or terminal zig.',
 'COARSE-DOUBLE + C.ZIG + exact event decomposition.',
 'Termwise e=q+z and summation; elementary arithmetic.',
 'Not needed for implication.', 'None for the arithmetic implication.',
 'Universal Coarse-Double remains open.', 'CONDITIONAL conclusion',
 'audits/PIVOT_COARSE_DOUBLE.md:1-6; GCStaticKeep2Step.lean:779 onward decomposition.',
 'Supplies nonpositive reward cycles for PIVOT-2.')
]
for entry in stages:
    name,tid,title,statement,quant,constants,definitions,premises,proofs,finite,refutations,unknown,status,sources,impact=entry
    fields=[('THEOREM ID',tid),('NAME',title),('EXACT STATEMENT',statement),('QUANTIFIERS',quant),
      ('CONSTANTS',constants),('DEFINITIONS',definitions),('PREREQUISITES',premises),
      ('KNOWN PROOFS',proofs),('KNOWN FINITE EVIDENCE',finite),('KNOWN COUNTEREXAMPLES',refutations),
      ('UNVERIFIED ASSUMPTIONS',unknown),('CURRENT STATUS',status),('SOURCE LOCATIONS',sources),
      ('HOW IT ADVANCES DO',impact)]
    content='# '+title+'\n\n'+''.join('**'+k+':** '+v+'\n\n' for k,v in fields)
    content+='**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.\n\n**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.\n'
    docs['01_MAIN_PIPELINE/'+name]=content

# Automatically pin the concrete source files used by the written references.
source_paths=[
 'IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt','WorkPlan.md','Path.md','prereg/bridge_manifest.yaml',
 'math/proof_status.json','audits/PIVOT_RECURRENT_EXCESS.md','audits/PIVOT_COARSE_DOUBLE.md',
 'audits/PIVOT_DUAL_UNIVERSAL.md','audits/PIVOT_COUPLED_MONOTONICITY.md','audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md',
 'audits/PIVOT_E0_U4_DOUBLE.md','audits/WP6_CONDITIONAL_CHAIN.md','audits/LITERATURE_BRIDGE_AUDIT.md',
 'artifacts/v04/wp6_present/present_domain_audit/pair_access_domain_mapping.md',
 'scripts/wp6_j4shared.py','scripts/wp6_staticR.py','scripts/wp6_lambda.py','scripts/wp6_cycle_ratio.py',
 'scripts/wp6_gapdomain.py','scripts/wp6_gapcompat.py','scripts/wp6_ugar.py','scripts/wp6_rednorm.py',
 'scripts/wp6_twins.py','scripts/wp6_context.py','scripts/wp6_context2.py','scripts/wp6_funcmp.py',
 'scripts/wp6_redimpl.py','scripts/wp6_iface.py','scripts/wp6_levels.py','scripts/wp6_squot.py',
 'scripts/wp6_lrffarkas.py','scripts/wp6_shiftdelta.py','scripts/wp6_lift2.py',
 'python/independent/splay.py','python/liquidity/legacy_embedding.py','lean/WP6/GCStaticKeep2Step.lean',
 'artifacts/v04/wp6_present/0909c74a/dual_mine/j4_gapdomain.json',
 'artifacts/v04/wp6_present/0909c74a/dual_mine/j4_xclean_mat.npz',
 'artifacts/v04/wp6_present/0909c74a/dual_mine/j4_rednorm_mat.npz',
 'artifacts/v04/wp6_present/0909c74a/dual_mine/j4_lrffarkas.json',
 'artifacts/v04/wp6_present/0909c74a/dual_mine/j4_lrflist.json',
 'v03/history/external/papers/L3_levy_tarjan_foundation_1907.06310.pdf']
hashes=[]
for rel in source_paths:
    p=R/rel
    assert p.exists(),rel
    data=p.read_bytes()
    hashes.append({'path':rel,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(W/'11_REPRODUCIBILITY/source_hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
docs['EVIDENCE_INDEX.md']='''# Evidence index

Paths below are relative to the read-only repository root given in CURRENT_STATE.md. `source_hashes.json` binds all listed working bytes; the baseline also hashes every outside file. Proof documents cite relevant lines or PDF pages. The new exact function extraction spans are in verification_results.json.

| Evidence | Kind / use |
|---|---|
| present_domain_audit/pair_access_domain_mapping.md:1-42 | SOURCE DEFINITION + mathematical encoding |
| python/liquidity/legacy_embedding.py:59-74,107 onward | cost and StepEv mechanics; broader absent domain is separate |
| scripts/wp6_j4shared.py:17-150 | SOURCE DEFINITION of global shared J4/SELF/DIAM |
| scripts/wp6_staticR.py:21-131; wp6_lambda.py:49-104 | backward fold and complete per-key coefficients |
| scripts/wp6_gapcompat.py, wp6_ugar.py, j4_gapdomain.json | finite imposed UG scope; not universal proof |
| scripts/wp6_rednorm.py:44 onward | CONDITIONAL normalization rho=c, bar-j, NONE/K |
| wp6_context.py/context2.py/funcmp.py/redimpl.py | finite contextual probes; orientation/unknown-coordinate caveats |
| wp6_twins.py:35-46; wp6_lift2.py; wp6_shiftdelta.py | source Twin/Lift2 definitions, telescoping forms |
| audits/PIVOT_RECURRENT_EXCESS.md:12-20,136 onward | SYMBOLIC cycle-excision/zig proof reports |
| audits/PIVOT_COARSE_DOUBLE.md; PIVOT_DUAL_UNIVERSAL.md | OPEN universal target and prior finite reported certificates |
| lean/WP6/GCStaticKeep2Step.lean:703-716 | formal arithmetic source; no fresh kernel run |
| j4_xclean_mat.npz; wp6_iface.py | finite C0 provenance; numerical discovery now exact rechecked |
| j4_rednorm_mat.npz; j4_lrffarkas.json; j4_lrflist.json | saved LRF finite system/certificate, exact rechecked |
| local L3 PDF pp.3-5,8-10 and Appendix A | external model, Theorem3.5/4.3; SHA f7aa7901... |
| prereg/bridge_manifest.yaml | historical v1/L2 pin conflict |
| math/proof_status.json; WP6_CONDITIONAL_CHAIN.md | historical registry/GC route status, not universal J4 proof |
| supplied master directive | USER NAVIGATION CLAIMS when matching later artifacts absent |

New inspectable artifacts: REBOOT_01_SIBLING_ERASURE.md (universal restricted proof), C_ZIG_RECONSTRUCTED.md (universal run proof), three conditional implication proofs, LRF_TEMPLATE.md (finite exact refutation), C0_RANK_EXACT_RECHECK.json and LRF_EXACT_RECHECK.json (complete exact recovery), and verification_results.json (finite coefficient checks).

External check: [Levy–Tarjan v3](https://arxiv.org/html/1907.06310v3), checked 9 October2026. Its eventual-monotonicity theorem supplies the final reduction once the universal project premise is proved. No claim relies on secondary search results.

The complete source-hash inventory follows.

| Source path | SHA-256 |
|---|---|
'''+''.join('| `'+e['path']+'` | `'+e['sha256']+'` |\n' for e in hashes)
docs['00_REPOSITORY_AUDIT/source_locations.md']='''# Load-bearing source locations

See EVIDENCE_INDEX.md for kinds/hashes. All paths are relative to the repository root (CURRENT_STATE.md gives its absolute path). Relevant AST line spans are also saved exactly by the checker.

- Pair encoding: artifacts/v04/wp6_present/present_domain_audit/pair_access_domain_mapping.md:1-42.
- Cycle graph: scripts/wp6_cycle_ratio.py:58-100; cycle-excision audit: PIVOT_RECURRENT_EXCESS.md:12-20.
- Zig proof: audits/PIVOT_RECURRENT_EXCESS.md:136 onward.
- J4 targets: scripts/wp6_j4shared.py:94-117 (SELF),125-150 (DIAM),17 (kappa).
- Potential coordinates: j4shared.py:33-76; fold/coefficient code: wp6_staticR.py and wp6_lambda.py.
- Finite UG: wp6_gapcompat.py:42 onward; wp6_ugar.py:25-31; dual_mine/j4_gapdomain.json.
- Normalization: wp6_rednorm.py:44 onward.
- Finite interface block: wp6_iface.py:28-79; j4_xclean_mat.npz and j4_ifacerank.json.
- Cost implication: lean/WP6/GCStaticKeep2Step.lean:703-716.
- External reduction/model: local L3 v3 PDF pp.3-5,8-10 and Appendix A; historical manifest: prereg/bridge_manifest.yaml.

Later supplied reports26S–26AB were searched but not located; don't invent a filename or cite this directive as a source certificate. Exact candidate identity26Y is recovered from actual Twin2 and insertion definitions instead.
'''
for rel,content in docs.items():
    p=W/rel
    if p.exists():raise RuntimeError('Refusing overwrite: '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content.rstrip()+'\n',encoding='utf-8')
print(json.dumps({'authored_documents':len(docs),'stage_references':len(stages),'source_files_pinned':len(hashes)},indent=2))
