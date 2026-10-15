# PC_SOURCE_AUDIT.md — entry, triage, frozen configuration

## Entry (STEP 01)
- HEAD `052d92dc4f485ecf3f0e6897a85ba1bcdbe09d42` == FETCH_HEAD == mission checkpoint. No reset.
- Sources 4/4 SHA256 verified (same frozen hashes).
- Previous verdict: OUTCOME B (052d92d). Bank25 at 25 (no promotion authorized here).
- Previous inventory (all present, read-only): 4 theorem mds + 9 implementation/test scripts + 10 JSON evidence files + gates/verdict/AZ. Nothing modified.

## Triage (proved vs imported vs diagnostic)
- PROVED (math + corroborating tests): port commutation induction (pending C3 re-audit of rotation counting); shared-inventory predicate biconditional (soundness by construction, completeness by reading); T=266 via E1-E8/L1-L8 import + ledger.
- IMPORTED LEMMAS (prior certificates, not re-proved): UFRL E1-E8/L1-L8 + B-compat (Control-F discipline); AF-2 flow soundness/completeness 80/80; WQ fiber/midpoint five-point equivalence 400/400; Hall 1024-inequality characterization + 67/67 reconstruction; m=3 grammar + 55-type contiguity; zero-op identities.
- DIAGNOSTIC ONLY (not universality evidence): small-domain agreements; guard census counts (per C1: not a lower bound); q_terms arithmetic tests (per C2: recategorized below); 7-key product/operator tests (implementation tests, not scope proofs).

## Frozen configuration
- Source model: pointer BST semantics exactly as `python/independent/splay.py` (`_descend`/`_rebuild`/`trace`); KEEP splays A+B; DELETE splays A only; a=ceil(d_A/2); KEEP q=floor(d_B/2); DELETE q=0.
- Solver backend: (i) NEW typed-DAG finite-domain solver PC_SOLVER_BACKEND.py (backtracking + propagation, exact, UNKNOWN only on cap); (ii) Dinic circulation for inventory subproblems (exact, imported). No external SAT/SMT; no solver switch mid-campaign.
- Representation: slot-based symbolic prefix (127) + ports (128) + atoms (137 counters) + 9-core symbolic B + 126 masks via one 9-bit variable.
- Resources: h=2, T=266, 12 CPU-h, 32 GiB, 4M DAG nodes, 2M states, 5M edges, 1M solver queries; 15% verification reserve.

## Gate G01: PASS.
