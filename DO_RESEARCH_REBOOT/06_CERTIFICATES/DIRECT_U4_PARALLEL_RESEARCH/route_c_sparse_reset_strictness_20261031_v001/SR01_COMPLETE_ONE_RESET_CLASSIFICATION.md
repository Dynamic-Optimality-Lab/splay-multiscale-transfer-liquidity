# Complete exact classification of the gated one-reset architecture

Status: FINITE-EXACT for the full 121-case, 13-key parameter class below. Every extracted cycle has a concrete old-UD accepting cut. Consequently the class contains no requested nowhere-diagonal, E>C_D, FI-only witness. This is not a refutation of such witnesses outside the declared skeleton, seed and reset architecture. Strict new closed-walk coverage and universal CD remain OPEN/unestablished.

## Exact domain fixed before execution

Start diagonally at R13 and apply the fixed reachability prefix D13,D12. Let

    W=(13,11,12,9,10,7,8,5,6,3,4,1,2)

be the KEEP skeleton. After position g in {2,...,12}, insert one DELETE t, with t unequal to W[g] and W[(g+1) mod 13]. There are exactly eleven gaps and eleven allowed keys per gap: 121 generators of length fourteen. The exclusion before/after neighboring targets ensures the reset is neither an A-root no-op nor immediately completed by a KEEP of the same key. Its block is KEEP-less and has positive actual A cost. The first three KEEP targets are unchanged in the initial lap.

The recurrent trajectory was not assumed periodic. Each actual pair map was iterated at whole-word boundaries, with complete exact states retained, until its FIRST repeated pair or the fixed 64-lap limit. All 121 repeated within five laps; none reached the cap. Every extracted paired cycle is primitive even at individual request boundaries, as independently checked by distinct actual source pairs. Its diagonal reachability prefix includes the initial two DELETEs and the exact transient laps; none of those prefix units pays cycle work.

## Complete outcome

| Recurrent cycle property | Cases |
| --- | ---: |
| Has at least one A=B state | 90 |
| A!=B at every state | 31 |
| A!=B everywhere and E=0 | 29 |
| A!=B everywhere and E>0 | 2 |
| E>C_D | 0 |
| A concrete old-UD accepting cut verified | 121 |
| Required FI-only witnesses | 0 |
| Unclosed/cap-limited cases | 0 |

Here E=sum max(q_i-2a_i,0) and C_D=sum 2a_i over KEEP-less cyclic A-root blocks, with all costs from the actual source. Every cycle, including the ninety that contain a diagonal state, satisfies E<=C_D. Thus all 121 already belong to UD by CW01's independently proved DELETE-budget theorem. FI contains UD, so these cycles cannot lie in the strict difference. Zero candidates survive the mandatory source filters; no new FI/UD all-cut comparison is claimed.

The initial source perturbation did defeat permanent synchronization in the intended sense: after each reset, A's root is t and B's root is the preceding KEEP target, which differs. Thirty-one recurrent cycles even satisfy the stronger all-state non-diagonality condition. The failure is the independently mandatory budget test, not an assertion that all reset trajectories simply become diagonal.

## Exact recurrence dimensions

| Transient whole laps | Primitive cycle whole laps | Cases |
| ---: | ---: | ---: |
| 1 | 1 | 80 |
| 1 | 2 | 13 |
| 2 | 1 | 20 |
| 2 | 2 | 3 |
| 3 | 1 | 3 |
| 3 | 2 | 1 |
| 4 | 1 | 1 |

All cycle lengths are fourteen or twenty-eight. The normal source orbits contain 4,102 requests including transients; their recurrent cycles contain 1,932 requests. Reflection doubles those to 8,204 and 3,864 respectively. The shared B boundary trajectory becomes fixed after the first lap and is independent of DELETE placement, as source semantics predicts. These are exact finite-class observations, not fitted all-tree bounds.

## Two non-diagonal positive cycles

The only nowhere-diagonal cycles with positive excess are:

| Gap / inserted request | Transient laps | Period laps | E | C_D | A | Q_B | Reset a |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| g=8, D13 after K6 | 1 | 1 | 1 | 8 | 31 | 23 | 4 |
| g=12, D8 after K2 | 2 | 1 | 1 | 6 | 23 | 23 | 3 |

Both are actual reachable, closed, non-synchronizing source walks. They fail E>C_D and have explicit old-UD acceptance maps, so neither is a strictness witness. They are included as failure illustrations, not relabeled as successful new CD cases.

The exact cheap-reset subcase D13 after K12 also recurs, after two transient laps, with period one, E=0,C_D=2,A=29,Q_B=23. Its recurrent cycle has diagonal states. The one-zig a_D=1 identity holds at every reset, as predeclared, but it produces no positive recurrent excess in that subcase.

## Independent certificates and exact scope

The tuple producer derives complete source rows and stores their event/cost data plus source/destination pair digests, with raw boundary trees. The pointer verifier independently reconstructs every raw state from the literal seed and word, checks every digest, event, orientation and cost, verifies first recurrence and primitive paired closure, and replays the reflected source as well. No state digest alone supplies the closure argument: reconstructed raw boundary pairs are compared exactly.

For every normal and reflected cycle the verifier constructs a DELETE-only minimum-cut injection and runs old UD at that same cut. It verifies 242 explicit UD acceptance certificates, 6,348 old-UD assignments and 6,348 alternative DELETE-only assignments. Each map uses distinct actual units/demands; maps for different cases, orientations or proof choices are separate resource universes. No alternative budgets are pooled. A single concrete accepted UD cut is sufficient to disprove rejection at every cut; exhaustively rejecting old UD is neither assumed nor necessary here.

The first verifier omitted lap zero in a shared-B verification dictionary and failed its final metadata comparison. SR00A and the retained first script record that bookkeeping error. The successful independent_verify_v002.py includes the already replayed b0 endpoint. Source words, trajectories, ceilings and success criteria were unchanged. No independent result was claimed before v002 passed.

The result completely excludes this declared finite reset architecture, rather than merely a sampled word. It does not classify gaps before the known triple, other skeletons, other seeds, multiple resets or all finite BSTs. SR02 gives a structural arbitrary-fringe extension, with no additional finite n. The original strictness target remains unmet; no new original CD case is claimed.
