# C27-C — an actual raw-two-zero prefix, and why it is not a guarded witness

NEW symbolic source calculation; INDEPENDENT-AUDIT PENDING. No replay,
search or verifier was executed. This file is NOT a G27 witness certificate.
It preserves a substantial construction and two exact failure diagnoses.

## 1. Original full B inventory and actual prefix

Use the literal common initial tree from C23/C24, on keys1..13, with
M={1,3,5,7,9,11,13}; dot means an empty subtree:

    T0=9(2(1,8(3(.,4(.,7(6(5,.),.))),.)),12(10(.,11),13)).

The full KEEP prefix P is the following26 targets, in order:

    1,5,13,7,11,7,9;
    11,13,9,13,7,1,13,1,7,13,9,7,1,7,5,1,7,1,9.

All commands here are original KEEPs. A-only preparation below is inserted
explicitly and never changes full B. The first7 full B paths have the
following bottom-up SS lists (source q is the list length):

| Target | Actual SS list |
|---|---|
|1|LL|
|5|LL,RR,LL,RR|
|13|RR,RR|
|7|RR,LL|
|11|RR,LL,RR|
|7|LL|
|9|LL,RR|

In particular after K5 and K13 the actual trees are the already inspected
C25 prefix formulas. Put X=2(1,4(3,.)), Y=9(.,10(.,11)). Before the first
K7 the tree is

    13(8(5(X,6(.,7)),12(Y,.)),.).

After that K7 it is

    7(6(5(X,.),.),8(.,13(12(Y,.),.))).

The marked ancestors of7 were5 and13, both branching;7 was a leaf.
Thus Q7=2,beta7=2,z7=1. After K11,K7 the actual tree is

    7(6(5(X,.),.),8(.,11(10(9,.),12(.,13)))).

The following K9 has ancestors11 and7, both branching, with9 a leaf.
Its output is

    9(8(7(6(5(X,.),.),.),.),10(.,11(.,12(.,13)))).

Thus it too has Q2,beta2,z1. All13 vertices still have a marked descendant.
This repairs the old invalid five-edge K3 attempt with actual even-depth
SS accesses; it does NOT label both zeros selected without checking A.

## 2. An explicit A preparation: one selected zero, one paid zero

Before the prefix's K5, insert descending DELETEs13,12,...,5. They leave
A rooted at5, its right subtree the right vine6..13, and a left ordered
tree L on1..4. Then insert this literal DELETE target word:

    12,5,7,5,13,5,12,5,7,13,5.

Ordinary splaying gives, at the final K5 (which is an A identity),

    A5=5(L,13(7(6,D),.)), D=12(9(8,11(10,.)),.).

The next original A states/costs are:

| Original KEEP | Actual resulting A tree | A events |
|---|---|---:|
|13|13(5(L,7(6,D)),.)|1, zig|
|7|7(5(L,6),13(D,.))|1, LR|
|11|11(7(5(L,6),9(8,10)),13(12,.))|2|
|7|7(5(L,6),11(9(8,10),13(12,.)))|1, zig|
|9|9(7(5(L,6),8),11(10,13(12,.)))|1, RL|

The prep identity can be checked by substituting the initial right vine
in the original zig/SS/mixed formulas. It uses arbitrary L consistently;
it is an exact finite word, not an assumed arbitrary A/B state stitching.
All preparation costs belong to the unrestricted K5 macro, not the later
H1 zeros. Root-repeat KEEPs and all DELETEs remain actual operations.

For the first K7 zero the watched marked-middle outer edge is13->5.
It was created at the immediately previous K13 zig. That producer has
H1/Q2,beta2,z1, so its h_Lambda prefix already occupies both units and
its protected creator tail is0. The zero7 branch hole remains undefined
after that creator rule.

For K9 the watched marked-middle outer edge is7->11, created at the
immediately preceding K7 zig. That producer has H1/Q1,beta1,z0: its
first bit pays its branch demand, and its second bit is the sole tail.
The only new edge lifetimes from this zig are7->11 and11->9. Both die
at the immediately next K9; that one zero watches7->11, not the inner
11->9 edge. Hence its exported zero-claim group has exactly ONE member.
The mandatory protected creator rule pays that K9-double2 with

    (actual preceding K7 occurrence, 1, 1).

Therefore THIS candidate's zero9 is NOT selected for T19. No later
extension or legal cut can manufacture a second creator-unpaid origin.
The physical unit belongs to that actual K7, not to the later v producer.

For explicit relative original-body occurrence IDs: the first K1 is1,
the nine descending DELETEs and eleven preparation DELETEs occupy2..21,
and K5,K13,K7,K11,K7,K9 are22..27. Thus the candidate has raw zero7
at(24,2), and the actual creator payment is

    demand(27,2) -> unit(26,1,1).

These are actual ORIGINAL body occurrences. They are not a claim that
this printed body boundary is the auxiliary legal maximum-debt cut.

