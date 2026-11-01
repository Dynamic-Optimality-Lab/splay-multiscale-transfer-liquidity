# All276 fixed-tour mode assignments have zero positive excess

Status: FINITE-EXACT for the declared twenty-four-action, thirteen-key source class and reflection. Every boundary orbit reaches its FIRST exact repeat within the declared64-lap cap. There are no cap-limited cases. The requested G_B>=5,J_B>=5,two-reset,E>C_D witness is NOT FOUND. No general nonexistence theorem is claimed.

## Complete outcome

| Actual recurrent pair property | Cases |
| --- | ---: |
| One A period, exactly two pure one-StepEv resets | 168 |
| Two A periods, four physical pure one-StepEv resets | 108 |
| No A=B source state in the recurrent word | 12 |
| Of those, one period and exactly two resets | 9 |
| Of those, two periods and four resets | 3 |
| G_B>=5 | 0 |
| J_B>=5 | 0 |
| E>C_D | 0 |
| Cap-limited / unclosed cases | 0 |

The transient whole-lap counts are zero for183 cases, one for90 and two for3. The recurrent periods are one for168 and two for108. The tuple and pointer sources agree on every raw boundary tree and the first-repeat indices; A is exactly T_1 at all those boundaries by the independently verified source identity.

In fact every KEEP in every replayed transient or recurrent word has B edge depth at most FOUR, and therefore q_B<=2. The recurrent quantities are consequently

    G_B=J_B=E=0 in ALL276 cases.                             (1)

For the168 exact-two-reset cycles C_D=4; for the108 longer cycles C_D=8. The longer periods fail the physical reset-count criterion independently, but their budgets are also zero. No artificial period multiplication, prefix demand or alternate-case capacity can meet either threshold.

The source depth ceiling in (1) is an exact statement about this complete pinned corpus, not a universal bound on arbitrary tours, BSTs or n. A larger-n fit or an unproved all-tour induction is not used.

## A concrete non-diagonal failure control

The first lexicographic one-period control with no diagonal state is case45, DELETE positions2 and3 (zero-based), keys4 and6. Its literal word is

    K3,K2,D4,D6,K5,K7,K9,K8,K10,K12,K11,K13,
    K11,K12,K10,K8,K9,K7,K5,K6,K4,K2,K3,K1.

One actual lap from the diagonal R13 reaches the recurrent pair with A=R13 and B equal to the right vine on1,2,3,4,6,7,...,13 with key5 as the left child of6. The next identical literal word returns to that exact pair. Every A action still costs one event, and the two DELETE blocks are pure one-StepEv blocks. Its totals are

    A=24, Q_B=16, Z_B=8, C_D=4, G_B=J_B=E=0.

The recurrent walk has no A=B source state. It has15 distinct paired source states across24 actions, so it is explicitly a non-simple closed walk, not a promoted simple-cycle witness. The requested numeric thresholds fail. This illustrates that exact A closure and persistent separation were achieved within the class; the missing property is positive excess. It is not counted as a successful candidate or a new original CD case.

## Every demand pays locally, without credit reuse

For each actual source occurrence t, its sole A event gives two distinguishable units (case,t,event0,bit0/1). Its B doubles have their original source event indices; final zigs are omitted from that demand list. Since q_B<=2, assign double ordinal b to its own unit (case,t,event0,bit=b). Units from pure DELETE blocks are unused. Unused prefixes or bits are not banked.

The independent verifier constructs and checks5,746 such local assignments over the276 normal recurrent walks, and verifies the reflected events separately. All demand identities and unit identities are unique within their physical case. Different cases/orientations are alternative resource universes and are never pooled. No reachability-prefix, later-lap or alternate-cut unit pays a demand.

Every block is nonpositive, so this local certificate works at every physical A-root cut. Old UD and FI therefore accept every cut by their existing local-work rule; no cut recognizer, new allocation optimizer or historical-fact theorem is executed here. This is already covered behavior, not strict FI-only coverage.

## Analytic untouched-fringe family

Substitute an arbitrary finite BST F with keys>13 at the right child of core13 in the diagonal tree. Every requested key, in both modes, is in the core. No search enters F and every core source rewrite preserves it as that same attached fringe. The fixed A identity becomes T_r with F at its core13 right child; its costs and closure remain unchanged. The same substitution commutes with every recorded B transition and recurrence. Projection deleting F recovers the original core states.

Thus all276 exclusions, local assignments and budgets remain valid for this untouched-fringe family of arbitrary total size. Reflection gives the corresponding lower-fringe family. This is a structural substitution proof, not additional finite replay. It does not classify extra-key requests, arbitrary initial pairs, other tours or unbounded genuine KEEP support.

The declared source class is exactly excluded. General existence of the user-requested non-scanning A/B cycle with both budgets at least five remains OPEN.
