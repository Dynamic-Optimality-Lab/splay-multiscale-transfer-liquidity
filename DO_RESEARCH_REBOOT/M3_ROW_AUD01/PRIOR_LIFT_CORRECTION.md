# Correction to the previous uniform-formula lift attempts

This addendum supersedes the interpretation of the source-rejection
statements in M3_UNIFORM02/RESULT.md, PROOF_AUDIT.md and STRATEGY_REVIEW.md.
Old files and their exact recorded evaluations remain unchanged.

The UNIFORM01 and UNIFORM02 adapters called build_slow(dag,'UNIFL'), but
their unmodified witness factory populates names MXLw,MXLv,MXLbt,MXL_H,
MXL_w and MXLsb. State fill() follows the passed state object, so source
and destination interfaces were filled; the intended private witness was
not. In the saved UNIFORM02 environment UNIFLw_p0=False, UNIFLw_nev=0,
UNIFL_H=0. The unchanged original root consequently rejects that wrongly
bound assignment. This was an adapter error, not evidence that the
intended physical completion violated original semantics.

The new audit compiles MXL to match the factory, without changing any
source predicate. It accepts a witness with EXACTLY the same full147
source and destination states as the old attempt's proposed interfaces.
An independent process builds the original root under ROWV, bijectively
renames the complete saved assignment, calls no fixture factory and
again obtains TRUE. Independent parent-map A/B replay confirms the
actual depths1/2, H1,q1 and weight+1.

Therefore the specific UNIFORM02 row IS original-realizable, and its
specified sign-run formula IS refuted on the original LOW relation.
That status upgrades the prior original-validity OPEN result for this
candidate. No original realization of the separate UNIFORM01 row was
tested here; its original validity stays unresolved by this audit.

The earlier exact proof-matrix/debt audits were unaffected. Prior signature
source controls use matching MXL tags and remain unchanged. No existing
valid certificate or M3 model is withdrawn. This audit proves no negative
cycle, no new J formula and no full M3/Dynamic Optimality theorem.
