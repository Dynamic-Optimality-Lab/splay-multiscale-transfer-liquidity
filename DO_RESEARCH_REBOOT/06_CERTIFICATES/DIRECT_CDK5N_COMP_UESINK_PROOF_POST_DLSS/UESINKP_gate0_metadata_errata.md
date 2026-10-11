# Gate-0 metadata errata (append-only; historical files untouched)

## Erratum A — Malformed entry checkpoint (CONFIRMED)

`UESINK_source_hashes.json` field `checkpoint` and `UESINK_terminal_status.json`
field `entry_head` record `6bf87814bbdd4d0a47dbd024c79abdaf0cef7b91`
(64 hex chars but NOT a real commit). Genuine DLSS checkpoint verified from
Git: `6bf8781c129122b4e69cd4409316c280351f16a0` (remote HEAD at DLSS-PROOF).
The UESINK-G0 commit descends from it (ancestry verified). Correction: read
`6bf8781…` wherever the typo appears. No evidence depended on the typo string.

## Erratum B — IN primitivity count (CONFIRMED)

Five Gate-0 prose spots write IN as "32 distinct (pre-closure states)":
verdict:8, IN_worksheet:17, proper_subclass:6, distance_zero.md:5,
search_manifest:7. Fresh recount: IN n=33 → 35 boundaries → 34?? NO —
33 pre-closure states P_0..P_32, ALL 33 DISTINCT, zero repeats, P_33=P_0.
Correct: 33/33 (OUT: 32/32; control: 34/34). The code always verified
`len(set)==len(word)` correctly; only prose numbers were wrong (33 belongs
to IN's n, miswritten as 32 — likely OUT-count bleed). Verdicts unaffected
(primitivity property holds either way).

## Erratum C — IN hash suffix (CONFIRMED)

Verdict:5 + proper_subclass:3 abbreviate IN as `a7c6504c…c7c76cc`. Suffix
`c7c76cc` belongs to the secondary control (`6b242e23…cc30c7c76cc`).
Authoritative IN SHA (re-gated): `a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8`.
OUT SHA unchanged: `593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9`.

## Erratum D — Distance-zero summary (CONFIRMED)

Verdict:29 says "2 members + 3 banked". Fresh reconstruction: exactly ONE
UESINK member (IN) + FOUR previously banked (exIN/exCTL DLSS, mr33 MR+DLSS,
concat35 MSINK). Correct: 1+4. (Multi-membership: mr33 carries DLSS+MR;
recorded separately, disposition unchanged.)
