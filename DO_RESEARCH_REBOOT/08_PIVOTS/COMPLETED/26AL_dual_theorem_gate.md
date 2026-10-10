# PIVOT-26AL (DUAL-THEOREM GATE) REPORT — OUTCOME B

## Verdict

```text
26AL-G AND 26AL-S PROVED

NO SOURCE-VERIFIED NEW SAME-SIDE
CLOSED-WALK COVERAGE

STRICT EXTENSION NOT CERTIFIED

RULE 4: NO
```

## A. Safety
Branch `coarse-double-branch`, HEAD `88d3007` (+ only 26AJ/26AK/26AL untracked
artifacts). No reset/clean/stash/commit. All writes inside `DO_RESEARCH_REBOOT/`.
26AJ/26AK foundations re-read; no defects affecting reuse (block structure, depth
lemma ≤2, successor repayment, m=1, degenerate handling all sound).

## B. Foundations
26AJ (immediate repayment + witness) and 26AK (opposite-branch delayed repayment +
witness) stand as banked. This gate adds: universal +2 displacement (new),
generalized capacity repayment, signed repayment.

## C–D. L1 + cost model
`d_{S_y(B)}(r) ≤ d_B(r)+2` for all present y≠r (frame joining ≤+2 once,
re-carry ≤0 thereafter; op-sites step by 2; tight example documented).
KEEP/DELETE costs, blocks, deficits per source; no model changes.

## E–H. Theorems proved
- **26AL-G**: H1/H2/H4/H5 + capacity (no geometry) ⇒ Q_B≤2A; contains 26AK domain
  (drop opposite-branch only). Disjointness/wraparound/m=1,2,3 proved.
- **26AL-S**: S1–S6 ⇒ δ_{i+2}≤−2 ⇒ triple ≤0; containment in G proved
  (`2a−c ≥ 2 ≥ δ_i`). Disjointness inherited.
- Full statements + proofs: `02_PROVED/26AL_generalized_signed_repayment.md`.

## I. Novelty: NOT established
Same-side closed walk with signed triple: not found (bounded hunt:
~270k random samples, 37 triple-BFS closures attempted, cycle-enumeration BFS;
details + void-run disclosure in companion audit). Hence
`C_26AK ⊂neq C_26AL-G` UNCERTIFIED. 26AJ's word is not same-side delayed.

## J. Four-rule audit
RULE 1 — STRICTLY SMALLER: PASS (one-positive-triple closed walks).
RULE 2 — CONCRETE SOURCE MECHANISM: PASS (frame mechanics + capacity arithmetic).
RULE 3 — COMPLETE BOUNDED PROOF OR DECISIVE STOP: PASS (theorems proved; hunt
bounded and stopped with documented negative result).
RULE 4 — NEW ORIGINAL COARSE-DOUBLE OBLIGATION DISCHARGED: **NO**
(no verified new coverage).

## K. Pipeline effect
Direct branch gains two proved conditional theorems (no new assumptions beyond
their stated H/S-hypotheses) but no new covered walk class. Unrestricted CD,
B≤3A chain, PIVOT-2/LT/DO unchanged (still conditional-open).

## L. Terminal verdict: OUTCOME B (above). No 26AM launched.
Artifacts: `02_PROVED/26AL_generalized_signed_repayment.md`,
`06_CERTIFICATES/26AL_depth_signed_capacity_audit.md`,
`06_CERTIFICATES/26AL/` (probes, hunts, logs, JSONs), this report.
