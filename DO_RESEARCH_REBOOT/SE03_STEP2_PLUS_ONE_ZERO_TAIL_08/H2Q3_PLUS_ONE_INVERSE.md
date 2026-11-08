# P1-B: complete two-event source forms and universal exclusion

First the price arithmetic is exhaustive. A singleton has Q<=4 and H>=1.
At H>=3 its price is at least2, even with the inherited min(H,4) cap.
At H1/H2 price+1 gives exactly Q1/Q3. A q5/q1 pair has Q6 and an even
price, so never+1. H0 cannot be a genuine full root change. Thus P1-A and
P1-B are the only possible positive-one classes in this source partition.

## All original H2 A-event arrangements

Let a full macro start at synchronized root g and finish at distinct
genuine target v. Its total A StepEvs is2. Zero-event operations always
access the current A root. The last positive operation must target v.
There are exactly two possible positive-operation decompositions.

1. ONE operation has two StepEvs. It targets v, at actual source depth3/4.
   It is terminal KEEP v or an earlier DELETE v. All earlier operations
   target g; all later preterminal operations are DELETE v. At depth3
   ordinary bottom-up splay executes a lower double and terminal root zig;
   at depth4 it executes a lower double and a root double. These are the
   actual one-access operations, not synthetic separate accesses. Each
   lower/root orientation and all ordered hanging terms are unrestricted.
2. TWO operations have one StepEv each. The first is DELETE h with
   h distinct from g,v, making A root h. It cannot be a KEEP: a KEEP h
   would terminate the genuine full macro earlier. The second targets v,
   at terminal KEEP v or earlier DELETE v. Intervening identities are
   DELETE h; afterwards only DELETE v precedes terminal KEEP v. A KEEP g
   in between would spend another positive event and leave the wrong
   final root. Each actual one-event access uses any of the six ordinary
   root identities; h and both A parents can be arbitrary private/Score keys.

Writing Zg in {DELETE g,KEEP g}, the two-operation words are

    Zg* DELETE h (DELETE h)* KEEP v,
    Zg* DELETE h (DELETE h)* DELETE v (DELETE v)* KEEP v.

The one-operation forms replace the positive access to v in the H1 macro
language by its actual TWO-event splay. These forms exhaust all ways to
distribute two events among original operations. No timing is normalized
away. Root g persists until a direct deeper splay finishes, or the actual
roots are g,h,v in the split case. Source interval constraints apply to
each ordinary rotation, with arbitrary free subtrees and both orientations.

All preterminal KEEPs in these forms target g and occur before positive A
work. BE executes exactly that retained KEEP g subsequence and terminal
KEEP v (skipping the erased key). DELETE helper h never refreshes the full
MRU or chart. The actual full order changes only at terminal KEEP v.

## Source-derived obstruction, independent of ALL A arrangements

Q3 has actual BF-depth6 in the closed core11 domain; depth7 with a terminal
zig is excluded by the inherited maximal-source theorem. The three actual
SS doubles have three proper marked ancestors of v, with unmarked parents.
Marked-parent compression makes all THREE distinct ancestors children of
the new root v. Any old marked children of v are additionally retained.
Thus

                  marked_degree_BF(v after macro) >= 3.

This identity follows by induction through the original SS rotation frames.
It is unaffected by any DELETE, A helper, event timing, private inventory,
erasure choice or chart switch, since BF changes only at terminal KEEP v.

But the ACTUAL source u of the last neutral zero is J2 or K2 and has
marked-root degree2 or1. Consequently NO H2/Q3 packet can enter u.
P1-B is UNIVERSALLY EMPTY in this precise return domain. All two-event
arrangements above are excluded by the same BF obstruction; none is
discarded by imposing an artificial A normalization or helper bound.

The independent engine derives all480 admitted Q3 output contexts, each
with degree>=3, and checks every one of the48 final-zero sectors has
degree<=2 and no Q3 predecessor. Free-gap lifting makes these term identities
universal. Historical controls contain no H2/Q3 macro; they do not prove
this exclusion. Its proof is the source marked-ancestor identity, checked
independently over the complete source grammar.

The two-event word normal form is support-independent. The marked-degree
bound is valid whenever the actual path has these alternating SS operands.
The numerical upper bound2 on u is a six-key terminal-geometry fact, not
an all-support theorem or a physical funding invariant.
