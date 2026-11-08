# Reproduction and audit boundary

Run from the repository root with Python and the existing source files.
Do not run the append-only producers in their sealed directory: their
exclusive-create outputs intentionally refuse overwrites. For reproduction
use a fresh sibling directory with copies of the four new Python scripts
and gate/scope files, or review the deterministic outputs in place.

Order:

    python -X utf8 -B <fresh-run>/audit_first_return.py

The historical V001 run retained its entry pins and stopped on the inherited
seed sentinel [-1,0]. For the exact retained run, completion used

    python -X utf8 -B <run>/audit_first_return_v002.py
    python -X utf8 -B <run>/build_witness.py
    python -X utf8 -B <run>/independent_verify.py

The V002 wrapper changes only the sentinel loop guard. It verifies rather
than overwrites existing entry pins; the source selection order is unchanged.
To repeat from scratch in a fresh directory, run V001 (which records pins
before that same expected metadata error), then V002. Independent verification
writes a new independent_audit.json exclusively; copying the checker into a
fresh audit sibling or changing only the new audit output name is necessary
to rerun without destroying its first result.

Inputs: hash-pinned RC01/PF01 reports and source profiles; the existing complete
seven-core transition table/relation and independent audit; original tuple
and pointer splay engines. `entry_source_pins.json` pins their raw bytes plus
the prior research inventory and all125 Stage11G files. All source lookups
use existing integer rows. No optimizer, fit, new active-core size or numerical
approximation is used.

The selection audit examined193 existing (1,3) anchor edges,743 first payers,
64 second payers,5 third payers and1 first-return candidate before finding
the lexicographically first witness. These counts describe the deterministic
prefix search, not a universal enumeration of all trees or all histories.
The later-positive cost-one BFS found no such exit in its selected fixed
class; no universal impossibility is inferred from that negative subtest.
The predeclared unrestricted source closure in the same old component
produced the exact19-key word in PG02, which was retained unaltered.

Independent verification uses the TWO ORIGINAL physical splay engines at the
already inherited n=13 embedding, not the producer's profile routine. It
reconstructs source entry by original subtree membership and all76 one-period
FI/PF cut ledgers, including event/demand multiplicity and unused reservations.
The tuple engine separately checks the closed source identity on an opaque
fringe term. The formal variable is not an abstract source counterexample:
the actual n=13 BST witness, legal startup and exact closure are also supplied.
Universal fringe substitution follows from the local tree identities.

Control replay counts:104 physical tuple calls,104 physical pointer calls,
38 opaque-term calls. No additional m or n is replayed. The all-m theorem
uses identical returning sources and the explicit +19ell ceiling relation,
not finite induction evidence. The full general one-unit repay-or-synchronize
theorem remains open.
