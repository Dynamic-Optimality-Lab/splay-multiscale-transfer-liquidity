"""Publish source-grounded audit metadata; never execute research engines."""
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
FSROOT = Path("\\\\?\\" + str(ROOT))
PRIMARY = json.loads((OUT / "semantic_chunks.json").read_text())["cd_internal"]
P5 = "DO_RESEARCH_REBOOT/CD5_BASE01/"
P6 = "DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/"
P3 = "DO_RESEARCH_REBOOT/PARALLEL_ROUTE03_CD_INDUCTION_20261108_01/"
PS1 = "DO_RESEARCH_REBOOT/PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP01_20261108/"
PS2 = "DO_RESEARCH_REBOOT/PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP02_20261108/"
P4 = "DO_RESEARCH_REBOOT/ROUTE04_RELAXED_UNIVERSAL_CD_20261108/"
PC = "DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/"
F1 = PS1 + "PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP01.md"
F2 = PS2 + "PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP02_GLOBAL_COUPLING.md"
F4 = P4 + "RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md"
F31 = P3 + "PARALLEL_CD_INDUCTION_STEP01.md"
F32 = P3 + "PARALLEL_CD_INDUCTION_STEP02.md"
F33 = P3 + "PARALLEL_CD_INDUCTION_STEP03_GLOBAL_REDUCTION.md"


def evidence(path, first, last, meaning):
    return {"path": path, "line": first, "end_line": last, "meaning": meaning}


def sha(path):
    return hashlib.sha256((FSROOT / path).read_bytes()).hexdigest()


def pins(path, entry_key):
    body = json.loads((FSROOT / path).read_text(encoding="utf-8"))
    base = str(Path(path).parent).replace("\\", "/")
    records = []
    for item in body["files"]:
        target = base + "/" + item[entry_key]
        actual = sha(target)
        records.append({"path": target, "expected_sha256": item["sha256"], "actual_sha256": actual, "match": actual == item["sha256"]})
    return {"source": path, "entries": len(records), "unique_paths": len({r["path"] for r in records}), "all_match": all(r["match"] for r in records), "records": records, "scope": "publication-byte integrity only; no historical semantic computation rerun"}


