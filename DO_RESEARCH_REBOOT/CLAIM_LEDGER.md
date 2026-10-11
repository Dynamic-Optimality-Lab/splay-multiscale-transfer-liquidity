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
| C10 | One-splay depth displacement d'(r)<=d(r)+2, all present keys | PROVED universal (frame joining/re-carry argument) | 26AL_generalized_signed_repayment.md; 154126-trial corroboration |
| C11 | Generalized (G) + signed (S) delayed-repayment restricted theorems | PROVED universal conditional (capacity/signed arithmetic + disjointness) | 26AL_generalized_signed_repayment.md |
| C12 | Strict same-side closed-walk coverage (17-access n=7 witness, triple +1/0/-3) | PROVED finite-exact closed walk + universal-theorem membership | 26AL_postgate_strict_novelty_certificate.md; engine comparison 21/21 |
| C13 | Double-positive four-block packet: universal signed theorem + global packet theorem + 8-key 13-access witness (+1,-1,+1,-4), strict extension beyond 26AM-G | PROVED universal + finite-exact closed walk + novelty audit | 26AN_double_positive_packet_repayment.md; 26AN_vine8_witness_certificate.json; engine comparison 18/18 |
| C14 | Consecutive-positive four-block packet (+1,+1,-1,-3) + two-order theorem with deterministic DP recognizer + 10-key 18-access witness, strict extension beyond 26AN | PROVED universal + finite-exact closed walk + machine-checked novelty | 26AO_order_expanded_double_positive_repayment.md; 26AO_ten_key_witness_certificate.json; 26AO_recognizer_audit.json; engines 27/27 |
| C15 | Variable-length bulk repayment (p unit positives + return a>=p) + O(m) cut-independent recognizer + 16-key 29-access p=3 witness (+1,+1,+1,-4), strict extension beyond 26AO | PROVED universal (all p>=1) + finite-exact closed walk + banked-26AO rejection | 26AP_variable_length_bulk_repayment.md; 26AP_vine16_witness_certificate.json; 26AP_recognizer_selftests.json; 26AP_26AO_rejection_certificate.json; engines 38/38 |
| C16 | Shallow-bridge cross-run repayment (p1+p2>=3, bridge -1 cancels depth-tax +1) + mixed exact-cover recognizer + 16-key 30-access witness (+1,+1,-1,+1,-6), strict extension beyond 26AP | PROVED universal (all p1,p2>=1) + finite-exact closed walk + banked-26AO/26AP rejection | 26AQ_shallow_bridge_cross_run_repayment.md; 26AQ_vine16_witness_certificate.json; 26AQ_recognizer_selftests.json; 26AQ_26AO/26AP_rejection_certificates.json; engines 39/39 |
| C17 | Essential split-sink allocation (p>=3 run, two distinct sinks r!=s, independent dA thresholds, AR-P8) + ARmix recognizer + 16-key 37-access witness (+1,+1,+1,-2,-2, essential), strict extension beyond full AJ-AQ union | PROVED universal (all p>=3) + finite-exact closed walk + 3 banked rejections | 26AR_essential_split_sink_allocation.md; 26AR_vine16_closed_witness.json; 26AR_recognizer_selftests.json; 26AR_26AO/26AP/26AQ_rejection_certificates.json; engines 53/53 |
| C18 | Coupled straddling displacement (pair +2, universal) + dual-push eligibility + parity-corrected Hall allocation + ASmix recognizer (AP/AQ/AR preserved) | PROVED universal restricted theorems; strict novelty NOT certified (complete 14742-hunt negative) | 26AS_source_derived_shared_credit_allocation.md; 26AS_coupled_root_universal_proof.md; 26AS_search_manifest.json; 26AS_bounded_search_summary.json |
| U-B | DIRECT-U1: C1/M authoritative failures; no invariant candidate (parametric obstruction); 3 strictly-uncovered closed walks (W<=0); n=7 truncated screen negative | Coverage gap CERTIFIED; universal proof OPEN; no W>0 walk found | DIRECT_U1_universal_coverage_global_invariant_audit.md; DIRECT_U1_uncovered_closed_witness.json; DIRECT_U1_n7_reachability_results.json |
| CWC-C1 | DIRECT-CWC: frozen ECT cut-expansion REFUTED by certified deficient cut (tok16, K15 pair (7,6), 1>0) on U1 gap walk (W=-96); 2/3 gaps fully allocate (not promoted) | Transport conjecture FALSE; universal OPEN; no counterexample | DIRECT_CWC_global_closed_walk_conservation_report.md; DIRECT_CWC_first_deficient_cut.json; DIRECT_CWC_frozen_spec_hash.json |
| RT2-A | DIRECT-NFKS-RT2: root-return conservation (RT2 +2, universal) + idempotence + depth-4 + Coarse-Double for <=3 KEEP keys (arbitrary n/length/DELETEs) | PROVED universal restricted class; 52362-config regression clean; nonvacuity walk certified | DIRECT_NFKS_RT2_three_keep_key_coarse_double.md; DIRECT_NFKS_RT2_regression.json; DIRECT_NFKS_RT2_nonvacuity_replay.json |
| CDK4-A | DIRECT-CD-K4: marked-core compression (K4-L1+pruning+7-node) + 68876-case one-bit certificate + Coarse-Double for 4 KEEP keys (<=4 with RT2-A) | PROVED universal restricted class; finite cert 0 viol / 0 eng-mismatch | DIRECT_CD_K4_four_keep_key_coarse_double.md; DIRECT_CD_K4_finite_verification.json; DIRECT_CD_K4_Gate0_uncovered_four_key_witness.json |
| CDK5L-A | DIRECT-CDK5-LOW: nine-bound + conserved closed cores + 142385-edge 0/1-potential certificate + Coarse-Double for 5 KEEP keys with core<=8 | PROVED universal restricted class; independent verification PASS; 9-core obstruction stands | DIRECT_CDK5_LOW_five_key_submaximal_core.md; DIRECT_CDK5_LOW_potential_certificate.json; DIRECT_CDK5_LOW_independent_verification.json |
| CDK5NP-A | DIRECT-CDK5N-DP: nine-core distinct-key prepayment (Type K/P interval charging) for 5 KEEP keys with nine-core | PROVED universal restricted class; witness 29/18/8 strictly outside all prior domains | DIRECT_CDK5_NINE_distinct_key_prepayment.md; CDK5NP_verification_results.json; CDK5NP_novelty_regression.md |
| CDK5NS1P-A | DIRECT-CDK5N-S1: one-successor transfer (exception w=1/R=0 + successor w<=1/R>=2) for 5 KEEP keys with nine-core | PROVED universal restricted class; witness 33/18/8 strictly outside all prior domains | DIRECT_CDK5_NINE_one_successor_transfer.md; S1P_verification_results.json; S1P_novelty_regression.md |
| CDK5NS2P-A | DIRECT-CDK5N-S2: two-successor reserve transfer (exception + creditless + paying second) for 5 KEEP keys with nine-core | PROVED universal restricted class; witness 29/18/8 strictly outside all prior domains | DIRECT_CDK5_NINE_two_successor_transfer.md; S2P_verification_results.json; S2P_novelty_regression.md |
| CDK5NVRP-A | DIRECT-CDK5N-VR: variable-length creditless relay (exception + t>=2 bridges + payer) for 5 KEEP keys with nine-core | PROVED universal restricted class; witness 31/18/8 strictly outside all prior domains | DIRECT_CDK5_NINE_variable_creditless_relay.md; VRP_verification_results.json; VRP_novelty_regression.md |
| CDK5NMRP-A | DIRECT-CDK5N-MR: disjoint multi-exception relays (complete E + maximal scans + disjoint packets) for 5 KEEP keys with nine-core | PROVED universal restricted class; witness 55/36/16 strictly outside all prior domains | DIRECT_CDK5_NINE_multi_exception_relay.md; MRP_verification_results.json; MRP_novelty_regression.md |

