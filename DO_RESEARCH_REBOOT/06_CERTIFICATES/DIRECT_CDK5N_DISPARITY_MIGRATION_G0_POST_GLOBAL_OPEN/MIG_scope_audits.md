# Scope, noncircularity and double-spend audits (P8/P7 + §7 limitation)

## Arbitrary ambient BSTs

P1 identity: ambient-free (finite sums over actual keys) — UNIVERSAL.
P2 bounds: exhaustive n≤7 + locality lifting (frames above untouched by
construction) — UNIVERSAL (bound 2n/rotation scales, no fixture).
P3/P4: rotation counting from code — UNIVERSAL. P5 traces: 5 frozen walks
(FINITE-EXACT; method universal). Net bridge: NONE (OPEN at every scope).

## Arbitrary multiplicity / E4

E3 traces: arbitrary-count compatible (per-interval books; no count bound
used). E4: ZERO source-valid observations (corpus 0/670+, audit 0, controls
0, SELR 0) — E4 extension mechanism ABSENT (explicit blocker; L0 covers E4
conditionally, no witness).

## Noncircularity (P7)

Proved content assumes: splay code semantics, finite arithmetic, replay
validity — none is Q≤2A or a renaming thereof. No Ψ, no potential, no
matching, no aggregate premise anywhere in P1–P5. The excised net clauses
were the circularity risk; excision verified by text diff (freeze vs
corrected: net/restoration/bound sentences removed, blockers named).

## Double-spend (E-type failure check)

No cost unit is spent twice because NO cost unit is spent at all: gross
packet counts are never treated as surplus (P3/P4 docs + ledger convention
forbid it). Receiver coordinates are not charged (traces mark them
redistributed). One access's packets attributed once (ledger convention).
**Double-spend status: NOT PRESENT (no spending constructed).** Any future
bridge must re-audit this from scratch.

## Primitive/nonprimitive, relays, lengths, overlap

Identity/tables/bounds hold regardless of primitivity, relay length,
word length, or K/P overlap (per-access/per-rotation locality). No
unsupported case classification used.
