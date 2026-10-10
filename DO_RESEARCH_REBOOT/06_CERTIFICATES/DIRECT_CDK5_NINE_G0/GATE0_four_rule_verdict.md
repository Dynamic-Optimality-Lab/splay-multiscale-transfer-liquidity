# GATE0 four-rule verdict — CDK5N-G0-C (NOVELTY REFUTED)

- **R1 — PASS.** Class properly inside the open nine-core domain; nonempty
  (witness satisfies K/P at its sole debt event); excludes a genuine instance
  (control: K3 a=0, prev D3 a=0 ⇒ Type K/P both False, verified both engines).
- **R2 — PASS.** Interval-charging proof complete and sound (8/8 steps verified;
  see charging-proof file). Not promoted (see R4).
- **R3 — PASS.** One candidate, one mechanism, one witness, bounded program; no
  expansion, no post-hoc predicate change, no replacement search.
- **R4 — FAIL.** Preconstructed witness lies in banked C_26AM-G (packet
  {K3,K7,K1,K9}, h=2, G1–G7 all pass, sole positive). Strict-union novelty
  absent. The witness's positive block excess (+1, required) is real, but the
  walk is already covered.

```text
FINAL: CDK5N-G0-C — NOVELTY REFUTED (witness in 26AM-G; mechanism sound but
unauthorized for promotion; no 02_PROVED entry; universal Coarse-Double OPEN;
DO OPEN). STOP. No successor run.
```

Note for future work (not authorized here): any nine-core successor must clear
26AM-G capacity first — deeply-negative intermediates satisfy, not escape, the
generalized triple. A qualifying witness needs positives whose AM-G triples
fail (e.g. positive intermediates violating G3, or returns missing G4).
