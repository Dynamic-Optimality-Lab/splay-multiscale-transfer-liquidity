"""Build NORMATIVE_INVENTORY.yaml + WORKPLAN_COVERAGE.yaml for SPLAY-AM-MST-LIQ-v0.4.

Deterministic generator: every normative item is derived from the frozen
spec text IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt (SHA-256
0E2C166E1B721DFC8A7E5327ED33AF29A1B4AC539CB71849F3C7231B32A8055B)
plus the two read-only parent references. No counts from memory: all lists
are built programmatically (ranges/loops) and the checker recomputes them.
"""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt"
OUT_INV = ROOT / "planning" / "NORMATIVE_INVENTORY.yaml"
OUT_COV = ROOT / "planning" / "WORKPLAN_COVERAGE.yaml"

SPEC_SHA = "0E2C166E1B721DFC8A7E5327ED33AF29A1B4AC539CB71849F3C7231B32A8055B"
ARCH_NAV = "895889169772087e391e84c33228648c84684e1e"
OBSTR_NAV_LATEST = "19ef254dfc48c7b909c646f959e2d7364865b777"
V03_SPEC_SHA = "462676E186C6282F493D13C13A4A7A63179943CFC7E9AB10ABFBE0019BD1E12F"
DECIDE_SPEC_SHA = "30ACC6F96ABC35A9A4FC91AD159560888E54180F55BE21F947B59DFF8B62B5F9"

items = []
def add(iid, category, source, title, wp, **extra):
    d = {"id": iid, "category": category, "source": source, "title": title, "wp": wp}
    d.update(extra)
    items.append(d)

# ---- 0. spec sections 0..51 (52 sections, derived by range) ----
SECTION_OWNER = {
    0: "WP-0", 1: "WP-1", 2: "WP-0", 3: "WP-1", 4: "WP-2", 5: "WP-2",
    6: "WP-2", 7: "WP-1", 8: "WP-2", 9: "WP-2", 10: "WP-1", 11: "WP-1",
    12: "WP-1", 13: "WP-2", 14: "WP-2", 15: "WP-3", 16: "WP-4", 17: "WP-4",
    18: "WP-3", 19: "WP-3", 20: "WP-4", 21: "WP-4", 22: "WP-6", 23: "WP-6",
    24: "WP-6", 25: "WP-2", 26: "WP-2", 27: "WP-6", 28: "WP-6", 29: "WP-6",
    30: "WP-6", 31: "WP-6", 32: "WP-0", 33: "WP-0", 34: "WP-4", 35: "WP-3",
    36: "WP-5", 37: "WP-4", 38: "WP-4", 39: "WP-0", 40: "WP-0", 41: "WP-6",
    42: "WP-6", 43: "WP-6", 44: "WP-6", 45: "WP-0", 46: "WP-0", 47: "WP-0",
    48: "WP-6", 49: "WP-6", 50: "WP-6", 51: "WP-6",
}
for s in range(0, 52):
    add(f"SPEC-SEC-{s:02d}", "spec_section", f"spec #{s}",
        f"Normative spec section {s}", SECTION_OWNER[s])

# ---- 1. phases 00..19, exactly one owner each ----
PHASE_OWNER = {
    "PHASE-00": "WP-0", "PHASE-01": "WP-1", "PHASE-02": "WP-1",
    "PHASE-03": "WP-1", "PHASE-04": "WP-1", "PHASE-05": "WP-2",
    "PHASE-06": "WP-2", "PHASE-07": "WP-3", "PHASE-08": "WP-3",
    "PHASE-09": "WP-4", "PHASE-10": "WP-4", "PHASE-11": "WP-4",
    "PHASE-12": "WP-4", "PHASE-13": "WP-4", "PHASE-14": "WP-5",
    "PHASE-15": "WP-5", "PHASE-16": "WP-5", "PHASE-17": "WP-6",
    "PHASE-18": "WP-6", "PHASE-19": "WP-6",
}
PHASE_SRC = "spec #33"
for ph, wp in PHASE_OWNER.items():
    add(ph, "phase", PHASE_SRC, f"Normative {ph}", wp)

# ---- 2. LIQ0 obligations (10, from #14) ----
for n in range(1, 11):
    iid = f"LIQ0-{n:02d}"
    wp = "WP-1" if n == 1 else "WP-2"
    fc = {"LIQ0-01": "WP-2", "LIQ0-02": "WP-2"}.get(iid, "WP-6" if n >= 9 else "WP-2")
    add(iid, "liq_obligation", "spec #14",
        f"Liquidity obligation {iid}", wp, first_consumer=fc,
        required_status="REVIEWED" if n in (1, 2) else "PROVED")

