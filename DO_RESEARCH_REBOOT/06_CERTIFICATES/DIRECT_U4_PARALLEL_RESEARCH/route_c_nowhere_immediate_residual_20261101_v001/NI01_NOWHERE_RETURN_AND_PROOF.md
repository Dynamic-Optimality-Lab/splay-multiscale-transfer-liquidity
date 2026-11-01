# Nowhere-diagonal D3,D5,K7 return beyond immediate helpers

2026-11-01, Asia/Karachi. **PROVED—RESTRICTED DOMAIN.**

An explicit reachable, nowhere-diagonal closed A/B walk has exactly two one-StepEv resets per recurrent period and

\[
E=G_B=J_B=5>4=C_D.
\]

It also has R_imm=5: five units of positive demand remain after giving every immediate next KEEP helper its entire actual spare capacity. Even all four DELETE units cannot pay those five residual units. This removes both defects of the previous example: diagonal return and repayment by distinct immediate helpers.

The actual period has102 source actions, A=137, Q_B=98 and Z_B=63. It has no full seven-key ascending or descending scan in either the cyclic full request sequence or the cyclic KEEP subsequence. It is a **non-simple closed walk**, not a simple cycle. FI acceptance and UD rejection at every cut are not established. Universal Coarse-Double remains OPEN.

## Explicit initial pair and return word

Let F be any BST with all keys greater than7, including the empty tree. T(F) is the right chain1,...,7 with F at7.right. Form V(F) by leaving the right chain1,2,3,4 in place and replacing its subtree rooted at5 by7(6(5,empty),F). Thus V(F) has the right path1,2,3,4,7 and the left chain7,6,5.

The recurrent initial pair is

\[
(A_0,B_0)=(T(F),V(F)).
\]

Its core IDs are(0,4), state12919 of the pinned source relation. Both trees have root1 but are unequal. They contain exactly the same keys. F is identical in the two trees and remains untouched.

Write Kx for a shared KEEP splay and Dx for an A-only DELETE splay, with the key retained in the tree. Define

\[
\begin{aligned}
P&=D3,D5,K7,K6,K5,K3,K7,K1,\\
W&=K(2,1,5,3,4,5,7,3,1,6,4,5,3,2,3,7,1),\\
X&=K(5,4,2,6,7,2,4,3,1),\\
H_m&=P\,W^m\,X\qquad(m\in\mathbb Z_{\ge0}).
\end{aligned}
\]

The exact source identities are

\[
(T(F),V(F))\xrightarrow{P}(A_u(F),B_u(F))
\xrightarrow{W}(A_u(F),B_u(F))
\xrightarrow{X}(T(F),V(F)).
\]

The intermediate pair has core IDs(60,94), state1871. With x(L,R) notation, bare keys denoting leaves and a dot denoting empty,

\[
\begin{aligned}
A_u(F)&=1(\cdot,4(2(\cdot,3),7(6(5,\cdot),F))),\\
B_u(F)&=1(\cdot,7(2(\cdot,3(\cdot,6(5(4,\cdot),\cdot))),F)).
\end{aligned}
\]

Every equality is of the complete A/B trees, not merely roots, B alone, or cost profiles.

## The two physical resets and nowhere-diagonal closure

D3 and D5 act on the actual A=R7 core. Their edge depths are2, with the single RR StepEvs[1,3] and[3,5]. B stays rooted at1, while A's roots after the DELETEs are3 and5. These intermediate pairs are unequal.

The actual recurrent B source V(F) has depth4 to7, so its KEEP7 costs **q_B=2**, not the q_B=3 from a fresh diagonal right vine. This actual source computation sends state12919 to the old off-diagonal seed state0. The banked KEEP path6,5,3,7,1 then reaches1871. It is valid to pass through transient seed0 before entering the recurrent component; the previous stronger requirement of direct output into that component was unnecessary.

All W and X states lie in the independently certified18,232-state off-diagonal component containing1871 and12919. The DELETE intermediates, seed bridge, loop states and return states are all checked unequal, including the cyclic last/first boundary. Therefore every H_m is nowhere-diagonal throughout its recurrent period.

There is exactly one D3 and one D5 in H_m and no DELETE in W or X. Every cyclic adjacent query key differs, so every maximal A-root block is a singleton positive leader, both DELETE blocks are KEEP-less, and C_D=4. Repeating W creates new KEEP source events, never extra copies of the reset credits. The request word cannot be a proper power of a shorter reset word because D3 occurs exactly once.

## The aligned surviving-demand loop

The source table gives this exact17-KEEP profile for W:

|Occurrence|KEEP|a_A|q_B|
|---:|---:|---:|---:|
|1|2|1|1|
|2|1|1|0|
|3|5|3|2|
|4|3|2|1|
|5|4|1|1|
|6|5|1|0|
|7|7|1|0|
|8|3|2|1|
|9|1|1|1|
|10|6|1|3|
|11|4|1|2|
|12|5|1|1|
|13|3|1|1|
|14|2|1|0|
|15|3|1|0|
|16|7|2|1|
|17|1|2|1|

The only positive delta=q_B-2a_A is occurrence10, KEEP6: delta=1. Its immediate successor KEEP4 has a_A=1,q_B=2 and hence **zero actual spare capacity**. In particular, it cannot repay that excess even if a recognizer could see its exact future work instead of a conservative ceiling.

