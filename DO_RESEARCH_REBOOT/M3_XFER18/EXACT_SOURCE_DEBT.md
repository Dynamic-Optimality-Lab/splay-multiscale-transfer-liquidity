# Exact source debt of any surviving H1 failure

This proof sharpens a necessary condition; it does not assert that a
remaining cell is empty. It applies to zero and positive H1 failures.
Every negative H1 row is already proved, and all new operations preserve it.

For each upward operation Lambda->D_Q->D_R->D_cut->D_release->D_RR
->D_anon->D_direct->D_buried->D_interval->D_grand->D_marked->D45
->D_exp, use BOTH conclusions established in its original proof:

 (i) every previously valid original H1 row survives;
 (ii) every H1 row whose source is strictly raised holds afterwards.

The authoritative premises are XFER01 SATURATION_THEOREM sections on
new Q sources; XFER02 CUT_PAIR sections2/3; XFER03 BURIED_CUT sections3
and its T/L source proofs; XFER04 RELEASE_CAPACITY sections3/4;
XFER05 RR_RELEASE sections3-5; XFER06 ANONYMOUS_RELEASE source cases;
XFER07 DIRECT_BARRIER sections4/5; XFER08 BURIED_BARRIER's K/R/C/T/G
source cases; XFER09 INTERVAL_CHILD's new-source proof; XFER10
GRANDCHILD sections2/3; XFER11 MARKED_RELAY's J/G source proofs;
XFER12 DEPTH_FIVE_RELAY sections2-7; XFER13 NON_EXTREMAL_EXPOSURE
sections2-6. Boundary-only stages change NO actual source, so (ii)
is vacuous there. The cap1 stages assert (ii) only at NEW value1,
which is exactly the hypothesis used here. They need not prove every
row from an unchanged auxiliary source already at2.

The audits of those proofs and their hashes are reused, not executed.
Inspection of their fresh-source cases is a new logical dependency
audit; it does not infer (ii) from (i) alone.

Suppose a specific original H1 row fails for D_exp. By contrapositive
of (i), it fails at every preceding stage. By (ii), its source was
never raised at any stage. Hence its source value still equals
Lambda(s). The seed proof gives all H1 rows when c(s)>=psi(s);
therefore c(s)<psi(s) and Lambda(s)=psi(s). In particular

             D_exp(s)=Lambda(s)=psi(s).

No target equality to an old seed is inferred: its target may have
been raised during the lineage. Failure only implies it is still
below psi(s)-w. This distinction prevents treating an old necessary
seed-drop label as the actual present debt drop.

Transfer16 and17 preserve every old row. Therefore a D_term failure
was an old D_exp failure. For a zero or positive failed row, the
source debt must be positive. That makes the old psi positive by
the preceding equality; psi1/2 core height is at most6/5. It cannot
belong to Transfer16's height>=7 ceiling. By Transfer17's all-unmarked
source theorem it is marked synchronized, so normalization also leaves
its source unchanged. Thus D_term(s)=psi(s) at any such failure.

The accepted corrected spread stages have (i) and (ii) by their
one-credit source proofs, and every Z-source row is proved at2.
All are upward. The same contrapositive induction gives, for any
surviving D_spread zero or positive H1 failure,

                   D_spread(s)=psi(s).

The entire debt is integer0..2. A zero failure can therefore only
be actual1->0,2->0 or2->1, with exact source psi1/2 respectively.
In particular an old S10 slot cannot hide a newly augmented source2
failure. A +1 failure must have source psi2 and actual target0.
These are necessary signed conditions, not a repayment proof.

This induction remains valid after any further upward operation for
which (i) and (ii) are separately proved. It will be applied to the
cross-median child rule below. No private history, completion or
new observable appears in the formula or the proof.
