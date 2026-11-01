# Provenance and reproduction of the complete sparse-reset audit

All outputs in route_c_sparse_reset_strictness_20261031_v001 use exclusive creation. Every earlier source/research/status file is read-only. Reproduction requires another fresh versioned directory under the same parent; never overwrite a prior output.

SR00 was written before source execution. It fixes diagonal R13, setup D13,D12, KEEP skeleton 13,11,12,9,10,7,8,5,6,3,4,1,2, reset gaps g=2..12, targets t=1..13 excluding the preceding and following KEEP targets, lexicographic order and 64-lap cap. That is exactly 121 source generators at the existing key size. No generator was adapted, enlarged or replaced after execution.

build_sparse_audit.py reads the previous FI producer as text, preserves the unchanged tuple-source/ceiling/ledger definitions and writes standalone audit_sparse_resets.py. It does not import or execute an old auditor. The producer imports only python/independent/splay.py for source splaying. Before execution it verifies inherited pins and records 659 old/source hashes, the entire 125-file Stage 11G inventory, branch/HEAD and tracked-clean status in entry_source_pins.json.

The producer stores all per-request event identities/costs and source/destination pair digests, plus exact raw boundary trees, for every actual orbit. It takes the first repeated whole-word pair and extracts the recurrent source cycle; no cap-limited trajectory occurs. It computes actual cyclic A-root block costs, E, C_D and every diagonal phase. Survivors alone would receive unchanged FI/UD all-cut comparison. None survives because all E<=C_D, so no new all-cut FI comparison or FI-only map is claimed.

build_independent_audit.py reads the previous FI pointer verifier and CW DELETE-only map routine as text, and writes standalone independent_verify.py. The first version omitted lap zero from its shared-B verification dictionary and failed the final metadata check after reconstructing the source cases. SR00A and the unchanged first scripts preserve that provenance. build_verifier_v002.py changes only the dictionary initialization to include independently replayed b0 and writes independent_verify_v002.py exclusively. No first-pass audit JSON or acceptance-map file had been created at the failure.

V002 imports only python/liquidity/legacy_embedding.py for pointer-source splaying. It independently reconstructs every normal raw state and its reflected source counterpart, checks all stored digests, exact events/depths/costs, reset-root separation, shared B states, first paired recurrence, primitive closure, diagonal phases and budget values. It constructs both a DELETE-only minimum-cut proof and an old-UD successful pass at that cut, for all 121 cases in each orientation. old_UD_acceptance_certificates.json stores the normal maps and records their independently checked mirrored assignments. Each wrapper's case/orientation is a separate resource universe; alternative proofs are never pooled.

Exact independent totals: 8,204 orbit requests in both orientations, 3,864 recurrent-cycle requests, four setup requests, 15,826 source accesses, 32,834 raw BST occurrences, 242 accepting old-UD cut certificates, 6,348 old-UD assignment checks and 6,348 separate DELETE-only assignment checks. All first returns occur by lap five, with primitive periods one or two. Ninety cycles have a diagonal state, thirty-one have none, and only two non-diagonal cycles have positive excess. All 121 satisfy E<=C_D.

verify_seed_phase.py checks the special initial post-setup state is never returned to in any of the 4,102 normal destinations already independently source-verified; reflection gives the other orientation. This completes the initial-seed qualification in SR02's rotation/power argument. It does not execute another source word or search another case. Unequal canonical source-state digests suffice for this nonreturn statement without a collision-free-hash assumption.

From the repository root, with scripts/gates/reports in a new directory at the same relative depth:

    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/build_sparse_audit.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/audit_sparse_resets.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/build_independent_audit.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/build_verifier_v002.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/independent_verify_v002.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/verify_seed_phase.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/seal_delivery.py

Later fresh reproductions naturally pin more old artifacts than the historical 659 count. -B and dont_write_bytecode prevent source import caches. No installer, source/config/test edit, Git mutation, old executable recognizer or Stage 11G status writer is involved. The successful independent check means a different source implementation and separate credit/closure verification, not independent human authorship or a formal-assistant build.

The seal rechecks every inherited hash, exact Stage 11G inventory, branch/HEAD/tracked state, active matching-terminal freeze, audit/certificate hashes and explicit no-strict-witness status. It creates final_integrity.json and hashes all direct delivery files except delivery_manifest.json in that manifest.

Certificate SHA-256:

    a483bd745d301394e6f3fee56ff16d84921b88493eb32326e56c40bac7bfe0e7

The complete finite-class exclusion and its structural fringe lift do not imply universal E<=C_D or general FI=UD. Universal Step 3/CD and strict FI-only closed-walk existence remain OPEN. No larger finite key size, fitted coefficient or new Lean verification claim was used.
