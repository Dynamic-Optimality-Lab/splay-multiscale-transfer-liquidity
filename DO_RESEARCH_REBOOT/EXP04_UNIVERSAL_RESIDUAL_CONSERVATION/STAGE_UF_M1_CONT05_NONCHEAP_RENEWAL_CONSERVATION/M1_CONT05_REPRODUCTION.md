# Reproduce and inspect

Python3.13 with -B; no installations. Historical checkpoints and tracked Git state are read-only.

Read-only delivered seal:

    python -B finalize5.py --verify-only

Writer reproduction: copy this stage's .py and .md files into a fresh sibling under the same parent, preserving old stage directories. Never rerun writers inside the sealed stage.

    python -B base5.py
    python -B rn1_audit5.py
    python -B cheap_entry5.py
    python -B new_audit5.py
    python -B renewal_sources5.py
    python -B renewal_audit5.py
    python -B physical_renewal5.py
    python -B fringe_sources5.py
    python -B fringe_audit5.py
    python -B finish_audits5.py
    python -B finalize5.py

physical_renewal5_v1.py is the retained failed implementation, not the reproduction entry point. Its partial96-source output and failed receipt are preserved. The successful implementation handles a later P vertex as its own first promotion-mediated entry.

NEW/RENEW/FRINGE_SOURCE_CATALOG files contain all8 complete original A/B words, full labelled initial states and legal prefixes. Their PHYS state pools, actual events, FOREST/BIRTH/M1_AUDIT/ORDERED/REDUCTION/RENEWAL files preserve original predicates, exact C_old/F/E/H/D/quota and literal IDs.

RN1_REDUCTION_AUDIT preserves34 historical exact accounting checks. New RENEWAL files add8. FILTERED_RENEWAL_GEOMETRY holds direct full-component and primitive interval evidence. PHYSICAL_RENEWAL_RESULTS_FINAL and ALL_CONTROL_REFERENCES_FINAL cover104 complete sources, including the two pinned long event expansions.

EXACT_NONCHEAP_VERSUS_C_OLD_OBSTRUCTION and EXACT_OWNERSHIP_DEBIT_OBSTRUCTION are exact scoped refutations. LOCAL_PRIMITIVE_TABLE_AUDIT and REPLICATION_RENEWAL_INVARIANCE disclose their finite/physical/selector scopes.

M1_CONT05_SOURCE_WITNESSES, FINAL_VERIFICATION, RESOURCE_RECORD and M1_CONT05_DELIVERY_MANIFEST index all complete witnesses, hashes, limits and preservation. No unrun long native R_* set is treated as empty.

