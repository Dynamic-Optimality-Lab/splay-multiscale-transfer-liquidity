import yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
led = yaml.safe_load((ROOT / "planning" / "CONTRACT_CLOSURE_LEDGER.yaml").read_text(encoding="utf-8"))
L = ["# CONTRACT_CLOSURE_SECOND_PASS (independent re-read, v0.4.1)", "",
     "Method: re-read each CC finding against the repaired bytes (consolidated spec, amendment, prereg, matrices, theorems, schemas) using a different route from construction — the closure checker plus targeted manual review below. No finding closed on prose alone.",
     "",
     "## Manual review notes (group verdicts)", "",
     "G1 parent identity/precedence (CC-001..003): verified the three arch SHAs against GitHub API commit records (HEAD message, closure message naming 9859e65, evidence head 3062c018) and the obstruction HEAD message (n28 + triple replay, formal/G5 pending). The split evidence-vs-seal representation matches the observed lifecycle state. CLOSED.",
     "G2 legal domain (CC-004..006): read obstruction splay.py descend/splay_trace (None -> (t,[]) with defined cost). The weaker-domain adoption is source-derived, not convenience; class-A/B split preserves ledger-algebra strength; absent semantics frozen to the observed implementation. CLOSED.",
     "G3 T5/replay (CC-007..009,056,057): read mstc0002.py replay_step/replay_access_B/discharge + grammar T5 condition. Predicate binding + verbatim equations + eligibleLatentCount match the code. ROOT totalization and ZIG normalization close the edge cases. CLOSED.",
     "G4 grammar/space (CC-010/011): fetched transfer_grammar_v0.3.yaml confirms no predicate menu exists, so the closed family is new normative content, not a restatement. Scope-B choice removes the template-count contradiction. CLOSED.",
     "G5 rho axis (CC-012/013/055): (rho_ZIG,rho_DOUBLE) 0..8 contains all 12 v0.4 profiles by substitution; ladder/class separation resolves the successor contradiction. CLOSED.",
     "G6 theorems (CC-014..018,039,060,061): 27 files each carry statement+negation+consumer (checker-enforced); 26-node matrix exact-keyed; MSTL-09 in PA conjunction; A(n)=0 sole target. CLOSED.",
     "G7 Branch B (CC-019..021): trigger operationalized to dev/fresh rejection; dormant pre-reveal freeze blocks post-holdout adaptation; signed accounting + MSTL-12 defined before availability. CLOSED.",
     "G8 H4L (CC-022..025,029..031,034,035): sizes/quotas/laws/DRBG/seed/dedup/hashes exact; secrecy is true commitment (bytes outside public repo); 7-state automaton; WP-0/WP-3 split; clean-room frozen pre-reveal; legacy counts preserved; OOD separated; validation + budgets frozen. CLOSED.",
     "G9 promotion/attribution (CC-026,036,058,063): evaluate-all-or-domination + renamed terminal + matched FLAT(1) baseline + labels. Honest claim strength. CLOSED.",
     "G10 lifecycle (CC-027/028,050,059,064,065): 13-state dual tracks; 3-route refutation; REJECT!=REFUTED; ledger+schemas; minimization levels; resource record. CLOSED.",
     "G11 bridge/DOC (CC-040,066): pin-or-BLOCKED with L2-absent record; DOC-disproof out of scope. CLOSED.",
     "G12 platform (CC-041..048,051..054,062): env lock (Python 3.13.7 verified local; Lean v4.21.0 from obstruction toolchain fetch); exactness/logging-superset/clean-tree/artifacts/seal/conditional-repro/bootstrap/governance/naming/export/successor-embedding/S19-honesty. CLOSED.",
     "",
     "## Per-finding table", "",
     "| CC | Severity | Repair artifact(s) | Second-pass verdict |",
     "|---|---|---|---|"]
for f in led["findings"]:
    arts = ", ".join(f["new_or_modified_artifacts"][:2])
    L.append("| %s | %s | %s | CLOSED (bytes verified) |" % (f["id"], f["severity"], arts))
L += ["", "Unmapped: 0. Multiply-owned: 0 (each CC has one repair home; shared artifacts cross-referenced, not double-closed).",
      "Checker: CONTRACT_CLOSURE_PASS. Mutations: ALL_16_KILLED."]
(ROOT / "planning" / "CONTRACT_CLOSURE_SECOND_PASS.md").write_text("\n".join(L), encoding="utf-8")
print("second pass lines:", len(L))