claims = [
    {
        "id": "cd5_complete_support_base", "label": "CD(5): genuine KEEP support at most five",
        "statement": "For every finite ordered physical key set and every original reachable exactly paired-closed W with |G(W)|<=5, Q_B(W)<=2A(W).",
        "assumptions": "Present-key ordinary bottom-up splay; A processes KEEP and DELETE, B only KEEP; reachability from some permitted common-tree diagonal; both full labeled trees close; source itself may start nondiagonally.",
        "budget": "Q_B<=2A using the appropriate single whole-period class theorem; all ambient sizes, private populations, DELETE supports and finite lengths allowed.",
        "recorded_status": "Sealed computer-assisted symbolic assembly, same-agent separate checker; no external peer review or whole-compiler formalization.",
        "dependency_chain": "If G empty then Q=0; otherwise all KEEP targets equal G by cyclic root provenance. Marked-core set inclusion plus B closure yields fixed S and |G|<=|S|<=2|G|-1. Exhaustive leaves: <=3 marks, 4 marks, 5 marks/core<=8, 5 marks/core9.",
        "not_controlled": "Unbounded genuine KEEP support; nonclosed prefixes; a stronger uniform physical I(5) allocator at every auxiliary scope.",
        "evidence": [evidence(P5+"CD5_PROOF.md",5,25,"Exact theorem/domain/costs"), evidence(P5+"CD5_PROOF.md",86,128,"Exhaustive class assembly and trust limits"), evidence(P5+"RESULT.md",31,37,"Sealed result and remaining uniform extension")]
    },
    {
        "id": "cd6_complete_support_base", "label": "CD(6): genuine KEEP support exactly six",
        "statement": "For every original admitted closed W with exactly six genuine KEEP target keys, an explicit total injection from full B-double occurrence IDs into two original A accounting bits per StepEv gives Q_B<=2A.",
        "budget": "Two accounting bits per original A StepEv. Select ONE whole-period backend from fixed B core sizes 6..11; its independent source witness has working bound <=11 within Bank25=25.",
        "dependency_chain": "Core constancy and |S|<=11 -> exhaustive 57 necessary masks -> own/predecessor/signed backends preserving same h0 -> actual occurrence bijection -> optional licensed complete-h/locked-owner exchange -> cardinality.",
        "recorded_status": "CD6_FINAL_CERTIFICATE status PROVED_COMPLETE_ORIGINAL_SIX_KEY_COARSE_DOUBLE. Historical 2746 input pins and separate immutable implementation accepted by same agent; not formal/external review.",
        "not_controlled": "A universal source-credit premise for arbitrary support, all-r I(r), or an owner map invented on an auxiliary domain absent from its original contract.",
        "evidence": [evidence(P6+"CD6_THEOREM.md",3,54,"Theorem and distinction between scalar and stronger owner scope"), evidence(P6+"FULL_PROOF.md",16,79,"Actual source construction and accounting"), evidence(P6+"FROZEN_OWNER_COMPATIBILITY.md",33,48,"Owner retirement and raw versus stronger interface")]
    },
    {
        "id": "uniform_physical_transfer_conditional", "label": "Uniform transfer is conditional on source credit",
        "statement": "I(r-1)+E_r implies I(r), and I(r) implies CD(r), when E_r supplies an independently source-proved disjoint seed law or valid owner-inclusive signed packet law, exact alignment and Bank25-compatible storage.",
        "budget": "License B: 2c_e-Q_e+D_r(t)-D_r(s)>=0, D_r in [0,K_r], natural h0 owners among chosen 2c_e bits. K_r+2max c_e<=25 is a sufficient working bound, not an established all-r fact.",
        "recorded_status": "U-B sufficient transfer proved in source record; universal source hypotheses OPEN. Stronger I(5) cannot be deduced from scalar CD5.",
        "first_missing_implication": "Arbitrary original larger-support geometry -> independent source supply/sign license with complete coverage and permitted physical storage. Uniform representation and owner exchange do not establish supply.",
        "evidence": [evidence(P6+"UNIFORM_R_TRANSFER.md",9,89,"Precise noncircular licenses and transfer"), evidence(P6+"UNIFORM_R_TRANSFER.md",107,149,"Uniform active-frame reduction, <=2r+2H-3 known nodes"), evidence(PC+"ROUTE2_CD6_FUNDING_GATE_VERDICT.md",180,221,"Deep-pair grouping is only a first bridge, not universally sufficient by itself")]
    },
    {
        "id": "fixed_carry_gamma_obstruction", "label": "Gamma_r refutes unchanged bounded carry",
        "statement": "The modified Gamma_r original qmax/q1 packet has H=2,Q=r, so any local signed law on those unchanged packets needs width>=r-4. The complete original paired-closed source has A=6r,Q_F=6r-6.",
        "consequence": "Width3 fails r>=8. Original natural h0 uses 3/4 local bits and leaves r-3 residual demands with only one local spare; incoming carry>=r-4 exceeds Bank25 at r>=30. This falsifies that fixed-packet carry extrapolation, not CD(r), aggregate O(A), or all packet/grouping architectures.",
        "evidence": [evidence(P6+"UNIFORM_R_TRANSFER.md",151,179,"Exact parameterized obstruction and scope"), evidence(PC+"ROUTE2_CD6_FUNDING_GATE_VERDICT.md",149,164,"Original full-demand rule is not automatically g1 residual F")]
    },
    {
        "id": "internal_neutral_exact_accounting", "label": "Exact internal-neutral residual and inventory",
        "statement": "For Psi=|J_S(B)\\J_S(A)| with SET labels, 2A=P+N+T_A+V_A and P=N+B1+2B2+Z1. Therefore 2A-Q_B=2N+T_A+V_A+B2+Z1-B0.",
        "budget": "ND35 pays every nonneutral double using its first-decrease lambda upcrossing. ZRC35 pays every neutral LAST double using its following decreasing terminal B zig. PC35 then pays same-access releases: F has |F|=sum(B0_t-B2_t-Z1_t)_+, and raw complement R1 has |R1|=2N+T_A+V_A+sum(B2_t+Z1_t-B0_t)_+.",
        "first_missing_implication": "A source-uniform augmentation/cost law for the literal surviving strictly internal neutral occurrences. |R1|-|F|=2A-Q is an identity and cannot be reintroduced as a new solved solvency lemma.",
        "recorded_status": "ND35/ZRC35/PC35 recorded scopes are raw whole-period source accounting; later symbolic comparisons have their own pending audit flags. Raw normalization is not stronger frozen-owner permission.",
        "evidence": [evidence(F1,40,73,"Conservation and physical/accounting distinction"), evidence(F1,90,160,"gZ and PC35 disjoint exact partition"), evidence(PC+"ND35_COMPLEMENT_08/EXACT_OPEN_OBSTRUCTION.md",7,26,"Uniform completed classes and exact open child")]
    },
    {
        "id": "chain_boundary_structure", "label": "Boundary-switch chains have no branching",
        "statement": "Every selected opposite-boundary neutral-output history has a unique last B parent switch; the selector is globally injective. Designated-output continuations form disjoint same-producer chains with strict label inclusion and exact co-consumption/near-side attachment.",
        "budget": "One B rotation can be one such switch; at most two per B double. This is no A-work bound by itself. Arbitrary-length descending-scan chains refute constant demand per chain endpoint.",
        "recorded_status": "Symbolic/self-reviewed, independent-audit pending.",
        "evidence": [evidence(F1,237,314,"Switch uniqueness, chain theorem and attachment"), evidence(F1,358,382,"Unbounded complete-source family and restricted refutation")]
    },
    {
        "id": "producer_child_work_class", "label": "Producer-child transitions have global A multiplicity one",
        "statement": "On unacquired designated outputs currently directly attached to their original B producer, each actual producer-flag transition is a real zero A rotation, and choosing one transition per demand is globally injective across producers, sides and runs: |T|<=T_A.",
        "budget": "Activated erasures are quiet and unused under exact g_pre; decreasing reverse switches force activation and two distinct actual A rotations, yielding |D|<=A. Cross-access inner links have a separate aggregate <=2A bound. Recognized complete descending scans supply 2L distinct nonpositive real A units, disjoint from producer-child transitions. Counts of overlapping certificates are not added as new physical capacity.",
        "literal_complement": "Producer-silent same-access bursts; cross-access neutral reattachments whose A root avoids the interval and later jumps across it with potentially shared positive work; producer-near-side demands already flagged at every attachment entry; larger maps' actual outside owners/reservations.",
        "recorded_status": "New symbolic scope, independent-audit pending. Explicit h_cov covers only its declared domain; source COV is not proved necessary or universal.",
        "evidence": [evidence(F2,187,208,"Cross-access <=2A cost association; units may be owned"), evidence(F2,210,284,"Quiet erasures and exact raw payment"), evidence(F2,333,408,"Mixed zero-transition theorem, occupied L6 owner descent, silent complement"), evidence(F2,611,690,"Scan separation and independently defined covered comparison"), evidence(F2,728,774,"Exact missing cases and audit status")]
    },
    {
        "id": "guarded_detour_reduction", "label": "Guarded detour deletion has positive signed price",
        "statement": "Two adjacent constant-target runs z then y, each containing KEEP, with z child and y in one of three exact admitted frames in BOTH actual A and full B, admit deletion of the z run. Complete endpoints agree; A_hat=A-m and Q_hat=Q-sum beta, beta in {-1,0,1}.",
        "budget": "Delta(W)=Delta(W_hat)+sum(2-beta) with local prices 3,2,1. Shadow A inventories inject into original units, omitting distinct first-z events. Full coverage of one key yields a smaller-support source; partial deletion only reduces length.",
        "recorded_status": "Analytic author-checked source theorem, not new independent/formal certification.",
        "not_controlled": "No universal availability, favorable-key, or nonnegative sign theorem on packet-free sources. Changing erased seeds changes E, not original full source guards.",
        "evidence": [evidence(F32,198,227,"Exact inspectable guards"), evidence(F32,294,445,"Source/price proof and owner limitation"), evidence(F33,485,539,"Fixed-key guard tests imply disjoint complete cover")]
    },
    {
        "id": "guarded_induction_universal_barrier", "label": "Deep accesses and maximal cores escape guarded induction",
        "statement": "Every original full-B KEEP of depth>=3, with complete A/F pre-state and charge, survives every guarded detour rewrite. All closed sources of s genuine keys and maximal core 2s-1 have even positive genuine KEEP depth, so contain no depth-one guarded packet.",
        "witness": "Arbitrary-fringe diagonal all-KEEP W_s=K3 K5 ... K(2s-1) K(2s-3) ... K3 K1 is exactly closed, all genuine depths2, A=Q=C=2s-2, positive slack2s-2. It refutes universal packet availability and automatic support drop, not the negative-source-only implication.",
        "quantitative_invariant": "E_src=A-C and D_deep=sum(q-2)_+ are invariant under rewrites; only shallow surplus is removed. A negative source must have q>=3 (depth>=6), a permanent occurrence. Thus this rewrite alone does not address its deep deficit.",
        "first_missing_implication": "A minimum negative original source has an eligible source reduction, or every irreducible source (including all maximal-core sources) has nonnegative slack. This is unproved, not supplied by well-founded termination.",
        "evidence": [evidence(F33,228,361,"Deep permanence and quantitative invariants"), evidence(F33,365,416,"Source-uniform maximal-core obstruction and actual complete family"), evidence(F33,570,635,"First missing implication and failure of routine induction")]
    },
    {
        "id": "phase_seed_exact_scope", "label": "Erased recurrent price depends on reached seed",
        "statement": "Transporting an actual recurrent erased orbit across a cyclic cut preserves normalized erased cost. Starting erasure afresh from another reached FULL state is a different source and can select a different recurrent orbit and charge.",
        "witness": "For all k>=4,m>=1, explicit arbitrary-fringe W_(m,k)=P^m C_k on k+3 genuine keys has Q_F=2m. One erased-p seed has Q_E=0,D=0,J=2m after warmup; another reached seed has Q_E=Q_F=2m,D=J=0. An all-KEEP diagonal realization has A=6m+2k and is CD-safe.",
        "consequence": "A smaller erased core need not give a smaller signed marginal. More legal comparison choices do not prove a favorable universal choice.",
        "evidence": [evidence(F31,258,323,"Actual-orbit transport and fresh phase seeding"), evidence(F31,324,546,"Complete free-term family and exact scope"), evidence(F31,573,604,"Missing universal source-complete signed repayment theorem")]
    },
    {
        "id": "aggregate_exposed_frame_class", "label": "Whole-frame exposure gives Q<=4A+u",
        "statement": "For each neutral double use its proper whole grandparent frame, unique preceding B creator and prior removal. Exposed means A-present at some snapshot from that preceding removal through current post-A/pre-B birth. Real A SET-creation and following loss selectors have global multiplicity one each. Thus e<=R_A<=2A; all nonneutral doubles <=2A; Q_B<=4A+u for independently defined unexposed neutral count u.",
        "budget": "Real A rotation count R_A=2A-V_A. No owner vacancy or unused donor premise. Each selected rotation supplies at most one creation role and one loss role; exact union cardinality is retained. Nested exposed-frame collections have e<=A.",
        "recorded_status": "Symbolic source-uniform derivation, no external/formal audit and no finite-C conclusion. u/A boundedness remains equivalent to full relaxed CD, so its assertion alone is no new proof.",
        "evidence": [evidence(F4,379,415,"Nonneutral bound and honest support-dependent Q<=(r-1)A"), evidence(F4,426,507,"Exact independent exposure predicate, global uniqueness and residual inequality")]
    },
    {
        "id": "relaxed_aggregate_owner_bypass", "label": "Aggregate constants bypass owner vacancy",
        "statement": "If a concrete source-defined class selector maps its demands into REAL A rotations with global multiplicity at most k, then class size<=k R_A<=2kA, even if those rotations already pay old demands. A finite exhaustive partition of such independently controlled classes sums their constants honestly.",
        "assumptions": "Concrete eligibility; universal coverage or a separately controlled literal complement; bounded GLOBAL multiplicity on complete original sources including recreation, repeated demand and cyclic closure.",
        "not_required_for_scalar_bound": "Extending old g1/fE/h0 injections; owner vacancy; a physical carry trace under Bank25; exactly coefficient2. Existing physical owners remain unchanged.",
        "not_permitted": "Calling kA new physical bits; using virtual A zig accounting units as real rotation credit; summing a variable number of uncontrolled classes; inferring globally bounded congestion from per-demand witness existence.",
        "evidence": [evidence(F4,342,375,"Exact aggregate relaxation and limits"), evidence(F4,495,525,"Ownership-free count and coverage still open")]
    },
    {
        "id": "relaxed_cd_do_bridge", "label": "Any absolute coarse-double constant suffices for DO",
        "statement": "If some absolute C bounds Q_B<=CA on EVERY original diagonally reachable closed source at all supports and starting trees, C.ZIG gives B<=(C+1)A. Reachable-cycle excision gives E_B<=(C+1)S_A+g(T0), g=(Cat_n^2-1)floor(n/2). Exact LT cost conversion gives eventual monotonicity with universal multiplier, hence external Levy-Tarjan Theorem4.3 yields DO.",
        "constants": "Conservative L(Y,T0)<=(2C+3)L(X,T0)+2g(T0); stronger C+2 multiplier available in same proof. C need not be2. g may depend arbitrarily on the fixed initial tree, not source/mask/sequence length.",
        "converse": "Eventual monotonicity with universal b and tree-only overhead implies relaxed CD with C=3b/2 after cyclic same-target-run normalization and repeating a reachable paired-closed word. Thus finite-C existence is equivalent to DO in the audited model, subject to the external characterization and exact source assumptions.",
        "recorded_status": "Conditional downstream implications and converse are source-recorded symbolic proofs. External paper not independently browsed/reverified in this subtask; parent must verify precise citation/model. No DO proof supplied because universal finite-C premise is open.",
        "evidence": [evidence(F4,139,264,"Full sufficiency chain, exact costs and initialization"), evidence(F4,265,317,"Converse transfer and limitations")]
    },
    {
        "id": "historical_absolute_renewal_candidate", "label": "Historical absolute unexposed-forest renewal candidate",
        "statement": "Candidate L_h says every path in the unexposed induced whole-frame forest has at most absolute h vertices. Forest outdegree<=2 and roots<=B1+2e would yield Q_B<=(6*2^h-2)A.",
        "recorded_status": "Unproved in the Nov8 report; its implication is complete, but no established reason it holds or is easier. This subtask does not assert its current status after later EXP04/UF investigations.",
        "first_missing_implication": "Nested neutral creators, continuous A absence on full history windows and exact paired closure -> A SET exposure within an absolute number of ancestry links. Strict inclusion only gives size-dependent rank.",
        "evidence": [evidence(F4,529,649,"Exact candidate, complete conditional coefficient and failed proof step")]
    }
]

