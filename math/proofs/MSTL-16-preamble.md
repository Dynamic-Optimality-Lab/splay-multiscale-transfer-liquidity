# MSTL-16 structural partition — WP-1 preamble (no theorem claimed, no status change)

**Purpose.** Record the trace infrastructure on which the WP-6 block-partition proof will build.

**Facts established in WP-1.** Every Pair-Access edge elaborates to an exact StepEv trace: ROOT (no event), terminal ZIG (oriented L/R, normalized to class ZIG), or LL/RR/LR/RL doubles. Absent-key accesses elaborate to the empty trace with unchanged tree. Both engines emit identical normalized traces on 40,152 differential episodes (0 mismatches) and on the sealed n28 bundle.

**Preamble claim (not a theorem).** The per-access StepEv sequences produced by `splay_trace`/`trace` are well-defined, deterministic, and complete: every access yields exactly one of {empty trace} ∪ {non-empty StepEv sequence}, and KEEP/DELETE replay consumes each event exactly once in order. The full partition theorem (every execution covered exactly once at block level) is WP-6 work against `math/theorems/MSTL-16.md`; this note only freezes the trace facts it may assume.

**Status:** MSTL-16 remains UNPROVED in `math/proof_status.json`. Consumer: WP-6.
