# RCG0 entry state (task A)

- Branch `coarse-double-branch`; HEAD `333236219c9c5909e34f577dfa4daae09df7ae5c`
  (authorized checkpoint; ancestry + remote HEAD verified equal, no divergence).
- Worktree at entry: only pre-existing untracked items (sibling frozen-theorem
  dir; two Gate-0 finalization worktree files). No staged/unstaged tracked
  changes. No newer theorem supersedes MSINK.
- `02_PROVED/` intact (scoped status empty throughout); MR PROVED untouched;
  no MSINK promotion present (ledger/deps contain no MSINK entry — verified).
- Prior Gate-0 failure (OUTCOME B erratum), PROOF dir, and cyclic-audit commit
  `3332362` all intact and read-only.
- Source SHA-256 values verified equal to the authorized pin table (4/4).
- No destructive reset/clean/checkout/rewrite; unrelated work preserved.
