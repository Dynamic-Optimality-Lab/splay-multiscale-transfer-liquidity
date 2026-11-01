# Nonlinear endpoint matching repairs vines but fails helpers

No nonlinear repair satisfying all requested conditions was found. The explicit endpoint-matching candidate proves DELETE universally and pays full q on every opposite-vine access, but it fails the first six-key arbitrary-fringe helper at the allowed empty fringe.

For each tree, take its proper nonempty subtree key sets and fix the full-set match separately. Join two proper sets when their minima agree or their maxima agree. If nu is the maximum one-to-one matching cardinality, define

    E(A,B)=(n-1)-nu(A,B).

This is a nonlinear repair of F: E-F equals the number of exact common proper sets minus nu. It uses only the current physical trees.

One primitive A rotation replaces one vertex, so Delta_DELETE E<=d_A<=2a on every size. On opposite vines, explicit matchings and equal-size covers prove

    Delta_KEEP E=-(q+2), n>=4,

and all smaller cases also pay q. The nonlinear bonus therefore repairs the old unbounded opposite-vine deficit without breaking DELETE. See [the definition and DELETE proof](EM01_DEFINITION_AND_DELETE.md) and [the all-size vine proof](EM02_OPPOSITE_VINE_PROOF.md).

The helper requirement nevertheless fails:

    E source=1, E after A=2, E destination=2,
    a=1, q=2, Delta E=+1 > 0=2a-q.

The old F decreases from 4 to 3 on the same operation. The matching correction itself increases by two and loses F's helper safety. [The exact obstruction](EM03_EXACT_HELPER_OBSTRUCTION.md) includes the full trees and small hand-checkable optimal matching certificates.

[Independent verification](independent_audit.json) passed: eighteen graph values have equal-cardinality matching/cover certificates, and the complete eleven-operation source replay closes exactly. Its totals A=16,Q_B=4 do not refute Coarse-Double. See [the replay audit](EM04_SOURCE_REPLAY_AND_VERIFICATION.md).

The [four-rule gate](EM00_FOUR_RULE_GATE.md) preceded execution. Testing stopped at the first helper failure, and the [mandatory strategy review](EM05_MANDATORY_STRATEGY_REVIEW.md) records two unsuccessful subtree-set repairs without combining their incompatible component proofs. No larger finite fits, new source-state graphs or Stage 11G edits occurred. Universal Coarse-Double remains open.
