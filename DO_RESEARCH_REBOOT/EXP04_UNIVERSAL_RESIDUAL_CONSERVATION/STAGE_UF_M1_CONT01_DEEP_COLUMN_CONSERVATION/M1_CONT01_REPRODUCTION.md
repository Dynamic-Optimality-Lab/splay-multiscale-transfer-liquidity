# Reproduction and sealing

Run from this continuation directory with Python3.13 (the current environment); use -B. No installation, network access, Git mutation, subagent or historical certificate write is required.

## Read-only delivered-checkpoint verification

    python -B finalizec.py --verify-only

This verifies the exact continuation file inventory/hashes, all mandatory artifacts, sealed historical M1/M0 and transitive inputs, Git HEAD/branch and tracked-file preservation. It writes nothing. The delivery manifest excludes only itself.

## Re-running mathematics/experiments

Do not rerun writer scripts in the sealed delivery directory. Use a fresh isolated sibling with the same parent (copy only the continuation .py sources), preserving ROOT-relative import placement. Its artifact and resource receipts will be new; timings need not match. Run sequentially:

    python -B basec.py
    python -B auditc.py
    python -B freshc.py
    python -B adapterc.py
    python -B guardedc.py
    python -B frontierc.py
    python -B canonicalc.py

auditc rechecks36 historical controls. freshc constructs12 complete sources. adapterc natively selects the four large loop variants after cross-checking old577. guardedc constructs four additional full-support paired-closed sources at k4,16,64,256, checks independent and native U/R6, and selects original R_* only at k4,k16. frontierc composes exact reference-pair comparisons and the scoped birth frontier. Reproduction can exceed a different host's original wall/CPU timing; no test count is a theorem hypothesis.

The delivered first audit receipt predates the full cohort extension; its second run is the current all-cohort implementation and both measured costs are retained. A full rerun of the final scripts needs only one audit run. The delivered failed adapter receipt is administrative and need not be recreated.

The pinned coerce implementation is imported read-only from C05; its four-node macro table, mutable/immutable engines, original oracle and full native selectors are inherited exact dependencies. Module writer roots for native trajectory output are redirected to the new continuation ROOT.

## Evidence navigation

- SOURCE_CATALOG.json:36 complete inherited sources and source/input hashes.
- BIRTH_00..35.json: independent full SET/Pi/U/cohort/R6, birth and exception-flow evidence.
- NEW_SOURCE_CATALOG.json:12 full new initial states, prefixes, words and inserted loops.
- NEW_PHYS/FOREST/WEIGHTS/M1_AUDIT/BIRTH_00..11.json: their full original physical/forest/distance evidence.
- NATIVE_SELECTOR_RESULTS.json: old577 cross-check plus exact original R_* for large loop variants.
- GUARDED_SOURCES.json and GUARDED_*_00..03.json: four full new parameterized sources and state/event certificates.
- GUARDED_RESULTS.json: native R_* scope explicit per source, full original U/R6 and periodic certificates.
- CREATOR_CLOSURE_COUNTEREXAMPLE.json: precise false candidate, original rho, consumer and creator.
- EXACT_REFERENCE_PAIR_CHECKS.json: eight full pair-field cross-checks against sealed earlier implementations.
- FRONTIER_RESULTS.json: exact B0/B1/silent predicates applied to physical deep U C vertices, separate actual weights.
- M1_DEEP_SOURCE_WITNESSES.json: canonical source/file/hash index and explicit verification scopes.
- FINAL_VERIFICATION.json, RESOURCE_RECORD.json, M1_CONT01_DELIVERY_MANIFEST.json: final audit, measured receipts and exact seal.

## Scope

Physical state pools encode all complete labelled child-pointer trees collision-free; they are not hash-only trace summaries. Every population, marked support and period is fixed by the full source entry. Archived original R_* classifications are not recomputed from a filtered event word. Native R_* unrun at guarded k64,k256 remains unknown, even though independent original R6 and the theorem-backed current zero residual are known.

The symbolic guarded-family argument is in M1_ADVERSARIAL_COUNTEREXAMPLES.md. The source-uniform supporting budgets are in M1_RESIDUAL_SENSITIVE_INVARIANT.md and M1_GLOBAL_CONSERVATION_PROOF.md. The unresolved full target is not a software test failure.
