# GSO trace/ports backend, 2026-11-22 v001

This version extends the sealed GSO engine through read-only adapters. The full
mathematical proof and current frontier belong to the [Notion composition
ledger](https://app.notion.com/p/41f6251839be81cbbf9fef223a08cabd).
Universal Coarse Double is **OPEN**.

The backend is an annotated view of the original physical execution. It never
interprets an induced rotation trace as an ordinary local splay word. Named
outside endpoints and original StepEv/bit IDs remain present. Virtual A bits
and reaching-prefix work supply no credit.

## Modules

- `trace.py`: physical source/port compiler, exact masks and annotated views.
- `trace_teacher.py`: joint anonymous-state potential LP with rational checks;
  exact cyclic per-block-bank flow/min-cut teacher.
- `joint_synthesis.py`: simultaneous shared local/interface values and bounded
  cyclic block-bank optimization; `verify_joint.py` checks all signed changes
  and seam equations independently over exact rational numbers.
- `trace_induction.py`: exact finite ICE successor-implication feedback.
- `trace_symbolic.py`: gap-observer factorization checks, RR permutation
  certificate, learned bank loop invariant and Z3 induction.
- `resource_audit.py`: disjoint cyclic KEEP-gap vouchers, integral path
  decomposition back to literal original A units.
- `padding_attack.py`: complete cost-preserving private-gap witnesses and the
  anonymous-port histogram pump adversary.
- `verify.py`, `extra_verify.py`: separate immutable replay, two-split interval
  projection, full original carrier/Pi verification, ports, bank/min-cut and
  resource-path checks; no current producer or learner imports.
- `TraceKernel.lean`: exact conditional conservation/telescope and obstruction
  arithmetic. The original source model is not fully formalized.
- `gso.py`: backend CLI and explicit root acceptance gate.

## Run

From this directory, with installed dependencies only:

```powershell
python -B gso.py status
python -B gso.py verify
python -B tests.py
python -B preserve.py
python -B seal.py --verify
```

`gso.py research` orchestrates the bounded build in an **unsealed** fresh
versioned copy; sealed outputs are read-only. Existing stages are explicit
cached artifacts and are checked by the separate verifiers. Old engine state
is available through the pinned v1 CLI; it is not overwritten by this backend.

## Certificate boundaries

`run_001/JOINT_PORT_POTENTIAL.json` preserves a failed rounded recovery.
`FINITE_RELAXED_CANDIDATE.json` retains those coefficients with c=d=2 and checks
all 8563 training operations exactly. Its explicit zero extension is refuted
by the complete padded H3,5 source. No optimality is asserted.

The declared fixed shared anonymous-port state-sum grammar is excluded for
every finite c,d by the universal padding/RR-swap argument in Notion. This
does not exclude named-port geometry or history banks.

The capacity4/c=4 bank has exact deficient cuts; capacity5 repairs them on the
finite population. Resource provenance is in `resources_001/` and
`bank_relax_001/`. Such feasibility is not a source-uniform policy or proof.

The learned ledger identity is conditional on a physical policy that always
funds a B double and has a closed seam. That construction remains missing.
General automated mechanism invention, complete arbitrary-tree induction
synthesis and full Lean original-model verification are not implemented.
