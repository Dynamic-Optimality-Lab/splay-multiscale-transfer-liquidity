# RCG0 proper-subclass certificate (task N — Rule 1)

W_IN (`788b459d…efd6d0a`, 64/36/16): source-valid, closed, engines agree,
five genuine keys, core9 ×37, strict-MSINK member (E=[4,12], t=(0,2),
unique joint sink p=0 with H=13, sole other-positive strict-P), 20/20 direct
negatives, recursive C* negative (complete DAG: 36 rotations, all closed
segments tested, no tiling partition; 19 subproblems, budgets untouched).
Hence W_IN ∈ S_MSINK ∩ R_5^*.

W_OUT (`b8b02be7…bedab3`, 55/36/16): same validity backbone; strict-MSINK
nonmember at H3 (t=(2,2), no short relay); 20/20 direct negatives (MR-H6 at
iv0: dA=0/KEEP-a=0); primitive (34 distinct pre-closure states) ⇒ no
recursive partition possible. Hence W_OUT ∈ R_5^* ∖ S_MSINK.

Therefore ∅ ≠ (S_MSINK ∩ R_5^*) ⊊ R_5^* (R1 PASS). Rule 4 follows for IN
(complete negative recursion DAG mandatory and present; one-level
certificate superseded). Residual claims are relative to C_* only.
