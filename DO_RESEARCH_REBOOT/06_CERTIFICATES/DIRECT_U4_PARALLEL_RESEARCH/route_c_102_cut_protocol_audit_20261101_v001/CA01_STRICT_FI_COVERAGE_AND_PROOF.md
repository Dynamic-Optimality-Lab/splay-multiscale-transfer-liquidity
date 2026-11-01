# The102-action nowhere-diagonal walk is in FI and outside UD

2026-11-01, Asia/Karachi. **PROVED: strict FI closed-walk coverage beyond UD.** The source witness and its protocol classification are exact, with no larger finite fit.

|Established protocol|Accepted cuts|Rejected cuts|Final unpaid debt|
|---|---:|---:|---|
|UD|0|102|1 through5|
|FI|92|10|0 on acceptance;1 on rejection|

All102 cyclic cuts were scanned for each protocol, for exactly one period each. The reflected source walk has the same results. An independent implementation passed418,253 checks, including complete source-fact reconstruction, every reservation, every physical assignment, chronological debt cursors, pool retirement, source reflection and all rejected tails. There are no reused, startup, earlier-lap or later-lap credits.

The established theorem that every UD-successful cut is FI-successful gives UD subset FI on reachable source closed walks. This actual reachable witness has no successful UD cut and has successful FI cuts, so the inclusion is **strict**. This closes the previously open nonvacuity of strict FI closed-walk enlargement. It does not prove that FI accepts every reachable closed walk; universal Step3/Coarse-Double remains OPEN.

## The fixed source object

The inherited NI witness is the102-action H5=P W^5 X, where numerical lists denote shared KEEP keys:

\[
\begin{aligned}
P&=D3,D5,K7,K6,K5,K3,K7,K1,\\
W&=K(2,1,5,3,4,5,7,3,1,6,4,5,3,2,3,7,1),\\
X&=K(5,4,2,6,7,2,4,3,1).
\end{aligned}
\]

Its recurrent start has A core R7 and B core1->2->3->4->7, with7.left=6 and6.left=5. Both have the same unqueried subtree F>7 at7.right. NI proves exact joint closure, reachability from a diagonal source pair, nowhere-diagonal recurrent states and exactly two one-StepEv resets per period. All102 cyclic A-root blocks are singleton positive leaders. The source word is a non-simple closed walk, not a simple cycle.

The actual costs are

\[
A=137,\quad Q_B=98,\quad Z_B=63,\qquad
E=G_B=J_B=R_{\rm imm}=5>4=C_D.
\]

Positive source occurrences are zero-based17,34,51,68,85, each KEEP6 with(a,q)=(1,3). Each is followed by KEEP4 with(a,q)=(1,2), then KEEP5 with(a,q)=(1,1). Thus the immediate helper has zero actual spare, but the delayed KEEP5 has one actual spare unit. Whether a protocol certifies that unit is the point of this audit.

The reachability startup is separate and contributes zero credits to every audited pass. Cut k starts at physical recurrent occurrence k, wraps at most once, and visits each of the102 physical pools exactly once. Every cut starts with empty charging history and zero debt; the actual source pair at that cut is the corresponding state of the closed walk.

## The established reservations, without a future-work oracle

Use the definitions in old UD01 and FI01. For a positive anchor i and a later KEEP payer j with key y, h_i(y) is y's depth in the anchor's B destination, and k_i(j) counts genuine intervening B-changing KEEPs, including zero-double zigs. DELETEs and B-root no-ops do not count.

UD reserves using

\[
c_{UD}(i,j)=\lfloor h_i(y)/2\rfloor+k_i(j).
\]

FI keeps that ceiling when k=0. When k>=1, it refines only the FIRST intervening B change S_x, on the original post-anchor tree T:

\[
c_{FI}(i,j)=\lfloor U_T(x,y)/2\rfloor+k_i(j)-1.
\]

U is the proved first-intervention source-frame bound, computed from original source paths, entry roles and later outer frames. It is not a lookup of actual payer work or a repeated exact-depth update. Both ceilings are0 for KEEP-less payers.

At a nonpositive physical pool of capacity C=2a, take the minimum over **all encountered positive facts, including paid anchors**. Reserve r=min(C,c_min), or the full C if history is empty. Own demands occupy the reserved prefix. Only[r,C) may lend, oldest residual first. A visited pool is retired, with unused units discarded. These rules are followed identically at every cut; histories and budgets from alternatives are not combined.

## Why every UD cut rejects

There are five positive anchors and95 nonpositive KEEP payers, giving475 cyclic anchor/KEEP-payer facts. The exact source-fact certificate verifies

\[
c_{UD}(i,j)\ge2a_j
\quad\text{for every one of these475 pairs}.
\]

Therefore every KEEP payer under UD reserves its **entire** capacity. With empty history this is prescribed directly; with nonempty history every available ceiling is at least that capacity. KEEP pools can never lend, at any cut. Positive pools also do not lend.

