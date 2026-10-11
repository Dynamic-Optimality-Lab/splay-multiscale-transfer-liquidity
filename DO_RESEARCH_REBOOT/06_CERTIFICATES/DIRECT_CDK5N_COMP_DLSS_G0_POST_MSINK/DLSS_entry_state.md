# DLSS Gate-0 entry state (§2)

- Branch `coarse-double-branch`; entry HEAD `6213764` (authorized checkpoint;
  remote HEAD equal, no divergence; ancestry verified).
- Worktree at entry: only pre-existing untracked items (sibling frozen-theorem
  dir; two Gate-0 finalization worktree files). No staged/unstaged tracked
  changes. No newer theorem supersedes DLSS target.
- MSINK present in `02_PROVED` (file at HEAD), ledger row present, dependency
  addendum present; failed campaigns + errata intact (worktree clean for them).
- No MSINK promotion beyond the existing banked record.
- Source SHA-256 values verified equal to the §2 pin table (4/4 True).
- No destructive reset/clean/checkout/rewrite/force-push; unrelated work kept.
