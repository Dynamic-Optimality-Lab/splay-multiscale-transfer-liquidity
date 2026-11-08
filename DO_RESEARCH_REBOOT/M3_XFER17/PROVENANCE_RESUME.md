# Inherited long-path pin repair, with completed checks reused

The first bounded audit stopped at audit.py line113, requiring every
dependency path to appear in entry_baseline.json. Its original status
remains FAILED_OR_UNKNOWN_STOP. The source and sign stages had already
PASSED and written checkpoint01_source.json/checkpoint02_sign.json.

The legacy entry directory traversal did not list the long LDR01 path.
The inherited Transfer16 dependencies.json DOES pin that SAME file at
SHA2566c8a44fb305129a21ea539b3bd566047aa4bffebf1194a17cb2b7b0642f68a6a.
This is a missing membership in the entry index, not a failed theorem,
changed dependency or inability to read the file with extended paths.

resume_audit.py validates the inherited dependency metadata against its
entry pin, verifies the LDR01 file against that existing inherited hash,
and records a supplemental dependency pin. It then performs only the
previously UNFINISHED coverage/status checks. Completed source AST and
symbolic sign checks are read from their checkpoints, never re-executed.
The failed component and both CPU exits remain immutable. No UNKNOWN
is promoted: the composed result requires both checkpoint PASS and the
continued provenance/coverage PASS.

Integrity wording must be exact: the entry baseline verifies its14181
listed prior files; inherited mathematical dependencies have additional
explicit pins, including long paths. Do not call the legacy directory
index a proved exhaustive inventory of every filesystem path. This
campaign writes only its new directory, and the dependency/interface
coverage relevant to this theorem is explicitly verified.

First child0.28125 plus controller0.21875 gives0.5 CPU seconds, charged
in full. Prior762.53125 becomes763.03125. The continuation child cap
is at most119.5, keeping the original combined120 phase ceiling and
all other caps/reserve. This is one source-audit bookkeeping repair,
not a new mathematical pivot or a repeat of completed checks.