The only possible UD loans come from D3 and D5, with four units total. Every one-period pass encounters five distinct one-unit positive debts. Since the reset units cannot be reused or multiplied, at least one debt must remain at the end of every pass. This proves rejection at all102 cuts independently of which cut exposes the DELETEs before or after the debts.

The full enumeration corroborates the proof: final UD debt1 occurs at33 cuts, debt2 at17, debt3 at18, debt4 at17 and debt5 at17. At cut0 the DELETEs arrive before any history and are retired; all five debts remain. No claim that earlier unused capacity can be banked is made.

`UD_no_KEEP_lending_certificate.json` lists all475 integer inequalities, not a sampled subset or fitted ceiling.

## The source-frame fact that releases FI capacity

Fix the first positive anchor, occurrence17=KEEP6. For y=5 in B immediately after that splay,

\[
h=3.
\]

The immediate next B change is occurrence18=KEEP4. Its original source depth is4, and its bottom-up frame word is

\[
RL,\ LR.
\]

The original inner frame has grandparent3 and parent5. Tracked y=5 enters as that parent, so the proved first-gain allowance is mu=0. One later outer LR double shifts the tracked target fringe upward by1. No matching RR double is present. The source-only bound is consequently

\[
U_T(4,5)=\min(3+2,\max(0,3+0-1-0))=2.
\]

At delayed payer occurrence19=KEEP5, exactly one genuine B change intervenes. Hence

\[
c_{UD}=\lfloor3/2\rfloor+1=2,
\qquad
c_{FI}=\lfloor2/2\rfloor+0=1.
\]

This payer has actual capacity2 and own B work1. UD reserves both units and lends none. FI reserves exactly one unit and lends the other to the earlier KEEP6. Additional retained source facts cannot invalidate this loan: their minimum is no greater than the displayed ceiling1, and soundness requires it to be at least the actual own demand1. Thus the minimum and reservation are exactly1.

The same source pair and frame fact recur inside all five physical W copies. At FI cut0 the five loans are:

|Positive KEEP6 occurrence|Immediate KEEP4|Delayed KEEP5 payer|Third B-double demand|Distinct A unit|
|---:|---:|---:|---|---|
|17|18|19|(0,17,2)|(0,19,0,1)|
|34|35|36|(0,34,2)|(0,36,0,1)|
|51|52|53|(0,51,2)|(0,53,0,1)|
|68|69|70|(0,68,2)|(0,70,0,1)|
|85|86|87|(0,85,2)|(0,87,0,1)|

Demand IDs are(period,source occurrence,B-event index); B zigs are excluded. Unit IDs are(period,source occurrence,A-event index,bit). All IDs use period0. The five donated bit1 units are distinct and outside their payers' own reserved prefixes. The other93 B demands pay from their own source pools. Thus cut0 supplies a complete injection of all98 demands into98 distinct actual A units, with no DELETE or startup credit.

`FI_three_block_payment_certificate.json` contains the five source facts and the complete98-assignment injection.

## Why FI accepts exactly92 cuts

Each positive occurrence i is repaid in its internal three-block span(i,i+1,i+2). These five spans are disjoint. A physical cut splits such a span only when it starts at i+1 or i+2. Therefore the ten rejected cuts are exactly

    18,19,35,36,52,53,69,70,86,87.

If the cut begins at i+1, anchor i is last in the pass and has no later lender. If it begins at i+2, the delayed pool was retired at the beginning; the final anchor is followed only by its immediate KEEP4, whose two units are all required for its own demands. Either way exactly one debt remains. An extra lap or banked starting pool would change that answer and is not allowed.

At every other cut all five repayment triples fit within the one-period order. Each delayed KEEP5 certifies the unit just proved, so all debts are paid. This gives102-10=92 successful cuts and explains the independent enumeration, rather than replacing it with a successful-cut assertion.

## Verification, all-size scope and pipeline consequence

The producer identifies first entry by original-path LCA depth. The independent checker instead uses membership in original source subtrees and rebuilds the FIFO transfers unit by unit. It verifies all970 ordinary/reflected source facts, all408 protocol passes, all41,616 block visits and all physical assignments and tails. After every aligned step it checks FI reservation and total-debt dominance over UD, with paid source facts retained.

The102-cut classification is **FINITE-EXACT** on the pinned concrete source walk. It extends to the same fixed H5 with arbitrary untouched fringe F>7: every query, tracked payer key, path, frame, h, k, A/B cost and reservation is unchanged by fringe substitution. Thus the same witness and cut results hold for every n>=7 with F=R_[8,n], and in the reflected order. No new m values, larger n replays or finite fits are used or claimed.

The original universal FI accepted-cut theorem now has a demonstrated strict closed-walk class beyond UD. The witness's source-identity and immediate-template obstruction remain true. This result does not prove universal cut success, a bound on all walks outside FI, or universal Coarse-Double. No new campaign follows this audit. Matching-terminal remains FROZEN, and all125 Stage11G files and prior statuses are preserved.
