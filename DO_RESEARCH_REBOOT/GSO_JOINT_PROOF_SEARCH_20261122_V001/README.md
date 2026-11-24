# GSO joint proof search, 2026-11-22 v001

This is the first working **bounded certificate language** that searches an
accounting mechanism, affine invariants, structural bounds, energy coefficients
and induction certificates together. It is not a general mathematical proof
inventor. Universal Coarse Double remains **OPEN**.

The compiler uses all six original splay final-step schemas with arbitrary
hanging BST subtrees and a frame induction for unbounded access depth. The
learner searches initialization/preservation implications and original-q cost
obligations over unbounded integer states. It emits a proof DAG and Lean code
containing the learned coefficients. The independent checker imports neither
the learner nor the schema producer.

## Accounting and unpaid cost

The mechanism combines optional physical capacity-H block banks with a persistent
globally shared overflow reserve G<=gN. Each actual A unit supplies at most J
extra global credit; each genuine KEEP supplies at most T. The global reserve
pays local-bank-unpaid cost and persists across accesses, ancestry recreation
and restoration. Nonzero local-bank unpaid cost is expressly permitted.

The potential grammar is beta*localBankTotal+gamma*globalReserve. These weights,
H,J,T,g, the role rule, ledger invariant coefficients, reserve inequality and
structural post-depth bound are joint search variables. No cumulative unpaid
counter is allowed to masquerade as a cyclic state potential.

The coupled update is monotone and has a constructed greatest cyclic balance.
Actual issuance is at most(8H+J) per original A unit and(H+T) per genuine KEEP.
Weighted accounting is checked against original q, not only the paid subset.

## Results and exact limits

The target remains unrestricted Universal CD. In response to the user's
direction to continue beyond the control, `global_energy.py` attacks an
unrestricted physical energy grammar and emits an all-parameter original-source
obstruction. A complete modified H3q has an original fragment with A=14,
Q_B=q+1, and exactly equal paired-tree rotation distance at its two ends.
Thus no arbitrary family f_N(distance) can satisfy a whole-operation original-q
potential law for any finite constant. All restoration is retained. This
rejects that energy grammar; it does not reject global memory banks or CD.
`MetricKernel.lean` proves the arbitrary-tree left-spine distance construction
and obstruction arithmetic. `verify_metric.py` checks three complete sources
and auxiliary geodesic paths using the pinned immutable physical primitive.

The joint engine also learns the two-target control theorem Q_B<=K_B<=A on arbitrary full
physical support and arbitrary hanging subtrees. It derives cyclic entry from
the previous-root splay postcondition; it does not assume positive spine credit.
This is a control/recovery of a scoped fact, not new unrestricted CD progress.

The final cold run (run_006) learns its invariants in16 iterations, including
energy weights, without reusing any prior counterconstraints. The warm run
(run_005) reuses14 valid inductive counterconstraints and closes in2 additional
iterations. Both select H=0,J=0,T=1,g=1, bank energy weight0 and global
energy weight1. All original B cost in the control is unpaid by the local bank
and is paid by the global reserve. No zero-overflow premise is used.

Unrestricted attempts remain open. A checked parametric obstruction proves the
scalar target-OTHER entry relaxation permits free repeated deep ancestry and
unbounded abstract cost ratios. This is **not** an original paired-source
counterexample and does not refute the selected old H=5 policy or Universal CD.
The language needs an original-state relation linking unconsumed B frames,
physical bank owners and prior A work. It does not currently synthesize that
richer relation or invent arbitrary new invariant atoms automatically.

## Reproduction

```powershell
python -B gso_joint.py status
python -B gso_joint.py root
python -B gso_joint.py accept --scope two_targets
python -B gso_joint.py accept --scope unrestricted
python -B gso_joint.py verify
python -B seal.py --verify
```

The unrestricted acceptance command correctly rejects the scoped control.
Verification is read-only after sealing. Discovery commands require a fresh
unsealed version and fresh output names. All old code/configuration/Git and
all5,625 prior artifacts remain read-only; nothing is installed or committed.

`run_002`, `run_003`, `run_004`, `run_005` retain intermediate successes and UNKNOWN
results; `run_006` records the final cold reproduction. The search command's
`--cold` option disables counterconstraint reuse. All discovery runs must go
in a fresh unsealed checkpoint. `IMPLEMENTATION_CORRECTIONS.json` and `COUNTERCONSTRAINT_REUSE.json`
record the search and proof-emitter corrections, including rejected Lean error
recovery. Only the final successful proof is accepted.

Mathematical proofs, their source scopes and the remaining original-state
abstraction gap are recorded in the connected Notion GSO ledger. Complete
original controls, a historical C=1 rejection and a real target-OTHER burst
are checked by `verify_audit.py`. The finite audit supports implementation
integrity; it does not supply the unbounded theorem.

The first missing implication is a physical inductive relation that pays
target-OTHER work from a globally conserved earlier-A-funded balance or from
a proved full-shape energy decrease. The scalar alias and distance-only
obstructions are permanent constraints for that search. Seventeen rejection
and acceptance-boundary tests include a check that the flat metric fragment
does not falsely refute persistent-bank accounting. No restriction on support,
target count, interleaving, ancestry recreation or period length is added to
the root acceptance condition. No universal constant has been proved.
