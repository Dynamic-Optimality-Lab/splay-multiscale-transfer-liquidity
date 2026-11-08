# Uniform LOW source-depth exclusion

One ordinary rotation changes any fixed physical node's depth by at most1.
A StepEv performs at most two rotations. If an original macro ends at9
and has H<=2, it has at most four rotations, so its initial physical9 depth
is<=4. All original intermediate DELETE/root KEEP operations are included.

The seven-mark source branch quotient prunes private mark-free terms and
contracts unmarked unary nodes, while retaining physical9 as a distinguished
mark. Its9 depth cannot exceed the actual9 depth. Therefore a quotient
basis whose9 depth exceeds4 cannot realize ANY cold LOW macro. Such a basis
is recorded as exhaustively excluded, not sampled, silently omitted, or used
as a HIGH exclusion. HIGH source states remain in the conservative comparison.

The compiler now records these exclusions before exposing first/second LOW
frames. Its original source-path predicate is explicitly queried/charged.
cold_frames_v2 preserves the prior code, and completed prior producer/audit
batches are reused. The pruning changes no admitted LOW relation and does
not impose a private BST population cutoff.
