# Uniform FI/UD separation for H_m, every m>=5

2026-11-01, Asia/Karachi. **PROVED—RESTRICTED DOMAIN, uniform in m, fringe size and orientation.**

For every integer m>=5, every BST fringe F with all keys greater than7(including empty F), and the source-defined reachable recurrent pair below,

\[
H_m\in FI\setminus UD.
\]

More precisely, with N_m=17+17m singleton cyclic A-root blocks,

\[
\begin{array}{c|cc}
&\text{accepted cuts}&\text{rejected cuts}\\\hline
UD&0&17+17m\\
FI&17+15m&2m.
\end{array}
\]

Every rejected FI cut has exactly one unpaid demand. Every UD cut has final debt at least m-4>0; this lower bound is attained at cut2, while cut0 leaves debt m. Each pass starts with empty charging history, scans one physical period and uses no startup, other-lap, alternative-cut or reused units. This theorem is proved from fixed source identities, not larger H_m trials or a fit in m.

## 1. Exact source identity and indexing

Write Kx for shared KEEP splay at x and Dx for A-only DELETE splay, with the key retained. Let T(F) be the right chain1,...,7 with F at7.right. Let V(F) have right path1,2,3,4,7, with7.left=6,6.left=5 and7.right=F. Start the recurrent period at(T(F),V(F)). The established NI source identity is

\[
\begin{aligned}
P&=D3,D5,K7,K6,K5,K3,K7,K1,\\
W&=K(2,1,5,3,4,5,7,3,1,6,4,5,3,2,3,7,1),\\
X&=K(5,4,2,6,7,2,4,3,1),\\
H_m&=P W^m X.
\end{aligned}
\]

P reaches a fixed unequal joint pair u, W returns exactly u, and X returns to the recurrent start. All source pairs in P,W,X and their joining seams are off-diagonal. Every A leader is positive; consecutive query keys differ, including the cyclic seam. The two DELETEs each have one actual RR StepEv. All other requests are KEEPs, and each genuinely changes B, including those with zero B-double count and a final zig. Consequently all blocks are singletons, C_D=4, and the genuine B-change counts are6 in P,17 in W and9 in X.

The unique positive W occurrence is local slot9(zero-based), KEEP6, with a=1,q=3,delta=q-2a=1. There are no other positive occurrences in P,W,X. For copy r,0<=r<m, the global source occurrence is

\[
i_r=8+17r+9=17+17r.
\]

Its immediate successor i_r+1 is KEEP4 with(a,q)=(1,2); its delayed payer i_r+2 is KEEP5 with(a,q)=(1,1). Each triple is internal to its W copy. The triples have disjoint supports since adjacent anchors are17 source blocks apart inside the repetition. Across X P the B-change gap between consecutive anchors is32, so no boundary creates a closer anchor.

These source identities hold for arbitrary F by untouched-subtree substitution. The recurrent pair is reachable from the diagonal by the previously supplied startup; its units never enter the recurrent proof. The periods are non-simple closed walks, not claimed to be simple cycles.

## 2. Every UD KEEP pool is fully reserved, for every m

For an encountered positive anchor i and a later nonpositive KEEP payer j, the established UD ceiling is

\[
c_{UD}(i,j)=\lfloor h_i(y)/2\rfloor+k_i(j),
\]

where y is the payer key, h_i(y) its depth in the anchor's B destination, and k_i(j) the number of genuine B-changing KEEPs STRICTLY between them in the selected one-period order. DELETEs do not increment k. Zero-double zigs do.

Every queried key lies in the seven-key active core. Source search paths do not enter F, so d_A<=6, a<=3 and every KEEP capacity C=2a is at most6.

**Long lag.** If k>=7, then

\[
c_{UD}(i,j)\ge k\ge7>6\ge C_j.
\]

This argument has no upper bound on k or m. It applies across any number of complete copies and across the X P boundary.

