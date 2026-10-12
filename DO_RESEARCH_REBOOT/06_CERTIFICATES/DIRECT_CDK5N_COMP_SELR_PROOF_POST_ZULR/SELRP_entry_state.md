# SELR-PROOF entry and preservation audit (§2)

- Root: splay-multiscale-transfer-liquidity-k6c2; branch coarse-double-branch.
- Local HEAD 3701f7355d6af8f22342558443c3796a8a822d20 == origin
  (ls-remote verified at entry); parent ce009c8 (ZULR-PROOF).
- Tracked worktree clean; 6 pre-existing MSINK-era untracked files
  preserved, out of scope, untouched.
- SELR Gate-0 package verified present (37 files, committed in 3701f73);
  Gate-0 verdict: CDK5NSELR-G0-A APPROVED (treated as evidence, not PASS).
- SELR not promoted: no 02_PROVED single_exception file, no CDK5NSELR-A
  ledger row/dependency addendum (checked pre-write).
- All 24 pre-SELR domains verified importable and evaluated (bank24 smoke:
  ZULR-IN flags exactly ZULR; SELR-IN/OUT flag nothing).
- Source SHAs 4/4 match pins (recomputed from bytes).
- No reset/clean/destructive checkout/force-push/history rewrite. Gate-0 and
  predecessor files read-only (append-only errata live here).
