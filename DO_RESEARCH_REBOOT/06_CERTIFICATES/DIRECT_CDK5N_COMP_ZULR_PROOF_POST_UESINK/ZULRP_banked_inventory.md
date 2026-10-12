# Pre-ZULR bank-23 inventory (Gate D — reconciled)

Core/support: RT2-A (|supp KEEP|≤3 closed reachable), CDK4-A (==4),
CDK5L-A (5 keys + core≤8 throughout). Nine-core: CDK5NP-A (all positives
strict-K/P), CDK5NS1P-A (unique (c=1,q=3,H=1) + successor c=1/q≤3/H≥2 +
strict others), CDK5NS2P-A (+creditless H=1 + paying second),
CDK5NVRP-A (relay t∈[2,s−2] + payer + strict others), CDK5NMRP-A (|E|≥2,
all t≥2, payers, disjoint), CDK5NMSP-A (|E|=2, mixed short+long, joint H≥3,
strict others), CDK5NDLSP-A (|E|=2, both t≥2, joint H≥3, strict others),
CDK5NUESP-A (|E|=1, long relay t≥2, joint H≥3 sink, strict others).
Blocks/packets: 26AJ/AK/AL-G/AL-S/AM-G/AM-S/AN (exact hypotheses),
26AO/AP/AQ/AR/AS (unmodified recognizers, all-cut searches, pointer push +
snaps for AS). Count: 3+8+12 = 23. Reconciled against 02_PROVED + ledger +
dependency graph + certificate files (no other applicable coverage class;
AE/AF/AG/AH/U1/CWC are obstructions/audits). ZULR excluded from its own
baseline. Z-basis: proved closed-A0 ⇒ Q=0 (single key, no-op chain).
MSINK/DLSS/UESINK bank predicates are exists-versions (all jointly eligible
sinks enumerated).
