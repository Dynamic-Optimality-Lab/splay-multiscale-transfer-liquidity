# REBOOT-01: equal-signature sibling erasure

**Status: PROVED — RESTRICTED DOMAIN, universal over the stated subclass.** This is a written mathematical proof of a source-defined identity, not a Lean certificate. It removes sibling quantification for qualifying SAME-CHILD pairs; it does not prove their base width or construct an admissible J.

## Definitions and exact domain

A finite valid BST has distinct keys in a totally ordered set, with strict left/right ordering. Depth d_B(y) counts edges (the root has depth zero). Write B=[p,T,S], with u≠v in T. The mirrored orientation is B=[p,S,T]. In both cases B0 retains p and the same positioned child T and replaces only S by the empty tree.

The source's backward fold returns (a_L,a_R,(f_0,...,f_(d−1)),c). Its terminal state is (0,0,[],0) for even d, and (-1,0,[1],0) or (0,-1,[1],0) for odd d, according to the side of y relative to the original root. It then applies Tmap to the reversed bottom-up double word. The four exact maps are:

| Pattern | a_L' | a_R' | prepended fringe coefficients | c' |
|---|---|---|---|---|
| LL | a_L−2 | a_R−1 | (1+a_R,2+a_R) | c+1+2a_R |
| RR | a_L−1 | a_R−2 | (1+a_L,2+a_L) | c+1+2a_L |
| LR | a_L−1 | a_R−1 | (a_L,1+a_R) | c+a_L+a_R |
| RL | a_L−1 | a_R−1 | (a_R,1+a_L) | c+a_L+a_R |

Each map preserves all previous fringe coefficients as the tail. The top fringe coefficient is f_y=f_(d_B(y)−1). It is defined even when that fringe is empty.

Partition the keys other than y into y's left and right descendant subtrees, off-path fringe blocks F_j at ancestor distance j+1 from y, and the ancestors of y (NONE). These blocks are disjoint and exhaustive: a nonancestor's path either continues below y or first diverges at a unique ancestor of y. The source assigns coefficients a_L,a_R,f_j,0 to these blocks. Thus its two fold evaluators give exactly

\[
R_{static}(B,y)=c_y+\sum_{z\ne y}\lambda_{yz}.
\]

Define tau_yz=(slot_yz,lambda_yz,d_B(z)−d_B(y),d_B(y)). A shared assignment consists of arbitrary functions j(tau) and rho(c) on every realized coordinate; repeated atoms are counted repeatedly. No gauge, UG, root normalization, or NONE identification is imposed. Define

\[
J_y(B)=\sum_{z\ne y}j(\tau_{yz})+\rho(c_y),\quad
H_y(B)=-R_{static}(B,y)+4(|B|-subsize_B(y))+J_y(B),\quad D_J(B;u,v)=H_u(B)-H_v(B).
\]

## The theorem

For every such B,u,v and every shared assignment j,rho, if d_B(u)=d_B(v)=d and f_u=f_v, then

\[
\boxed{D_J(B;u,v)=D_J(B_0;u,v).}
\]

Consequently |D_J(B;u,v)|≤2 if and only if |D_J(B0;u,v)|≤2 under the same assignment. All equal-depth pairs of odd ambient depth qualify. The theorem holds separately in both child orientations, without assuming any left/right symmetry of j.

## Proof: all old contributions are fixed

Fix a row node y in T. Deleting S changes no path to an old node in {p}∪T, no old-node depth, no subtree rooted at y, and no double pattern on the path to y. Therefore the fold outputs a_L,a_R,f,c are unchanged. Its root atom rho(c_y) is unchanged.

For every old z≠y, its membership in L,R,F_j,NONE is unchanged: only the root's off-path sibling block loses keys. Its coefficient lambda_yz, depth difference, and row depth are unchanged. Hence its complete tau and its contribution to J_y are unchanged. This argument treats occurrences individually; when several keys share one tau, all those old occurrences retain their multiplicity. A newly added key may share an old tau, but that adds exactly one occurrence and does not modify an old one.

Every z in S lies in the unique top fringe F_(d_B(y)−1). It has lambda_yz=f_y. Its contribution to R_static is f_y; none of these keys belongs to y's subtree. With d_y=d_B(y), summing the complete differences gives

