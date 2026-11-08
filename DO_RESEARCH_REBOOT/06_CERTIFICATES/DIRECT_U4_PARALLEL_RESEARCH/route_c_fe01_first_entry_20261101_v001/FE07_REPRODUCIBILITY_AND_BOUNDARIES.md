# FE01 reproducibility, provenance and proof boundaries

All outputs use exclusive creation. Do not run producers over the sealed
files. For reproduction create a fresh versioned SIBLING under the same
DIRECT_U4_PARALLEL_RESEARCH directory; copy the new .py files, FE00..FE07
reports and status ledger there, WITHOUT copying generated output JSON.
Keep the original source tree and inherited PG01/PG02 files unchanged.

From the repository root, in order:

    python -X utf8 -B <fresh-sibling>/capture_entry.py
    python -X utf8 -B <fresh-sibling>/build_FE_certificates.py
    python -X utf8 -B <fresh-sibling>/independent_verify_FE.py
    python -X utf8 -B <fresh-sibling>/seal_delivery.py

Entry capture refuses to overwrite pins and records the ACTUAL unchanged
HEAD/branch. The retained run initially captured exactly the same data with
an inline Python command before implementation; capture_entry.py is the
saved reproduction equivalent. The original user directive path/hash is
recorded separately. If that attachment is unavailable on another machine,
supply its path with --directive to pin the same input, or record its absence;
no source theorem depends on the attachment's filesystem location.

## Source map

- `python/independent/splay.py::_descend,_rebuild,trace`: original immutable
  tuple source path and parent-first LL/RR; final oriented zig.
- `python/liquidity/legacy_embedding.py::_rot_right,_rot_left,splay_trace`:
  independent original pointer rotations and source events. The unrelated
  liquidity depth+1 cost helpers are NOT substituted for A StepEv counts.
- RC01/FI01/PF01: source ceilings, block semantics and previous procedures.
- PG01: PF-fresh budget, exact reservation-loss identities.
- PG02/PG03 and `closed_source_certificate.json`: the fixed reachable source
  pair,19-block word, original event identities and all-m/fringe return proof.
- `source_first_entry.py`: the NEW source-only H/ceiling implementation. It
  imports no splay engine, constructs no splayed tree and consults no future
  payer q or observed post-depth. Root, access-key and zig-entry cases are
  explicit. No original source function is changed.

Raw SHA256 provenance is in entry_source_pins.json and the new certificates;
the final manifest hashes each new artifact except the manifest itself.

## New independent checks

The producer derives path differences from the six symbolic identities.
The independent checker instead feeds opaque-fringe identities to BOTH
original engines, derives all28 double/10 zig shift entries from their actual
relative positions, and checks the target-fringe outer-shift table too.
Opaque variables stand for arbitrary subtree terms; descendant/internal-depth
generality is a mathematical cancellation proof, not finite depth sampling.

The gate-fixed geometry corpus consists of99 DISTINCT physical source trees
already present in PG02's ordinary/reflected witness and startup/reflection,
all on the existing n=13 embedding. For each tree, all present ordered x,y
pairs are evaluated:16,731 cases. The checker uses original LCA/divergence
coordinates rather than importing the new role selector. It validates H
against BOTH source outputs and verifies H<=U_PF<=U_FI, the consumed source
frame word, original-site containment, root no-ops, y=x, zig entry and exact
later terminal-zig effects. Output inspection occurs only in this validator.
The input trees and deterministic source-formula digest are fully recorded.

For the ONLY strictness witness, both original engines replay the ordinary
and reflected19-block closed word plus the ordinary diagonal startup. The
checker reconstructs all114 one-period trials:19 cuts,3 algorithms,2
orientations. Every FI/PF outcome, reservation and physical assignment agrees
with the frozen PG record. New FE facts and FIFO assignments are calculated
independently, including each demand index, own prefix and loan suffix.
FE accepts17 cuts per orientation, rejects2, and accepts the required cut0.
Its designated loan is donor(copy0,block2,A-event0,bit1) to
recipient(copy0,block0,B-event2); all22 demands are paid exactly once.

Source-call counts in the retained run:

|Purpose|Tuple|Pointer|
|---|---:|---:|
|Six opaque local source identities|6|6|
|Fixed physical geometry inputs, one call per tree/x|1287|1287|
|Fixed physical witness and startup|104|104|
|Opaque common-fringe closed-word identity|38|0|

Independent audit: PASS,350,259 checks in the retained run. Check count
includes preservation checks and may grow in a reproduction that has more
prior artifacts; the mathematical corpus dimensions and cut trials stay
fixed. No source witness search, enlarged key count, fit, solver or m>1
replay is performed. The symbolic local templates are tree identities, not
additional finite-size success examples.

## Universal proof versus finite evidence

FE01/FE02 prove the all-tree identity using source-site induction, complete
role partition and exact shift summation. FE03 proves safe source minima,
monotone debt domination and physical-unit injectivity on all admissible
histories. FE04 proves strictness for every m>=1 and arbitrary untouched common
F from exact returning sources, +19ell older-fact arithmetic and disjoint copy
tags. FE05 proves the fresh-budget corollary by the explicit cyclic minimum.

None of these universal statements is inferred from the16,731 checks or from
an m=1 success. The fixed audit verifies definitions, indexing, source
convention, nonvacuity and claimed physical certificates. PG02's older
17,587 checks remain separate inherited evidence.

Boundaries: arbitrary ordered finite BSTs and present keys for geometry;
empty role subtrees are vacuous, arbitrarily deep role descendants inherit
the same shift, and entry at an outer/final-zig site uses the original-site
invariant. Charging preserves mixed blocks, zero-double genuine zigs,
repeated coordinates and retired pools. The strict witness uses seven core
keys and arbitrary common outer F; it does not classify all other source
pairs/fringe positions. Universal FE completeness, arbitrary one-unit-positive
coverage and universal Coarse-Double remain unproved. Matching-terminal and
Stage11G stay frozen.
