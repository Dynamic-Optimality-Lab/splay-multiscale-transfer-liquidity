# One positive-one intervention: E1 is realized

Target: analyze the original P1 and resolve E1 separately from E0.
Conditions: source-valid H1/Q1 packet before the first lowering.
Inheritance: source compression, deltaL=a-b and initial N* length<=1.
Ambiguities: the intervention may occupy any allowed location, not
necessarily Sigma's previously known predecessor. Bridge: q1 changes
only target and old root in the marked-parent tree, then use an actual
closed source witness.

## Complete marked-parent effects of the first P1

Before P1, the initial N* is empty or one N; its possible source marked
shapes are S5,S4,P4 or D4. For q1, a is1 iff the old root has no marked
child off the target, and b is1 iff the target is a marked leaf.

| Source form | Admitted target category | Delta L | Result |
|---|---|---:|---|
|S5|a leaf| -1 |P4 (L4)|
|S4|the sole nonleaf child|0|D4 (L4)|
|S4|one of the other leaf children|-1|L3; new root above old root|
|P4|its sole nonleaf child|+1|S5 (L5), no N successor|
|D4|its leaf child|-1|L3; two-root chain above the remaining fork|
|D4|its nonleaf fork child|0|S4 (L4)|

These are necessary source effects, not independent realizability claims
for every target ordering. In particular P1 need NOT preserve leaf count.
Where L becomes3, additional N packets may preserve or increase it;
the E0 length bound cannot be transferred past P1 without proof.

## Exact E1 witness

Use the actual full core S7 from the sealed Sigma source proof. Define

    V=(9,1,3,5,3,1,11,1,3,5,9,11,9,5,3,1).

K(V) maps R11 to S7. Let V^- omit its last1 and SCAN be as above.
The following is one original90-operation closed word:

    K(V^-) D(SCAN) D10 D7 D1 K1
    K7 K9 K1
    D(SCAN) D(V) D7 D9 D1
    K9 K7 K1 K3 K5 K3 K1.

After the terminal K1 at40, BF is exactly S7 and A has been prepared
by the charged DELETEs. The critical source data is:

| Occurrence | Actual segment | H | Q | w | L before->after |
|---:|---|---:|---:|---:|---|
|41|cold K7 (NEG2-S)|1|4|-2|2->4|
|42|K9 (P1)|1|1|+1|4->4|
|43|K1 (first lowering)|1|2|0|4->3|

The positive packet moves the S4 nonleaf child9 to the root, producing
D4 and making a genuine lowering K1 available in A as well as BF.
The actual A paths at41,42,43 are R,RL,LL. The full BF paths have depths
8,2,4 respectively. The old recent order before41 is[1,3,5,9,11,7],
so K7 is cold. At T it is[7,1,3,5,9,11]; at ell it is[9,7,1,3,5,11].
The single P1 is the entire prefix; both N* blocks are empty.

Erasing3 has a one-copy preperiod and period1. The actual recurrent
period closes A,BF at R11 and BE at its actual recurrent tree, with
A125,QF44,QE14 and positive original CD slack206. Its reaching prefix
is one90-operation copy; critical absolute occurrences are131,132,133.
All physical events belong to this period and its actual packets.
Both independent engines and the reflected word pass.

The inherited genuine Sigma +1 predecessor remains a separate mandatory
control, with marked-leaf count3 and cap<=1. Its source data is reused
without replay or alteration; counting its actual BF again confirms3.
The new P1 is NOT identified with that old full state or its chart.

Thus E1 is SOURCE-EXACTLY REALIZED. No relocation of a general P1 is
assumed, and no abstract marked-tree route is used as a witness. The
post-lowering suffix has zero positive-one budget left and is analyzed
separately; entry alone creates no width-two contradiction.
