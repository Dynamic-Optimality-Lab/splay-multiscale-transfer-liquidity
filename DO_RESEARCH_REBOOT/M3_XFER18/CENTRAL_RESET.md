# Central three-mark reset and its signed returns

This phase keeps working on Step4. Let the mask have five bits, include
3,4,5 and exclude1,2; the two other marks may be ANY of0,6,7,8. These
are quantified set conditions, not tested masks. Define actual opposite
regions with include3,4,5 and exclude6,7. All signatures, compatible
private witnesses, G/unused fields and raw B annotations remain free.

Use these exact nine-core patterns (leaf shorthand, E core-empty):

 C=3(0(E,2(1,E)),4(E,8(7(6(5,E),E),E)));
 X=5(3(0(E,2(1,E)),4),8(6(E,7),E));
 Y=4(3(0(E,2(1,E)),E),5(E,8(6(E,7),E)));
 Z=7(5(4(3(0(E,2(1,E)),E),E),6),8).

All classes require P, the appropriate mask and named core, and:

 C: root3,L0,R4,RR5; no other alpha guard.
 X: root5,L4,LL3; no other alpha guard.
 Y: root4,R5; no other alpha guard.
 Z: root7,L5,LL4; no other alpha guard.

Add ACTUAL opposite patterns/observations. Starting from D_allmarks,
floor Z to1, then Y to1, then X to2, then C to2. Call the result
D_central. Each operation preserves every previously proved LOW row;
ALL X/C-source LOW rows hold. No complete Step4 assertion follows yet.

## One-credit Z and Y

At a fresh Z source, marked0/3 are below the displayed Score4 at LL,
at depth>=3. The only eligible nonroot marked Scores are4/5/6/8.
Their core depths are2/1/2/1, so all H1 prices are positive.
The one-credit LOW rule therefore proves Z's floor, including the
global Gamma1 zero target floor and marked-endpoint Gamma0 theorem.
G reads owner7 or child5, never the lower hidden marks.

Y's marked core depths are d(0)=2,d(3)=1,d(5)=1,d(6)=3,d(7)=4,
d(8)=2; core4 is root. Its only possible marked zero target is7.
The public Score5 at R forces such a target to be the actual RR
Score7. Its A pair leaves L5,LL4, and its exact B output is Z.
Thus the zero exit ends with at least1. All other eligible marked
exits are positive; cores1/2 may be deep but are unmarked by hypothesis.
The one-credit LOW rule proves Y's floor, with no V filter.

## Two-credit X

At a fresh X source, marks0 and3 lie below the displayed Score3
at LL (0 still deeper), so0 cannot be an H1 target;3 is eligible
at LL and has core depth1, price2. Mark4 at L has depth2, price1.
Upper marked6/7/8 may appear at R/RL/RR, with core depths2/3/1.
There is no marked zero or negative H1 exit.

Access4 produces core Y and the actual A child identity puts old5
at R, hence reaches its literal full Y class, now with credit1.
Access6/7 yields respectively

 6(5(3(0(E,2(1,E)),4),E),8(7,E));
 7(5(3(0(E,2(1,E)),4),6),8).

Every permitted marked core0/3/4/5/6/7/8 in these two outputs has
depth<=3. Hence E1 supplies credit1 irrespective of any new anonymous
exposure. Targets3/8 are range-safe at price2. All +1 rows are paid.

No minimum Gamma1 helper can have A depth1/2: L4 and LL3 are Scores,
LR is between4,5, and the entire R side exceeds5. For maximum helpers,
the entire L4/LL3 block moves down;3 and0 become too deep, while4
can remain eligible only in the first-helper-R case. Every eligible
terminal is therefore4 or an upper mark>=5. Deep helpers cost>=2.
The shallow maximum helper must have B depth2 (root5 is not8), and
its exact B output is f(8(5(L,6(E,7)),E),E). Here5/8 have depths2/1,
4 has depth4, and6/7 have depths3/4. All eligible terminal depths
are<=4, so q<=2 and the ORIGINAL H2 price is>=2. No helper support
is erased. Gamma0 uses the marked-endpoint floor law. Thus X may
be saturated at2 for every original exit.

## Two-credit C

At a fresh C source its only possible nonroot marked Scores are0,4,5.
Score8/6/7 are below5 at depth>=3, and1/2 are unmarked. G cannot
invent an additional marked eligible label. Core0/4 have depth1,
price2; key5 has depth5, price0. Its exact core output is X, and
the actual RR pair puts L4,LL3 at the endpoint. Thus the zero row
ends in X at debt2, giving exact residual0 at source2.

Only a minimum helper at LL below present0 is possible at A depth2.
L0,R4,RR5 are Scores; LR is above0, RL between3,4. After that helper
only old0/3 can be marked charge1 terminals. Its B path is3,L0,Lf,
so their preterminal depths1/2 give H2 prices4/3. Gamma0 is floor-safe.
This proves every C-source LOW row at2, not merely a zero sign test.

## A concrete necessary zero repayment

Let S=4(0(E,1(E,2(E,3))),8(7(6(5,E),E),E)). It is the exact
depth-eight splay-to4 output of the proper all-nine-core path
8,L0,R7,L1,R6,L2,R5,L3,R4. The complete negative-core law and
range force psi(S)=2, with no bank lookup. Access3 in S has depth4
and yields C. The proper A source4(3(0(A,B),Cblock),5(D,Eblock))
has eligible target3 at L; its endpoint has C's L0,R4,RR5 fields.
The original H1 lift supplies this original zero transition with
the same full shared endpoints and original H=1,q2,w0 for every
compatible completion. Canonical sigma0 completions exist, using
the two unmarked lower/upper chains in opaque subtrees. No original
compiler/root is evaluated, and no negative-cycle claim is made.

For the symmetric mask{0,3,4,5,8}, the inverse-word certificate
proves psi(C)=0 and psi(X)=1. Every old augmentation guard at C
vanishes: first/last marked pairs0,3 and5,8 miss all central-pair
guards; Q/I fail the multiple visible targets0/4/5; R has no
required PORT; unmarked-root caps fail; XFER13's exact masks differ.
The new spread classes have roots2/6,1/7 or0/8, never C's3; the
cross-median child rule needs its R child>=5, while C has R4.
C has marked visible targets0/4 at price2 and5 at price0. Therefore
c(C)=psi(X)=1, Lambda(C)=1 and the previous D_allmarks(C)=1.
This original 2->1 zero reset is repaired to2->2 by D_central.

The accompanying inverse certificate derives EVERY possible negative
incoming core word to C and X by last-operation inversion. C has none;
X's only negative predecessor is at depth6 and has psi0, proved by
the same absence-of-incoming-word certificate. The complete core
recurrence then gives psi(C)=0,psi(X)=1. This is a universal word
proof over all predecessors and arbitrary raw/private data, not
finite population testing, fitted labels or a new psi-table query.

All rows previously proved, terminal floors, unmarked-source0, integer
range2, HIGH/h0 and exact-source-debt induction are retained. This
closes the stated central family for all six quantified masks and
all signatures plus their actual opposite classes. It does not prove
that every remaining marked-source zero edge belongs to these or
earlier regions. The exhaustive 36-slot frontier still needs that
global coverage implication before Step4 can be declared complete.
