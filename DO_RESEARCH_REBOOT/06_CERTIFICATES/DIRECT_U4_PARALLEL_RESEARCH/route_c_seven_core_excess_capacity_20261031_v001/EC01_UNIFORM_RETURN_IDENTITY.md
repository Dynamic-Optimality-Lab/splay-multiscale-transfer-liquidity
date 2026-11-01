# Source-exact D3,D5,K7 amplification and return

Completed 2026-11-01, Asia/Karachi. **PROVED—RESTRICTED DOMAIN.**

There is an explicit family of closed A/B walks with exactly two physical one-StepEv resets and

\[
(E,C_D,G_B,J_B)=(2+2m,4,2+3m,m)\qquad(m\in\mathbb Z_{\ge0}).
\]

In particular, every m>=5 satisfies the requested numerical conjunction. The m=5 word has139 actions, A=204, Q_B=176, Z_B=73, E=12>4=C_D, G_B=17 and J_B=5. No larger finite fit or new source engine was used.

This is a closed walk with repeated source pairs and a diagonal return. It does **not** certify a nowhere-diagonal cycle, FI acceptance, or UD rejection at every cut. Universal Coarse-Double remains OPEN.

## The explicit identity

Write Kx for a shared KEEP splay at x and Dx for an A-only DELETE splay. DELETE does not remove the key. A grouped StepEv costs one; each such event supplies two capacity units. A B double contributes one demand, and a B final zig contributes zero double demand.

Let F be any BST whose keys are all greater than7, including the empty tree. Let T(F) be the right chain1,2,...,7 with F at7.right. Both executions start at exactly T(F).

Define the following concrete words, with all numerical lists denoting KEEP keys:

\[
\begin{aligned}
P&=D3,D5,K7,K6,K5,K3,K7,K1,\\
W&=K(4,1,5,6,2,3,7,1,\ 4,2,5,1,3,5,6,7,\ 1,3,2,4,5,3,7,1),\\
X&=K(4,2,6,4,1,3,2,5,4,2,1),\\
H_m&=P\,W^m\,X.
\end{aligned}
\]

The exact source identities are

\[
(T(F),T(F))\xrightarrow{P}(A_u(F),B_u(F))
\xrightarrow{W}(A_u(F),B_u(F))
\xrightarrow{X}(T(F),T(F)).
\]

Using x(L,R), with a bare key denoting a leaf and a dot denoting an empty subtree,

\[
\begin{aligned}
A_u(F)&=1(\cdot,4(2(\cdot,3),7(6(5,\cdot),F))),\\
B_u(F)&=1(\cdot,7(2(\cdot,3(\cdot,6(5(4,\cdot),\cdot))),F)).
\end{aligned}
\]

These are core IDs(60,94), state1871, in the pinned source relation. They have common root1 and are unequal. W returns this exact pair, including every subtree; it does not just return the common root or B alone.

The only DELETEs of H_m are the single D3 and single D5 at its start. Their source paths have edge depth2 and exactly one RR StepEv each: [1,3] and [3,5]. There is no DELETE inside W or X. All consecutive query keys, including the cyclic last/first boundary, differ. Thus all maximal A-root blocks are singleton positive leaders, both DELETE blocks are KEEP-less, and C_D=2+2=4 for every m. Inserting more W copies creates new KEEP events, not new resets or copies of the old DELETE credits.

## Exact loop cost and J identity

The following rows are source costs at each successive occurrence of W, starting from the displayed pair:

|Occurrence|KEEP|a_A|q_B|
|---:|---:|---:|---:|
|1|4|1|3|
|2|1|1|0|
|3|5|2|1|
|4|6|1|1|
|5|2|2|2|
|6|3|2|1|
|7|7|2|1|
|8|1|2|1|
|9|4|1|3|
|10|2|1|1|
|11|5|2|1|
|12|1|2|1|
|13|3|2|2|
|14|5|1|1|
|15|6|1|1|
|16|7|1|0|
|17|1|2|3|
|18|3|1|2|
|19|2|1|1|
|20|4|2|1|
|21|5|1|1|
|22|3|1|1|
|23|7|2|1|
|24|1|2|1|

Consequently

\[
A(W)=36,\quad Q_B(W)=31,\quad Z_B(W)=13,\quad E(W)=2,\quad G_B(W)=3,\quad J_B(W)=1.
\]

Only occurrences1 and9 have positive delta=q_B-2a_A, each exactly1. All active B depths are at most6, so q_B<=3. For this source domain, the high/low helper-pair definition reduces exactly to

