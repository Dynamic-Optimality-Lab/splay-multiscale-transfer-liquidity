# A source-exact positive-gap closed family outside FI and PF

The fixed first-return mechanism is **REFUTED—EXACT**. Its predetermined
closure supplies a stronger result: the unchanged FI and PF procedures are
not complete even for closed walks whose positives all have (a,q_B)=(1,3).
The residual source class Gamma_PF>0 is nonempty. These are failures of the
certifiers, not counterexamples to Coarse-Double.

There is also a separate, explicit source injection for this family. Thus
the claimed coverage beyond FI/PF below has its own source proof; it is not
inferred from a local ceiling improvement or an assumed successful cut.
No FI or PF rule is altered.

## 1. The exact source identity and reachability

Use x(L,R), a bare key for a leaf, and dot for empty. Let F be ANY common
finite BST whose keys exceed7, including empty. Define the source pair S(F):

    A = 1(.,3(2,7(5(4,6),F))),
    B = 1(.,2(.,3(.,4(.,5(.,6(.,7(.,F))))))).

It is the old verified source state17478, core pair (as recorded in the
certificate), with a common untouched outer fringe. The following common-KEEP
word W returns BOTH source trees exactly:

    W = K(7,5,3,1,5,6,4,1,2,1,5,1,6,7,1,2,1,3,1).           (4)

Every displayed occurrence is a complete nontrivial A-root block and a
genuine B change. There is no DELETE or synchronization in W. The source
relation states along the walk are

    17478,8544,1929,954,2451,2293,2395,3219,4864,1741,
    2356,698,1926,4211,7431,10907,13897,15970,16599,17478.

All of them have unequal A/B trees. This is a closed walk; no simple-cycle
property is needed or claimed. It is reachable from a diagonal source pair:
start with both trees equal to the right spine1,...,7 with F at7.right,
then execute

    D3,D5,K7, K(2,6,5,1,7,6,7,1,2,1,3,1).                  (5)

The startup endpoint is exactly S(F). Its A units and source facts are never
imported into a recurrent pass. The fixed physical certificate uses the
already inherited n=13 embedding, F=the right spine8,...,13.

Why arbitrary F is proved: all accesses in (4) and (5) are to present core
keys1,...,7. No search descends inside F, and each rotation treats it as an
unchanged child subtree. Its size, shape and internal depths occur in no
core search depth or event. The recorded source rotations are therefore
literal tree-term identities with F as an opaque variable, not samples of
larger trees. Substitution proves (4),(5) for every such F. Reflecting order
gives the corresponding arbitrary common lower-fringe family. Order-preserving
relabeling is harmless. Arbitrary OTHER internal fringe placements or arbitrary
unequal fringe pairs are not asserted to be classified by this fixed family.

## 2. Source costs and the unchanged fresh reservations

After the positive KEEP7 the B tree is

    T = 7(2(1,4(3,6(5,.))),F).

Its first intervention is KEEP5, with original source frames inner RL
(grandparent4,parent6) followed by outer LR (grandparent7,parent2).
For every later payer, compute h and U_PF from THIS tree and THIS first
intervention, exactly as in PF01. No first-post-depth or future payer-demand
oracle chooses a reservation. In the table k is the number of genuine B
changes strictly between the positive and the payer. At the immediate payer
k=0 the ceiling uses h, not U.

|Block|Key|a|q_B|C|k|PF ceiling|PF offer|
|---:|---:|---:|---:|---:|---:|---:|---:|
|0|7|1|3|2|--|positive|0|
|1|5|1|2|2|0|2|0|
|2|3|1|1|2|1|2|0|
|3|1|1|1|2|2|2|0|
|4|5|1|1|2|3|2|0|
|5|6|1|1|2|4|4|0|
|6|4|2|2|4|5|5|0|
|7|1|1|1|2|6|6|0|
|8|2|1|1|2|7|6|0|
|9|1|1|0|2|8|8|0|
|10|5|3|2|6|9|8|0|
|11|1|1|1|2|10|10|0|
|12|6|1|1|2|11|11|0|
|13|7|1|0|2|12|12|0|
|14|1|2|1|4|13|13|0|
|15|2|2|1|4|14|13|0|
|16|1|1|0|2|15|15|0|
|17|3|2|2|4|16|17|0|
|18|1|1|1|2|17|17|0|

Thus

    A(W)=25, Q_B(W)=22, E=1, C_D=0, L_PF,fresh=0,
    Gamma_PF(W)=1,
    Q_B-2A=-28, Lambda_PF,fresh=29.                          (6)

The positive source gap is ENTIRELY reservation loss: 1=-28+29.
At the cut beginning with KEEP7, the entire period is the canonical busy
suffix, so the actual PF identity of PG01 is also exactly D=1=-28+29.

The first return to the first intervening key5 occurs at block4. Its exact
source fact U_PF(T,5,5)=0 gives c=k-1=2 at k=3, equal to its capacity2.
The residual unit is still unpaid, PF releases nothing, and the full trees
remain unequal. The proposed first-return repay-or-synchronize rule is
therefore false on an actual reachable source walk, not just on abstract
states. The old parent-fringe example (6,4,1) did not represent this case.

## 3. Every cut fails, uniformly in the number of copies

For m>=1 concatenate the EXACT returning word and let W_m(F)=W(F)^m.
This is source-closed and reachable by (5), with all-size identities

    A=25m, Q_B=22m, E=m, C_D=0, Gamma_PF=m.                 (7)