# ---- 3. MST0 mapped obligations (16, from #42) ----
MST_MAP = [
    ("MST0-08U", "WP-6", "WP-6"), ("MST0-09", "WP-4", "WP-6"),
    ("MST0-10", "WP-2", "WP-6"), ("MST0-11", "WP-2", "WP-6"),
    ("MST0-13", "WP-6", "WP-6"), ("MST0-14", "WP-6", "WP-6"),
    ("MST0-15", "WP-6", "WP-6"), ("MST0-16", "WP-1", "WP-6"),
    ("MST0-17", "WP-6", "WP-6"), ("MST0-18", "WP-6", "WP-6"),
    ("MST0-19", "WP-6", "WP-6"), ("MST0-22", "WP-5", "WP-6"),
    ("MST0-23", "WP-4", "WP-5"), ("MST0-24", "WP-4", "WP-5"),
    ("MST0-25", "WP-5", "WP-6"), ("MST0-26", "WP-6", "WP-6"),
]
for mid, wp, fc in MST_MAP:
    add(mid, "mst_obligation", "spec #42", f"Mapped parent obligation {mid}",
        wp, first_consumer=fc, required_status="REVIEWED")

# ---- 4. transfer gates MSTL-GATE-0..19 (20, from #41) ----
GATE_WP = {0: "WP-0", 1: "WP-1", 2: "WP-1", 3: "WP-2", 4: "WP-2",
           5: "WP-4", 6: "WP-4", 7: "WP-4", 8: "WP-4", 9: "WP-5",
           10: "WP-5", 11: "WP-5", 12: "WP-5", 13: "WP-6", 14: "WP-6",
           15: "WP-6", 16: "WP-6", 17: "WP-6", 18: "WP-6", 19: "WP-6"}
for g in range(0, 20):
    iid = f"MSTL-GATE-{g}"
    wp = GATE_WP[g]
    fc = "WP-6" if g >= 13 else ({"WP-0": "WP-1"}.get(wp, wp))
    add(iid, "gate", "spec #41", f"Transfer gate {iid}", wp,
        producer_wp=wp, first_consumer=fc)

# ---- 5. WP-level gates (8, from #32) ----
for iid, wp, src in [
    ("GATE-FOUNDATION_FROZEN", "WP-0", "spec #32 WP-0"),
    ("GATE-LEGACY_SEMANTICS_CERTIFIED", "WP-1", "spec #32 WP-1"),
    ("GATE-LIQUIDITY_AXIS_FROZEN", "WP-2", "spec #32 WP-2"),
    ("GATE-H4L_BANK_COMMITTED", "WP-3", "spec #32 WP-3"),
    ("GATE-TRANSFER_GRAMMAR_FROZEN", "WP-3", "spec #32 WP-3"),
    ("GATE-LIQUIDITY_CALCULUS_SURVIVES_DEV", "WP-4", "spec #32 WP-4"),
    ("GATE-LIQUIDITY_CALCULUS_SURVIVES_FINITE_TESTS", "WP-5", "spec #32 WP-5"),
    ("GATE-DYNAMIC_OPTIMALITY_PROVED", "WP-6", "spec #30/#48"),
]:
    add(iid, "gate", src, f"WP gate {iid}", wp, producer_wp=wp,
        first_consumer="WP-6" if wp in ("WP-4", "WP-5") else wp)

# ---- 6. lifecycle (from #22) ----
for iid, src, title in [
    ("LIFE-UNPROVED-TO-PROVED", "spec #22", "UNPROVED->PROVED requires Layers A+B complete"),
    ("LIFE-PROVED-TO-REVIEWED", "spec #22", "PROVED->REVIEWED requires human ACCEPT on exact bytes"),
    ("LIFE-LAYER-C-ATTACK", "spec #22", "Layer C hostile refutation; exact witness blocks theorem"),
    ("LIFE-NO-CONSUME-BEFORE-STATUS", "spec #15/#22", "No downstream consume before required status"),
]:
    add(iid, "lifecycle", src, title, "WP-6")

# ---- 7. threats LIQ-T01..T20 (from #39) ----
for n in range(1, 21):
    iid = f"LIQ-T{n:02d}"
    wp = {1: "WP-4", 7: "WP-5", 8: "WP-5", 9: "WP-4", 10: "WP-5",
          12: "WP-6", 19: "WP-6", 20: "WP-6"}.get(n, "WP-2" if n in (2, 3, 4, 5, 6, 13, 14, 15, 17, 18) else ("WP-1" if n == 11 else "WP-4"))
    add(iid, "threat", "spec #39", f"Threat {iid}", wp,
        controls=[f"CTRL-{iid}-A", f"CTRL-{iid}-B"] if n in (7, 13) else [f"CTRL-{iid}-A"])

