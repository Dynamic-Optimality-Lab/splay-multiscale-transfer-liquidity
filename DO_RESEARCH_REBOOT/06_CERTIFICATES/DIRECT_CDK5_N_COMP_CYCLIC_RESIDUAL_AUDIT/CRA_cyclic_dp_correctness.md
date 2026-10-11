# Cyclic DP correctness (tasks F6/F8)

## Algorithm

Per cyclic origin r (0..n-1): vertices 0..n (vertex k = original boundary
(r+k)%n); edge i→j (j-i<n) iff cyclic segment [(r+i),(r+j)) is exactly
pair-closed (full labeled serials) AND covered by ≥1 banked theorem on fresh
from-state replay. BFS shortest path 0→n (≥2 edges automatic: whole-cycle
edge j-i==n excluded). First r (asc) with a path wins; canonical certificate.

## Soundness (PROVED by construction)

Every edge's segment is verified closed (end serial == start serial from
fresh replay) and banked-certified (named theorem predicate True on the
segment's own legs/snaps/domain). Parts partition accesses exactly once
(A/Q additivity checked in every certificate: ΣA_seg==A, ΣQ_seg==Q).
Summing certified Q_seg≤2A_seg gives Q≤2A for the cycle. A0-trivial segments
(all-a==0 closed ⇒ single key + Q==0 verified) satisfy 0≤0 directly.

## Completeness relative to the banked inventory (PROVED)

Any valid cyclic partition into banked-covered closed segments has cuts at
repeated pair states; rotating to its first cut (some r) makes all parts
DP-edges (each part closed + covered by hypothesis); BFS finds a 0→n path.
Hence every certifiable decomposition is found for at least one r. No
heuristic pruning (memoized exact search; 400-segment budget flags
INDETERMINATE rather than negative — never triggered: 0 budget-hits).

## F7 primitive shortcut (lemma PROVED, applied only after verification)

If P_0..P_{n-1} pairwise distinct, no nonempty proper cyclic interval is
closed (its endpoints would repeat), so no ≥2-partition exists. Applies to
pair-state simplicity only, never as aperiodicity, never replacing banked
membership tests (whole-word battery always runs).

## F8 abstract oracle: 8/8 PASS

anchored-2part, nonanchored-needs-rotation (r=1), three-part-shortest
(canonical BFS), primitive-none, whole-only-none, label-inequality
(same-root-different-tree ⇒ no edge), n1-none, rotation-found (first path
at r=3, not r=5 — search order verified).
