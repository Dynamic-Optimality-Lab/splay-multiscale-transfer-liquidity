# A DELETE bridge separates two runs paid by one later pool

The strict witness comes from the already-certified thirteen-key SP word by inserting one source DELETE. It uses the same key size and no fit or search. The source calculation, rather than any general deletion-monotonicity claim, establishes the modified behavior.

## Reachable prefix and exact cycle

Start diagonally at R13 and execute D9. From that reachable pair use

    K13 D11 K12 K11 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D9.

Both full trees close exactly. Independent pointer replay gives

    A=62, Q_B=35, Z_B=28, 2A-Q_B=89.

The first five A-root blocks are:

| Role | Request | a | q | delta=q-2a |
| --- | --- | ---: | ---: | ---: |
| First positive run | KEEP13 | 2 | 6 | +2 |
| Separating bridge | DELETE11 | 2 | 0 | -4 |
| Second positive run | KEEP12 | 1 | 3 | +1 |
| Saturated B-changing intervener | KEEP11 | 1 | 2 | 0 |
| One common payer | KEEP2 | 2 | 0 | -4 |

The positive runs are distinct singleton runs at source occurrences 0 and 2. The selected packet spans all five blocks and has deficit -5. DELETE11's four unused units are not lent. KEEP11 spends its two units on its own B doubles and also lends nothing.

## Exact source rejoin after the inserted DELETE

Let M=2(1,4(3,6(5,8(7,empty)))). After the original KEEP13, A is

    13(10(9(M,empty),12(11,empty)),empty).

DELETE11 searches at depth 3, so a=2. Its source splay gives

    A=11(10(9(M,empty),empty),13(12,empty)),

while B stays S_13 R13. The following KEEP12 searches A at depth 2, giving

    A=12(11(10(9(M,empty),empty),empty),13).

Its B access is unchanged from SP and has depth 6, hence q=3. KEEP11 next uses one A zig, giving

    A=11(10(9(M,empty),empty),12(empty,13)).

This is exactly SP's A tree after its KEEP11. The B trajectory is also identical there because DELETE11 never touched B and the B request sequence remained KEEP13,KEEP12,KEEP11. The modified pair therefore rejoins SP's full pair at this point; the complete closing suffix is unchanged apart from occurrence indices.

The source A traces before the rejoin need not agree with SP's traces. The exact calculations show the same grouped costs for KEEP12/KEEP11 and the added DELETE cost 2. No assertion that arbitrary DELETE insertions preserve cost or CD is used.

## Why sharing across the gap is necessary for these rules

Before the first positive, its shallow set is {1,2}. The only block in that run's following gap before KEEP12 is DELETE11. Its key is 11, outside that set. Thus SP finds no payer for the first run, despite the bridge having unused A capacity, and rejects the whole walk.

The new batch does not discard that unpaid deficit. At KEEP12 it appends the second positive, whose pre-B shallow set is {13,2}. The common set becomes {2} and pending excess becomes 3. KEEP11's key is not 2. At KEEP2 the batch closes:

    source ceilings: 2 and 1,
    common ceiling: min(2,1)=1,
    pending excess + common ceiling = 3+1=4=2a_payer.

DELETE11 contributes no B tax. The first anchor's two genuine interveners are KEEP12 and KEEP11; the second anchor's only intervener is KEEP11. Both have post-anchor height h=1 for key 2.

The payer pool's first two units pay the first anchor's excess 2; the third pays the second anchor's excess 1. Their source ranges [0,2) and [2,3) do not overlap. Payer q=0 leaves its fourth unit unused. Prefix/startup credits and all bridge credits are excluded from this transfer.

## Cut outcomes are honest one-period certificates

For each orientation, 38 of the 42 block-cut passes succeed. Four end with unpaid anchors and are rejected. A cut inside the unpaid interval cannot use a payer processed before the debt existed by borrowing another lap.

The cyclic class accepts because a complete successful pass exists. Its certificate at cut 0 processes every block once and pays all 35 B demands with distinct units among the 124 A units. Other accepted passes are separate alternative proofs; their credit budgets are not combined. The reflected word has the same values.

Across the new and six preserved controls, independent verification checks 256 trials: 236 accepted covers and 20 rejected passes with explicit unpaid debt. The selected covers have 186 unit assignments. All 6,286 assignments checked across alternative accepted covers are separate per-cover checks, not one enlarged resource budget.

## Analytic size and support extension

After the local KEEP11, the full pair rejoins SP's source pair. The subsequent common ascending requests synchronize both trees by KEEP10. Full scans restore R13 and final D9 restores the cycle's initial A, with B frozen at R13.

Grafting an arbitrary unrequested BST of keys greater than 13 to key 13's right child commutes with every fixed request. The inserted DELETE11 also stays outside that fringe. Hence arbitrary fringe size and shape preserve the local source calculation, sharing and full closure.

For every n>=13, start at R_n, retain prefix D9 and use

    K13 D11 K12 K11 K2 K3 ... Kn
    K1 K2 ... Kn
    K(n-1) ... K1 D9.

There are 3n+3 cycle accesses. The untouched right fringe preserves the local rejoin and synchronization. Thereafter the full common ascending/descending scans restore R_n; final D9 restores the initial A. Every key is genuinely requested by KEEP. The two separated positive runs and their common payer remain unchanged. This is an analytic unbounded-support family, not a finite size sweep.

The named older former-root conditions fail on the positive anchors, and the first non-unit deficit 2 rules out the named unit-run packet predicates. The strict relation proved here is C_SP strictly contained in the new cut-certified class; no claim of an exhaustive classification of all older consequences is made. General cut success and unrestricted CD remain OPEN.