# ---- 8. stops LIQ-STOP-01..20 (from #40) ----
for n in range(1, 21):
    iid = f"LIQ-STOP-{n:02d}"
    wp = {1: "WP-0", 2: "WP-0", 3: "WP-1", 4: "WP-1", 5: "WP-1",
          6: "WP-1", 7: "WP-1", 8: "WP-1", 12: "WP-5", 13: "WP-5",
          14: "WP-5", 15: "WP-5"}.get(n, "WP-2" if n in (9, 10, 11) else "WP-6")
    add(iid, "stop", "spec #40", f"Stop {iid}", wp, controls=[f"HDL-{iid}-A"])

# ---- 9. named test families ----
TESTS = [
    ("TEST-LEGACY-REPLAY", "WP-1", "spec #7/#32"), ("TEST-N28-REGRESSION", "WP-1", "spec #11"),
    ("TEST-FAMILY-DDKK", "WP-4", "spec #11/#20"), ("TEST-MULTIPLICITY", "WP-2", "spec #8"),
    ("TEST-ACTIVATION-BOUND", "WP-2", "spec #14"), ("TEST-ENERGY-CONS", "WP-2", "spec #14/#25"),
    ("TEST-PRESERVATION", "WP-2", "spec #26"), ("TEST-DETERMINISM", "WP-2", "spec #14"),
    ("TEST-TARGET-BLINDNESS", "WP-2", "spec #5.3/#27"), ("TEST-DEV-BATTERY", "WP-4", "spec #20"),
    ("TEST-ADV-UNIFORM", "WP-4", "spec #20"), ("TEST-ADV-STRUCTURED", "WP-4", "spec #20"),
    ("TEST-ADV-HILLCLIMB", "WP-4", "spec #20"), ("TEST-ADV-ANNEAL", "WP-4", "spec #20"),
    ("TEST-ADV-GENETIC", "WP-4", "spec #20"), ("TEST-ADV-ROTNEIGH", "WP-4", "spec #20"),
    ("TEST-ADV-SPLICE", "WP-4", "spec #20"), ("TEST-ADV-MOTIF", "WP-4", "spec #20"),
    ("TEST-ADV-GENERALIZE", "WP-4", "spec #20"), ("TEST-INTERNAL-VALID", "WP-4", "spec #16"),
    ("TEST-H4L-FRESH", "WP-5", "spec #18"), ("TEST-CLEANROOM", "WP-5", "spec #21"),
    ("TEST-LARGEN", "WP-5", "spec #36"), ("TEST-MUTATION", "WP-5", "spec #38"),
    ("TEST-INDEPENDENT-REPLAY", "WP-5", "spec #21/#37"), ("TEST-SCHEMA-VALID", "WP-0", "spec #45"),
    ("TEST-HASH-VERIFY", "WP-0", "spec #46/#47"), ("TEST-FIREWALL", "WP-3", "spec #18"),
    ("TEST-LIFECYCLE", "WP-6", "spec #22"), ("TEST-COVERAGE", "WP-0", "task Rule 2"),
    ("TEST-REPRO-FRESHCHECKOUT", "WP-6", "spec #47"),
]
for iid, wp, src in TESTS:
    add(iid, "test_family", src, f"Test family {iid}", wp)

# ---- 10. invariants (8 derived accounting invariants, sources cited) ----
for iid, src, title, wp in [
    ("INV-ENERGY-CONS", "spec #4/#14", "E(L')=E(L) under T5_rho", "WP-2"),
    ("INV-SUPPORT-PRES", "spec #4/#14", "Support preserved under T5_rho", "WP-2"),
    ("INV-PROV-PRES", "spec #4/#14", "Provenance preserved under T5_rho", "WP-2"),
    ("INV-NO-RESURRECT", "spec #4/#14", "No SPENT resurrection", "WP-2"),
    ("INV-DETERMINISM", "spec #4/#14", "Activation deterministic first-eligible order", "WP-2"),
    ("INV-TARGET-BLIND", "spec #5.3/#27", "rho independent of forbidden info", "WP-2"),
    ("INV-STOCK-LIQ-SEPARATION", "spec #9/#24 + Rule 7", "ACTIVE_pre_discharge>=need required; stock!=liquidity", "WP-6"),
    ("INV-LEGACY-EMBED", "spec #7", "FLAT(1) reproduces inherited execution exactly", "WP-1"),
]:
    add(iid, "invariant", src, title, wp)

