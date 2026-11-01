# Shallow successor charging proves a restricted Coarse Double class

Status: PROVED—RESTRICTED DOMAIN. For every finite reachable closed present-key pair walk in the source-defined class below, Q_B<=2A. There is no bound on tree size, KEEP-support size, walk length, or fringe shape. The class hypotheses are explicit restrictions, not asserted universal source facts.

The depth transport component already follows from the banked 26AL displacement theorem. Its direct source proof is included for completeness. The new result is the immediate-successor charging class, which admits old-root children as well as the old root and strictly extends the banked 26AJ class. Generic CD and Stage 11G remain OPEN and unchanged.

## Source quantities and cyclic blocks

At a present-key request x, a=ceil(d_A(x)/2) counts A StepEvs. A KEEP also has q=floor(d_B(x)/2) B doubles and a possible final zig z=d_B(x) mod 2. DELETE splays A only; actual q=z=0. Depth counts edges.

If the closed walk has A=0, every request targets the same fixed A root. B is frozen except for KEEPs of that key; after the first such KEEP it cannot change again. Exact B closure therefore forces every B splay to have been a no-op, so Q_B=0. The empty walk and empty/one-key boundaries are included.

Otherwise split the cycle at its positive-A-cost accesses into maximal A-root blocks B_i. A block consists of one leader with a_i>=1 followed by zero-A-cost accesses. All of them request its leader key x_i, since a present-key A no-op must target the current root. Before the first KEEP in the block B is unchanged; that KEEP roots B at x_i, and later same-key KEEPs are no-ops. Hence there is at most one nontrivial B splay per block. Let q_i count its doubles, or zero if it has none. Define

    delta_i=q_i-2a_i,
    sum_i delta_i=Q_B-2A.

This is the source block decomposition from 26AJ, without changing any original operation or cost.

## Source lemma for the old root and its original children

Let T be any finite nonempty BST with root r. Let y be r or either nonempty original child of r. For any present target x,

    d_(S_x T)(y)<=3.                              (1)

The stronger old-root bound is <=2. To prove this directly, use the source's bottom-up search frames. Earlier StepEvs consume only inner frames. The original root is first consumed by the final StepEv, and original fringe subtrees outside the path are not rotated internally.

| Tracked node and source path | Its final depth bound | Source reason |
| --- | ---: | --- |
| Old root r, target already r | 0 | No-op |
| Old root r, final zig | 1 | Old root becomes target's child |
| Old root r, final same-side double | 2 | Parent rotates over grandparent first; old root is below the parent |
| Old root r, final opposite-side double | 1 | Old root is target's child |
| Root child y off the search path | 3 | It stays a child of r, whose final depth is <=2 |
| Root child y is the target | 0 | Present-key root property |
| Root child y on path, target depth even >=2 | 1 | It is the parent in the final double |
| Root child y on path, target depth odd >=3 | 3 | It is grandparent in the penultimate double, then undergoes the final root zig |

For the last row, the penultimate double roots its rebuilt unit at x and puts y at relative depth at most 2. The sole remaining outer frame is r. The final zig can increase y's depth relative to the new root x by at most one, by moving the facing fringe below r. Thus the final depth is at most 3. In the off-path case, each of the four source double formulas leaves the original far child attached to r; no ancestry claim about a changed fringe is assumed.

These cases exhaust target depth zero, depth one, positive even depth and odd depth at least three, and both root children. Swapping left/right gives the same cases in the other orientation. The proof uses the actual parent-first LL/RR order in `_rebuild`; replacing it by two target-over-parent rotations is unnecessary and is not done.

The bound 3 is sharp: in R4, splay 4 and track the old root's child 2. Its depth changes 1->3. A subsequent access to 2 has one B double. The reflected control has the same values. These exact controls are independently checked; the universal statement follows from the case proof.

## Restricted class

For every block i with delta_i>0, let x_i be its key and let T_i be B immediately before that block's unique nontrivial B splay. Let j=i+1 cyclically, and let y=x_j be the next block's leader key. Require:

    d_(T_i)(y)<=1,                                (S1)
    delta_i<=2a_j-1.                              (S2)

Thus y is the old B root or one of its original children. S2 is the source A threshold a_j>=ceil((delta_i+1)/2). It is openly a restricted-domain condition; no universal availability of that A work is claimed. There is no assumed aggregate packet sum, unknown allocation, or potential witness.

For unit-positive blocks delta_i=1, S2 follows automatically from a_j>=1. The unit-positive corollary therefore needs only S1 at every positive block.

## Successor repayment

The positive block really splays B because q_i>0. By (1), after its splay y has depth at most 3. The rest of the block cannot change B: DELETEs freeze it and later KEEPs are B-root no-ops. In the successor block B stays unchanged until its first KEEP of y. Therefore

    q_j<=1,
    delta_j<=1-2a_j<=-1.                          (2)

If the successor has no KEEP, q_j=0 and the same bound holds. Combining (S2) and (2),

    delta_i+delta_j<=delta_i+1-2a_j<=0.            (3)

The successor is forced negative. Distinct positive blocks therefore own disjoint adjacent pairs: sharing a block would make a positive block someone else's negative successor. The cyclic successor map itself is injective. An alleged one-block positive case would pair the block with itself and contradict (2); it cannot satisfy the hypotheses. Two-block cases and seam-crossing pairs follow by the same sign argument.

All unpaired blocks are nonpositive, since every positive has its pair. Summing (3) and those singletons proves Q_B-2A<=0. This is a completed proof on the stated class, not a conditional theorem awaiting another open source lemma.

## Explicit unit charging with no reuse

Give each A StepEv two distinct credit units. In a positive block i, pay its first 2a_i B doubles with its own leader credits. Its remaining delta_i demands use the first delta_i units of its successor's leader pool. Pay the successor's at most one B double from the next unused unit in that pool. S2 gives delta_i+1<=2a_j, so these uses fit.

Every unpaired nonpositive block pays its q_i<=2a_i demands locally. The adjacent pairs are disjoint; leaders have disjoint actual event identities. Thus every B double is assigned one actual credit and no credit is reused. The assignments can cross the cyclic seam and may use successor work: this is closed-walk scalar charging, not a claim of an online algorithm or the original refuted creator/setup eligibility graph.

No terminal function, matching potential, or matching optimization appears in this proof. The user-imposed matching-terminal freeze remains active.

## Exact relation to older results and remaining scope

The 26AJ capacity class is contained here: its successor is exactly the old root, so (S1) holds at depth zero, and its A-capacity condition is (S2). SC02 supplies an explicitly reachable old-child successor that fails 26AJ, so the inclusion is strict. Necessary source predicates also exclude the witness family from the named AJ-AS and <=5-support domains; these comparisons do not claim an exhaustive account of every logical consequence of prior work.

The complementary cases remain unresolved: a positive block may have no shallow immediate successor, its successor may lack the stated A capacity, or repayment may require delayed/overlapping regions. No assertion is made that all reachable walks satisfy S1-S2. Universal CD, the full Step 3 witness, and all Stage 11G statuses are unchanged.
