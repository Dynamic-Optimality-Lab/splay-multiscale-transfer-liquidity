# CL-02A CL-02 Process CPU Inventory (measured, disjoint processes)

Builder run 1 (seed 701, 16 chains/139 legs, file OVERWRITTEN by run 2):
~700s (run stdout; artifact lost — provenance gap documented, counts from
run log). Builder run 2 (seed 702, 9 chains/86 legs): 351.5s (embedded).
Pairing seed 801: 30.9s. Pairing seed 802: 49.1s. Pairing FULL rerun
(seed 801): 33.0s (embedded 32.98). Verifier runs + doc authoring CPU:
~30-50s estimated (lightweight; flagged ESTIMATED). Measured subtotal:
~1195-1215s. CL02_RESOURCE_LEDGER.json claims 1400 total with parts
1051+209+60=1320 (inconsistent: 1400 != 1320; +80 unexplained padding).
Adjudication: use measured component sum (~1205s); ledger's 1400 is
UNRECONCILED (overstates by ~200 incl. unexplained +80). Builders alone
(1051s) are the dominant, well-evidenced component.
