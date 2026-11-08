# Complete symbolic terminal root-order table

Every row denotes arbitrary ordered gap substitutions. Rank0 is the minimum
among the word keys. Both engines independently derive this table; the
source/frame lifting proof is FULL_PROOF.md section4. False means the
entire universally parameterized one-event word has no A frame.

| Root rank word | BF term contexts | A word feasible |
|---|---:|---|
| 0,1,2,0,3 | 8 | NO |
| 0,1,3,0,2 | 8 | NO |
| 0,2,3,4,1 | 4 | NO |
| 0,3,2,1,4 | 4 | NO |
| 0,3,2,4,1 | 4 | NO |
| 0,4,2,1,3 | 4 | NO |
| 0,4,2,3,1 | 4 | YES: requires original provenance |
| 1,2,3,4,0 | 4 | NO |
| 1,3,0,4,2 | 4 | NO |
| 1,3,2,0,4 | 4 | NO |
| 1,3,2,4,0 | 4 | NO |
| 1,4,0,3,2 | 4 | NO |
| 1,4,2,0,3 | 4 | NO |
| 1,4,2,3,0 | 4 | NO |
| 2,0,4,1,3 | 4 | NO |
| 2,1,4,0,3 | 4 | NO |
| 2,3,0,4,1 | 4 | NO |
| 2,4,0,3,1 | 4 | NO |
| 3,0,2,1,4 | 4 | NO |
| 3,0,2,4,1 | 4 | NO |
| 3,0,4,1,2 | 4 | NO |
| 3,1,2,0,4 | 4 | NO |
| 3,1,2,4,0 | 4 | NO |
| 3,1,4,0,2 | 4 | NO |
| 3,2,0,3,1 | 8 | NO |
| 3,2,1,0,4 | 4 | NO |
| 3,2,1,3,0 | 8 | NO |
| 4,0,2,1,3 | 4 | YES: requires original provenance |
| 4,0,2,3,1 | 4 | NO |
| 4,1,2,0,3 | 4 | NO |
| 4,1,2,3,0 | 4 | NO |
| 4,2,1,0,3 | 4 | NO |

All144 preceding-packet contexts are covered. Only two reflected orders
survive locally, in eight BF contexts; their full cheap-prefix provenance
is excluded by the closed260-frame backward certificate, not by this table alone.
