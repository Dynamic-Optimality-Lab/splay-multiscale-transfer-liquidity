# Fixed source controls and the closed replay

The exact audit used nine pre-registered controls at n=6 or n=7, plus one complete seventeen-operation source replay. It built no source graph, generated no tree corpus and fitted no coefficient.

## Exact failures and successful old tests

| Source operation | Source F | Destination F | a | q | Delta F | Required upper bound |
| --- | --- | --- | --- | --- | --- | --- |
| DELETE 6 from (R6,R6) | 0 | 5 | 3 | 0 | 5 | 6 |
| KEEP 6 from (L6,R6) | 5 | 4 | 0 | 2 | -1 | -2 |
| DELETE 7 from (R7,R7) | 0 | 6 | 3 | 0 | 6 | 6 |
| KEEP 7 from (L7,R7) | 6 | 4 | 0 | 3 | -2 | -3 |

At n=6 the scale would need c_6<=6/5 from DELETE and c_6>=2 from KEEP. At n=7 it would need c_7<=1 and c_7>=3/2. These controls check the symbolic parity formulas; they do not replace the all-size proof in CC03.

The previous n=6 source with arbitrary middle tree instantiated by the balanced tree on 2 through 5 gives

    Delta_DELETE G=21/8, Delta_DELETE R=-21/8, Delta_DELETE Psi=0.

KEEP 1 from that same pair gives Delta Psi=-1 and budget zero. Mirrored controls agree, including the opposite-vine repayment failure. The countercertificate saves all complete trees, subtree key sets, rational values, grouped oriented events and primitive rotation states.

## A closed word starting at the right-vine diagonal

Start from (R6,R6) and execute

    D2 D3 D4 D5 D6 K6 K1 K2 K3 K4 K5 K6 K5 K4 K3 K2 K1.

The sixth operation, K6, is exactly the starved counterexample. The actual final pair equals (R6,R6). The totals are A=19, Q_B=4 and Z_B=12, so this is not a Coarse-Double counterexample.

The original producer replays a cyclic rotation of this word starting at (L6,L6). right_vine_closed_rotation.json identifies the precise row permutation into the fully recorded replay; verify_sharp_bound.py verifies the complete rotated shared-state chain and endpoint. No new connector search is used.

## Independent verification

audit_clade_correction.py compares the frozen pointer and frame source engines on every full state and oriented event. It instruments primitive rotations only in its local Python process, restores the functions after each trace, and writes no source file. Its seventy-five primitive rotation records verify the one-set identity in the fixed controls and replay.

independent_verify.py imports neither the producer nor its set-counting routine. It computes subtree key sets through exact rank intervals and recomputes G and R by an independent depth DFS with rational arithmetic. It verifies every primitive transition as an actual immutable-tree rotation, every changed interval, all grouped events and source costs, all twenty-six recorded source edges and exact paired closure. independent_audit.json reports PASS.

verify_sharp_bound.py checks the sharper at-least-one B drop, the distinguished newly shared root-side set, and the bound Delta_KEEP F<=d_A-indicator(d_B>0) on the SAME saved source edges. Its report sharp_bound_audit.json is PASS. Arbitrary-fringe helper safety is an analytic consequence of that universal bound, not a larger helper fit or an extra finite experiment.