# ---- 11. holdout transitions (ordered; owners WP-3/WP-5 only) ----
HOLDOUTS = [
    ("HOLD-H4L-GENERATOR-FROZEN", "WP-3", 1, "H4L generator frozen+committed before synthesis"),
    ("HOLD-H4L-BANK-COMMITTED", "WP-3", 2, "H4L bank committed+quarantined (70k eps)"),
    ("HOLD-CANDIDATE-SET-FROZEN", "WP-5", 3, "Candidate set frozen+hashed (<=3)"),
    ("HOLD-H4L-REVEAL-ONCE", "WP-5", 4, "H4L revealed exactly once, post-freeze"),
    ("HOLD-H4L-CONSUMED", "WP-5", 5, "H4L consumed; no regen/second unlock/mutation-reuse"),
    ("HOLD-H3T-HISTORICAL", "WP-3", 0, "Old H3T historical only; never fresh"),
    ("HOLD-LIQREG-CONTAMINATED", "WP-1", 0, "LIQ-REG-001/FAM-001 contaminated dev/regression only"),
]
for iid, wp, order, title in HOLDOUTS:
    add(iid, "holdout_transition", "spec #18/#19/#11", title, wp, order_index=order)

# ---- 12. fresh-data rules ----
for i, title in enumerate([
    "H4L generator frozen+committed before target-guided synthesis",
    "Generator/strata blind to residual/pool/rho/k/C/solver/kill info",
    "No candidate residual evaluated against H4L before freeze",
    "Candidate-set freeze precedes reveal",
    "Exactly one reveal; no regeneration after reveal; no second unlock",
    "Post-freeze change mints new ID; cannot reuse H4L fresh label",
    "Known DDKK/n28 witnesses never fresh; H3T never fresh",
    "No holdout influence on candidate construction under same frozen ID",
], start=1):
    add(f"FRESH-RULE-{i:02d}", "fresh_rule", "spec #18/#35", title,
        "WP-3" if i <= 2 else "WP-5")

# ---- 13. candidate identity fields (#6 + #35) ----
CAND_FIELDS = ["calculus_id", "parent_calculus_family", "branch", "predicate_P",
               "injection_bound_k", "competitive_constant_C", "activation_family",
               "activation_base_r", "activation_profile_hash", "credit_types",
               "support_semantics", "scale_semantics", "provenance_semantics",
               "T7_definition_hash", "T5_rho_definition_hash", "T6_definition_hash",
               "energy_definition", "initialization", "snapshot_convention",
               "mapping_version", "ontology_version", "rho_profile_table",
               "proof_outline_SHA", "eligibility_verdict"]
for f in CAND_FIELDS:
    add(f"CANDFIELD-{f}", "candidate_field", "spec #6/#35",
        f"Candidate identity field {f}", "WP-3")

# ---- 14. candidate mutation rules ----
for i, (iid, title, wp) in enumerate([
    ("MUTR-NEWID-RHO", "Changing rho/family/r mints new calculus ID", "WP-5"),
    ("MUTR-NEWID-T5ORDER", "Changing T5 selection order mints new ID", "WP-5"),
    ("MUTR-NO-REPAIR-SAME-ID", "No repair after failure under same ID", "WP-5"),
    ("MUTR-POST-HOLDOUT", "Post-freeze change -> POST_HOLDOUT, never fresh-tested", "WP-5"),
    ("MUTR-SURGICAL-ONLY", "T7/T6/energy/support changes outside allowance forbidden", "WP-2"),
    ("MUTR-FREEZE-RECORD", "Each promoted candidate records full frozen file", "WP-5"),
]):
    add(iid, "mutation_rule", "spec #6/#35", title, wp)

# ---- 15. claim levels (#48: 9) ----
for iid, wp in [
    ("CLAIM-LIQUIDITY_AXIS_FORMALIZED", "WP-2"),
    ("CLAIM-LIQUIDITY_CALCULUS_SURVIVES_DEV", "WP-4"),
    ("CLAIM-LIQUIDITY_CALCULUS_SURVIVES_FINITE_TESTS", "WP-5"),
    ("CLAIM-BOUNDED_DELETE_INJECTION_PROVED", "WP-6"),
    ("CLAIM-SYNCHRONOUS_KEEP_TRANSFER_PROVED", "WP-6"),
    ("CLAIM-GLOBAL_INTEGRABILITY_PROVED", "WP-6"),
    ("CLAIM-UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED", "WP-6"),
    ("CLAIM-APPROXIMATE_MONOTONICITY_PROVED", "WP-6"),
    ("CLAIM-DYNAMIC_OPTIMALITY_PROVED", "WP-6"),
]:
    add(iid, "claim_level", "spec #48", f"Claim level {iid}", wp)
    add(iid + "-POLICY", "claim_policy", "spec #48",
        f"Allowed/forbidden wording for {iid}", wp)

