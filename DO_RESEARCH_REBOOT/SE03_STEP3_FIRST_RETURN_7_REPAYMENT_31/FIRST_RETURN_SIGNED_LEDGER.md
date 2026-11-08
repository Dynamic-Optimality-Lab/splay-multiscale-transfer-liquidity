# Gate D — complete actual first-return ledger

The original formulas are rho=2min(H,3)-beta-z and
sigma_E=2min(H,3)-QF+Delta E=rho+Delta(3-b), where b is actual marked
branch count. E counts nearest-marked-ancestor excess, not physical BST
binary children. No old chart-switching normalization is revived.

|short-prefix t|key|H|QF|QE(short prefix)|beta|z|rho|E before->after|sigma_E|A path|B path|
|---|---|---|---|---|---|---|---|---|---|---|---|
|123|7|1|2|2|2|0|0|1->1|0|L|LLRR|
|124|11|1|2|0|1|1|0|1->0|-1|RL|RRLL|
|125|5|1|3|2|3|1|-2|0->1|0|LL|LLLLRR|
|126|11|1|1|0|1|0|1|1->0|0|RR|RR|
|127|9|1|3|2|2|1|-1|0->1|0|LR|LLRRRR|
|128|5|1|1|0|1|0|1|1->0|0|LL|LL|
|129|7|1|2|1|2|1|-1|0->0|0|R|RRLL|
|130|11|1|2|0|1|0|1|0->1|1|RR|RRRR|

The six macros124..129 have sum H6, QF12 and price0; E1->0 gives sigma-1.
Helper124 owes1, comb125 preserves it, and every upper/bridge/return term
is0. Thus R_return0<D_entry1. No hidden return boundary resets E.
Next11 at130 has+1 and restores this particular accumulated signed balance.
The rho and branch-correction columns are retained through every boundary;
rho alone is not silently substituted for sigma.

QE above belongs ONLY to the replayed short reaching prefix. In the actual
erased-aligned closed period its exact states/costs are defined by the
original F_E orbit, not those numerical columns. FR31's intrinsic full-B
inequality uses A,QF,E and is unchanged by that orbit alignment. No unknown
auxiliary normalized owner, physical spare freedom or chart correction is
inferred from the short QE data.


Verification scope: the NEW local trajectory has a distinct mutable source
execution and a tuple-engine check of the revised suffix. Whole W101 and
the enormous erased-aligned period are proved by the written source-word
construction, NOT reported as replayed. Same-agent distinct implementations
are not external peer review or proof-assistant verification. Uniform source
inductions retain their manuscript/audit-pending status. Principal
FR31-PREFIX's stated local signed law is refuted; universal FR31-FIX,
all-source owner supply, Gate U, Universal CD and Dynamic Optimality remain
OPEN. Historical receipts, audit labels, owners, R1-R4, Bank25 and caps
are unchanged.
