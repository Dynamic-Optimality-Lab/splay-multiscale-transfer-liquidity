# Concurrent archive commit and final seal

After all mathematical audits passed, the first metadata publication
attempt found that HEAD had advanced from fea2a25b05e97f726b6e1891cebb12c4cfca821a
to8c378d49283b3738b18e7175886772a98025e4e9. This campaign performed only
read-only Git commands. The external commit is named
"Archive DIRECT-U4 campaign and Route C proof certificates".

The exact diff has809 ADDITIONS, all below
DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/.
Of these,750 files were in this campaign's old entry pin list; every
one was rehashed and matched its original bytes. The other59 are new
external archive files. No M3 mathematical dependency changed. The
tracked worktree remains clean. concurrent_archive_integrity.json records
the complete targeted check; final_immutable_integrity.json retains the
earlier complete14704-file check. No mathematical check was replayed.

This supersedes statements in the first RESULT.md and FINAL_PROOF_AUDIT.md
that HEAD remained identical at publication. Source bytes and proof
premises remain unchanged; the current HEAD is recorded honestly in the
final manifest. R1–R4 semantics/caps and this campaign's read-only Git
discipline are preserved. The first finalizer stopped on its old-HEAD
assertion and emitted no final manifest. Its partial metadata artifacts
are retained; RESULT_v2.md and the final manifest are the sealed result.

The first targeted metadata script used the wrong directory prefix and
stopped before checking files. Version2 uses the observed exact path
above. Both scripts remain. This was metadata only, with no solver call,
proof modification or new resource allowance.