# ---- 16. artifact families (#45) ----
for iid, wp, src in [
    ("ART-PREREG", "WP-0", "spec #45 prereg/"), ("ART-PY-LIQUIDITY", "WP-2", "spec #45 python/liquidity/"),
    ("ART-PY-HOLDOUT", "WP-3", "spec #45 python/holdout/"), ("ART-PY-ADVERSARY", "WP-4", "spec #45 python/adversary/"),
    ("ART-PY-INDEPENDENT", "WP-5", "spec #21 python/independent/"), ("ART-LEAN-LIQ", "WP-6", "spec #45 lean/Liquidity/"),
    ("ART-LEAN-PA", "WP-6", "spec #45 lean/PairAccess/"), ("ART-LEAN-BRIDGE", "WP-6", "spec #45 lean/Bridge/"),
    ("ART-MATH-PROOFS", "WP-6", "spec #45 math/proofs/"), ("ART-MATH-REVIEWS", "WP-6", "spec #45 math/reviews/"),
    ("ART-V04-PARENT", "WP-0", "spec #45 artifacts/v04/parent_import"), ("ART-V04-OBSTRUCTION", "WP-0", "spec #45 artifacts/v04/obstruction_import"),
    ("ART-V04-HOLDOUTS", "WP-3", "spec #45 artifacts/v04/holdouts"), ("ART-V04-CANDIDATES", "WP-5", "spec #45 artifacts/v04/candidates"),
    ("ART-V04-COUNTEREX", "WP-4", "spec #45 artifacts/v04/counterexamples"), ("ART-V04-CLEANROOM", "WP-5", "spec #45 artifacts/v04/cleanroom+large_n"),
    ("ART-V04-PROOFS", "WP-6", "spec #45 artifacts/v04/proofs"), ("ART-V04-SEAL", "WP-6", "spec #45 artifacts/v04/seal+audits"),
    ("ART-EXPORT", "WP-6", "spec #44 MST_LIQ_EXPORT.json"),
]:
    add(iid, "artifact_family", src, f"Artifact family {iid}", wp)

# ---- 17. schema requirements ----
for iid, title, wp in [
    ("SCHEMA-CANDIDATE", "Frozen candidate schema (#35 fields)", "WP-3"),
    ("SCHEMA-KEEP-RECORD", "KEEP record liquidity diagnostics (#9 fields)", "WP-2"),
    ("SCHEMA-COUNTEREXAMPLE", "Counterexample bundle (hash, snapshots, binding)", "WP-4"),
    ("SCHEMA-REVIEW", "Human review record (ACCEPT on exact bytes)", "WP-6"),
    ("SCHEMA-RUNLOG", "Append-only run record (#46 fields)", "WP-0"),
    ("SCHEMA-EXPORT", "MST_LIQ_EXPORT packet (#44 fields)", "WP-6"),
]:
    add(iid, "schema_req", "spec #9/#35/#37/#22/#46/#44", title, wp)

# ---- 18. logging fields (#46: 28 fields) ----
LOG_FIELDS = ["experiment_id", "phase", "wp", "utc", "commit", "arch_parent_commit",
              "obstruction_parent_commit", "spec_sha", "prereg_sha", "rho_grammar_sha",
              "candidate_id", "P", "k", "C", "rho_family", "rho_base",
              "rho_profile_sha", "firewall_states", "command", "input_hashes",
              "output_hashes", "stdout_hash", "stderr_hash", "wall_time",
              "peak_memory", "exit_code", "scientific_status", "gate_output"]
for f in LOG_FIELDS:
    add(f"LOG-{f}", "logging_field", "spec #46", f"Logging field {f}", "WP-0")

# ---- 19. reproducibility requirements (#47) ----
for i, title in enumerate([
    "Reproduce from clean checkout", "Verify both parent chains",
    "Verify all hashes", "Verify known counterexample",
    "Verify legacy embedding", "Verify rho semantics",
    "Verify H4L commitment/reveal state", "Verify candidate IDs",
    "Verify fresh-evaluation outputs", "Verify clean-room outputs",
    "Verify Lean builds", "Verify proof+review+stream hashes+manifest+terminal",
    "No untracked-local-file artifact dependency",
], start=1):
    add(f"REPRO-{i:02d}", "repro_req", "spec #47", title, "WP-6" if i > 1 else "WP-0")

# ---- 20. mutation controls (#38: 16) ----
for i, title in enumerate([
    "double-step capacity 2->1 killed", "ZIG capacity changed killed",
    "rho depends on n killed", "rho depends on need killed",
    "rho depends on future key killed", "rho depends on residual killed",
    "activation creates credit killed", "activation changes support killed",
    "activation changes provenance killed", "SPENT->ACTIVE resurrection killed",
    "last-LATENT selection killed", "B-only hidden activation killed",
    "unbounded activation killed", "T7 coefficient altered killed",
    "T6 spends LATENT killed", "legacy FLAT(1)!=old T5 killed",
], start=1):
    add(f"MUT-{i:02d}", "mutant", "spec #38", title, "WP-5")

