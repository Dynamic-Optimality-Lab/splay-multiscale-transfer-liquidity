# Gate for shallow successor charging on reachable walks

2026-10-31, Asia/Karachi. Continue Step 3 with one strictly restricted source charging lemma. The user-imposed matching-terminal freeze remains active. No potential, terminal matching, graph feasibility problem or class-wide no-go is proposed. Old sources, reports, statuses, Git and Stage 11G remain read-only; all new writes are exclusive to this run.

## Exact smaller target

Use cyclic maximal A-root blocks. A block has one leader of positive A cost a_i, followed by root no-ops of that same key; B has at most one nontrivial KEEP in it. Put delta_i=q_i-2a_i. The zero-A cycle is handled separately.

For every positive block i, freeze these two source-testable hypotheses:

1. Its next block's leader key y is at depth at most 1 in B immediately BEFORE the positive block's nontrivial B splay of x.
2. delta_i <= 2a_(i+1)-1.

Prove CD for all reachable closed walks satisfying these hypotheses, with arbitrary key set, support, length, DELETEs and fringes. This is a restricted source class, not a claim that the hypotheses hold universally.

## Concrete source mechanism

A splay carries the old B root and both its original children to depth at most 3. Source proof: an off-path root child stays attached to the old root, which finishes at depth <=2. An on-path root child is either the target, participates as parent in the final even-depth double (depth 1), or is the grandparent of the penultimate odd-depth double (depth <=2 before the final root zig, hence <=3 afterward). Root no-ops and reflection are included. This is also a consequence of the banked 26AL displacement bound, but the restricted root/child proof will be written directly from the pinned source.

Therefore the next block's first B splay has q_(i+1)<=1, or q=0 if it has no KEEP. Its deficit is at most 1-2a_(i+1). The displayed A threshold pays delta_i and forces the successor nonpositive. Pairwise disjointness follows because a positive block cannot itself be another positive's negative successor. Every other block is nonpositive. This is explicit two-block charging, with no unknown allocation witness.

## Four rules

1. **Strictly smaller — PASS.** Only immediate-successor repayment from the old root's depth-1 neighborhood, with an explicit source A threshold. No arbitrary all-walk existence problem, support enlargement or equivalent CD reformulation. A source-defined local family is removed while its complement remains open.
2. **Concrete reason — PASS.** The source's final/penultimate grouped rotations give a complete depth-3 transport table. Then q<=1 and the two-block sum is determined. The only sharing issue is adjacent pair overlap, resolved by the forced negative sign. No independent open geometry, endpoint bound or global flow theorem is needed.
3. **One bounded mechanism — PASS.** Prove this theorem and audit one predeclared seven-key diagonal prefix and closed word, plus reflection, and the sharp four-key root-child transport control plus reflection. No alternate word search, larger fit, potential optimization, source graph or successor lemma. Stop if the fixed witness fails or novelty cannot be justified; do not search automatically for a replacement.
4. **Original connection — PASS subject to the exact novelty check below.** Success closes the original CD obligation on the stated structural class. It strictly extends 26AJ's former-root successor class by admitting an old B child as successor. It does not discharge universal CD or any Stage 11G obligation. Do not count a reproof of the already banked <=3/4/5-support cases or the depth-displacement component as a new result.

## Predeclared reachable novelty witness

Start diagonally at the seven-key right vine R7. Prefix D7,D6 reaches a pair with A rooted at 6 and B still R7. Freeze the cycle

    K7 K2 K3 K4 K5 K6 K7
    K1 K2 K3 K4 K5 K6 K7
    K6 K5 K4 K3 K2 K1 D7 D6.

The first KEEP7 is expected to have a=1,q=3,delta=1. Its successor key 2 is B's old root child, not the old root 1. KEEP2 should synchronize A and B; subsequent common accesses are termwise nonpositive, and the final D7,D6 restore the cycle's initial pair. The sole positive's former-root return 1 is delayed beyond the first three successor positions, excluding AJ/AK/AL/AM. One isolated positive excludes AN/AO two-positive packets and the multi-positive AQ/AR/AS packets; the next key 2 excludes AP's p=1 immediate former-root return. All seven keys are genuine KEEP targets, excluding banked support<=5 classes. These exact exclusions must be checked against the source trace and pinned old theorem definitions; no blanket claim about every imaginable consequence of older work is made.

For unbounded ambient size, graft an arbitrary finite BST of keys >7 to the right of key 7 in both initial trees. Since every requested key is <=7, the fringe remains attached to key 7 and the complete source word commutes with this graft. This is an analytic arbitrary-fringe family, not a finite size sweep. The theorem itself has no bound on KEEP-support size.

## Verification, promotion and preservation

Check the full table including odd/even path lengths, both child orientations, the source parent-first same-side order, exact A-root block boundaries, cyclic seam, no-op and zero-A cases, q versus final zig, distinct positive/successor pairs, source units and physical A/B closure. Construct actual per-A-StepEv two-unit credit assignments inside each paid pair, with no reuse. Check every cyclic cut of the fixed witness and both orientations. Independently replay with the pointer engine; import no producer or allocation optimizer.

If proved with strict coverage, status is PROVED—RESTRICTED DOMAIN: one genuine restricted CD class removed. Universal CD remains OPEN; the universal load-bearing obligation is not marked complete. If the fixed witness fails, preserve the component proof but record no new coverage. Record BEFORE/RESULT/AFTER, assumptions, deleted restricted case and net advancement without conflating it with a full proof. Preserve inherited non-advancing counts; no matching-terminal reopening or automatic follow-up occurs.

Pin all inherited/previous-run files plus the exact old theorem definitions used for comparison. Preserve all 125 Stage 11G files and their complete inventory, current branch/HEAD and tracked status. Do not execute Stage 11G code or any old status writer.
