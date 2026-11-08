# A fully closed six-key source family requiring nonlocal donors

Status: source derivation complete; see INDEPENDENT_AUDIT.md for the separate
audit. This is a universal arbitrary-fringe identity and a scoped repayment
theorem. It is not a finite-population test, a negative CD cycle, or a
universal Step2 certificate.

Use eleven ordered distinguished roles 1<...<11 and twelve independent
arbitrary ordered BSTs F0,...,F11 in the inorder gaps. Every key in every Fi
remains present. No Fi is instantiated, required empty, or bounded. R11 is
the right vine on these roles, carrying those Fi. Start at the diagonal
(A,B)=(R11,R11). K is original KEEP; D is original DELETE, which splays A
and freezes B without removing any key.

Reuse the completed source identities W6 and H6 from REPAY01:

    W6 = K3 K5 K7 K9 K11 K9 K7 K5 K3 K1
    H6 = K11 K1 K3 K5 K7 K9 K11 K9 K7 K5 K3 K1.

W6 fixes the full pair R11 with A=QF=10. H6 fixes B with QF=20.
After its first two KEEPs, the ten-KEEP suffix has A=QF=14 whenever A is
aligned with that actual B endpoint. These whole source identities are
premises, not replayed old semantic rows.

Insert the following source block between W6 and H6, and insert the stated
A-only repair between the first two and the remaining ten KEEPs of H6:

    W6
    K3 K5 K3 D1
    D8 D1 D9 D11 D8 D1 D9 D1
    K1
    K11 K1
    D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11
    D10 D9 D8 D7 D6 D5 D4 D3 D2 D1
    D11 D1
    K3 K5 K7 K9 K11 K9 K7 K5 K3 K1.             (Xi)

Its full B word is W6 V H6, where V=K3 K5 K3 K1 is a neighboring
RR,RR,LL,LL identity at R11, with four doubles. All inserted D operations
freeze B. Xi has 58 original operations: 26 KEEPs and 32 DELETEs. Every
source operation, including each zero A operation, belongs to this word
exactly once. All six odd KEEP roles are genuine, and their full ancestor
core consists of the eleven distinguished roles.

## New free-term A identities

Write k(L,R) for a node and retain each independent Fi. Immediately after
the new K3 K5 K3, D1 has path LL and returns A to R11. The next eight
DELETE paths and actual StepEv counts are

    D8: RRRRRRR,4; D1: L,1; D9: RR,1; D11: RR,1;
    D8: LLL,2; D1: L,1; D9: RRL,2; D1: L,1.

They prepare the exact tree

    Lmid = 3(2(F1,F2),5(4(F3,F4),7(6(F5,F6),F7)))
    P = 1(F0,9(8(Lmid,F8),11(10(F9,F10),F11))).       (1)

The next K1 is an A root operation. The critical K11,K1 at occurrences
24,25 have actual A paths RR,LL, costs1,1, and restore P. In B they are
the H6 q5,q1 pair. Thus this is the core11 paired H=2 class in the request.

The ascending DELETE scan from P has paths

    [empty],RLLL,RL,RLLL,RL,RLLL,RL,RL,R,RL,R

for roles1 through11, costing13. It ends at the left vine L11. Descending
D10,...,D1 are ten single L rotations and return A to R11, costing10.
Finally D11,D1 have paths R^10,LL and cost5,1. They put A at precisely the
already certified full B endpoint after H6's first K11,K1. The inherited
ten-KEEP suffix now acts identically on A and B and closes both at R11,
including every Fi. Therefore Xi is reachable and fully paired-closed.

Its exact actual totals are

    A = 10+3+1+13+0+2+23+6+14 = 72
    QF = 10+4+20 = 34,       2A-QF = 110.            (2)

The new identities are checked as free terms on prescribed source paths
in source_terms.json; no key search, source engine, or finite fringe
instance is involved. Each original parent-first splay double is one A
StepEv, as in the inherited source semantics.

## The aligned erased history

Erase key3: change K3 to D3 while retaining the same A operations and IDs.
Reuse the completed W6 H6 comparison, whose recurrent erased B tree T9
is the right skeleton on {1,2,5,6,7,8,9,10,11}, with
G=4(3(F2,F3),F4) in the left gap of5. W6 returns this erased tree to T9.
The inserted V becomes D3,K5,D3,K1. Its retained RR,LL doubles fix T9,
costing2. This new identity is proved separately by prescribed rotations.
The original full V costs4.

The first erased warmup still differs by precisely one double: its first
retained K5 joins the same old recurrent state, and every new insertion
subsequently fixes the same states. Therefore u=1,L=1, first QE=27 and
recurrent QE=26. Only recurrent QE finances the aligned period. Totals:

    D3=7, J3=1, P=8, N=0,
    RE=2A-QE=118,   RF=RE-(D3+J3)=110.             (3)

The seven direct erased doubles are two from W6, two from V, and three
from the H6 suffix. Retained V counts agree, and the only retained
positive discrepancy is qF5 versus qE4 at occurrence24. No retained
negative discrepancy occurs. The original and erased B states disagree
at every boundary: reuse the old W6/H6 result; during V the roots differ
at K3, at K5 their left-child distinguished roles are4 versus2, and at
K1 they are R11 versus T9. DELETEs freeze these differences.

## A full source-unit receipt on Xi

In the FIXED Step1 allocation, the auxiliary macro after V's K5 at12
ends at K1 at23. Its actual A events are K3:1, D1:1, the preparation:13,
and terminal K1:0, so H=15. Its first three events are (13,1),(14,1),
(15,1). Hence BOTH bits of

    (15,2), (15,3), (15,4), (16,1)                  (4)

are guaranteed members of U by the sealed first-three tail exclusion.
They are actual DELETE-origin units, independent of auxiliary debts.
Take the eight units in this event order, bit0 before bit1, and assign
them respectively to full demand IDs

    (1,1),(9,1),(11,1),(13,1),(24,5),(49,1),(49,2),(57,1).    (5)

A demand ID is (absolute-period occurrence, local full B-double ordinal);
a unit ID adds local A-event ordinal and bit0/1. The first four and last
three demands in (5) are exactly the direct erased doubles; (24,5) is
the unmatched critical fifth double. The receipt is injective, retains
every common fE assignment, and spends no fE(N). It covers every unmatched
demand on this family, not merely the critical pair. All other original
B demands are the ordinal common demands already funded by fE.

Transport all IDs together to Step1's actual aligned period if its legal
maximum-debt cut differs. That cut is an auxiliary macro boundary, so it
does not split the H15 macro. These are actual units in that period, not
startup funds or a second copy of a period. Some demands precede their
donors; payment is at cyclic block level, not native causal matching-
terminal eligibility. Repetitions have fresh actual operation IDs.

This is a smaller complete source-level repayment theorem. Equation(3)
is a consistency check after the explicit receipt, not the proof of it.
