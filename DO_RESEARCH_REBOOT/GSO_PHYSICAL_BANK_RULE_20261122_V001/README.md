# GSO physical bank rule, 2026-11-22 v001

This module implements one frozen physical bank and proves a canonical cyclic
balance construction. The all-finite-capacity payment claim for this rule is
**refuted**. Universal Coarse Double remains **OPEN**.

The actual source model, real rotations, carrier and original cyclic Pi/U
predicates are unchanged. All old checkpoints are read-only. Main mathematical
proofs and decisions are in the connected Notion research ledger; this README
documents the executable companion and exact verification scopes.

## Frozen rule

Each fixed rank block of at most five physical keys has a persistent capacity-H
bank. Original A StepEv footprints replenish their banks to H with total load
at most8H per actual A unit. A genuine B KEEP replenishes its target bank once,
with load at mostH via the original disjoint A-gap injection. An original B
step pools its footprint, pays its one original double cost, and fills target
first then other touched blocks by increasing physical rank. B mints no credit.
An underfunded event is recorded as a failed guard, never a successful payment.

The clipped diagnostic map is monotone. Starting from the full vector and
iterating the full period computes its greatest cyclic balance in at most mH
strict descents for integer capacity. Failure there rules out every closed
initial balance for this same rule. The source proof also excludes every
positive finite real capacity for the natural continuous version.

## Commands

```powershell
python -B gso_bank.py status
python -B gso_bank.py verify
python -B tests.py
python -B preserve.py
python -B seal.py --verify
```

`gso_bank.py research` builds the bounded pipeline in an unsealed fresh
versioned copy, reusing explicit existing stage markers. The sealed checkpoint
is read-only. No dependencies are installed and no old replay output is written.

## Principal modules and artifacts

- `bank_rule.py`: exact guarded policy, clipped completion and monotone descent.
- `fast_trace.py`: complete physical source/StepEv/bit compiler.
- `coarsening.py`: six physical RR roles, stationary carry, exact Z3 transfer
  identities and finite source-window bindings.
- `family.py`: complete all-capacity original H-source recipe and two materialized
  obstruction records. The private artifact alias W_H1 is H_(7,44), a member of
  this new recipe; it is distinct from historical EXP-01 W-family notation.
- `source_induction.py`, `real_capacity.py`: universal source-window arithmetic,
  real-capacity recurrence, finite burn and exact rational recipe checks.
- `original_events.py`: sealed old mutable original-model producer, full Pi.
- `verify.py`: independent immutable source/Pi and bank replay of both reported
  counterexamples, importing no current producer or bank module.
- `verify_audit.py`: independent policy replay on the eighteen sealed physical
  source traces at five capacities; upstream full Pi verification reused.
- `BankKernel.lean`: greatest fixed point by finite-rank descent, conservative
  accounting, conditional cost bound, coarsening loss and dry packet arithmetic.
  It does not formalize the entire original BST source/comb proof.

`counter_001/H8_H9q5_policy.json.gz` fails at original (6400,9),(6400,10).
The complete source has6145 keys,A=24576,Q_B=11342; both unpaid events are
independently checked original U_int. The second complete11521-key source
charges only671 genuine original U RR steps and makes every other B step free;
129 remain underfunded at capacity1. All original operations and restoration
remain in both sources.

The all-H theorem comes from the explicit complete source and interior-window
induction, not from these finite counts. It excludes this redistribution rule,
including larger issuance constants and different cyclic initial balances.
Other redistribution, nonlocal/history potentials, previously paid classes
and the original cost theorem remain outside the refutation.