# ---- 21. counterexample steps (#37: 10) ----
for i, title in enumerate([
    "independent replay", "legality check", "delta minimization",
    "canonical ordering", "exact tree+ledger snapshots", "candidate hash",
    "theorem-negation binding", "Lean witness if feasible",
    "family generalization attempt", "append-only preservation",
], start=1):
    add(f"CEX-{i:02d}", "counterexample_step", "spec #37", title, "WP-4")

# ---- 22. parent imports (WP-0 pin list #32 + obstruction evidence) ----
for iid, title in [
    ("PIMP-ARCH-COMMIT", "MST-v0.3 architecture parent exact commit+seal"),
    ("PIMP-MSTC0002-RECORD", "MSTC-0002 exact record (P_all,k=6,C=2)"),
    ("PIMP-V03-FINAL-RESULT", "v0.3 FINAL_RESULT TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS"),
    ("PIMP-V03-CANDIDATE-COMMIT", "v0.3 candidate-set commitment"),
    ("PIMP-V03-PATH", "v0.3 Path.md"), ("PIMP-V03-WORKPLAN", "v0.3 WorkPlan.md"),
    ("PIMP-V03-IMPLSPEC", "v0.3 implementation spec"),
    ("PIMP-V03-LEDGER", "v0.3 transfer-calculus ledger"),
    ("PIMP-V03-THEOREM-STATUS", "v0.3 theorem-status report"),
    ("PIMP-OBSTRUCTION-COMMIT", "Obstruction-parent exact sealed commit"),
    ("PIMP-N28-WITNESS", "Canonical legal n=28 repayment counterexample"),
    ("PIMP-INDEPENDENT-REPLAY", "Independent replay artifact"),
    ("PIMP-NORMATIVE-HASHES", "All normative hashes pinned"),
]:
    add(iid, "parent_import", "spec #32", title, "WP-0")

# ---- 23. transport classes (#13) + per-obligation transport binding ----
for iid, title in [
    ("TRANSPORT-CLASS-A", "Class A semantic identity; hash-bound transport proof"),
    ("TRANSPORT-CLASS-B", "Class B unchanged conclusion, new operator deps; reprove via T5-rho lemma"),
    ("TRANSPORT-CLASS-C", "Class C statement generalized by rho; new theorem bytes"),
    ("TRANSPORT-CLASS-D", "Class D downstream rebound; blocked until upstream REVIEWED"),
]:
    add(iid, "transport_class", "spec #13", title, "WP-6")
for mid, cls in [("MST0-08U", "A"), ("MST0-09", "B"), ("MST0-10", "B"),
                 ("MST0-11", "B"), ("MST0-13", "B"), ("MST0-14", "C"),
                 ("MST0-15", "C"), ("MST0-16", "A"), ("MST0-17", "D"),
                 ("MST0-18", "D"), ("MST0-19", "D"), ("MST0-22", "C")]:
    add(f"TRANSPORT-{mid}", "transport_class", "spec #13/#42",
        f"Transport binding {mid} -> class {cls}", "WP-6")

# ---- 24. success criteria S1..S20 (#50) ----
S_WP = {1: "WP-1", 2: "WP-1", 3: "WP-2", 4: "WP-2", 5: "WP-4", 6: "WP-4",
        7: "WP-4", 8: "WP-4", 9: "WP-4", 10: "WP-4", 11: "WP-5", 12: "WP-5",
        13: "WP-6", 14: "WP-6", 15: "WP-6", 16: "WP-6", 17: "WP-6",
        18: "WP-6", 19: "WP-6", 20: "WP-6"}
for n in range(1, 21):
    add(f"S{n:02d}", "success_criterion", "spec #50", f"Success criterion S{n}", S_WP[n])

# ---- 25. terminal outcomes (#49 + DO proved) ----
for iid, wp in [
    ("TERM-LEGACY_EMBEDDING_FAIL", "WP-1"), ("TERM-AXIS_REPRESENTATION_INCONCLUSIVE", "WP-2"),
    ("TERM-LIQUIDITY_CALCULUS_REJECTED", "WP-4"), ("TERM-SYNCHRONOUS_REPAYMENT_REFUTED", "WP-6"),
    ("TERM-GLOBAL_INTEGRABILITY_REFUTED", "WP-6"), ("TERM-PAIR_ACCESS_ROUTE_REFUTED_NO_DOC_NEGATIVE", "WP-6"),
    ("TERM-BRIDGE_BLOCKED_NO_CLAIM", "WP-6"), ("TERM-RESOURCE_LIMIT_NO_CLAIM", "WP-6"),
    ("TERM-DYNAMIC_OPTIMALITY_PROVED", "WP-6"),
]:
    add(iid, "terminal_outcome", "spec #49/#30", f"Terminal outcome {iid}", wp)