## 3. Full B continuation to the actual hard-unary predecessor

For the remaining19 targets of P, the actual bottom-up SS lists are:

| Index | Target | SS list |
|---:|---:|---|
|1|11|RR|
|2|13|RR|
|3|9|LL,LL|
|4|13|RR|
|5|7|LL,LL|
|6|1|LL,LL|
|7|13|RR,RR|
|8|1|LL|
|9|7|LL,RR|
|10|13|RR|
|11|9|RR,LL|
|12|7|LL|
|13|1|LL|
|14|7|RR|
|15|5|RR,LL|
|16|1|LL|
|17|7|RR,RR|
|18|1|LL|
|19|9|RR,RR|

The resulting physical full B tree is

    Tf=9(2(1,8(7(6(5(4(3,.),.),.),.),.)),12(10(.,11),13)).

Its marked tree is9 with children1,13,11 and the chain7->5->3. Both7
and9 remain NONLEAF throughout this19-access continuation: one verifies
it by the source path-to-star update (a target retains its old children;
every ancestor loses only its path child). Thus the two raw zero deaths
above have not yet had their next leaf births. Nonleaf retargets are
essential; this is not the false no-retarget exclusion argument.

Append the actual R-type full target word

    F=13,1,13,11,1,13,1; then e=3.

From Tf its full costs are1,2,1,3,1,2,1; the pre-e physical chain is

    1->2->13->12->11->10->9->8->7->6->5->4->3.

The deep K3 has Q6. The next leaf births of9 and7 are exactly its
double ordinals3 and2. Recent C/R/G births4/5/6 have their usual source
origins. This certifies RAW lifetime geometry; the mandatory creator
payment above still prevents a two-selected-arrival claim.

## 4. A H1 hard-unary suffix is available without editing the zeros

All A accesses during the19-access continuation are ordinary originals;
no bound on their H is imposed. Before j, reset A by DELETEs13..1.
Use C24's literal P preparation

    12,1,11,1,13,1,12,1,11,13,1

to obtain1(.,13(11(X5,12),.)), where
X5=5(3(2,4),9(7(6,8),10)). Next apply the DELETE word

    3,1,13,11,1,12,1,11,13,1.

Its output is

    Aprej=1(.,13(11(X3,12),.)),
    X3=3(2,5(4,9(7(6,8),10))).

This last identity follows successively by the original rotations; the
last five commands restore the displayed outer1/13/11 frame. These
preparations are in the unrestricted j macro, after the earlier zeros.
Now j=13 is a zig. h=1,g=13 are inverse zigs, s=11 is LR,
t=1 a zig, v=13 RR,p=1 LL,e=3 RL. Thus H_h..H_e=1 and H_j>=3.
This does not change the earlier creator receipt or make zero9 selected.

## 5. Transient erased geometry — exact and insufficient

Start erased B at the SAME initial T0 and erase only KEEP11 processing.
Before the first omitted11 it equals full B. Direct substitution shows
the two omitted11 operations are reconciled by target7 at continuation
index5; its erased physical tree then equals full B exactly. There is
no later11 in P, so both executions reach Tf together.

After j,h the erased tree is

    E*=1(.,12(2(.,9(8(7(6(5(4(3,.),.),.),.),.),10(.,11))),13)).

Its g,t pair and v,p pair each return this entire tree with epsilon1.
The erased e=3 search path is

    1,12,2,9,8,7,6,5,4,3,

depth9, hence qE_e=4. This is an ACTUAL transient original/erased source
calculation, not an independent invented erased tree.

But E* has auxiliary core11, and at e the upper mixed double has
unmarked grandparent12 and unmarked parent2. It leaves key2 without a
marked descendant. The final auxiliary core is at most10. Core labels
are monotone under accesses to the fixed auxiliary support, so E* cannot
belong to a CLOSED auxiliary period containing this e. The computed
epsilon/q4 row therefore cannot be used as the accepted closed h6 input.
After genuine recurrence normalization a different core10/9 state might
still realize e4; no exclusion of those states is established here.

## 6. Original A/full-B closure does not repair either failure

Every full KEEP in P,F,e is all-SS. The inherited O24-S inverse word
undoes them in reverse order and restores full B exactly to T0. Append
DELETEs13..1 to restore A to the right vine. Start that body from the
pair(right-vine,T0), reached from common T0 by the same DELETE reset.
This gives an actual finite A/full-B paired-closed source, with all seven
KEEP keys and full core13, retaining the entire prefix and every event.

It does NOT fix the missing second selected origin, and it does NOT put
the transient erased E* in a closed auxiliary period. No numerical
recurrence indices, h6 debt values, normalized f6 owner map or effective
funding ledger have been fabricated. This construction is a rejected
candidate with two precise guard failures, not a G27 witness or a
universal exclusion theorem.
