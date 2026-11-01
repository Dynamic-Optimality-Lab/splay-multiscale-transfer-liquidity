# Provenance of the two-reset budget stop

All current delivery artifacts are exclusive writes in route_c_two_reset_budget_20261031_v001 in the verified repository. Existing source/research/status/Git and Stage 11G files are read-only. Reproduction requires another fresh versioned run directory at the same depth; never overwrite a prior output. The corrected mistyped placeholder and completed cleanup are recorded separately in TR00A.

TR00 fixed the B-budget gate before any new source request. It first excludes two effective pure resets on the old B order using its source G_B=4. It then fixes one new order V=1,9,5,13,3,11,7,2,10,6,4,12,8 at thirteen keys, a 64-round B recurrence cap, and 78 conditional two-slot path-reset policies. The gate explicitly stops before A enumeration if the B source budget is <=4 per period. No other skeleton is tried afterward.

audit_B_budget.py imports only python/independent/splay.py. Before source execution it verifies inherited pins and records 683 old/source hashes, the entire 125-file Stage 11G inventory, branch/HEAD and tracked-clean status in entry_source_pins.json. It replays the B source only. The unchanged setup D13,D12 would not alter B, so the B gate starts directly at R13; no A setup replay is counted here.

The new order reaches T=8(4(2(1,3),6(5,7)),12(10(9,11),13)) after one round and returns to it after the second. B_budget_certificate.json contains all 26 source/destination trees, depths, exact events, raw boundaries, first-repeat indices and recurrent q vector. Q_B=27,Z_B=6,G_B=3; the intended two effective reset pools would have capacity four per round. Its outcome is BUDGET_BLOCKED and zero A policies executed.

independent_verify.py imports only python/liquidity/legacy_embedding.py for pointer splaying. It independently checks the literal new order, every B state/event/depth/cost, first primitive boundary repeat and reflection. It also replays the OLD order from R13 for two rounds, matching the already pinned SR B states and verifying its G_B=4. This old-profile validation is not a second new candidate selected after failure. old_B_budget_replay.json records it.

Exact independent totals: 26 new B source requests plus 26 old B source requests per orientation, giving 104 pointer accesses and 208 raw BST source/destination tree occurrences. No A request, policy trajectory, new paired closed walk, FI/UD cut trial or cycle-unit assignment is asserted. The no-reuse corollary follows from the established minimum-cut DELETE-only construction for any actual A cycle meeting the proven budget condition.

From the repository root, with gate/report sources and scripts in a fresh versioned directory:

    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/audit_B_budget.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/independent_verify.py
    python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/<fresh-run>/seal_delivery.py

Later reproductions naturally pin more old files than this historical run. Scripts set dont_write_bytecode and commands use -B. No installation, source/config/test change, old executable recognizer, Git mutation or Stage 11G writer occurs. The final seal rechecks every inherited hash, exact Stage 11G inventory, branch/HEAD/tracked state, active terminal freeze, independent certificate hash and explicit no-strict-witness status, then writes final_integrity.json and delivery_manifest.json. The manifest hashes every direct delivery file except itself.

Certificate SHA-256:

    e2b73c78a11cd0cda91586bab64fba888bf5431e78e249fa9de4b978db41ab8e

TR01 is the universal source-block inequality and scoped multi-reset exclusion. TR02 proves the recurrent source identities and structural arbitrary-fringe lift, without evaluating another finite n. The exclusion does not imply a universal upper bound on G_B for other source orders. Strict FI-only existence and universal Step 3/CD remain OPEN; no formal-assistant or new Lean verification is claimed.