The same positive KEEP6 contributes1 to G_B and1 to J_B because its q=3 is followed by q=2. In this source family the guard contribution and the un-repaid immediate demand come from the **same physical occurrence**. This differs from the previous loop, whose J contribution had sufficient own A work and whose positive occurrences had cheap helpers.

Since every active core depth is at most6, q<=3. The standard disjoint high/low helper formula reduces exactly to J_B=count of cyclic q=3 occurrences whose successor q>=2. The only such occurrence in W is the displayed KEEP6.

Define the generous immediate-KEEP residual

\[
R_{\rm imm}
=\sum_{i:\delta_i>0}
\max\!\left(\delta_i-\max(2a_{j(i)}-q_{j(i)},0),0\right),
\]

where j(i) is the immediate next cyclic KEEP. Each successor has only one immediate predecessor, so these successor pools cannot be reused across distinct anchors. The definition grants all actual spare, not just a source-ceiling-certified suffix. DELETE pools are separate. For W,

\[
(A,Q_B,Z_B,E,G_B,J_B,R_{\rm imm})=(23,16,11,1,1,1,1).
\]

## Uniform amplification, without a larger fit

The base return P X has17 actions with A=22,Q_B=18,Z_B=8 and no positive excess or q=3 occurrence. W returns the exact pair, and its sole high and positive occurrence has its KEEP4 successor strictly inside the copy. The first and last W q values are both1, so no J or immediate-residual contribution can change at a copy boundary. Consequently, for every m>=0,

|Quantity|H_m|H_5|
|---|---:|---:|
|Source actions|17+17m|102|
|Physical DELETE resets|2|2|
|A StepEvs|22+23m|137|
|B doubles Q_B|18+16m|98|
|B final zigs Z_B|8+11m|63|
|Positive excess E|m|5|
|Pure DELETE capacity C_D|4|4|
|G_B|m|5|
|J_B|m|5|
|Surviving immediate demand R_imm|m|5|

Thus **every m>=5** meets all requested numerical bounds and the stronger R_imm>C_D condition. The choice5 follows from these exact identities, not from trying larger words or fitted coefficients.

## Exact obstruction to immediate-pair plus DELETE repayment

In H_5 the five KEEP6/KEEP4 pairs occupy zero-based source occurrences

    (17,18), (34,35), (51,52), (68,69), (85,86).

These ten physical occurrences are disjoint. Each pair has3+2=5 B-double demands and2(1+1)=4 local A units. Together they contain **25 distinct demands and20 distinct local units**. Adding every unit from the two DELETEs adds only4, leaving the strict cut

\[
25>20+4=24.
\]

Therefore no repayment restricted to those immediate pair pools plus all reset units can cover those demands in one period, with any allocation and without reuse. At least one capacity contribution from a KEEP outside those pair supports is necessary. This is a cut in that restricted repayment template, **not** a deficient set in the original unrestricted charging graph. Delayed KEEP contributions are expressly outside this obstruction.

`immediate_helper_cut.json` lists all25 demand IDs, all20 pair-unit IDs and all4 DELETE-unit IDs. Every identity includes the physical period and source occurrence. No earlier startup, extra lap, alternative cut or multiplied reset credit is used. More generally the cut has5m demands versus4m+4 local/reset units, with deficit m-4.

## Reachability, arbitrary fringes and both orientations

The recurrent start is reachable from the diagonal(T(F),T(F)) by the source-exact startup word

    D3,D5,K7,K4,K2,K7,K6,K7,K2,K4,K3,K1.

This startup has its own two DELETEs and is **separate** from H_m. The recurrent period still has exactly two physical resets. Startup units and costs are not used to fund the period; the nowhere-diagonal claim concerns the closed recurrent period, not the diagonal startup.

All queries and recorded rotation endpoints lie in1,...,7. F is never entered by an accessed search path; rotations move it as one untouched subtree at7.right. Substitution of any BST F>7 therefore preserves every event, cost, inequality, source-pair distinction and exact return. Choosing F=R_[8,n] gives the family for every n>=7, including empty F at n=7. No larger n was replayed or fitted. Order reversal and child swapping give the reflected family; the concrete thirteen-key table independently executed that reflection under x mapped to14-x.

## What is proved and what remains

The four-rule gate preceded the complete local audit:282 internal positive edges and1,508 internal successor fragments in the fixed component. Exactly16 fragments had zero-spare successors; the first in the predeclared order fixed the construction. Its connecting and return paths are supplied, not postulated. The independent checker passed10,706 checks, including source composition, complete fragment classification, reachability, reflected events, cyclic blocks, exact resets, all-m seams and the physical cut. All detailed actual source trees are in `full_source_replays.json`.

The requested **nowhere-diagonal numerical return beyond immediate helpers is established** for this explicit all-m, arbitrary-untouched-fringe family. The family itself satisfies Q_B<=2A from its exact costs. No FI acceptance or UD rejection at every cut has been proved, and no strict new FI-only walk class is claimed. Universal Step3/CD remains OPEN. Matching-terminal is FROZEN. All prior research and all125 Stage11G files remain unchanged.