**Short lag.** If0<=k<=6, j is among the first seven genuine B changes after i. They are exactly the seven contiguous W slots10,...,16 in the SAME copy. All occur before its end; no repetition/return seam or DELETE can intervene. Since every anchor has exactly the same post-anchor B tree, only the following seven source identities are required:

|W slot|KEEP key|a|q|h_i(key)|k|UD ceiling|Capacity2a|
|---:|---:|---:|---:|---:|---:|---:|---:|
|10|4|1|2|4|0|2|2|
|11|5|1|1|3|1|2|2|
|12|3|1|1|2|2|3|2|
|13|2|1|0|1|3|3|2|
|14|3|1|0|2|4|5|2|
|15|7|2|1|1|5|5|4|
|16|1|2|1|2|6|7|4|

Every ceiling is at least its capacity. This table is a bounded set of exact local source cases; completeness comes from the short/long lag argument, not from testing more periods.

Thus **every encountered anchor fact** gives c_UD>=C for every KEEP payer, at every m and every cut. If history is empty, UD reserves C by definition. Otherwise the minimum of its retained source ceilings is still at least C. Hence all KEEP reservations equal C and their lending suffixes are empty. Paid anchors remain in history; adding them cannot change this conclusion. Positive pools themselves do not lend.

## 3. UD rejects all cuts when m>=5

Each pass encounters m distinct one-unit positive debts. The only pools that may lend are D3 and D5, each of capacity2, so total lending is at most4. Physical pools are retired once; their credits cannot be copied with W, banked across periods or imported from a startup. Therefore

\[
D^{UD}_{\rm final}\ge m-4>0
\]

at every physical cut. UD accepts no cut of H_m for m>=5.

The endpoint bounds are exact. At cut0, D3 and D5 occur before any positive history; their pools are retired and no KEEP can lend, so final debt is m. At cut2, the pass starts with the first KEEP of P, encounters all m anchors, and ends with D3,D5. Their ceilings are0 and their four units lend to already pending debt, leaving exactly m-4. Neither argument changes the source trace or uses another lap.

## 4. The same FI source identity repays every positive

Let B* be the B tree immediately after W slot9=KEEP6. It is identical at every anchor because W returns the exact source pair. The first intervening B change is always the following KEEP4, also on the identical B* source tree.

For tracked y=5 in B*, h=3. KEEP4 has original depth4 and bottom-up source frame word RL,LR. The inner RL frame's original parent is5, so y enters as the parent with first-gain allowance mu=0. One later outer LR double decreases its target-fringe depth by1; there is no matching RR double. The established source-only frame ceiling is

\[
U_{B^*}(4,5)=\min(3+2,\max(0,3+0-1-0))=2.
\]

No future payer work or observed first-post depth selects this bound. At KEEP5=i_r+2 the newest anchor has k=1, giving

\[
c_{FI}(i_r,i_r+2)=\lfloor2/2\rfloor+1-1=1.
\]

The pool has C=2 and own demand q=1. Retained **older** anchor facts cannot remove the released unit. They have the same B* and the same first intervention KEEP4. A later payer with key5 cannot be that immediate KEEP4, so every older such fact has k>=1 and

\[
c_{FI}=\lfloor2/2\rfloor+k-1=k\ge1.
\]

The newest fact supplies1 and every other fact supplies at least1, so the minimum is EXACTLY1. FI reserves the own-work unit and releases one real suffix unit, regardless of how many paid facts are retained.

For the immediate KEEP4, the newest fact has h=4,k=0 and ceiling2. Every older anchor is at least17 genuine B changes farther back. Since U(4,4)=0, its refined ceiling is k-1>=16. Hence this pool reserves exactly2 and pays its own two doubles, without lending. The same statement follows from soundness and own demand2, but the explicit source facts show the reservation directly.

## 5. Chronological induction and no reused credits

Suppose no debt is pending immediately before a complete repayment triple. KEEP6 uses its two own units for its first two doubles and adds one debt. KEEP4 uses its two units for its own two doubles; debt remains1. At KEEP5 the preceding source fact releases one suffix unit. FIFO assigns it to the sole pending anchor and returns the debt to0:

