# Pair-state primitivity documentation erratum (Gate B — NONFATAL)

## The error

Three Gate-0 artifacts describe the 34-access IN as having "33 distinct
pre-closure states":
- `DLSS_IN_worksheet.md:13` ("primitive (33 distinct pre-closure states…").
- `DLSS_four_rule_verdict.md:8` ("primitive: 33 distinct states…").
- `DLSS_adversarial.py:42` + `DLSS_adversarial_results.json:131`
  ("IN 33 distinct recomputed; OUT 33/34 recomputed").

## Fresh recount (this proof stage, independent replay)

- IN (n=34): 35 boundary entries P_0..P_34; 34 pre-closure states P_0..P_33;
  ALL 34 DISTINCT; zero repeats; P_34=P_0 closure exact; engines agree.
- OUT (n=33): 34 boundary entries; 33 pre-closure states; ALL 33 DISTINCT;
  zero repeats; closure exact; engines agree.
Full serials compared (labeled A+B trees); equality classes enumerated;
no root-only comparison.

## Why nonfatal

Primitivity (pairwise distinctness ⇒ no nonempty proper closed subwalk ⇒
no recursive partition can begin) holds for IN regardless of whether the
count is written as 33 or 34 — the code verified `len(set)==len(word)`
correctly (prim=True on 34 states); only the prose number was wrong
(33 belongs to OUT, n=33). No classification, battery, DP, or verdict
depended on the mistyped number. All IN/OUT novelty conclusions stand
unchanged with corrected counts (IN 34/34, OUT 33/33).

## Disposition

Historical files left untouched. Corrected counts used throughout this
proof-stage package. No STOP condition met.
