# S02_AZ_REPORT.md — independent verification summary (anti-fabrication record)

- Every PASS names a machine artifact (16 JSONs + 8 runners/modules + replays).
- Corpus methodology: fixtures supply query pins only (concrete cases ssertify-gated
  BEFORE engine runs); engine never sees witnesses. Recovered words/keys diverge
  from fixtures (canonical 300/700 vs fixture 6/7).
- Three pursuit failures admit openly: (1) symbolic-only staging stalls at ~1.1M
  residuals (measured, pivoted to source-level search); (2) N5 draft negative was
  unsound (w=4 admits B-words) — replaced with airtight w=5, both recorded;
  (3) Step-01 legacy hash transcription typo (file git-clean, corrected with erratum).
- Hand-built corpus bugs caught by BST-validity assertions (ascending-vine fix,
  key-0 placement, key-13 side) — methodology, not cherry-picking: first-ok kept.
- UNSATs rest on complete B-level reasoning; A-level exhaustion yields UNKNOWN by
  design (never UNSAT) — the exact scoping in the Gate-J document.
- Reproduction: S02_CORPUS_GEN.py, S02_SYNTHESIS_RUN.py, S02_GENERALIZE_RUN.py,
  S02_VERIFY_RUN.py from repo root (~10 min total, ~2.5 GiB, seeds fixed).
  No unfinished proof labeled PROVED. No assumed speedups reported as measured.
