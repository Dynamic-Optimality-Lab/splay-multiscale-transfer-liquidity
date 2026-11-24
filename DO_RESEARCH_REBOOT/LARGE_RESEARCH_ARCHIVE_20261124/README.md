# Large research traces

This folder contains the complete bytes of 21 original JSON traces whose raw sizes exceed GitHub's regular file limit. The manifest records each original repository path, byte count, and SHA-256 digest. All gzip payloads were verified against the original files.

From the repository root, verify the published payloads.

```powershell
python -B DO_RESEARCH_REBOOT/LARGE_RESEARCH_ARCHIVE_20261124/restore.py --verify
```

Restore the original paths before running a replay or checking an original preservation manifest.

```powershell
python -B DO_RESEARCH_REBOOT/LARGE_RESEARCH_ARCHIVE_20261124/restore.py
```

The restore command verifies existing files and leaves their bytes intact. It writes missing traces only after checking their full size and SHA-256 digest.
