# Exact source replay and matching verification

The candidate was evaluated on two prescribed opposite-vine controls and then the first six-key helper. That helper failed, so the audit stopped candidate testing and reused an existing exact closed word to certify physical reachability.

## Fixed values

| Whole KEEP | E source | E after A | E destination | a | q | Delta E | Budget |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Opposite vines, n=6, access 6 | 5 | 5 | 1 | 0 | 2 | -4 | -2 |
| Opposite vines, n=7, access 7 | 6 | 6 | 1 | 0 | 3 | -5 | -3 |
| Six-key L helper, access 2 | 1 | 2 | 2 | 1 | 2 | +1 | 0 |

The all-size opposite-vine claim is proved by symbolic matchings and covers in EM02. The two controls only check source wiring and parity values. There was no fitted table or larger tree corpus.

## The closed physical witness

Start from the diagonal (B0,B0), with B0 as displayed in EM03. Execute

    D1 D3 D6 D2 D6 K2 D5 D2 K1 K4 K6.

The first five operations reach exactly (A0,B0), and the sixth is the failing zero-weight KEEP 2. The final physical pair equals the initial diagonal. This exact word was inherited read-only from route_c_analytic_20261030_v001/six_key_closed_controls.json, control zero. The new audit replays the whole word with both source engines and attaches the new matching certificates at every state.

Its totals are A=16, Q_B=4 and Z_B=2. Coarse-Double holds on this walk (4<=32). Only the proposed E edge inequality is refuted; no negative closed-walk claim is made. No connector search was needed.

## Independent exact verification

audit_endpoint_matching.py constructs maximum matchings in the CURRENT-pair endpoint graphs and supplies equal-cardinality vertex covers. These graphs are part of E's definition; they are not source-state graphs or potential-feasibility systems.

independent_verify.py imports neither the producer nor its matching algorithm. It regenerates every proper subtree interval, every endpoint edge and nonedge, and checks that each saved matching has distinct valid endpoints. It checks every cover covers all edges, and that its size equals the matching size. Weak duality then certifies all eighteen maximum matching values exactly, without another solver or a fitted coefficient.

The verifier also checks the two hand-readable certificates in EM03. It independently replays all fourteen recorded whole source edges using the pointer engine, verifies oriented events and the original d_A,d_B,a,q,z conventions, and checks complete shared tree states and exact paired closure. independent_audit.json reports PASS.

No singleton-fringe controls, port-embedding search, hook-vine control, graph enlargement, new tree corpus, coefficient search or finite potential fit followed the first helper failure. Those were conditional audit branches, not unfinished proofs needed for this exact refutation.
