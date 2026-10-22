# RC-01 DELETE A-Cost Erratum (informational; no proof depended on it)

macro_H = sum over ALL active events of ceil(d_A/2) with NO KEEP/DELETE
branch (verified in PC_ROTATION_INTERPRETER.macro_H + event_a). An active
DELETE therefore contributes a_e >= 0 (positive when its A-path depth is
nonzero) while contributing NOTHING to B (b_blend identity). Zero-depth
root operations contribute a=0 on both sides. Inactive events contribute
nothing to either. AUDIT RESULT: no CORE-01/01B/02 conclusion used H at
all (all monotonicity arguments are B-structural and weight-independent);
hence NO downgrade is required. The erratum stands as a correction to
prose suggesting DELETEs are cost-free, and as a warning for any future
cost-coupled argument (A-cost does not imply B-change and conversely).
