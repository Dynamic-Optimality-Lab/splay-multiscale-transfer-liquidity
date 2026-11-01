# Exact source controls and the new closed safeguard

The cap pays the old six-key starved KEEP and retains all prior named source controls. A different six-key KEEP underpays q by one. Both claims use exact residual matching values and full physical source replay.

## Fixed values

| Whole KEEP | F source to destination | Ehat source to destination | J source to destination | a | q | Budget |
| --- | --- | --- | --- | --- | --- | --- |
| Opposite vines, n=6, access 6 | 5 to 4 | 5 to 2 | 5 to 3 | 0 | 2 | -2 |
| Established L helper, m=0 | 4 to 3 | 2 to 2 | 3 to 2 | 1 | 2 | 0 |
| Established R helper, m=0 | 3 to 3 | 3 to 1 | 3 to 2 | 1 | 2 | 0 |
| Old hook-vine starved KEEP 1 | 5 to 2 | 1 to 2 | 4 to 2 | 0 | 2 | -2 |
| Known starved B phase of the L helper | 5 to 3 | 2 to 2 | 4 to 2 | 0 | 2 | -2 |
| New padded-hook starved KEEP 1 | 4 to 2 | 1 to 2 | 3 to 2 | 0 | 2 | -2 |

Both m=1 helper controls and the reflected m=0 controls also pass. The all-size DELETE/vine/helper claims are the analytic arguments in CR01; no finite control is promoted to a universal proof.

## Complete new source word

Use A_P,B_P from CR02. Starting from (B_P,B_P), execute

    D1 D3 D1 D5 D1 K1 K1 K2 K3 K4 K5 K6 K5.

The first five DELETEs reach exactly (A_P,B_P). The sixth operation is the new failed KEEP 1, with a=0,q=2,z=0 and J=3->2. The common ascending pass K1 through K6 brings both trees to L6, and the last K5 returns both to B_P. The actual full paired endpoint equals the initial diagonal.

The totals are A=15,Q_B=4,Z_B=4, so Coarse-Double holds on this walk (4<=30). The failure concerns this candidate's pointwise source bound, not the original closed-walk conjecture.

One bounded n=6 single-tree BFS located the DELETE prefix: 104 distinct trees visited, 61 expanded and 366 source requests examined. It was a connector search only, not a fitted potential, a new paired source graph or an enlarged corpus. The saved complete word and full shared-state replay are the certificate; shortest-path optimality is not needed.

## Exact matching and independent verification

The producer reuses previously pinned Ehat matching certificates when a physical pair is identical and constructs a residual graph only for other fixed evaluation points. Each value includes all forced exact pairs, a residual matching and an equal-cardinality vertex cover. Capping the resulting integer rank is a deterministic formula, not an optimization over potential labels.

independent_verify.py imports neither the producer nor its matching routine. It regenerates every proper subtree set, residual graph edge and nonedge, verifies all exact-pair constraints, and checks the matching/cover equality proving each residual maximum. It then recomputes F, Ehat, t_n and J for every source, after-A and destination state.

The verifier replays all 23 saved whole source edges through the frozen pointer engine, checks oriented events and exact d_A,d_B,a,q,z costs, and verifies the complete thirteen-operation paired closure. It also checks the realized coordinates and incompatible integer bounds in the monotone-aggregation proof. independent_audit.json reports PASS for all 39 matching values and the source audit.

All larger helper cases are handled by the inherited uniform identities and max closure, not a new fringe sample. No coefficient or cap was fitted, no larger potential system was solved, and Stage 11G was not modified.
