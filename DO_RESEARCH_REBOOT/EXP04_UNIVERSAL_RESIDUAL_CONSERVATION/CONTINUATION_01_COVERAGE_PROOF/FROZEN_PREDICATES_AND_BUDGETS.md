# Exact frozen coverage domain and budgets

This is a read-only reconstruction of the parent checkpoint predicates, not
a reinterpretation of a comparison as an original source. Executable hashes
are pinned in INPUT_MANIFEST.json. The original physical key universe,
allowed reachability, paired closure, measured A and Q_B, S, D6 I, original
cut/orientation, primitive IDs, cyclic Pi, chosen births, first-hit cohorts,
renewal predicates and three-slot interface are unchanged.

R_* is exactly EXP03's original unhandled occurrence set minus its equality-
restart-paid occurrences. For an occurrence rho, h is its original consuming
KEEP, p its original consuming B double, and g that double's original old
grandparent. Eligibility below concerns rho, not a newly classified shadow.

## 1. Carrier-boundary comparisons:12 C_seq A

At each actual operation boundary define Psi=|J_S(B)\J_S(A)| using nonzero
original S-labelled rooted-subtree SET carriers. Cut into actual positive-Psi
episodes, including the terminating Psi=0 operation, with cyclic handling
fixed by exp04_core.psi_episodes. A period with no zero is one persistent
episode. Do not replace Psi=0 by full physical equality.

For each direction d in {+1,-1}, collapse consecutive equal KEEP targets into
blocks inside the episode; intervening DELETEs do not form target blocks.
At each next unowned block, shadow_candidate starts only at the corresponding
extreme of ORIGINAL S. It retains successive ordered S ranks, skipping other
blocks, until the episode ends or S is exhausted. At least two targets must
be retained. From the actual B pre-state at the first retained KEEP, J is
their full initial path union. The retained targets must be the initial
consecutive segment of ordered J and ell>=ceil(|J|/2)+1. A successful window
owns through its last retained block; otherwise advance one block.

Initialize the B comparison at that exact full original B state. An original
rho is paid only if its operation h is retained AND its comparison access
has a physical double with the SAME original old grandparent g. This match
is the exact parent-to-comparison bridge; being in the span is insufficient.
No match across operation IDs is allowed. Each original parent has<=3 slots.

For each direction sum|J|<=2A with disjoint actual A transition witnesses;
sequential access gives6 C_seq A per direction. Two directions cost12 C_seq A.

## 2. Skipped-rank dynamic-finger comparisons:72 C_DF A

Use the same actual Psi episodes and original S ordered in either direction.
Run BOTH deterministic strategies separately in BOTH directions:

* records: from opening block i, retain i and every later strict record of
  directional original-S rank up to episode end;
* earliest_feasible: threshold=ceil(|S|/2)+1. Compute the strict increasing
  suffix subsequence lengths. Reject i if its suffix length is too small;
  otherwise choose the earliest feasible next rank repeatedly until exactly
  threshold targets are retained.

For either strategy require ell>=2 and the full initial B path union
|J|<=2(ell-1). Failure advances one block. Success owns through the last
selected block. Retain every original KEEP in each selected target block.
Skipped ranks are NOT ordinary consecutive-rank sequential access.

The same-operation SAME-old-g physical double matching rule of section1 is
required. Each system has monotone targets in J, integer log-rank travel
<=|J|-1, and ell<=|J|. Dynamic finger bounds its comparison doubles by
3 C_DF|J|. Three slots and sum|J|<=2A give18 C_DF A per system,72 for four.

## 3. Whole-cycle integer rank certificate:15 C_DF A

Rank every actual KEEP target in original S. Include the cyclic seam and put
L=sum ceil(log2(1+|rank(x_i)-rank(x_(i-1))|)); equal target terms are zero.
This class pays all still-unpaid original R_* ONLY WHEN L<=2A. The paired-
closed support bound |S|<=2A and cyclic collapsed target-block count<=A give
Q_B<=5 C_DF A, hence R<=15 C_DF A. L<=2A is an eligibility predicate, not
a source-uniform traffic theorem.

## 4. Locally A-paid actual comparisons:12 C_DF A

Inside each actual Psi episode, start at the next unowned original operation.
For EVERY remaining prefix [s,t] compute from actual pre-B(s) the full initial
path union J of all its KEEP targets, its collapsed target-block count m,
and L=sum ceil(log2(1+rank_J distance)). Define D=|J|+m+L. All actual KEEP
operations are retained. No second scan orientation or old-g matching is
needed because the original B trajectory is replayed exactly.

Accept precisely the LONGEST nonempty-KEEP prefix with D<=4 A([s,t]). If no
such prefix exists advance one original operation. A success owns its entire
span and proceeds after its end. These original operation spans are disjoint.
An original rho is paid if h lies in one. Dynamic finger and three slots give
R<=3 C_DF sum D<=12 C_DF A.

## Frozen endpoint and logical assertion under attack

Together with EXP03, the source-uniform partial bound is

    Q_B <=(35+48 C_seq+99 C_DF) A + R_frozen_next.

R_frozen_next is the literal complement of these predicates inside R_*.
The assertion that it is always empty is REFUTED by the complete65-key
source and occurrence rho=(645,(72,3),(80,1)). No predicate or old coefficient
is weakened, silently generalized or revoked by that refutation.

## External and inherited proof dependencies

C_seq and C_DF are absolute theorem constants, with no fitted numeric value.
The dynamic-finger interface used by the pinned parent checkpoint is
Q<=C_DF(N+m+sum log2(1+rank distance)) with linear initialization in N.
Primary sources verified for this continuation: Richard Cole,
[SIAM J. Computing30(1),44–85](https://epubs.siam.org/doi/abs/10.1137/S009753979732699X)
and the [NYU author-report catalogue,1995](https://cs.nyu.edu/dynamic/reports/?year=1995).
Taking integer ceilings only enlarges the comparison bound. Hanging original
fringes are retained physically and excluded from comparison population only
by the proved fixed initial path-union isolation argument.

The original three-slot, closed-core, physical projection, sequential access
and EXP01–03 quantitative dependencies remain inherited mathematical proofs.
This continuation is a same-agent proof and programmatic verification, not an
independent human or formal end-to-end audit of Dynamic Optimality.
