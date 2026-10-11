# MSP entry and provenance (Gate A record)

- Branch `coarse-double-branch`; entry HEAD `87a26a8` (authorized checkpoint).
- Remote `origin/coarse-double-branch` == `87a26a8` at entry (ls-remote).
- Worktree at entry: clean except pre-existing untracked sibling
  `DIRECT_CDK5N_COMP_MSINK_G0_R1HARD/` (frozen H1–H6 source, preserved
  untouched) and two uncommitted Gate-0 finalization worktree files
  (az_report, terminal_status — left uncommitted).
- `02_PROVED/`, ledger, deps, MR artifacts: verified intact, never staged.
- Sibling frozen theorem SHA-256: `31dc3058…ebd55`; committed appendix in
  `MSINK_finalization_four_rule_verdict.md` verified verbatim-identical
  (line-wrapping only). No specification conflict → no blocker.
- Authoritative rule: joint existential H4/H5 (∃p∉E: c=1,H≥3 ∧
  ∀j∉E∪{p}: w>0 ⇒ K∨P, strict Type K d_A≥3 / strict Type P prev-DELETE).
- No newer theorem supersedes MSINK; ledger does not promote MSINK.
- Source hashes re-pinned at certification (see terminal status).
