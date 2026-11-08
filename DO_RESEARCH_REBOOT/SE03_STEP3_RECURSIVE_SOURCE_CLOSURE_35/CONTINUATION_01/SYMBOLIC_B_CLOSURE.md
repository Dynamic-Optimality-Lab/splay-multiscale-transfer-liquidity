# Exact original B closure of the anchored forward/reverse word

Notation (k,L,R) is an actual ordered BST; empty terms are omitted below.
V+(a,b) is the full right vine on every INTEGER a,...,b; V-(a,b) the
full left vine, rooted at b. An empty interval denotes the empty tree.
Define C(a,b)=(2a,(2a-1),C(a+1,b)), empty if a>b. These are explicit
physical BSTs, not marked-tree quotients. Fix g=15, marked odd keys1..15,
x_i=2i+1, 1<=i<=6. Initial B is Z=V+(1,15).

The KEEP word is

    15; 1,3,1,5,1,7,1,9,1,11,1,13;
        1,11,1,9,1,7,1,5,1,3,1.                  (BWORD)

It has24 original KEEP operations. The full B has no root repeats in it.

## Forward states: an exact symbolic induction

After KEEP15 the actual tree is (15,C(1,7),empty). Ordinary RR-frame
induction from the bottom of the right vine proves this: every outer
RR inserts its unmarked parent with its old marked grandparent as left
child and the already rebuilt comb as right child. There are7 doubles.

After the following KEEP1 the tree is

    F0=(1,empty,(2,empty,(15,C(2,7),empty))).

This is one original LL double (15,2,1). After accessing x_i define

    Fi=(x_i,
           (2,(1),V-(3,2i)),
           (2i+2,empty,(15,C(i+2,7),empty))).

For i=1, F0 -> F1 uses LL(15,4,3), then RR(1,2,3), exactly2 doubles.
For i>=2, KEEP1 from F(i-1) is LL(x_(i-1),2,1) and gives

    T(i-1)=(1,empty,(2,empty,
        (x_(i-1),V-(3,2i-2),(2i,empty,(15,C(i+1,7),empty))))).

Access x_i has exactly these3 original doubles, in this order:

    LL(15,2i+2,x_i), RR(x_(i-1),2i,x_i), RR(1,2,x_i).

Substitution in the ordinary source frames gives Fi: the middle frame
extends the left vine V-(3,2i-2) by the consecutive keys2i-1,2i, and
the last frame attaches that vine below node2. No arbitrary graph edge
is substituted for a source operation. Every tree term includes every
physical key1..15 exactly once, and every unmarked vertex remains an
ancestor of a marked key.

In particular BEFORE x_i for i=2,4,6 the actual depth is6 and its old
marked ancestors, in root order, are 1,x_(i-1),15. Its full Q is3.
The three numerical instantiations are separately replayed in core44
and verify87; the induction itself establishes every intervening state.

## Reverse states and literal closure

At i=6, F6 has right subtree V+(14,15). Put

    Ui=(x_i,(2,(1),V-(3,2i)),V+(2i+2,15)).

Thus U6=F6. From Ui, KEEP1 is one LL(x_i,2,1). Then, for i>=2,
KEEP x_(i-1) is LL(x_i,2i,x_(i-1)), followed by RR(1,2,x_(i-1)).
The result is U(i-1): the right vine is extended by2i and2i+1.
This proves the five reverse pairs by induction. From U1, KEEP1 is
LL(3,2,1), giving exactly V+(1,15)=Z. Every original B event in BWORD
has been covered by an explicit ordinary SS-frame induction.

The full core is15 at all source boundaries, with8 genuine marked keys.
The full B cost is

    7+1+2 + 5(1+3) + 5(1+2) + 1 = 46.

This is a symbolic source-closure proof. It is not reported as a new
complete numerical replay of all24 B accesses. No source query is
hidden in evaluating a new full-history engine; only the three critical
instantiations are run numerically in each of the two implementations.