\[
J_B=\#\{i:q_i=3,\ q_{i+1}\ge2\},
\]

where adjacency is cyclic in the B-active KEEP sequence. This follows because a high3 paired with a successor0 or1 has residual max(3+q_next-4,0)=0, and every unpaired3 contributes1. Such high/low pairs are disjoint.

In W the highs are at1,9 and17. The first two have successors0 and1; only occurrence17 has successor2 and contributes to J_B. Notice that occurrence17 has a_A=2, so this J contribution is **not** itself a positive-excess source occurrence. The three budgets are not interchangeable.

## Proof for every repetition count

The old literal return P X has19 actions with

\[
(A,Q_B,Z_B,E,C_D,G_B,J_B)=(24,21,8,2,4,2,0).
\]

Since W returns the exact pair, all additive costs and positive excesses add independently on each copy. The only non-additive quantity requiring a boundary check is J_B.

The final KEEP of P has q=1. The first and final KEEPs of W have q=3 and1. The first KEEP of X has q=3. Therefore replacing the seam P|X by P|W^m|X creates no extra J contribution and loses none: every new seam is1 followed by3, and the sole contributing3 followed by2 in each W copy stays inside that copy. The cyclic X|P seam is unchanged. Hence J_B(H_m)=m, including m=0.

The resulting identities, with no asymptotic error or unproved terminal bound, are:

|Quantity|H_m|H_5|
|---|---:|---:|
|Source actions|19+24m|139|
|Physical DELETE resets|2|2|
|A grouped events|24+36m|204|
|B doubles Q_B|21+31m|176|
|B final zigs Z_B|8+13m|73|
|Positive excess E|2+2m|12|
|Pure DELETE capacity C_D|4|4|
|G_B|2+3m|17|
|J_B|m|5|

Choosing m=5 comes directly from the exact threshold inequalities, especially J_B=m>=5. It is not a fit over larger words. The word contains one D3 and one D5, so it cannot be a proper power of a shorter reset word. It is still a non-simple closed walk because W returns a previously visited pair.

## All-size substitution and reflection

Every query lies in1,...,7. Every recorded grouped rotation has endpoints in1,...,7. The subtree F at7.right is not on an accessed search path and is moved only as a complete uninspected subtree by the source rotations. Substituting any BST F>7 therefore preserves every transition, event, cost and pair equality in the identity.

For every n>=7, choosing F=R_[8,n] gives the identity starting from the exact diagonal(R_n,R_n). For n=7 the fringe is empty. No replay at a larger n is needed for this source-substitution argument. Reversing order and swapping children gives the reflected identity; the concrete thirteen-key source table independently executed that reflection with x mapped to14-x.

The all-size claim is restricted to this explicit word family and untouched-fringe embeddings. It is not an inequality for arbitrary A/B source pairs or arbitrary request words.

## Verification and proof boundary

`independent_audit.json` records53,143 independent integer/source-consistency checks, including the entire fixed graph, all SCCs, the actual source composition, reflected grouped events, reset and cyclic-block counts, and the all-m seam identity. `full_source_replays.json` supplies the complete actual thirteen-key trees before and after every occurrence, in both orientations. The old source table had already been independently executed in tuple and pointer engines; this campaign adds zero engine calls and zero finite fits.

`event_unit_injection_certificate.json` checks an explicit injection of all176 B-double demands in H_5 into176 distinct physical A units. Twelve assignments use a distinct next-KEEP spare unit; all other assignments use their own source occurrence. It uses no DELETE units and no reachability-prefix units. The positive excesses are therefore not a claim of unpaid demand. No FI/UD protocol classification is inferred from the numerical thresholds alone.

The predeclared stronger test required an off-diagonal state in the selected component with A=R7 whose literal D3,D5,K7 destination lay in that same component. All34 such inputs were checked; none satisfies that exact destination condition. This excludes only that specified direct re-entry predicate. It does not exclude destinations outside this component, transient excursions, or other nowhere-diagonal constructions. No replacement search was launched.

**What is deleted:** the open existence of a source-exact literal two-reset D3,D5,K7 return with G_B,J_B>=5 and E>C_D, within this diagonal-return/untouched-fringe domain. **What remains:** the intended non-synchronizing/FI-only closed-walk separation and universal Step3/CD. Matching-terminal remains FROZEN; all125 Stage11G files and prior statuses remain unchanged.
