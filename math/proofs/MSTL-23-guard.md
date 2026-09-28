# MSTL-23-guard (v0.4.1, WP-4 guard note — NOT a proof)

Guard: WP-6 may consume a WP-4 promoted candidate identity ONLY IF the identity
bytes are byte-identical to the frozen record in
`artifacts/v04/candidates/branchA/<calculus_id>/identity.json` AND the WORDING
rule holds ("candidate satisfies immutable LIQ-REG-001", never "repairs witness")
AND no post-freeze predicate, C-value, or rho-profile mutation occurred (C change
mints a new calculus_id; new predicate = successor experiment).

First consumer: WP-6. Required status before consumption: REVIEWED.
Current status: UNPROVED (guard note only).