\[
\boxed{H_y(B)-H_y(B_0)=(4-f_y)|S|+
\sum_{z\in S}j(F_{d_y-1},f_y,d_B(z)-d_y,d_y).}
\]

There are no other contributions. In particular the root atom has zero difference, the subtree-size difference is zero, and the n-term contributes precisely 4|S|.

## Proof: cancellation and parity

For u,v at equal d with equal f, the right sides of the boxed row formula agree term by term. The two sums range over exactly the same keys with identical tau values. Subtracting gives D_J(B)−D_J(B0)=0.

If d is odd, the terminal fringe list is [1]. Every subsequent Tmap prepends two entries and preserves the existing tail. There are (d−1)/2 such maps, so its last entry f_(d−1) remains 1. This is an induction on the number of maps, covering arbitrary depth. Thus both u,v have f=1. For completeness, at even d≥2 the first fold map applied to (0,0,[],0) produces last entry 2 for LL/RR and 1 for LR/RL; subsequent maps preserve it. Equal f is therefore an exact path-class condition, not a numerical guess.

## Mirror, empty sibling, and leaf insertion

Reflection exchanges LL↔RR, LR↔RL, and a_L↔a_R; the displayed maps show that f and c transform accordingly. The terminal zig states exchange. The path/slot argument also applies verbatim with T on the right and S on the left. This proves the mirrored cancellation within each reflected tree. It does not assert H or D are numerically equal between reflected trees for an arbitrary asymmetric j.

S=empty makes the sum and |S| term zero, so the boundary case holds exactly. Alternatively, repeatedly delete a leaf of S: each deletion leaves all surviving-node depths unchanged and gives the same cancellation. Every finite sibling BST reaches empty by finitely many such deletions, with p,T,u,v fixed.

For arbitrary distinct u,v in the fixed child (without equal-signature assumptions), a new leaf e at ambient depth h gives the complete identity

\[
\boxed{D_J(B';u,v)-D_J(B;u,v)=f_v-f_u+
j(F_{d_u-1},f_u,h-d_u,d_u)-j(F_{d_v-1},f_v,h-d_v,d_v).}
\]

This identity follows from the same old-occurrence proof and checks the signs in the proposed 26AB formula. With bar-j=j−lambda its right side is bar-j(a_e)−bar-j(b_e), but equating different atoms would require an additional established equation. REBOOT-01 uses identical atoms, so it requires no such equation.

## Nonvacuity and limits

Take p=80 and T=[40,[20,[10],[30]],[60,[50],[70]]], where [k] means a leaf. The pair u=10,v=30 has ambient depth 3 and f=1. S can be any finite valid BST with keys greater than 80. The theorem deletes S entirely for this pair, including arbitrarily deep siblings.

The exact full difference for this example contains a constant −7 and nonzero J-coordinate coefficients (recorded in verification_results.json). It is therefore not a tautological zero row or an already automatic width bound. Attaching arbitrary valid one-child ancestors above T, then a new root p, produces equal-depth/equal-f pairs at arbitrarily large depths. Reflection supplies right-child examples.

The remaining inequality on B0 may fail for an arbitrary j,rho. The theorem does not assert that such an assignment is admissible, or that an admissible global assignment exists. It merely removes an independent structural variable from these original row cases with no new compatibility assumption. Unequal depths, equal even depths with different f, cross-child pairs, root/child pairs, and J-SELF remain unresolved.

## Source binding and validation

The exact definitions are in scripts/wp6_staticR.py:21-131 (especially Tmap:58-69), scripts/wp6_lambda.py:49-104, and scripts/wp6_j4shared.py:17-76,78-150. Exact SHA-256 hashes and actual AST function line spans are in 10_EXPERIMENTS/verification_results.json; HEAD alone is insufficient because the source tree is dirty.

Command: `python -B DO_RESEARCH_REBOOT/10_EXPERIMENTS/verify_reboot.py` from the repository root. Selected pure function ASTs are read from the source; no source module initialization or entry point is run. Integer symbolic coefficient dictionaries cover 3,528 valid contexts (T sizes 1–6, S sizes 0–3, both orientations), 19,404 full row comparisons, 2,232 qualifying pair erasures, 4,872 arbitrary-pair leaf insertion comparisons, and 62 deeper family checks. All pass exactly. These computations are FINITE-EXACT supporting checks; the arbitrary-depth proof is the argument above.
