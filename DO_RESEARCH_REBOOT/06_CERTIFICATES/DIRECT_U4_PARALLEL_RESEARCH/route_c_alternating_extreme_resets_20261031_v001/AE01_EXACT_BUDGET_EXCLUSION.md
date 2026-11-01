# The alternating-extreme candidate fails its recurrent B budget

Status: FINITE-EXACT for the B orbit, plus PROVED—RESTRICTED DOMAIN for the source budget exclusion on that orbit. The requested A/B witness is NOT FOUND. There is no universal two-reset nonexistence claim.

The one word fixed before execution was

    V=(9,5,13, 3,11,7,1, 2,10,6,13, 4,12,8,1).

Its bursts alternate terminal maximum13 and minimum1. It has no cyclic ABA and contains every key1,...,13. It does not contain the K12,11,10,...,1 consecutive descending restoration tail used in the preceding AC obstruction. That exact scan-tail theorem is not the reason this attempt fails.

From diagonal R13, one V lap sends B to

    B*=1(.,8(2(.,4(3,6(5,7))),12(11(10(9,.),.),13))).

The next V returns exactly to B*. R13 differs from B*, and the first two lap boundaries at B* agree. Thus the first whole-word recurrence has one transient lap and period one. All fifteen recurrent source B states are distinct, so this is a simple source B cycle, not repeated-period padding. The certificate records every input/output tree and source event; the pointer engine independently reconstructs them and their reflection.

The recurrent profile is:

| Position | KEEP | B depth | B doubles q |
| ---: | ---: | ---: | ---: |
| 0 | 9 | 5 | 2 |
| 1 | 5 | 6 | 3 |
| 2 | 13 | 3 | 1 |
| 3 | 3 | 5 | 2 |
| 4 | 11 | 6 | 3 |
| 5 | 7 | 7 | 3 |
| 6 | 1 | 3 | 1 |
| 7 | 2 | 3 | 1 |
| 8 | 10 | 5 | 2 |
| 9 | 6 | 5 | 2 |
| 10 | 13 | 3 | 1 |
| 11 | 4 | 5 | 2 |
| 12 | 12 | 4 | 2 |
| 13 | 8 | 7 | 3 |
| 14 | 1 | 3 | 1 |

Consequently Q_B=29,Z_B=12 and

    G_B=sum max(q-2,0)=1+1+1+1=4.

## Why no A policy is executed

In a nontrivial cyclic A-root block the actual leader cost is a>=1, including a DELETE leader followed by starved KEEP of that key. A block has at most one genuine B-changing KEEP. Therefore its positive excess obeys

    max(q-2a,0)<=max(q-2,0),
    E<=G_B.

For any coupling using the certified recurrent B lap and exactly two effective pure one-StepEv resets, C_D=4. Hence

    E<=4=C_D.

This excludes the requested E>C_D witness before any reset key, gap or A state needs to be computed. In particular it excludes admissible effective realizations of all 105 declared gap-pair policies. A policy with an ineffective fallback would not have two effective resets and would fail the requested reset condition; this proof does not claim its E<=C_D without that condition. No A-policy orbit was run or classified.

For a recurrent policy that repeats p full V laps with two effective one-StepEv resets in every lap, the same source budget gives E<=4p=C_D. A longer A recurrence therefore cannot help that policy class. A cycle with more than two physical reset blocks is not counted as a cycle with two resets. Other distributions across repeated laps and other B orbits/seeds are not classified here.

The first transient B lap is a reachability prefix, not recurrent surplus or cycle capacity. Borrowing its costs or multiplying periods cannot raise the certified per-lap bound. All capacities are assigned to their actual physical source blocks once.

## The immediate-helper diagnostic is also unfavorable

The established adjacent-helper budget J_B pairs each q>=3 with its immediate q<=1 successor. Here the three pairs are positions(1,2), (5,6), (13,14), all with q=(3,1). Their residual upper contributions max(3+1-4,0) are zero. Position4, K11, remains an unpaired contribution one. Thus J_B=1.

The inherited BC02 sufficient theorem says C_D>=J_B gives some old-UD accepting cut on an actual closed coupling with these distinct adjacent KEEP keys. At C_D=4 that proof already applies, independently of the weaker raw G test. No literal return to the previous B root is required for these helpers: a positive query supplies the next key's exact fresh own-work ceiling. Avoiding ABA alone does not avoid automatic helper repayment.

J_B is a conservative residual upper budget, not an exact debt value or new pool. Neither its calculation nor the B-only orbit assigns actual A costs, constructs a paired cycle, proves FI-only coverage or changes universal CD.

## Uniform untouched-fringe extension and exact scope

Graft any finite untouched BST F with keys>13 at the right child of core13 in R13. All requested targets remain in the core, so every B search and source rewrite commutes with that substitution. Requested depths, event counts, G_B=4, J_B=1 and the two-lap B recurrence remain unchanged. Thus the same budget exclusion applies to core-only A couplings of that fringe family. Reflection gives the corresponding lower-fringe statement. This is an analytic substitution argument; no larger finite key size is executed.

The failed construction is one fixed seed/word/reset architecture. The source-exact A/B cycle requested on some other non-scanning architecture remains OPEN. The earlier 26-KEEP obstruction, B-only witnesses, matching-terminal freeze and every Stage 11G status remain unchanged.
