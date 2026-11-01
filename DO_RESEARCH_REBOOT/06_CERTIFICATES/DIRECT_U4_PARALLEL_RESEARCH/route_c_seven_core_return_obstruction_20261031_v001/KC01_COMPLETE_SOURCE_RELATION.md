# Complete seven-core transition relation and the refuted excess bound

Status: FINITE-EXACT for the complete core table and reachable relation up to proved diagonal absorption. The proposed no-further-excess statement(KC) is REFUTED—EXACT. Its failure does not establish the requested high-budget amplification-and-return identity.

## Domain and finite completeness

The prescribed diagonal is R13. The only DELETEs are D3,D5, followed by K7. Subsequent queries in this audit are shared KEEPs from1,...,7. Keys8,...,13 are an untouched fringe F at7.right. The source prefix ends at

    A=7(L_[1,6],F),
    B=7(2(1,4(3,6(5,.))),F).

Both roots are7 and every later shared KEEP gives a common root. There are429 BST shapes on the seven core keys. The numbers by root rank are132,42,28,25,28,42,132, giving at most

    132^2+42^2+28^2+25^2+28^2+42^2+132^2=40,569

common-root core pairs. This bound is derived from the Catalan recurrence before execution, not selected after an orbit computation.

All429 shapes and all7 target keys are executed through the authoritative source on their actual thirteen-key embeddings. Every destination is checked to preserve the whole fringe F at7.right, and its projected core shape must be one of the429 inputs. All3,003 transitions are also executed in the reflected lower-fringe embedding. Each table row contains the exact target shape, depth, A grouped cost, B-double count, zig count, source event case/interval and reflected event.

The reachable relation starts at the exact post-prefix pair and includes every nontrivial core KEEP at every non-diagonal state. A root no-op is an omitted zero-cost self-loop. At A=B, all subsequent shared KEEPs remain diagonal, with q_B=floor(d/2)<=2ceil(d/2)=2a_A. A diagonal state is therefore a proved absorbing terminal for this excess audit. The graph is complete for every pre-synchronization continuation; later diagonal transitions need not be enumerated again because they cannot add positive excess.

The exact reachable counts are:

| Certificate object | Count |
| --- | ---: |
| Core tree shapes | 429 |
| Source table rows | 3,003 |
| Reachable relation states | 18,450 |
| Non-diagonal states | 18,235 |
| Absorbing first-diagonal states | 215 |
| Nontrivial shared-KEEP edges | 109,410 |
| Positive edges, q_B-2a_A>0 | 324 |

There is no word horizon or state cutoff. The queue is exhausted below the proved40,569 bound. Every graph edge is exactly two independently verified source-table transitions. Every listed state has a finite predecessor path from the seed. A separate depth-first traversal independently reconstructs the same relation set.

## The proposed invariant is false

The intended claim was that every subsequent core KEEP satisfies q_B<=2a_A. The324 positive edges refute it. Their edge excess is one; this is consistent with the core bound q_B<=3 and nontrivial a_A>=1. It is not a bound on accumulated excess along a longer path, and324 distinct graph edges are not a pooled resource or a claim of324 attainable units in one word.

The first breadth-first positive edge has a shortest six-KEEP extension from the seed:

    6,5,3,7,1,4.

Independent source replay verifies that the last K4 has A depth2, B depth6, a_A=1 and q_B=3. Thus outer-fringe activation is NOT necessary to obtain another positive block. The proposed core-only obstruction must not be retained as a theorem.

The graph certificate does not classify maximum cumulative excess, positive-weight strongly connected components, all possible return identities or G/J feasibility. Those would require a separately determined analysis; none is silently assumed here. The all-horizon reachable relation is verified, while the particular universal edge inequality is refuted.

## Arbitrary fringe and reflection

For any finite F with keys>7, core searches never enter F. The same source frames preserve it at core7.right, so all core transitions, costs and the reachable relation commute with substituting F. This gives a structural arbitrary-fringe extension; no larger finite n is replayed or fitted. Reflection maps the core to the corresponding upper seven keys and F to an untouched lower fringe. All reflected thirteen-key source contexts are executed independently as part of the table audit.

Queries entering F before synchronization are outside this relation. A later cycle with additional DELETEs is also outside the literal two-reset-prefix domain. No general no-amplification or high-budget-cycle conclusion is drawn for either extension.
