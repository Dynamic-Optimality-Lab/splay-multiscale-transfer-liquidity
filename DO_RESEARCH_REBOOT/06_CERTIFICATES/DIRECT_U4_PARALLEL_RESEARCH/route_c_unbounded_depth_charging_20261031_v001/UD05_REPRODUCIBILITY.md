# Provenance, scope and reproduction

All writes are exclusive to this fresh route_c_unbounded_depth_charging_20261031_v001 directory. Existing source, research and Stage 11G files are read-only. Reproduce only in another fresh versioned directory under the same research parent; do not rerun an exclusive output writer against files that already exist.

UD00_FOUR_RULE_GATE.md was written before the bounded source audit. build_audit_scripts.py reads the previous SL producer as text and writes the new standalone audit_arbitrary_keys.py exclusively, with the new source-depth rule and fixed word. build_independent_auditor.py separately reads the previous SL pointer verifier as text and writes a new standalone independent_verify.py. These builders do not execute/import old audit modules and never modify them. The generated auditors retain source/serialization boilerplate; this provenance is explicit. The independent check means a different pointer splay implementation and a separate unit-claim reconstruction, not independent human authorship or a new formal proof assistant.

audit_arbitrary_keys.py imports only python/independent/splay.py as its tuple splay source. It verifies the inherited SL entry pins, adds all prior research artifacts and captures 606 old/source hashes, the 125-file Stage 11G inventory, branch/HEAD and tracked-clean status in entry_source_pins.json. It evaluates only the fixed new 13-key word and reflection, plus all ten unchanged SL/XR/SP/DS/SC controls. There is no word search or larger finite n. It writes arbitrary_key_certificate.json exclusively.

The certificate records complete diagonal prefixes, raw source/destination A/B trees, grouped event identities/orientations and exact costs at every cycle request. It records all old and new block cuts, explicit unpaid tails on failures, and a full selected ledger with every retained source fact, reservation, own-work prefix, loan slice, demand cursor and retired unit count. Old SL is reimplemented for comparison, never imported from an old executable recognizer.

independent_verify.py imports only python/liquidity/legacy_embedding.py for pointer-source splaying. It checks exact source keys/BST order, both orientations, every source event/depth/endpoint, diagonal reachability and paired closure. It independently reconstructs all post-depth bounds, genuine B intervention histories, old/new greedy passes, once-only reserved pools and unique unit-demand assignments. The strict witness validates a nonshallow KEEP with nonzero own work, zero-height facts elsewhere in the controls, conservative unused spare, changed new allocations, and preservation of every old successful cut.

Exact coverage: 432 cycle source rows, 20 prefix rows, 852 pointer accesses, 1,844 strict-BST occurrences, 432 cuts (404 accepted and 28 rejected), 328 selected assignments and 12,204 separate alternative accepted-ledger assignment checks. The old SL records agree on all ten preserved words and all cut transfer records: 314 successful cuts and 9,094 alternative assignment checks. New witness totals in each orientation are A=68,Q_B=35,Z_B=30,weight=101.

From the repository root, with builders, gate and report sources placed in a fresh versioned run directory:

    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/build_audit_scripts.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/audit_arbitrary_keys.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/build_independent_auditor.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/independent_verify.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/seal_delivery.py

As later runs accumulate, a fresh reproduction naturally pins more prior artifacts than this historical run. Here/ROOT relative path relationships must remain the same. The builders' source-text transformations are bounded and assert the expected unique sections; generated files use exclusive creation. Auditors set dont_write_bytecode; commands use -B to prevent import caches. No installation, source/config/test change, old status writer or Git mutation occurs.

seal_delivery.py rechecks every inherited hash, the exact Stage 11G inventory, branch/HEAD/tracked status, independent certificate hash, preserved-control counts and active matching-terminal freeze. It writes final_integrity.json and delivery_manifest.json, hashing every direct delivery artifact except the manifest itself. No old audit/recognizer or Stage 11G status writer is executed.

Certificate SHA-256:

    f729c699e4b7db790af96c5c44056b32e4ea883261fe2769d615399cb8b7970d

UD01 is the all-size source/ledger proof; UD02 proves the fringe/scan family without evaluating another n. The finite audit certifies its fixed strict core, not universal successful-cut availability. Universal CD stays OPEN; no Lean or other formal-assistant verification is claimed.