This conclusion needs no replay at larger m or n. Each copy has the same
positive destination T, the same first intervention5, and 19 genuine B
changes. For a payer at phase j>1, the newest anchor ceiling is the table's
ceiling. An anchor ell>=1 copies older has the identical U but k increased
by19ell, hence ceiling increased by19ell. It cannot lower the reservation.
At phase j=1, the newest anchor has k=0 and ceiling2; an older anchor has
k=19ell, U(T,5,5)=0, and ceiling19ell-1>=18>=2.

Therefore EVERY encountered positive fact gives a ceiling at least C at
EVERY nonpositive block. Before the first positive encountered by a cut,
empty history also reserves C. Paid facts are retained but do not help.
Every physical payer in every one-period cut offers zero. Each of the m
positives adds one residual unit. Hence

    D_PF,end(c)=m  for every one of the 19m physical cuts c. (8)

Since FI ceilings are at least PF ceilings, the same identity holds for FI.
The family stays nowhere-diagonal, including its copy boundaries. No startup
facts, startup units, second traversal, credits from another cut, or repeated
credit use enters this argument. The reflected proof is identical.

Equations (7),(8) prove the following exact scoped obstruction:

**Universal completeness of unchanged PF is false, even when all positive
blocks have one unit of excess, no reset occurs, and the walk is nowhere
diagonal. Requiring eventual PF-certified suffix repayment or synchronization
cannot prove the full one-unit theorem.**

This does NOT refute eventual repayment by some other source-derived
certificate. It also does not establish strict FI subset PF coverage: both
reject this family. Gamma_PF>0 is a nonempty necessary residual domain, not a
CD violation and not a sufficient criterion for all-cut rejection in general.

## 4. The actual missing physical unit has a source proof

The role ignored by PF here is the grandparent's outer subtree in the FIRST
inner RL operation. The exact source identity is

    g(A,p(x(B,C),D)) -> x(g(A,B),p(C,D)).

A tracked key in A has depth shift exactly +1: from site-depth+1+t to
site-depth+2+t. This is not the parent's outer-fringe role corrected in PF01.
For tracked key3, h=3, entry is the inner RL at4 and3 belongs to4.left.
The later outer LR shifts its target-left fringe by exactly -1. Therefore,
using only the ORIGINAL source-entry roles,

    d_(S_5 T)(3) = 3+1-1 = 3.                              (9)

The reflection uses inner LR grandparent-right outer fringe, then outer RL.
No future KEEP3 demand or observed first-post depth selected (9). It supplies
the safe own-work bound floor(3/2)=1 before the third block is processed.
PF continues to use its unchanged conservative U=4 and reservation2.

This gives an explicit DIRECT source certificate, separate from FI/PF:

- KEEP7's single A event supplies bits0,1 to its first two B doubles.
- KEEP5 pays its two doubles from its own two units.
- KEEP3 protects bit0 of its single A event for its own work using bound(9),
  and its bit1 pays KEEP7's third B double.
- Every remaining block is nonpositive and pays its own B doubles from its
  own first q_B actual units. It makes no nonlocal loan.

The first three blocks thus inject six demands into six physical units.
The whole word injects22 demands into50 units, leaving28 unused. The chosen
donor is fixed as (block2,A-event0,bit1), selected by source bound(9), not by
observed future own demand. Full B-event identities and every unit occurrence
are in `closed_source_certificate.json`.

In W_m(F), apply this same certificate separately to each physical copy.
The donor for copy r and the third positive double of copy r both carry
that copy occurrence. No two copies share a pool or demand, no endpoint
credit is borrowed, and each debt is paid before the next positive. This
proves a distinct-unit injection

    22m actual B doubles -> 50m actual A units.             (10)

Thus this particular all-size closed family is a separately proved repayment
case OUTSIDE both original certifiers, with successive positives accounted
for explicitly. The statement is restricted to the displayed source family;
it does not classify arbitrary valid BST pairs, internal fringe configurations,
closed histories, or competing donors. It is not the original U4 eligibility
matching theorem and claims no source-eligibility edges for that older graph.

## 5. Proof versus certificates and the unresolved principal theorem

Mathematical proof: PG01 supplies the universal PF-fresh cut corollary and
exact loss decompositions. The source rotations, unchanged ceiling table,
older-fact comparison and distinct copy identities above prove (4)-(10) for
all permitted F and every m>=1.

Source certificates: both unmodified original engines replay the one fixed
n=13 ordinary witness and its reflection, including the ordinary diagonal
startup. There are76 independently reconstructed one-period cut trials
(19 cuts times two algorithms times two orientations), all rejected with
debt1; both direct22-demand injections are checked. The original tuple source
also verifies the 19-block opaque-fringe identity, with no traversal inside
the variable. The independent audit passed17,587 checks:104 physical tuple
source calls,104 physical pointer source calls and38 opaque-term calls.
These are fixed-word verifications, not finite fits or a size sweep.

Remaining open: a quantitative source-derived theorem for EVERY (1,3)
positive in arbitrary reachable BST histories, including interleaved positives
and shared physical payers. This family shows why that theorem must handle
usable units inside PF's unused protected prefixes; demanding only existing
PF loan suffixes or synchronization loses them. The fixed source loan(9)
does not prove a globally compatible supply rule for other histories.

The first-return mechanism stops here. The strategy review is in PG03.
Matching-terminal stays FROZEN. Every inherited file and all125 Stage11G
files remain unchanged. Universal Coarse-Double remains OPEN.
