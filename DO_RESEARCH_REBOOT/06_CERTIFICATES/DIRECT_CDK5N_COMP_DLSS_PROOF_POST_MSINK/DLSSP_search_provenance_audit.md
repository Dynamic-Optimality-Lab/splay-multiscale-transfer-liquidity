# OUT provenance audit (Gate F — no new search launched)

Declared provenance: seed frozen IN (b8b02be7), L1, candidate index 4,
remove DELETE at zero-based position 7, result a7c6504c…93629fda.

Reconstruction (committed `DLSS_search.mutants` grammar, fixed order
removal→replacement→insertion, index asc, key asc): IN-L1 enumeration has
477 candidates; index 4 is the 5th removal (rm7 — DELETE positions 0,1,2,5,7
are the first five; rm7 removes IN[7]=D9). Recomputed word is
string-identical to the frozen OUT canon; SHA matches a7c6504c…93629fda.
(L1[2] rm2 correctly reconstructs MRW/f6476679 — IN minus its gap-2 D3 —
confirming grammar fidelity.)

Earlier candidates (rechecked): idx0 rm0 non-closed; idx1 rm1 non-closed;
idx2 rm2 DLSS-member (== MRW, MR-banked); idx3 rm5 AMG-banked. First
qualifying residual OUT is idx4. No earlier candidate skipped (all four
decided: 2 invalid-source, 1 DLSS-member, 1 banked).

Concurrent screening: ctl-L1 idx0–3 (rm0/rm1 non-closed, rm4 banked, rm6
hopeful-de3dff28) screened before the freeze registered. Global order
(distance, then seed priority IN < CTL) makes in-L1 idx4 strictly earlier;
the control hopeful is superseded, uncertified for OUT use, retained
as-run. Selection invariant holds; no substitution; no theorem change;
no retroactive provenance invention. Concurrent execution disclosed here
and in the Gate-0 manifest; Rule 3 holds (order-compliant selection).
