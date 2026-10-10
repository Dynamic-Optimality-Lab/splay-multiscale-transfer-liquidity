# ERRATUM: historical fixture comparison (access-by-access)

Committed G0 script `S1_authoritative_replay.py:154-159` vs frozen §2 fixtures.

## Old INC (SHA c9203dc7… = forbidden SHA — confirmed substitution)

`D5,D4,K3,K7,K1,D4,K9,D6,K5,K7,K1,K9,D8,D2,D1,D6,D9` (17 accesses).

## True INC (SHA ff156d94… ✓)

`D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9` (17 accesses).

## Position diff (0-based)

| idx | old (wrong) | true (frozen) |
|---|---|---|
| 0–3 | D5,D4,K3,K7 | identical |
| 4 | K1 | D5 |
| 5 | D4 | K1 |
| 6 | K9 | D4 |
| 7 | D6 | K9 |
| 8 | K5 | K5 (same op, different A/B state) |
| 9–11 | K7,K1,K9 | identical ops, different states |
| 12 | D8 | D2 |
| 13 | D2 | D5 |
| 14 | D1 | D6 |
| 15 | D6 | D1 |
| 16 | D9 | D9 |

The old word is a D4/D6-augmented variant of the CDK5N-DP GAP witness lineage
(A=29 lineage); the true word inserts D5@4, D4@6 and uses tail D2,D5,D6,D1,D9.

## Old CTL vs true CTL

Identical access-by-access (D5,D4,K3,K7,D9,D5,K1,D4,K9,K5,K7,K1,K9,D8,D2,D1,D6,D9;
18 accesses). Only INC was substituted. (Old run died at the INC assert, so old
CTL was never validated; this run validates it.)

## Classification (preserved, not overwritten)

- Historical A=29: arithmetically valid FOR THE WRONG INPUT (both engines
  agreed; closure held). Not evidence against S1.
- The prior G0-C verdict's mechanism audit (R2) is unaffected (predicate-level).
- The prior novelty failure stands only for the wrong word; true-word novelty is
  judged fresh below. Prior directory untouched.
