# PP_ACCEPTANCE_GATES.md

| Gate | Status | Evidence |
|---|---|---|
| PP-01 source hashes | PASS | 4/4 SHA256 (PP_SOURCE_AUDIT.md); verifier re-checked |
| PP-02 low-cost grammar | PASS | m=3 + 4-rotation + nongenuine audit imported (CC); K/D/zero-cost exercised in all harnesses |
| PP-03 port commutation | PASS | theorem + 4000/4000, maxrot 2, all 5 cases |
| PP-04 port replay | PASS | PP_PORT_ROTATION_TRANSDUCER.py + PP_PORT_SMOKE.json |
| PP-05 shared inventory | PASS | 600 flow + 800 dst-shared |
| PP-06 ordered completion | PASS | 600/600 both directions |
| PP-07 hidden S placement | PASS | S-cover/uniqueness/interval in every predicate check |
| PP-08 same-gap ordering | PASS | atom granularity + position-order verification |
| PP-09 T=266 | PASS | E1-E8/L1-L8 imported + 30/30 spot + 13-item ledger |
| PP-10 126 masks | OPEN | port product diagnostic 1 mask; 9-key all-126 by reference (UFRL nmasks=126) |
| PP-11 B-core controller | PASS | 9-key complete by reference (WQ 62,228/62,228); port diagnostic executable |
| PP-12 low relation compiled | OPEN | decide exact (52,920/52,920) + bounded exists small-scope; full compilation blocked (guard growth ~1/macro fringe) |
| PP-13 no src/dst split | PASS | single xi by construction; carried-view 800/800 |
| PP-14 exact weights | PASS | 52,920 incl. 21,168 negative, exact w=2H-q |
| PP-15 high-cost compiled | OPEN | fiber math imported (400/400) + 215-fiber executable (1302 covered); saturated D_g OPEN |
| PP-16 full product | OPEN | representation fixed; 7-key diagnostic (3144/20043, BF-clean); full scope blocked |
| PP-17 Pre exact | OPEN | diagnostic PASS (400 trials + oracle); full-scope symbolic OPEN |
| PP-18 Post exact | OPEN | diagnostic PASS; full-scope OPEN |
| PP-19 MinPre exact | OPEN | diagnostic PASS + hygiene; full-scope OPEN |
| PP-20 solver completeness | OPEN | Dinic exact (0 UNKNOWN at run scopes); full scope unrun (caps) |
| PP-21 circuit <=4M | BLOCKED | measured: fringe guards ~1/macro unbounded; 9-key reference alone 4.29M states |
| PP-22 runtime/memory | PASS | diagnostic totals ~3 min CPU, <1 GiB (PP_RESOURCE_LEDGER.json) |
| PP-23 simulation | OPEN | items 1-8 representative-level PROVED; 9-10 conditional on PP-16 |
| PP-24 verifier passes | PASS | PP_VERIFIER_REPORT.json ALL PASS (18 checks) |
| PP-25 reproducibility | PASS | command + versions in PP_AZ_REPORT.md |

STAGE 11F COMPLETE requires all 25: NOT MET. Verdict Outcome B (math passes, execution blocked).
