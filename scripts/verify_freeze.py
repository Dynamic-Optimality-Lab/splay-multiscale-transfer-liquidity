"""WP-0 STEP 05 helper: build + verify prereg/freeze_manifest.sha256 (no-self-hash)."""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "prereg" / "freeze_manifest.sha256"


def entries() -> dict[str, str]:
    out = {}
    for p in sorted((ROOT / "prereg").glob("*.yaml")):
        out[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main() -> int:
    print("[WP-0][STEP 05] Building prereg freeze manifest (manifest never hashes itself)")
    ents = entries()
    if "--verify-only" in sys.argv and MAN.exists():
        try:
            want = {}
            for line in MAN.read_text(encoding="utf-8").splitlines():
                h, n = line.split("  ")
                want[n] = h
        except ValueError:
            print("[WP-0][STEP 05] Freeze manifest malformed; WP-0 blocked")
            return 2
        ok = want == ents
        print("[WP-0][STEP 05] Freeze manifest verify: %s" % ("PASS" if ok else "FAIL"))
        return 0 if ok else 2
    MAN.write_text("".join("%s  %s\n" % (h, n) for n, h in sorted(ents.items())), encoding="utf-8")
    print("[WP-0][STEP 05] Freeze manifest written: %d files" % len(ents))
    return 0


if __name__ == "__main__":
    sys.exit(main())
