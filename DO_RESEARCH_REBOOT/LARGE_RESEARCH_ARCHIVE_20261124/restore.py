"""Verify and restore the oversized research traces with their original bytes."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import tempfile


ARCHIVE = Path(__file__).resolve().parent
RESEARCH = ARCHIVE.parent
ROOT = RESEARCH.parent


def verify_stream(stream, record, output=None):
    digest = hashlib.sha256()
    size = 0
    while chunk := stream.read(1024 * 1024):
        size += len(chunk)
        digest.update(chunk)
        if output is not None:
            output.write(chunk)
    if size != record["size"] or digest.hexdigest() != record["sha256"]:
        raise ValueError(f"Bytes do not match the manifest for {record['path']}")


def restore(record, verify_only):
    payload = (ARCHIVE / record["archive"]).resolve()
    target = (ROOT / record["path"]).resolve()
    if payload.parent != ARCHIVE or not target.is_relative_to(RESEARCH):
        raise ValueError("Archive entry is outside the research workspace")

    if verify_only:
        with gzip.open(payload, "rb") as stream:
            verify_stream(stream, record)
        return

    if target.exists():
        with target.open("rb") as stream:
            verify_stream(stream, record)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as part:
        temporary = Path(part.name)
        try:
            with gzip.open(payload, "rb") as stream:
                verify_stream(stream, record, part)
            part.close()
            os.link(temporary, target)
        finally:
            part.close()
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Check each archive against the manifest")
    options = parser.parse_args()
    records = json.loads((ARCHIVE / "manifest.json").read_text(encoding="utf-8"))
    for record in records:
        restore(record, options.verify)
    print(f"Verified {len(records)} archives" if options.verify else f"Ready: {len(records)} original traces")


if __name__ == "__main__":
    main()
