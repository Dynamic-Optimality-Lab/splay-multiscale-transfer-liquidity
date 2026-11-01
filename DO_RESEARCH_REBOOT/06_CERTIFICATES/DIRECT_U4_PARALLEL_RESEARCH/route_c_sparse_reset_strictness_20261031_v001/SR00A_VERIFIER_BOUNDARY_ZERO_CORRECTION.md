# Verifier bookkeeping correction, append-only

The first pointer verifier reconstructed all 121 normal/reflected source trajectories, cycles, costs and accepting maps, then failed its final shared-B dictionary comparison with `AssertionError: complete shared B recurrence`. The producer's dictionary includes boundary lap zero. The verifier initialized an empty dictionary and populated only laps 1 onward, omitting the already checked setup endpoint at lap zero.

The correction initializes that verification dictionary as {0:b0}. Here b0 is the independently replayed setup B destination. It does not alter a source input, generator, recurrence, ceiling, cost, cut, unit assignment or strictness criterion. The first verifier and its builder remain unchanged. A new builder writes independent_verify_v002.py exclusively. No first-pass result JSON or acceptance-map file was written before the failing assertion, so the corrected version creates the planned output names exclusively.

Source classification and the predeclared 121 cases are unchanged. This is a verification-index repair, not a source pivot or a promotion before independent checks pass. The final report must identify the successful v002 verifier and retain this provenance.
