# X21 — two-event obstruction behind the return frame

Status: NEW symbolic proof, audit pending. All roots and keys refer to
actual A, using the globally ordered source inventory. Let V be either
V1 or V2 in EXTREME_ORDER_NORMAL_FORM. Let the initial A root be a marked
key K with G<K<C and K!=x. Then NO natural macro of total H<=2 ending at
C can produce V.

## Final-root placement for one ordinary splay

For any single ordinary access, the old root participates in the last
top event and ends at depth1 or2. If that last event is zig or mixed the
old root is a child of the target; if SS it is an outer grandchild. More
particularly, after access C an old root y<C is either C.left or lies at
C.left.left; an old root y>C is either C.right or C.right.right. This
also holds for a longer single splay, since it concerns its last event.

In V every marked key strictly between G,C other than x lies below x,
inside G's right subtree. Its A depth is at least3. Thus one changing
access C, even of cost2, cannot put the old root K there.

Otherwise H<=2 admits at most TWO changing accesses, each of cost1. They
must be y followed by C; root repeats are identities in A and remain in
the source. Two changing accesses to C without another changing access
between them are impossible, so y!=C.

## Case y<C — includes anonymous y below all marks

The FINAL one-event C access places its old root y at C.left or
C.left.left. Both positions in V are <=G: V1 has left root G and its
left operand is below G; V2 has left root P<G and P.left is below P.
Therefore y<=G<K<C, including arbitrary anonymous y.

In the initial K-rooted tree, C belongs to K.right. Accessing y<K never
enters that operand, so K stays an ancestor of C. For C subsequently to
be at depth<=2 from y, the path must be y,K,C; any extra parent makes
it too deep. The final event is RR and leaves C.left=K. This contradicts
V's left root <=G. Equivalently the zig/mixed final possibilities have
no place for the necessary intermediate ancestor K.

## Case y>C — includes anonymous y above every mark

Both changing access targets y,C exceed K. The initial K.left operand
contains G and is never entered. Rotations along either rightward search
can move K but cannot detach G from K.left. Thus K remains an ancestor
of G after both accesses. V has G an ancestor of K, contradiction.

This exhausts every positive-event distribution, both orientations and
all anonymous helpers. No finite tree enumeration is used. The argument
uses root-to-key structure and off-path rigidity, not a fixed-chart debt
or an assumption about future accesses. QED.

## Own-tail freshness interface

If the old marked B root Y is unary and becomes a leaf in a macro, the
preceding genuine access created a degree1 root. Q+c=1 forces that access
to be Q1,z1. Hence the current birth of Y cannot be selected by the T19
H1/Q2,beta2 zero-death rule. At most u-1 births are selected here.

In the specified h_B stage, all occupied own ordinals are a prefix of
length at most beta+z+k. If 2H>=Q+z and this old-root exclusion applies,
that prefix is <=Q+z-1<2H. The LAST actual A-bit is therefore outside the
ENTIRE image of h_B after ALL own-tail payments. The strict alternative
2H>=Q+z+1 works without the exclusion. This is comparison eligibility;
it is not freedom under frozen a or a Bank25 receipt.