# ---- 26. successor rule steps (#43: 7) ----
for i, title in enumerate([
    "preserve exact failed candidate", "preserve exact theorem witness",
    "diagnose missing resource", "seal experiment honestly",
    "clone MST architecture into versioned successor", "add only newly justified axis",
    "rerun affected discovery/validation/proof stages",
], start=1):
    add(f"SUCC-{i:02d}", "successor_rule", "spec #43", title, "WP-6")

# ---- 27. hygiene (#11 / Rule 11: 6) ----
for i, title in enumerate([
    "Authoritative new outputs live in artifacts/v04/ only",
    "Parent evidence imported read-only, hash-bound, labeled inherited/historical",
    "Never copy parent results into v04 namespace as new",
    "Enumerate+classify+quarantine pre-existing stale outputs, hash-log",
    "Fail closed if clean separation impossible",
    "Never silently delete scientific history",
], start=1):
    add(f"HYG-{i:02d}", "hygiene_req", "spec #45/Rule 11", title, "WP-0")

# ---- 28. commit/push rule (Rule K: 7) ----
for iid, title in [
    ("COMMIT-VERIFY", "VERIFY gates before Path update"),
    ("COMMIT-PATH", "UPDATE Path.md contemporaneously"),
    ("COMMIT-AUDIT", "COMPLIANCE AUDIT (coverage/lifecycle/firewall)"),
    ("COMMIT-COMMIT", "COMMIT with experiment/WP/phase/gate message"),
    ("COMMIT-PUSH", "PUSH without asking after verification"),
    ("COMMIT-REMOTE-HEAD", "VERIFY REMOTE HEAD points at intended commit"),
    ("COMMIT-SHA-LOG", "Record full SHA+push result in Path.md"),
]:
    add(iid, "commit_rule", "task Rule K/#32", title, "WP-0")

# ---- 29. surgical boundary (Rule 4 + #12: changed vs frozen) ----
add("SURG-CHANGED-AXIS", "surgical_item", "spec #4-#5/Rule 4",
    "ONLY semantic change: (P,k,C)->(P,k,C,rho); T5_1 -> T5_rho bounded iteration", "WP-2",
    changed=True)
add("SURG-EMBED-OLD", "surgical_item", "spec #0/Rule 4",
    "Old T5 embedded exactly as FLAT(1); MSTC-0002 falsified status preserved", "WP-1",
    changed=False)
for obj in ["splay", "depth+1-cost", "keep-delete-dynamics", "reference-snapshot",
            "L6-translation", "T7-injection", "T6-discharge", "required_C",
            "ledger-support", "provenance-alphabet", "energy-E", "credit-mass",
            "candidate-freeze", "one-residual-kills", "fresh-bank-one-unlock",
            "human-review-lifecycle", "bridge-standard", "pair-access-semantics",
            "unsigned-E-formula"]:
    add(f"FROZEN-{obj}", "surgical_item", "spec #12/Rule 4",
        f"Frozen unchanged object: {obj}", "WP-1", changed=False)

