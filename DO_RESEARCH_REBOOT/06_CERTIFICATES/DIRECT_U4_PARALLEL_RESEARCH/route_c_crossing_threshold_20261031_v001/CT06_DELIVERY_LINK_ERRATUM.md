# Source link correction and preserved first seal

The first delivery seal stopped on two relative source links in CT01: each climbed one directory too far. It had already written proof_status_ledger.json; it wrote no final integrity or delivery manifest. The source and mathematical checks passed before that link assertion. No mathematical statement, source datum or certificate changed.

Append-only handling preserves the original report, proof, ledger and failed seal script. The active [proof](CT01_STRUCTURAL_DEFINITION_AND_DELETE_v002.md) corrects both links; the active [final report](CT04_FINAL_REPORT_v002.md) points to it and to [the versioned ledger](proof_status_ledger_v002.json). The corrected [seal](seal_delivery_v002.py) records the two archived broken links explicitly and verifies all active links. The independent source certificate and its PASS audit are unchanged.
