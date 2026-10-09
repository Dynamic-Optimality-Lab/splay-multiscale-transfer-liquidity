# Source-backed claim ledger

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
