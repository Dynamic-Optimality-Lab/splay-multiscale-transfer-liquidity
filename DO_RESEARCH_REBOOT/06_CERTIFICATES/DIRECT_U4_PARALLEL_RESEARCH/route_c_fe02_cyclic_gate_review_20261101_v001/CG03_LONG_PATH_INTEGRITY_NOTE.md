# Integrity reproduction: native Windows long paths

The original integrity writer stopped before writing any
final-integrity or delivery-manifest output. Its check of
CG01 used an absolute pathname of260 characters. Windows
reported is_file=False on that ordinary pathname, while the
file existed and PowerShell listed its5940 bytes normally.
This is an integrity-tool path issue, not a source or proof
failure. The original writer and every report are preserved.

`seal_delivery_v002.py` uses Windows' native extended path
prefix for filesystem reads/enumeration and the same original
checks. Git read-only checks keep the ordinary repository
cwd. No file is renamed, overwritten, moved or deleted.

Use `seal_delivery_v002.py` for the final reproduction step
specified in CG02. This versioned note supersedes only that
integrity invocation; all mathematical statuses remain OPEN.
