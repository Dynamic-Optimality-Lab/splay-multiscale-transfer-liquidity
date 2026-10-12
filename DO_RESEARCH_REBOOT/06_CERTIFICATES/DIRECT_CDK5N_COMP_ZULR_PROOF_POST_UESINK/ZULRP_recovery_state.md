# ZULRP recovery state (continuity document; update after each gate)

- Campaign: DIRECT-CDK5N-COMP-ZULR-PROOF (stage 8B, post-UESINK).
- Committed start: 87f1c02576d3281e1e0cc4abb214518faca3494c (parent 405861c).
- Local HEAD 2026-10-12: 87f1c02 == origin/coarse-double-branch (verified via
  ls-remote); tracked worktree clean; 50 untracked files (45 ZULRP_* in proof
  dir + 5 MSINK-era files), all preserved, none deleted.
- Frozen SHAs verified: theorem e39e8447...; IN 593b3f3a...; OUT 8cd970c7...;
  4 source SHAs per ZULRP_source_hashes.json (adversarial attacks 3-5
  re-check at runtime).
- Completed (file exists; revalidation status in §REC-4 log):
  charter, L1-L9 proof, IN/OUT replay + primitivity, 1449 rotation decisions
  (all EXCLUDED), independent recursive checker + negative certs + verifier
  PASS, cross-validation record, provenance audit + reverify (441 raw / 425
  distinct / rm7 OUT), corpus regression (378+6, 0 residual), 19-case oracle,
  80-attack adversarial PASS + fault injection (2026-10-12 rerun, exit 0).
- Outstanding: 90-obligation adversarial audit (80 present, IDs 81-90
  missing); final R1-R4 adjudication; conditional promotion (FORBIDDEN until
  all gates + all four rules PASS).
- Last successful verification: ZULRP_adversarial.py 80/80 PASS +
  FAULT-INJECTION all-True (rerun 2026-10-12).
- Next task: write/run ZULRP_adversarial_90_recovered.py (preserve
  ZULRP_adversarial.py byte-identical), normaal + -O, capture $LASTEXITCODE.
- Errors: prior session AST/regex inspection failed (tool quoting), new
  session uses python AST script (done: 80 IDs confirmed, missing 81-90).
- Blockers: none repository-side; promotion blocked pending 90-audit + full
  revalidation.
- Provisional R-status: R1/R2/R4 evidence present, adjudication OPEN pending
  90-audit; R3 adjudication OPEN pending provenance/R3 recheck.
- Files changed this continuation: ZULRP_historical_reconstruction.md (new),
  ZULRP_recovery_state.md (this file; update after each gate).
- Promotion: STILL FORBIDDEN.
