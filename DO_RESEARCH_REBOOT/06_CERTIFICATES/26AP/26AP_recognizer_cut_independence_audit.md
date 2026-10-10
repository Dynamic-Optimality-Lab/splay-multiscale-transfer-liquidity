# 26AP cut-independence audit (executed, not merely argued)

Witness: 27 blocks, positives {0,1,2}, nonpositive cuts = 24 indices.

## Procedure

For EVERY nonpositive j: linearize j+1..j (mod 27), run the O(m) scan,
record decision + cyclic (start,len,return) assignment.

## Result (machine, `26AP_recognizer_selftests.json`)

- 24/24 cuts: ACCEPT.
- 24/24 cyclic assignments identical: run (start 0, len 3, return 3, r=1).
- Printed linear indices differ per cut (expected); underlying cyclic
  run/return assignment invariant.

## Why (proof)

A cut after nonpositive j cannot split a maximal cyclic positive run (runs
contain only positives). The run following each cut position is the same
cyclic run; its following block (return) is cut-independent; r/a tests read
trace-intrinsic metadata. A return cannot be stolen by another run: returns
are consumed exactly once and a return block is nonpositive (rejected as
positive-run member), so assignments agree across cuts. Rotation invariance
follows (rotation = relabeling; scan is over the cyclic order).