| CDK5NMSP-A | DIRECT-CDK5N-MSINK: mixed-relay shared-sink repayment (joint H4-H5 sink + strict K/P others) for five-key nine-core | PROVED universal restricted class; IN 788b459d (64/36/16, E=[4,12], t=(0,2), sink p=0 H=13) in S/R5*; OUT b8b02be7 (55/36/16, t=(2,2)) residual; recursive C* novelty (19+1 subproblems, 0 budget hits, two independent engines agree) | DIRECT_CDK5_NINE_mixed_relay_shared_sink.md; DIRECT_CDK5N_COMP_MSINK_PROOF_RCG0/PROOF_four_rule_verdict.md; PROOF_negative_certificates.json |
| CDK5NDLSP-A | DIRECT-CDK5N-DLSS: dual-long-relay shared-sink repayment (joint H4-H5 sink + strict K/P others) for five-key nine-core | PROVED universal restricted class; IN b8b02be7 (55/36/16, E=[4,12], t=(2,2), sink p=0 H=18) in S/R5*; OUT a7c6504c (56/36/16, |E|=1) residual; recursive C21* novelty (primitive roots, 0 budget hits, two independent engines agree) | DIRECT_CDK5_NINE_dual_long_shared_sink.md; DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/DLSSP_four_rule_verdict.md; DLSSP_negative_recursive_certificates.json |
No universal source claim is upgraded merely because a JSON field says VERIFIED/REVIEWED, a float LP returns feasible/infeasible, or a report calls its result PROVED. Missing numerical report provenance is an evidence gap, not a mathematical disproof.
