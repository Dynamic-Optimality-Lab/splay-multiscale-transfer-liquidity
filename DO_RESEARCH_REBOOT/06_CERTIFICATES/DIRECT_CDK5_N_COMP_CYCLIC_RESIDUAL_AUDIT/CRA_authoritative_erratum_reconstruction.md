# Authoritative erratum reconstruction (task B)

Source: `DIRECT_CDK5_N_COMP_MSINK_PROOF/` (5 files read):
`MSP_critical_novelty_verdict.md`, `MSP_cyclic_decomposition_certificate.json`,
`MSP_rotation_replay.py`, `MSP_entry_and_ancestry.md`, `MSP_terminal_status.json`.

Demonstrated failure: frozen IN (`19ff110a…78df`, 61/36/16) has P_1=P_17
(full labeled A/B serials). Rotation at boundary 1 yields seg1 [1,17)
(16 accesses, A=30/Q=18, S1-covered from P_1) + seg2 [17,34)∪[0,1)
(18 accesses, A=31/Q=18, VR-covered from P_1; string-identical to VR rotated;
transitions identical to VR tail). B4: 30+31=61, 18+18=36; banked S1+VR imply
Q(IN)≤2A(IN). IN inside cyclic additive closure. MSINK not promoted.
Universal L1–L7 payment unrefuted, preserved separately.

## Mandatory regression (this audit, fresh engine): PASS

Recomputed with the new cyclic engine (`CRA_cyclic_coverage_engine.py`,
no Gate-0 imports): IN = CYCLIC-ADDITIVE-BANKED, r=1, cuts [0,16,34],
parts S1 (30/18) + VR (31/18), additive identities hold. If the new checker
had called IN uncovered, it would be invalid — it did not.
Record: `CRA_cyclic_coverage_regressions.json`.