\[
0\longrightarrow1\longrightarrow1\longrightarrow0.
\]

Between such triples there are no positives, so zero debt stays zero. Paid anchors stay in history, but the minimum-ceiling argument above is independent of their number. Induction in chronological triple order therefore proves FI acceptance whenever all m triples fit wholly inside the one-period cut. In particular cut0 works for every m>=5.

The explicit recurring assignment is

\[
\text{B demand }(0,i_r,2)
\quad\longleftarrow\quad
\text{A unit }(0,i_r+2,0,1),\qquad0\le r<m.
\]

Demand IDs are(period,source occurrence,B-event index), excluding B zigs. Unit IDs are(period,source occurrence,A-event index,bit). Every KEEP5 has one A event; bit0 pays its own B double and bit1 pays the earlier anchor. Different r give different source occurrences, hence different units and demands. The anchor's first two doubles use only its own two units. Every other demand pays from its own reserved prefix, disjoint from every donated suffix. There are18+16m demands and18+16m distinct assigned units, with zero DELETE or startup units. Source-shape repetition does not identify physical events across copies.

This is an explicit one-period injection with no existence premise or endpoint credit.

## 6. Exact FI cut classification for every m>=5

Set N_m=17+17m. A cut starts at one of the N_m physical source occurrences, with empty charging history and no banked pool. The m triples(i_r,i_r+1,i_r+2) are disjoint, and none crosses the fixed P|X period seam.

If a cut starts at i_r+1, anchor i_r is the last block of that pass. It adds one debt and has no later payer. If a cut starts at i_r+2, its delayed pool was retired at the beginning; the final anchor is followed only by its immediate KEEP4, all of whose capacity is required for its own two demands. In both cases that final debt cannot be paid in the permitted period. All other triples remain complete and pay by the induction, so final debt is exactly1.

These are the only cuts that split a repayment triple. At any other cut, begin with zero debt, retire any initial nonpositive pools, and apply the complete-triple induction in order. Every anchor is then paid. Therefore

\[
\begin{aligned}
\text{FI rejected cuts}
 &=\{18+17r,19+17r:0\le r<m\},\\
\#\text{FI rejects}&=2m,\\
\#\text{FI accepts}&=N_m-2m=17+15m.
\end{aligned}
\]

The2m indices are distinct and valid: distinct copy indices differ by multiples of17, while the two offsets differ by1; the largest rejected index is17m+2<N_m. Alternative cuts are separate passes, not jointly available budgets. No second lap is used to repair a rejected cut.

## 7. Quantifiers, verification and remaining boundary

The proof holds for every integer m>=5, not a bounded tested range. It uses only the existing34 source rows of P,W,X, seven short-lag UD facts, the fixed FI frame identity, a capacity bound and induction on disjoint physical triples. No H_m at another m is generated or run. The earlier H5 result is consistent with the formulas(N=102, FI accepts92), but is not an induction premise.

All active queries and tracked payer keys stay in the seven-key core, and the source identities preserve F at7.right. Replacing F by any BST on larger keys changes none of the paths, depths, frames, event costs or source-pair distinctions used here. Choosing F=R_[8,n] proves the same result for every n>=7. Order reversal and child swapping give the reflected family, with identical capacities, ceilings, physical indices and unit accounting.

The independent checker reconstructs the kernel and phase seams, the seven source cases and FI entry by original-subtree membership. It checks complete case coverage using the seven genuine successors and capacity bound, symbolic support/gap arithmetic, both orientations and physical-identity disjointness, without replaying another m. The mathematical all-m induction and cut classification are the proof above; finite local checking is validation of its exact premises, not a finite-fit replacement.

Thus every H_m,m>=5, is a reachable nowhere-diagonal member of FI outside UD. This supplies an unbounded explicit source family for the established strict FI closed-walk class. It does not show that FI covers arbitrary reachable walks, and universal Step3/Coarse-Double remains OPEN. Matching-terminal stays FROZEN. Stage11G and all earlier research/status files remain unchanged.