hash_checks = [pins(P5+"final_manifest.json", "file"), pins(P6+"CD6_FINAL_CERTIFICATE.json", "path")]
read_records = [{"path": p, "sha256": sha(p), "role": "primary canonical report body"} for p in PRIMARY]
duplicate = {"paths": [PS2+"PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP02.md", F2], "identical": sha(PS2+"PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP02.md") == sha(F2), "sha256": sha(F2)}
findings = {
    "audit_date": "2026-11-20", "task": "CD5/CD6, internal doubles and least-new-mathematics route assessment",
    "scope": "Source/report semantic audit and publication-byte checks only; no original semantic experiments, source-engine runs, witness replays, solver/proof-assistant or transitive proof recompilation.",
    "primary_read_count": len(PRIMARY), "primary_source_records": read_records, "duplicate": duplicate,
    "additional_reads": [
        {"path": PC+"ND35_COMPLEMENT_08/EXACT_OPEN_OBSTRUCTION.md", "coverage": "full 83-line theorem/frontier body"},
        {"path": PC+"ND35_COMPLEMENT_08/INTERNAL_NEUTRAL_RESEARCH_DOSSIER.md", "coverage": "headings, definitions, inventories, exact open conclusion and evidence register; middle mechanisms partly inspected, not full independent proof reconstruction"},
        {"path": P5+"CD5_CERTIFICATE.json", "coverage": "full certificate fields"},
        {"path": P5+"final_manifest.json", "coverage": "status and all 25 publication hashes checked"},
        {"path": P5+"independent_audit.json", "coverage": "status/scalar properties; old affine proof schemas not rerun"},
        {"path": P6+"CD6_FINAL_CERTIFICATE.json", "coverage": "full certificate fields and all 44 publication entries checked"}
    ],
    "publication_hash_checks": hash_checks,
    "claims": claims,
    "recommendation": {
        "preferred_working_route": "A source-uniform aggregate relaxed Coarse-Double bound with any absolute constant, integrating all independently controlled physical classes.",
        "reason": "Its final implication is already audited; it preserves all sharp bounded-support results while avoiding extra exact-2A allocation, vacancy, stronger physical-I(r) and Bank25 proof obligations unnecessary for scalar DO. This is a practical recommendation from existing interfaces, not a theorem of relative proof difficulty.",
        "do_not_make_primary": "Routine CD6-to-all-support guarded induction or unchanged fixed-width carry. The former cannot touch permanent deep requests and all maximal cores; the latter is quantitatively refuted by Gamma_r.",
        "smallest_concrete_unsolved_physical_issue_in_this_branch": "Preparation/restoration A work outside a same-access silent neutral-link burst, with a joint GLOBAL multiplicity bound across nested/recreated chains and near-side/outside-owner histories. The recognized descending-scan family proves one real model of such nonlocal work, not exhaustive coverage.",
        "comparison_limit": "This subtask has not audited the original MSTL Pair Access machinery or newest EXP04 UF/M1 C7 branch. Parent must compare those before final recommendation and must not treat Nov8 renewal status as latest.",
        "no_percentage": "Neither bounded support progress nor finite saved control counts imply a numerical fraction of the universal theorem remaining. Unbounded support source law is the hard missing mathematical implication."
    },
    "token_accounting": {"available": False, "graph_zero_fields_mean": "unavailable, not measured zero"}
}

