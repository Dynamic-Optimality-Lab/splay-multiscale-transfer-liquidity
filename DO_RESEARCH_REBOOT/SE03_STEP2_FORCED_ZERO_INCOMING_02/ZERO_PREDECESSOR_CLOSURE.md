# Zero predecessors: universal reductions and a closed restricted branch

## Box B1: complete packet cost grammar

Target: enumerate all zero and +1 COST classes, not all realizations.
Conditions: original six-key source partition. Inheritance: H>=1 for a
genuine full macro, singleton Q<=4, pair Q6/H>=2. Ambiguities: actual
source geometries in these classes remain to be proved individually.
Bridge: substitute the exact H/Q bounds in the frozen price.

| Packet | H | Q | Price | Full core scope |
|---|---:|---:|---:|---|
| Singleton |1|2|0|where source-valid, including9/10/11|
| Singleton |2|4|0|where source-valid, including9/10/11|
| Actual q5/q1 pair |3|6|0|11 only|
| Singleton |1|1|+1|where source-valid|
| Singleton |2|3|+1|where source-valid|

There is no +1 pair by parity. A singleton H>=3 has price>=2; a pair
H>=4 has price2. Root repeats and DELETEs are INCLUDED in H. Auxiliary
root repeats do not define extra full packets. There is no genuine H0
macro. These facts prove exhaustiveness of the table, in both directions
and every chart. No realizability of a listed combinatorial shape follows.

## Box B2: endpoint grammar through two A events

Target: prevent hidden nongenuine operations or anonymous helpers from
being omitted in the small-H predecessor problem. Conditions: one full
macro starts synchronized at g, ends at x!=g, total H<=2. Inheritance:
ordinary bottom-up source execution. Ambiguities: arbitrary helper
identities/fringes are not bounded. Bridge: classify the positive events
of A, retaining the original word rather than deleting its operations.

H1: its unique positive access must target x at actual depth1 or2.
It can be Kx, or Dx followed by zero Dx operations and the terminal Kx.
Before that event all zero A requests target g; after it they target x.
The latter zero DELETEs do not affect BE. Full nongenuine Kg requests
can occur before the positive event and may change BE, although BF is
fixed. Any number has the exact effect of optional one Kg, since splay
to an already rooted key is idempotent. This is an endpoint description;
the original timestamps and operations are not removed from the packet.

H2: either one actual access x at depth3 or4, or two one-event accesses
Dy then x, with y any actual present key, each at depth1 or2 when used.
The first positive y cannot be a genuine KEEP: that would end an earlier
macro. A nongenuine Kg between the two positive events would restore A
root g and require another positive event to reach x, exceeding H2.
Thus all nongenuine full root requests precede the first positive event,
with the same optional idempotent BE effect. A final Dx followed by Kx
again has the same endpoint as the final Kx but remains an actual word.

This proof includes anonymous y at arbitrary present-key population; it
does not identify arbitrary BE inventories or contract different charts.
The search only samples y among1,...,11, so it is a strict subfamily of
this universal grammar. H3 paired zeros retain both actual macros and
their synchronized midpoint, with costs(1,2) or(2,1); this grammar alone
does not classify the H2 macro's arbitrary helper geometry.

## Box B3: invariant labeled full core

Target: exclude artificial inter-core splices. Conditions: fixed M and
an exact full B closed history. Inheritance: for x in the marked core,
C_M(S_x(B)) is a labeled subset of C_M(B). Bridge: all full targets lie
in M, so labeled core sets can only decrease along the period; exact
closure forces equality at every boundary. DELETEs/root repeats fix BF.

Consequently every admitted packet preserves the actual labeled full
core. Composable paths with the SAME M cannot move from full core11 to
full core10/9. Their recent-five cores and Score charts may change and
are not the full six-key core. Core9/10 require separate components, not
exclusion from the original domain.

## Box B4: first entry into arbitrary core11 F

Target: reduce all zero/+1 predecessors of F11. Conditions: actual closed
core11 source. Inheritance: all-SS marked-G/unmarked-P theorem and the
fan accessibility bound: after q>=3, the next legal q is at most6-q;
after q5/q1, the next legal q is at most2. Ambiguities: no assertion about
the full backward zero closure follows. Bridge: any F11 source supports
q4 or q5 as its next full macro. It therefore cannot be the output of
one q>=3 splay, nor of a q5/q1 packet. BF is unchanged by intervening
nongenuine operations and DELETEs.

Thus any zero edge INTO F11 is necessarily singleton H1/Q2. Any +1 edge
INTO F11 is necessarily singleton H1/Q1. This excludes H2/Q4 zeros,
H3/Q6 paired zeros and H2/Q3 +1 edges at the FIRST entry, uniformly in
A, BE, chart, mirror and private fringes. It does NOT exclude these
types at earlier points of Z, where no q4/q5 successor is known.

## Box B5: extreme-root, unary-separator exclusion

Call an unmarked core vertex unary if at most one of its children is
nonempty in the marked core. Define C11 to consist of actual boundary
states whose BF root is min(M) or max(M), all unmarked core vertices
are unary, and BF has at most two marked core leaves. All A/BE/recent
states consistent with the domain are permitted.

Target: no incoming zero or negative packet into C11, and only H1/Q1
for incoming +1. Conditions: actual closed core11. Inheritance: all-SS
and q5 successor fan; no debt formula. Ambiguities: C11 need not contain
all F11. Bridge: a genuine splay ending at an extreme mark has an
all-left or all-right core path. If it has two or more doubles, after
the first inner double the target-side rebuilt subtree contains an old
marked grandparent. The second same-side double makes its unmarked P
have that subtree on one side and a DIFFERENT marked G on the other.
All later outer frames retain P's whole processed subtree. The final
P is branching, contradicting unary separators. Thus an incoming
singleton into C11 has Q<=1.

For explicit free terms the two LL frames give

 G0(P0(G1(P1(x(A,B),C),D),E),F)
       -> x(A,P0(P1(B,G1(C,D)),G0(E,F))).

P0 contains G1 and G0 on opposite sides. The separately derived RR
identity is

 G0(A,P0(B,G1(C,P1(D,x(E,F)))))
       -> x(P0(G0(A,B),P1(G1(C,D),E)),F).

No content of A,...,F is inspected. These proofs include reflected
orientations and arbitrary gap populations.

A q5/q1 pair has EXACTLY four marked leaves: the q5 fan has five
nonroot marked leaves, its extreme return removes the selected leaf
from that count, and the former root still has a marked descendant
because at least four other path marks remain. Its target is outside
C11. The cost table now excludes every zero and every negative packet
entering C11; an incoming +1 is necessarily H1/Q1.

Let F_C=F intersect C11. Then Pre0*(F_C)=F_C: a nonempty finite zero
path would have a final zero edge into C11, which has just been excluded.
This closes ARBITRARILY LONG zero predecessors of this declared subset,
without any finite-search inference. The known Omega/Gamma sources are
right vines (one marked leaf); Sigma's source has two marked leaves and
unary separators. All three belong to F_C, as do their reflections.

OPEN: F11 outside C11 can have an internal extreme of its q4 path as
root or a branching separator at the one off-path marked block. B4 leaves
H1/Q2 predecessors there. Their iterated closure, and core9/10 closure,
are not classified by B5. F_C is not substituted for the original F.
