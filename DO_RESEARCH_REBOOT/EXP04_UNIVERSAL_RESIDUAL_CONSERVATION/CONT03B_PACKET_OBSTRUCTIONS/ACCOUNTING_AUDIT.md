# Fixed primary residual and new packet accounting

The requested primary R_upper is unchanged: remove frozen carrier/skipped
payments, original j<=2A_gap B prefixes P, own-path O, then old hybrid H
from original R_*. All original IDs, guards and comparison thresholds stay.

| Mechanism in the new auxiliary reconstruction | Budget times A |
|---|---:|
| Inherited base |35+36 C_seq |
| Frozen two carrier directions |12 C_seq |
| Four frozen skipped-rank systems |72 C_DF |
| C3 E_old on its unchanged C_old pool |6 |
| Whole noncheap old hybrid H_all |30 C_DF |
| Q(D) quota replacing the old P budget |6 |
| Total |47+48 C_seq+102 C_DF |

The new order is an auxiliary proof, not a redefinition of R_upper.
E_old still selects on its original after-P pool; it is not refilled after
H. H_all's30 C_DF proof applies to all noncheap original R_* consumers in
its fixed paid union. Q(D) is selected only after those sets are removed.
Every old P parent left there has j<=2A_gap, so it is selected among the
first2A_gap distinct remaining parents. Old O outside P lies in E_old.
The new paid union therefore contains the old one and R_overflow is a
literal original subset of R_upper.

Per KEEP, selected parent k uses the actual ceil(k/2)-th A StepEv in its
incoming original gap. At most two parents and three gaps/parent give
load6 per cost-one StepEv. No two-bit StepEv is split into two cost-one
resources. Cyclic gaps partition A StepEv; original DELETE helpers count.
Old P is not charged again on top of Q. Comparison initialization and
source-disjoint periodic/local budgeting remain exactly the inherited proof.

For the original target alone the conservative bound is12A+|R_overflow|,
counting E_old and Q separately. Adding this again to the old47 coefficient
would double-charge replaced budgets. Optional old fringe12 and return42
can precede Q, keeping their coefficient101 and a deeper literal overflow.

The separate fixed-g column theorem uses load<=3 per first incoming-gap
StepEv across that whole column. Combining b columns costs3bA explicitly.
It is not free for all keys. Generic P2 may be tested on prehybrid C;
the actual P3 pool D is different and is named explicitly. On the new
counterexample H_all already pays the entire noncheap C, so P3's D is
empty. This does not turn the prehybrid obstruction into a final escape.

The original root-entry graph had stricter resource edges. These new
theorems do not assert a matching in that graph. Their exact scoped
count bounds and physical incoming-gap resources prove the stated loads.