nodes, edges = [], []
seen = set()


def add_node(record):
    if record["id"] not in seen:
        nodes.append(record)
        seen.add(record["id"])


def document_id(path):
    return "cd_audit_document_" + hashlib.sha256(path.encode()).hexdigest()[:12]


for p in PRIMARY:
    add_node({"id": document_id(p), "label": Path(p).stem, "file_type": "document", "source_file": p, "source_location": "1", "source_url": None, "captured_at": "2026-11-20", "author": None, "contributor": None})
for c in claims:
    first = c["evidence"][0]
    add_node({"id": c["id"], "label": c["label"], "file_type": "document", "source_file": first["path"], "source_location": str(first["line"]), "source_url": None, "captured_at": "2026-11-20", "author": None, "contributor": None, "statement": c["statement"], "recorded_status": c.get("recorded_status", "Scope-specific theorem or obstruction as recorded in source")})
    for e in c["evidence"]:
        add_node({"id": document_id(e["path"]), "label": Path(e["path"]).stem, "file_type": "document", "source_file": e["path"], "source_location": "1", "source_url": None, "captured_at": "2026-11-20", "author": None, "contributor": None})
        edges.append({"source": document_id(e["path"]), "target": c["id"], "relation": "references", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": e["path"], "source_location": str(e["line"]), "weight": 1.0, "scope_note": e["meaning"]})


def connection(a, b, path, line, description, confidence="EXTRACTED", score=1.0):
    edges.append({"source": a, "target": b, "relation": "conceptually_related_to", "confidence": confidence, "confidence_score": score, "source_file": path, "source_location": str(line), "weight": 1.0, "scope_note": description})


connection("cd5_complete_support_base", "cd6_complete_support_base", P6+"CD6_THEOREM.md",45,"Conjunction covers support<=6; not an all-support induction")
connection("cd6_complete_support_base", "uniform_physical_transfer_conditional",P6+"UNIFORM_R_TRANSFER.md",49,"Specific I(6) licenses supplied; generic transfer source hypotheses remain open")
connection("fixed_carry_gamma_obstruction","uniform_physical_transfer_conditional",P6+"UNIFORM_R_TRANSFER.md",163,"Refutes unchanged width3/packet instantiation only")
connection("internal_neutral_exact_accounting","producer_child_work_class",F2,24,"New source work controls a literal part of the original residual")
connection("chain_boundary_structure","producer_child_work_class",F2,52,"Atomic source attachment used in the transition theorem")
connection("guarded_detour_reduction","guarded_induction_universal_barrier",F33,365,"Maximal-core domain has no eligible guarded packet")
connection("aggregate_exposed_frame_class","relaxed_aggregate_owner_bypass",F4,491,"Positive/owned work remains valid counted A cost")
connection("relaxed_aggregate_owner_bypass","relaxed_cd_do_bridge",F4,797,"Any universal aggregate coefficient suffices downstream, coverage still open")
connection("historical_absolute_renewal_candidate","relaxed_cd_do_bridge",F4,576,"CONDITIONAL on unproved L_h, constant6*2^h-2 would close finite-C premise")
connection("producer_child_work_class","aggregate_exposed_frame_class",F4,520,"Complementary counted source classes; exhaustive union coverage not established")

graph = {"nodes": nodes, "edges": edges, "hyperedges": [], "input_tokens": 0, "output_tokens": 0, "token_accounting_unavailable": True}
(OUT / "cd_internal_findings.json").write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT / "cd_internal_graph.json").write_text(json.dumps(graph,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"primary_reports":len(PRIMARY),"claims":len(claims),"graph_nodes":len(nodes),"graph_edges":len(edges),"publication_pins":[{"entries":r["entries"],"all_match":r["all_match"]} for r in hash_checks]},indent=2))
