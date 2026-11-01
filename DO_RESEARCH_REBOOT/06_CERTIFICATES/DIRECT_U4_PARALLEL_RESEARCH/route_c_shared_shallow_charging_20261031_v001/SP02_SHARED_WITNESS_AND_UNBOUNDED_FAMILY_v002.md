# Two positive anchors use distinct slices of one delayed payer

The new witness is an analytically specified source word at thirteen keys, not a potential fit, size sweep or state-graph search. Its non-unit consecutive positives give strict coverage beyond delayed private charging and the named older unit-run packet classes.

## Diagonal prefix and exact closed word

Start diagonally at R13 and execute prefix D9. Freeze the cycle

    K13 K12 K11 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D9.

Independent pointer replay verifies exact A/B closure and

    A=60, Q_B=35, Z_B=28, 2A-Q_B=85.

The prefix proves reachability; none of its A credits is used for the closed-cycle charge. All forty-one cycle accesses are A-root block leaders in this witness. The only positive run is its first two blocks.

| Role | Request | a | q | delta=q-2a |
| --- | --- | ---: | ---: | ---: |
| First anchor | KEEP13 | 2 | 6 | +2 |
| Second anchor | KEEP12 | 1 | 3 | +1 |
| Saturated intervener | KEEP11 | 1 | 2 | 0 |
| Common delayed payer | KEEP2 | 2 | 0 | -4 |

The packet's total deficit is -1. The intervener spends both its own units on its two B doubles and lends none.

## Why the construction has these source values

Put M=2(1,4(3,6(5,8(7,empty)))), with omitted leaf children empty. The source RR recurrence gives

    S_9 R13=9(M,R_[10,13]).

Thus KEEP13 starts at A depth 4 and B depth 12, giving a=2,q=6. After it A is

    13(10(9(M,empty),12(11,empty)),empty),

while B=S_13 R13 has root 13 and a left subtree whose right spine visits 2,4,6,8,10,12. KEEP12 therefore starts at A depth 2 and B depth 6, giving a=1,q=3.

After KEEP12 the source trees are

    A=12(10(9(M,empty),11),13),
    B=12(2(1,6(4(3,5),10(8(7,9),11))),13).

KEEP11 then starts at A depth 2 and B depth 4, giving a=1,q=2. After it,

    A=11(10(9(M,empty),empty),12(empty,13)),
    B=11(2(1,10(6(4(3,5),8(7,9)),empty)),12(empty,13)).

Payer KEEP2 is at A depth 3 and B depth 1, giving a=2,q=0. These are the source formulas fixed before evaluation, including parent-first same-side doubles.

## One B ceiling and one physical credit pool

Before the first positive, the shallow set is {1,2}. Before the second it is {13,2}. Their intersection is exactly {2}. Key 2 has actual post-anchor depth h=1 after each positive.

For the first anchor, KEEP12 and KEEP11 are the two genuine intervening B changes before payer KEEP2: k=2 and ceiling 2. For the second, only KEEP11 intervenes: k=1 and ceiling 1. Both bound the same payer work, so

    c_shared=min(2,1)=1,
    E_run=2+1=3,
    E_run+c_shared=4=2a_payer.

The minimum tightens the payer's B-work bound. It is not extra money, and the two ceilings are not added. The sole actual payer pool has four distinguishable units.

The first anchor uses its four local units, leaving two demands; it receives payer slots [0,2). The second uses its two local units, leaving one demand; it receives payer slot [2,3). Payer q=0 uses no remaining unit. Slot 3 is unused. Every transfer has a concrete A-StepEv/bit identity, and no unit is repeated. In particular the saturated KEEP11 contributes no hidden credit.

The full cycle's 35 B demands are assigned distinct units among its 120 A units. Reflection has the same values. Every cyclic cut, including cuts through the positive run and across the shared payer, retains the same physical slices and source identities.

## Closure and arbitrary fringe lift

Following the common payer, the ascending requests KEEP3 through KEEP10 produce identical full trees at KEEP10:

    10(L_[1,9],R_[11,13]).

All later common KEEPs remain diagonal. The full ascending and descending passes restore R13, and final D9 restores S_9 R13 in A with B frozen at R13. The source certificate independently checks the synchronization and full closure.

An arbitrary unrequested finite BST of keys greater than 13 may be grafted to key 13's right child. All fixed requests are <=13, so the graft remains attached and commutes with every source operation. The same depths, deficits, shared slices and full closure hold for arbitrary fringe size and shape.

For genuine unbounded KEEP support, let n>=13, start diagonally at R_n, retain prefix D9 and use

    K13 K12 K11 K2 K3 ... Kn
    K1 K2 ... Kn
    K(n-1) ... K1 D9.

This cycle has 3n+2 accesses. Until synchronization at KEEP10, the extra right vine at 13 is untouched, so the fixed local computation lifts unchanged. The remaining KEEPs are on identical full trees. Full ascending/descending source scans restore R_n, and D9 restores the initial A. Every key is genuinely requested by KEEP; the only positives and shared payer remain unchanged.

This is an analytic family, not finite extrapolation. No other finite size was searched or evaluated to select the word or coefficients.

## Strict coverage and independent checks

DS rejects the new word because its first positive is immediately followed by another positive, leaving no private payer before the next positive. The common-pool construction admits both anchors together. The first anchor's deficit 2 excludes the named older unit-positive run/packet predicates. Its immediate successor is not its former root and its positive successor violates the older delayed nonpositive-intervener conditions. The second anchor's first three successors likewise do not return to its former root. Thirteen genuine KEEP targets exclude the <=5-support classes. These comparisons use pinned necessary conditions; old recognizer execution is not claimed.

All four DS/SC source words and their reflections remain accepted with identical rows and totals. Independent verification checks 172 cycle rows, ten diagonal-prefix rows, all 172 cyclic cuts and 116 actual demand-credit assignments. A separate source-domain check validates all 746 raw tree occurrences, strict BST ordering, exact ranked key sets and the predeclared initial vines and words.

This proves a strictly larger restricted charging class. It does not establish common-payer admissibility for every source run, sharing across separate runs or universal CD.
