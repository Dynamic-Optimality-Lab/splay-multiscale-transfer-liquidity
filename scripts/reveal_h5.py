"""H5 bind + reveal-once driver (single lawful transition to REVEALED_ONCE).

Usage:
  py scripts/reveal_h5.py bind    # CANDIDATE_SET_BOUND after K6-hash verification
  py scripts/reveal_h5.py reveal  # one-shot reveal + publish to artifacts/v04/h5_reveal/

Bind guards: firewall COMMITMENT_PUBLISHED, unlocks==0, commitment exists and
re-verifies against the secret bank, K6 survivor-set hash/count exactly match
the frozen artifacts/v04/wp5x_k6c2/specialized_survivors.json (63,
9dcdea2b...). No candidate mutation possible here (read-only check).

Reveal guards: firewall CANDIDATE_SET_BOUND, unlocks==0, no existing reveal
record. Publishes seed + bank + manifest to artifacts/v04/h5_reveal/ (public
reveal record). Never evaluates. Refuses second reveal and regen.
"""
from __future__ import annotations
import datetime
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import h5_firewall as FW
from holdout import h5_verify as V

K6_HASH = "9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748"
K6_COUNT = 63
BRANCH_REQUIRED = "wp5x-k6c2-specialized"


def _guard_branch() -> bool:
    import subprocess
    try:
        b = subprocess.check_output(["git", "branch", "--show-current"],
                                    cwd=str(ROOT), text=True).strip()
    except Exception:
        return False
    return b == BRANCH_REQUIRED


def cmd_bind() -> int:
    print("[H5] Binding frozen K6 set", flush=True)
    if not _guard_branch():
        print("[H5] Refuses: branch guard (must be %s)" % BRANCH_REQUIRED, flush=True)
        return 2
    st = FW.read_state()
    if st["state"] != "COMMITMENT_PUBLISHED":
        print("[H5] Refuses: bind legal only from COMMITMENT_PUBLISHED (state=%s)"
              % st["state"], flush=True)
        return 2
    if st["unlocks"] != 0:
        print("[H5] Refuses: unlock counter nonzero", flush=True)
        return 2
    com_p = ROOT / "artifacts" / "v04" / "h5" / "h5_commitment.json"
    if not com_p.exists():
        print("[H5] Refuses: no published H5 commitment", flush=True)
        return 2
    secret = FW._default_secret()
    if not (secret / "seed.bin").exists():
        print("[H5] Refuses: secret H5 bank absent", flush=True)
        return 2
    if not V.verify(secret, com_p):
        print("[H5] Refuses: commitment recompute failed", flush=True)
        return 2
    k6 = json.loads((ROOT / "artifacts" / "v04" / "wp5x_k6c2" /
                      "specialized_survivors.json").read_text(encoding="utf-8"))
    if k6.get("survivor_set_hash") != K6_HASH or k6.get("count") != K6_COUNT:
        print("[H5] Refuses: K6 survivor set drift (hash/count mismatch)", flush=True)
        return 2
    if sorted(k6.get("survivors", [])) != k6.get("survivors", []):
        print("[H5] Refuses: K6 survivor ordering not canonical", flush=True)
        return 2
    FW.transition("CANDIDATE_SET_BOUND",
                  "K6 63 bound hash=%s" % K6_HASH[:16])
    print("[H5] K6 set bound (63, hash=%s)" % K6_HASH[:16], flush=True)
    return 0


def cmd_reveal() -> int:
    print("[H5] Reveal-once driver", flush=True)
    if not _guard_branch():
        print("[H5] Refuses: branch guard (must be %s)" % BRANCH_REQUIRED, flush=True)
        return 2
    st = FW.read_state()
    if st["state"] != "CANDIDATE_SET_BOUND":
        print("[H5] Refuses: reveal legal only from CANDIDATE_SET_BOUND (state=%s)"
              % st["state"], flush=True)
        return 2
    if st["unlocks"] != 0:
        print("[H5] Refuses: unlock counter nonzero", flush=True)
        return 2
    com_p = ROOT / "artifacts" / "v04" / "h5" / "h5_commitment.json"
    if not com_p.exists():
        print("[H5] Refuses: no published H5 commitment", flush=True)
        return 2
    secret = FW._default_secret()
    if not (secret / "seed.bin").exists():
        print("[H5] Refuses: secret H5 bank absent", flush=True)
        return 2
    if not V.verify(secret, com_p):
        print("[H5] Refuses: commitment recompute failed at reveal", flush=True)
        return 2
    k6 = json.loads((ROOT / "artifacts" / "v04" / "wp5x_k6c2" /
                      "specialized_survivors.json").read_text(encoding="utf-8"))
    if k6.get("survivor_set_hash") != K6_HASH or k6.get("count") != K6_COUNT:
        print("[H5] Refuses: K6 drift at reveal", flush=True)
        return 2
    dest = ROOT / "artifacts" / "v04" / "h5_reveal"
    if dest.exists():
        print("[H5] Refuses: H5 reveal record already published", flush=True)
        return 2
    (dest / "bank").mkdir(parents=True)
    shutil.copy2(secret / "seed.bin", dest / "seed.bin")
    for sh in sorted((secret / "bank").glob("*.json.zst")):
        shutil.copy2(sh, dest / "bank" / sh.name)
    shutil.copy2(secret / "manifest.json", dest / "manifest.json")
    FW.transition("REVEALED_ONCE", "one-shot H5 reveal after commitment re-verify")
    (dest / "reveal.json").write_text(json.dumps({
        "bank": "H5", "bank_id": "H5-R1",
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "unlocks": 1, "state": "REVEALED_ONCE",
        "k6_survivor_set_hash": K6_HASH, "k6_count": K6_COUNT}, indent=2, sort_keys=True),
        encoding="utf-8")
    print("[H5] Revealed once (unlocks=1)", flush=True)
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    sys.exit({"bind": cmd_bind, "reveal": cmd_reveal}[cmd]())
