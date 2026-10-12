# ZULRP entry state (§2)

- Branch `coarse-double-branch`; entry HEAD `87f1c02576d3281e1e0cc4abb214518faca3494c`
  (authorized checkpoint; remote HEAD equal at entry; ancestry verified;
  parent is the promoted UESINK checkpoint `405861c`).
- Worktree at entry: only pre-existing untracked items (sibling frozen-theorem
  dir; two Gate-0 finalization worktree files). No staged/unstaged tracked
  changes. No newer theorem supersedes ZULR target.
- Promoted MSINK + DLSS + UESINK present in `02_PROVED` (files at HEAD),
  ledger rows present, dependency addenda present.
- Complete ZULR Gate-0 package intact (40 files + search state).
- No ZULR promotion (verified absent from 02_PROVED/ledger/deps).
- Source SHA-256 values verified equal to the §2 pin table (4/4 True).
- No destructive reset/clean/checkout/rewrite/force-push; unrelated work kept.
