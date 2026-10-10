# S1-G0 four-rule verdict — CDK5NS1-G0-C (SOURCE VALIDATION FAILURE)

- **R1 — FAIL.** The designated inclusion evidence does not match its specification
  (A=29 authoritative vs 33 specified; ΣH/ΣR/Q−2A cascade). No valid included
  witness is certified; proper-subclass nonemptiness is not established by this run.
  The excluded control was not reached (STOP at first mismatch per charter).
- **R2 — PASS (inherited, unchanged).** The eight-step charging mechanism is exactly
  the G0-C-audited proof (8/8 steps, same frozen predicate); no definition changed,
  no new defect found. Not promoted (see R1/R4).
- **R3 — PASS.** One candidate, one mechanism, one frozen word each, bounded
  verification; the word was not mutated to force success; no expansion.
- **R4 — FAIL.** No valid witness ⇒ no novelty certification. (Not reached:
  AM-G/exclusion audits are moot without a validated walk.)

```text
FINAL: CDK5NS1-G0-C — SOURCE VALIDATION FAILURE (A total 29 vs 33; Q−2A −40 vs
−48; both engines agree; closure exact; word unmutated). No 02_PROVED entry.
Universal Coarse-Double OPEN. DO OPEN. STOP. No successor.
```
