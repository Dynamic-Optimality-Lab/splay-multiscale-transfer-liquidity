# Exact new source debit and physical owner ledger

Complete words, reaching prefix, A/BF/BE trees and all event IDs are in comb_source_fixtures.json. No abstract transition substitutes for them.

|source|macro end|H|Q|beta|z|rho|E before->after|sigma_E|
|---|---:|---:|---:|---:|---:|---:|---|---:|
|C29-weak_zero_helper|159|47|1|1|0|5|1->1|5|
|C29-weak_zero_helper|160|1|2|1|1|0|1->0|-1|
|C29-weak_zero_helper|161|1|3|3|1|-2|0->1|0|
|C29-strong_paid_helper|159|47|1|1|0|5|1->1|5|
|C29-strong_paid_helper|161|2|2|1|1|2|1->0|1|
|C29-strong_paid_helper|162|1|3|3|1|-2|0->1|0|

W0: I129..256, 128 operations, A158,QF34,QE30. W1: I129..257,129 operations,A159,QF34,QE30. Both reach S after the SAME original128-operation W0 prefix from the explicit common diagonal T.

W0 actual prior33 map leaves helper demand(160,2), not two comb demands. Its nominal helper bit(160,1,1) is LOCKED by comb(161,3). The full native comparison sends that comb demand to preparation bit(129,1,1), which is physically real and outside the prior image. Append only (160,2)->(129,1,1).

W1 actual prior33 map leaves helper(161,2); bit(160,1,1) of the extra DELETE1 is locked by comb(162,3). The actual late extension is (161,2)->(129,1,1). All33 old values remain. The separate strong comparison can instead use terminal KEEP13 tail(161,1,0)/(161,1,1); it does NOT replace the current full map.

Both current maps have34/34 demands and Bank peak5. Their physical success alone does not prove a pointwise signed law. The helper debit is included in the pair/triple theorem.

Verification: exact new receipts passed a distinct mutable implementation
operated by the SAME research agent; this is not external peer review or
proof-assistant verification. Universal statements use the written source
proofs, not extrapolation from finite source tests. Accepted inherited scopes
and audit-pending labels remain unchanged. Principal MC29, all-r Gate U and
Dynamic Optimality are OPEN. See EXTREMAL_COMB_REPAYMENT.md and
MIXED_COMB_FAMILY_THEOREM.md for the exact restricted positive conclusions.
