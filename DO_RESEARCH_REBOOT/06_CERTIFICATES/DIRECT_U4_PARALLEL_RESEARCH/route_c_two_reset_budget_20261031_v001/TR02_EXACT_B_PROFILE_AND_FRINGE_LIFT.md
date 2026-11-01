# Exact recurrent B profile for the fixed two-reset gate

Status: FINITE-EXACT for the stated thirteen-key source identities; PROVED structurally for the corresponding fringe extension. No A-policy candidate was executed after the necessary budget failed.

The predeclared new KEEP order is

    V=1,9,5,13,3,11,7,2,10,6,4,12,8.

The actual source identity is

    S_V(R13)=T,
    S_V(T)=T,
    T=8(4(2(1,3),6(5,7)),12(10(9,11),13)).

Here k(L,R) is a node and a bare key is a leaf. The tuple/pointer sources agree on every rotation event, depth and raw source/destination tree in both rounds. The first exact whole-boundary repeat is at round two, returning to the round-one state. The recurrent thirteen source states are distinct, so the B period is primitive. Determinism proves every subsequent complete round repeats this profile; no finite stability extrapolation is used.

| KEEP key | B depth before access | B doubles q | Final zig z | max(q-2,0) |
| --- | ---: | ---: | ---: | ---: |
| 1 | 3 | 1 | 1 | 0 |
| 9 | 4 | 2 | 0 | 0 |
| 5 | 6 | 3 | 0 | 1 |
| 13 | 5 | 2 | 1 | 0 |
| 3 | 4 | 2 | 0 | 0 |
| 11 | 6 | 3 | 0 | 1 |
| 7 | 5 | 2 | 1 | 0 |
| 2 | 3 | 1 | 1 | 0 |
| 10 | 4 | 2 | 0 | 0 |
| 6 | 5 | 2 | 1 | 0 |
| 4 | 4 | 2 | 0 | 0 |
| 12 | 5 | 2 | 1 | 0 |
| 8 | 6 | 3 | 0 | 1 |
| Total | | 27 | 6 | 3 |

The gate's two effective depth-two resets each have one A StepEv and two units. Their four-unit funding already exceeds the entire possible three-unit positive excess in this B period. Arbitrary A shapes or different reset targets cannot increase E beyond G_B=3, by TR01. No FI-only cycle can result under the gated effective-two-reset condition.

## Independent old-profile check

The pointer audit also replays the PREVIOUS B order W from R13 for two rounds. The first round reaches the exact raw B state already stored in SR's shared-boundary source bank; the second returns to it. Its recurrent Q_B=23 and G_B=4. Reflection is checked request by request with full interval/orientation conversion. This is a validation of the prior source obstruction, not a second new skeleton tried after V failed.

There are 26 new-order B requests and 26 old-order B requests per orientation, giving 104 pointer source calls and 208 raw BST source/destination occurrences. No A splay, two-reset policy case, new paired cycle, FI/UD cut trial or cycle credit map is counted in this audit.

## Arbitrary unrequested fringe and A trajectory

Attach any BST F with keys >13 at key 13's right child in R13. Both B orders request only core keys <=13, so no search enters F. Every source rotation carries F as an unchanged off-path fringe. Replacing that leaf by F commutes with the finite source identities and fixed-round recurrences. All requested-key depths, q vectors and G_B budgets stay exactly the same. Reflection gives the corresponding left-fringe construction; order-preserving relabeling handles finite rank labels if desired.

TR01's inequality E<=G_B did not restrict A's internal structure. On these B cycles it therefore applies to every actual A trajectory with the same key set, including A-only requests to fringe keys, provided the closed word has the stated complete B rounds and enough distinct positive-cost KEEP-less blocks. Additional A cost cannot evade the lower funding bound. No particular reset key sequence, source policy or finite A recurrence is assumed to exist in that argument.

Thus the old-order obstruction E<=4p<=C_D and new-order obstruction E<=3p<4p<=C_D extend to arbitrary unrequested fringe size and shape. They exclude the stated multi-reset strictness families without a larger finite fit. They do not prove that G_B is bounded by four for other B skeletons, that arbitrary cycles are UD-covered, or that FI and UD have equal full closed-walk classes.

The declared 78 path-reset policies were deliberately not run. The gate required stopping if the B-only necessary test failed, and it did. No source A/B closure or strict new CD case is asserted. Universal Step 3/CD remains OPEN; matching-terminal work remains frozen and Stage 11G unchanged.
