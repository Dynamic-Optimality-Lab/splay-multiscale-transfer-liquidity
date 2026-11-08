# Removing the central reset's mask restriction

Apply the same C/X/Y/Z core and A guards of CENTRAL_RESET.md, now
to EVERY legal five-bit mask, dropping its include/exclude conditions.
P still requires the actual named root to be marked. Starting with
D_central, floor Z to1,Y to1,X to2,C to2, including actual opposite
orientations. Denote the result D_current. The changed source proofs
below establish row preservation and the fresh-source property for
each new floor. They reuse completed constructor/inverse proofs.

## The only new Y zero is1, and its target is E1

The entire Y core has no negative-depth node. Its only zero-depth
cores are1 and7 (both depth4). The old7 proof still reaches Z; it
uses present Score5 at R, independent of marking any other label.

Access1 has core output

 Y1=1(0,3(2,4(E,5(E,8(6(E,7),E))))).

The core labels0,2,3,4,5 ALL have depth<=3 in Y1. Every actual
full A target observes only those nonroot Score labels. Here is
the complete original-source proof, with Y's R5 guard retained:

 L: 4(1(A,B),5(C,D)) ->1(A,4(B,5(C,D)));
 LL:4(p(1(A,B),C),5(D,E)) ->1(A,p(B,4(C,5(D,E))));
 LR:4(p(A,1(B,C)),5(D,E)) ->1(p(A,B),4(C,5(D,E))).

Blocks below1 contain only Score0. In L/LR the other observed roots
are4,5 or labels strictly between1,4. In LL the parent p lies between
1,4 and the same interval bounds cover its side roots. Scores6/7/8
remain below present5 at depth>=3. G reads old owner4, whose children
afterward are5 or an interval-(1,4) block; it cannot fabricate6/7/8.
Thus the LITERAL full target is E1, for arbitrary mu and private
completions, without a new target source-admissibility premise.

All newly raised Y rows are paid: zero1 ends in E1, zero7 in Z;
all other H1 exits are positive. The one-credit LOW rule covers all
helpers, so the generalized Y floor is safe.

## Z and X do not acquire dangerous lower targets

At a fresh Z source Score4 at LL hides EVERY smaller Score0/1/2/3
below depth2. Only4/5/6/8 are eligible and their B depths are<=2.
The old one-credit proof is therefore already independent of mu.

At a fresh X source Score3 at LL hides0/1/2. The eligible targets
remain3/4/6/7/8. Targets3/8 have price2. Target4's price1 endpoint
is the generalized Y, now with floor1. Targets6/7 have the completed
core outputs in CENTRAL_RESET.md. Only cores1/2 can be deeper than3
in those outputs. Their A source subtrees lie below3 at source depth3
or greater and the upper access pushes the whole4/3 block deeper.
G reads old owner5, its child4, or a higher interval block. It cannot
expose1/2. The actual full targets therefore belong to E1 for ALL
masks, even though the entire core output need not have height3.
Do not replace this source-order/G argument by a global height claim.

X's helper proof used PRESENT separators4/3, not their marks. Its
only cheap helper is maximum at initial B depth2, and every eligible
terminal is4 or>=5, all at pre-B depth<=4. This proof is unchanged.
Gamma0 retains its marked-endpoint floor law. X may be raised to2.

## C's new +1 targets1 and2 are paid directly

The only new eligible Scores at C are1/2, in A LR below present0.
They have source B depths3/2, hence price1. Their exact core outputs
are

 C1=1(0,3(2,4(E,8(7(6(5,E),E),E))));
 C2=2(0(E,1),3(E,4(E,8(7(6(5,E),E),E)))).

For x=1 or2 an original H1 source necessarily has the proper form

 3(0(A,x(B,C)),4(D,5(E,F)))
      ->x(0(A,B),3(C,4(D,5(E,F)))).

Every full target nonroot observed Score is among0,1,2,3,4, excluding
the new root x itself. Other than these, all Score labels are below
the displayed Score4 at RR at depth>=3. In both C1/C2 every listed
nonroot label has core depth<=2. The old owner3's current child is
an interval-(x,3) root or4, so its G fallbacks also remain in that
same shallow set. Hence these ACTUAL targets are E1 and have credit1.

Other C exits are unchanged:0/4 at price2,5 at price0 into X2;
6/7/8 hidden below present5. The minimum LL helper only exposes
terminal0/3;1/2 move below terminal depth2. Its price>=3 proof is
mark-independent. Gamma0 is floor-safe. The generalized C cap2
therefore proves every C-source LOW row for ALL legal masks.

The four ordered floors preserve each valid old LOW row individually.
They preserve all existing terminal floors, unmarked-source0, range2,
HIGH/h0 and the exact-source-debt induction. Every full nonnegative
incoming row to C or X is now valid for every mask and sigma.
No original-root evaluation, population/mask test, new psi query or
completed semantic-check replay is used. This is additional uniform
coverage; complete Step4 still requires that the remaining 36-slot
marked-source frontier is exhausted by proved regions or new signed
arguments. This document does not assert that unproved implication.
