# MSINK finalization ledger/deps reconciliation (task D)

Gate-0 authorization predates separate theorem certification; the R1HARD run's
append-only additions to the claim ledger and dependency graph are therefore
reconciled OUT of those files here. Their full content is preserved verbatim
below; nothing else was touched; MR status and all prior entries unchanged.

## Removed CLAIM_LEDGER.md row (was appended after the CDK5NMRP-A row)

`| CDK5NCMS-G0 | DIRECT-CDK5N-COMP-MSINK Gate 0 PASS (OUTCOME A): shared-sink joint-payment class; IN 19ff110a7c60 (61/36/16, E=[4,12], t=(0,2), p H=13) + OUT b8b02be76c04 (55/36/16, t=(2,2)) residual witnesses; 956-word bounded campaign; 12 exact membership predicates + 5 recognizers all-neg; 41 attacks 0 fails | Gate-0 verdict only (no universal class proved); L1-L7 payment proof for frozen joint H4-H5 rule; S_raw properness witnessed both sides | DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/MSINK_gate_verdict.md; MSINK_IN/OUT_exclusion_worksheet.md; MSINK_worksheet_*.json; MSINK_attacks.json |`

## Removed THEOREM_DEPENDENCIES.md addendum (was appended after the MR addendum)

`DIRECT-CDK5N-COMP-MSINK append-only addendum: CDK5NCMS-G0 (Gate 0 verdict, OUTCOME A; no universal class proved). Depends on source semantics + banked CDK5NP-A supporting lemmas (partition/baseline/debt, scope-noted reuse) + NEW joint-sink L1-L7 proof (two exceptions, mixed short/long relays, canonical-first H>=3 sink, explicit joint+local payment, telescoping). Residual witnesses IN 19ff110a7c60 (concat35 minus seam D1; E=[4,12] t=(0,2) p=0 H=13) and OUT b8b02be76c04 (mr33 plus D3@2; t=(2,2) breaks mixed gate), both five-key nine-core closed aperiodic, outside all 17 banked mechanisms (12 exact predicates + 5 recognizers incl. pointer-push AS) and additive closure (no closed splits); 956-word L0L1 campaign within caps with early stop; 41-attack battery 0 hard fails. Alters no prior node status; complement, K>=6, universal, DO still OPEN.`

## Final authorized state (verified post-removal)

- `CLAIM_LEDGER.md`: no MSINK PROVED claim (ends at CDK5NMRP-A + standing footer).
- `THEOREM_DEPENDENCIES.md`: no MSINK theorem node (ends at MR addendum).
- `02_PROVED/`: unchanged (verified clean at entry and pre-commit).
- Gate-0 findings: complete inside
  `DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/`.
- Separately authorized MSINK-PROOF may re-add ledger/dependency entries after
  theorem certification.
