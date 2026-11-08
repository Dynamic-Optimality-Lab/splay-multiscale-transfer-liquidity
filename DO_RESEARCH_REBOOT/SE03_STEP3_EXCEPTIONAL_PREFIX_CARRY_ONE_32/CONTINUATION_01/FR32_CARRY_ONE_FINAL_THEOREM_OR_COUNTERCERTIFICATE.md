# OUTCOME A — source-uniform carry-one proved

The frozen EXC theorem is proved, with all immediate/delayed/HIGH cold and
all LOW/HIGH first-return cases covered. The complete statement, dependencies,
source lifting and induction are in `FULL_PROOF.md`. The bound D_out<=1 is
sharp by W101. This is not a zero-reset, eventual-repayment or physical-owner
theorem. Same-agent separate implementation checks pass; external/formal
verification is not claimed. `FINAL_VERDICT.md` is the current verdict.

|Completeness requirement|Disposition|
|---|---|
|FR32.1 frozen class|Exact original EXC; all permitted deeper PREFIX parameters|
|FR32.2 FIX|Separate zero-debt problem stays OPEN; only carry-one inherited where applicable|
|FR32.3 debt|Original cumulative sigma, D=max(0,-B), no running truncation|
|FR32.4 entry|Entry1 throughout EXC, from the frozen exact reduction|
|FR32.5 carry-two necessity|Exactly R<=-1, ruled out by R>=0|
|FR32.6 source geometry|Complete H1 source phase and first-H2 packet partition|
|FR32.7 upper cases|First upper11 by EXC definition; all later13 included; broader upper13 outside EXC unchanged|
|FR32.8 first return|Actual FIRST genuine full7 with every original gap operation retained|
|FR32.9 W101|Preserved, debt1 proves sharpness|
|FR32.10 negative controls|Preserved at inherited scope; no all-times positivity assertion|
|FR32.11 signed corrections|Original E and exact old/new cold gamma; no dropped seam|
|FR32.12 terminal state|Full source state retained, no geometric or owner reset|
|FR32.13 owners/Bank25|No new payment/owner claim; original licenses unchanged|
|FR32.14 closure evidence|Symbolic orbit completion remains distinct from executed replay|
|FR32.15 principal result|D_out<=1, complete symbolic computer-assisted proof|
|FR32.16 next target|Separate C33-FIRST-11 candidate, explicitly OPEN|
