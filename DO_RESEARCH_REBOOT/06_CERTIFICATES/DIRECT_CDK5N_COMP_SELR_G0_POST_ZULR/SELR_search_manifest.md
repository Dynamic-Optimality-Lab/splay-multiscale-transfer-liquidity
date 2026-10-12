# SELR streaming search manifest (frozen order, §12)

Grammar (DELETE-only): remove one DELETE; replace a DELETE key with another
T0 key (1–9); insert one DELETE (T0 key) at any gap. No KEEP/tree/key/
concat/state edits. Max distance d≤2. No third layer.
Order: distance, seed priority (selr-in, zulr-in, uesink-in, dlss-in,
dlss-ctl, mr33, concat35), parent first-seen order, op
(removal, replacement, insertion), DELETE position/gap, new key. L2 parents
(per-seed L1 first-seen canonical order, nonclosed included) never ran
(stopped at d1 OUT). Canonical equality = full word content; SHA index only.
Streaming: generate → canonical-seen register → full screen → decide →
advance; single log; stop at first OUT. Counters: raw 8, distinct 8,
replayed 8, screened 8, bank24-tested 3, recursive-tested 1, rejected 4,
banked 2 (rm2 S1; rm5 AMG+UESINK), SELR-member 1 (rm12), non-closed 3,
indeterminate 0, truncated none. Frozen OUT: selr-in d1 rm18 (remove DELETE
at original index 18), SHA c3a55f13…. No L2, no resume, no new mechanism.