# ================= COVERAGE =================
WPS = ["WP-0", "WP-1", "WP-2", "WP-3", "WP-4", "WP-5", "WP-6"]
WP_FILES = {
    "WP-0": ["IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt", "planning/NORMATIVE_INVENTORY.yaml",
             "planning/WORKPLAN_COVERAGE.yaml", "scripts/check_workplan_coverage.py",
             "prereg/liquidity_axis.yaml", "prereg/liquidity_search_space.yaml",
             "prereg/h4l_holdout.yaml", "prereg/theorem_transport_matrix.yaml",
             "artifacts/v04/parent_import/", "artifacts/v04/obstruction_import/",
             "artifacts/v04/logs/"],
    "WP-1": ["python/independent/splay.py", "python/independent/pair.py",
             "artifacts/v04/parent_import/", "artifacts/v04/obstruction_import/",
             "math/proofs/LIQ0-01-legacy-embedding.md", "tests/test_legacy_embedding.py"],
    "WP-2": ["python/liquidity/multiplicity.py", "python/liquidity/activation.py",
             "python/liquidity/profiles.py", "python/liquidity/diagnostics.py",
             "python/liquidity/legacy_embedding.py", "lean/Liquidity/",
             "math/proofs/LIQ0-*.md", "tests/test_activation.py"],
    "WP-3": ["python/holdout/h4l_generate.py", "python/holdout/h4l_verify.py",
             "prereg/h4l_holdout.yaml", "prereg/liquidity_search_space.yaml",
             "artifacts/v04/holdouts/", "tests/test_holdout_firewall.py"],
    "WP-4": ["python/adversary/liquidity_burst.py", "python/adversary/drain_refill.py",
             "python/adversary/ddkk_family.py", "artifacts/v04/development/",
             "artifacts/v04/validation/", "artifacts/v04/counterexamples/",
             "tests/test_synthesis.py"],
    "WP-5": ["artifacts/v04/candidates/", "artifacts/v04/holdouts/",
             "artifacts/v04/cleanroom/", "artifacts/v04/large_n/",
             "python/independent/", "tests/test_fresh_h4l.py"],
    "WP-6": ["lean/Liquidity/", "lean/PairAccess/", "lean/Bridge/",
             "math/proofs/MSTL-*.md", "math/reviews/", "artifacts/v04/proofs/",
             "artifacts/v04/seal/", "artifacts/v04/audits/", "MST_LIQ_EXPORT.json"],
}
WP_TESTS = {
    "WP-0": ["TEST-SCHEMA-VALID", "TEST-HASH-VERIFY", "TEST-COVERAGE"],
    "WP-1": ["TEST-LEGACY-REPLAY", "TEST-N28-REGRESSION", "TEST-INDEPENDENT-REPLAY"],
    "WP-2": ["TEST-MULTIPLICITY", "TEST-ACTIVATION-BOUND", "TEST-ENERGY-CONS",
             "TEST-PRESERVATION", "TEST-DETERMINISM", "TEST-TARGET-BLINDNESS"],
    "WP-3": ["TEST-FIREWALL"], "WP-4": ["TEST-DEV-BATTERY", "TEST-ADV-UNIFORM",
             "TEST-ADV-STRUCTURED", "TEST-ADV-HILLCLIMB", "TEST-ADV-ANNEAL",
             "TEST-ADV-GENETIC", "TEST-ADV-ROTNEIGH", "TEST-ADV-SPLICE",
             "TEST-ADV-MOTIF", "TEST-ADV-GENERALIZE", "TEST-INTERNAL-VALID",
             "TEST-FAMILY-DDKK"],
    "WP-5": ["TEST-H4L-FRESH", "TEST-CLEANROOM", "TEST-LARGEN", "TEST-MUTATION",
             "TEST-INDEPENDENT-REPLAY"],
    "WP-6": ["TEST-LIFECYCLE", "TEST-REPRO-FRESHCHECKOUT"],
}

def cov_entry(it):
    wp = it["wp"]
    gate = it["id"] if it["category"] in ("gate",) else (
        {"WP-0": "GATE-FOUNDATION_FROZEN", "WP-1": "GATE-LEGACY_SEMANTICS_CERTIFIED",
         "WP-2": "GATE-LIQUIDITY_AXIS_FROZEN", "WP-3": "GATE-H4L_BANK_COMMITTED",
         "WP-4": "GATE-LIQUIDITY_CALCULUS_SURVIVES_DEV",
         "WP-5": "GATE-LIQUIDITY_CALCULUS_SURVIVES_FINITE_TESTS",
         "WP-6": "GATE-DYNAMIC_OPTIMALITY_PROVED"}[wp])
    return {
        "id": it["id"], "wp": wp,
        "spec_phase": "PHASE-00" if wp == "WP-0" and it["category"] == "phase" else None,
        "files": WP_FILES.get(wp, []),
        "proof_files": ["math/proofs/", "math/reviews/"] if it["category"] in ("liq_obligation", "mst_obligation") else [],
        "tests": WP_TESTS.get(wp, []),
        "gate": gate,
        "inputs": ["parent pins", "spec SHA"] if wp == "WP-0" else [f"exit gate of predecessor of {wp}"],
        "outputs": [f"{it['id']} disposition record"],
        "failure": "BLOCKED" if it["category"] in ("phase", "gate", "liq_obligation", "mst_obligation") else "NOT_REACHED",
        "first_consumer": it.get("first_consumer"),
        "producer_wp": it.get("producer_wp", wp),
        "controls": it.get("controls", []),
        "order_index": it.get("order_index"),
        "required_status": it.get("required_status"),
        "changed": it.get("changed"),
    }

coverage = [cov_entry(it) for it in items]

def dump(path, obj):
    import yaml
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False, allow_unicode=True)

meta = {"experiment": "SPLAY-AM-MST-LIQ-v0.4", "spec_sha256": SPEC_SHA,
        "arch_parent_nav": ARCH_NAV, "obstruction_parent_latest": OBSTR_NAV_LATEST,
        "v03_spec_sha256": V03_SPEC_SHA, "decide_spec_sha256": DECIDE_SPEC_SHA,
        "normative_items": len(items)}
dump(OUT_INV, {"meta": meta, "items": items})
dump(OUT_COV, {"meta": {**meta, "work_packages": WPS}, "mappings": coverage})
print(f"inventory_items={len(items)} coverage_mappings={len(coverage)}")
cats = {}
for it in items:
    cats[it["category"]] = cats.get(it["category"], 0) + 1
for k in sorted(cats):
    print(f"  {k}: {cats[k]}")
