# Stage11G preservation audit: correction and exact evidence limits

Earlier reports described125 files as the complete Stage11G
inventory. That inventory claim was wrong. Native Windows
long-path enumeration finds528 files. Ordinary absolute-path
is_file checks silently excluded403 paths at/above the platform
path limit. Existing research reports are preserved; this
append-only correction supersedes their complete-count claim.

No Stage11G file was written, removed, renamed or modified
by this work. Do not delete the existing untracked/cache files.

## What has now been checked

- All125 original entry-pinned files retain their exact raw
  SHA256 hashes.
- The full inventory has528 files. All510 files tracked in the
  frozen HEAD are present. Of them416 match HEAD blob bytes
  exactly and94 differ only by CRLF/LF line endings. None has
  a non-line-ending content difference from HEAD.
- There are18 untracked files, including existing caches and
  research notes. Three had entry hashes and are unchanged.
  Fifteen had no entry hash. Their current raw hashes are now
  recorded; this is a NEW baseline, not a retrospective raw
  before/after proof for those fifteen files.
- The complete528-file current baseline is rechecked at the
  final seal. It does not manufacture an entry baseline for
  previously invisible files. Newly visible tracked files
  have independent frozen-HEAD content checks, with the exact
  raw/EOL distinction recorded per file.

`full_stage_inventory_review.json` contains every current raw
hash, every tracked HEAD object/hash, per-file comparison and
the exact untracked baseline lists. `audit_full_stage.py`
reads Git blobs via cat-file only; no Git or Stage writes occur.

## Integrity writer reproduction

The preserved original sealer stopped at the260-character
CG01 path. The preserved v002 sealer used native long paths
and correctly stopped when the larger true Stage inventory
did not equal the old125-file subset. Neither produced final
integrity/manifest outputs or changed source files.

Use `audit_full_stage.py`, then `seal_delivery_v003.py` for
the corrected final integrity steps. V003 preserves all old
entry pins, verifies the complete current528-file baseline,
and reports the missing historical baseline explicitly. It
does not label the old125-file subset a complete inventory.

FE01, PG02 and the prior research manifests remain unchanged.
The Stage inventory correction does not alter the mathematical
gate review: full FE02 remains OPEN and no new proof campaign
passed its gate.
