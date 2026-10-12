# SELRP pre-SELR bank24 inventory (3+9+12 = 24; reconciled)

Foundations: RT2-A, CDK4-A, CDK5L-A (02_PROVED DIRECT_NFKS_RT2,
DIRECT_CD_K4, DIRECT_CDK5_LOW; ledger rows present). Nine-core: NP-A
(DP-PROOF 3ac0f8c), S1P-A (a6ba09f), S2P-A (b837b78), VRP-A (783b1c7),
MRP-A (df416ec), MSP-A (6213764), DLSP-A (6bf8781), UESP-A (405861c),
ZULR-A (ce009c8; doc DIRECT_CDK5_NINE_zero_exception_unique_local_reserve,
ledger CDK5NZULR-A row, dependency addendum — all in HEAD). Packets:
26AJ–26AS (C10–C18 ledger rows; 02_PROVED 26AJ–26AS docs). Engine keys
(RT2,CDK4,CDK5L,NP,S1,S2,VR,MR,MSINK,DLSS,UESINK,ZULR,AJ,AK,ALG,ALS,AMG,
AMS,AN,AO,AP,AQ,AR,AS) each bound to its authoritative recognizer;
MSINK/DLSS/UESINK keep existential sink conditions; ZULR keeps
zero-exception + unique-local-payer conditions (smoke: ZULR-IN flags
exactly ZULR). No other applicable proved mechanism found (git log +
02_PROVED + ledger + deps reviewed). SELR excluded from own baseline.
