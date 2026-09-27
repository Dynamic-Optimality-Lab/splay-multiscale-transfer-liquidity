"""WP-0 STEP 01: verify dual-parent pins, content hashes, ledger counts, toolchain."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ARCH_CLONE = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\arch-parent")

def check(name, cond, detail=""):
    print("[WP-0][STEP 01] %s: %s %s" % (name, "OK" if cond else "FAIL", detail))
    return cond

def main() -> int:
    print("[WP-0][STEP 01] Verifying parent pins and content hashes")
    root = Path(__file__).resolve().parents[2]
    import yaml
    pc = yaml.safe_load((root / "prereg" / "parent_contract.yaml").read_text(encoding="utf-8"))
    ok = True
    # Full-SHA reachability in the local clone (no short hashes).
    for role, sha in [("navigation", pc["arch"]["navigation"]), ("closure", pc["arch"]["closure"]), ("seal", pc["arch"]["seal"])]:
        r = subprocess.run(["git", "-C", str(ARCH_CLONE), "cat-file", "-t", sha], capture_output=True, text=True)
        ok &= check("arch-%s-reachable" % role, r.stdout.strip() == "commit", sha[:7])
    head = subprocess.run(["git", "-C", str(ARCH_CLONE), "log", "--format=%H", "-1"], capture_output=True, text=True).stdout.strip()
    ok &= check("arch-head-is-navigation", head == pc["arch"]["navigation"], head[:7])
    # Content hashes recomputed from the imported tree (authoritative local bytes).
    hist = root / "v03" / "history"
    for rel, want in pc["arch"]["content_sha256"].items():
        got = hashlib.sha256((hist / rel).read_bytes()).hexdigest()
        ok &= check("content-%s" % rel, got == want, got[:12])
    # Obstruction content hashes recomputed by fresh download.
    urls = {"python/inherited/mstc0002.py": "https://raw.githubusercontent.com/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-/main/python/inherited/mstc0002.py",
            "python/inherited/splay.py": "https://raw.githubusercontent.com/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-/main/python/inherited/splay.py"}
    for rel, url in urls.items():
        data = urllib.request.urlopen(url, timeout=60).read()
        got = hashlib.sha256(data).hexdigest()
        ok &= check("obstruction-%s" % rel, got == pc["obstruction"]["content_sha256"][rel], got[:12])
    # Obstruction evidence commit reachable via API with witness marker in message.
    api = "https://api.github.com/repos/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-/commits/%s" % pc["obstruction"]["evidence_commit"]
    msg = json.load(urllib.request.urlopen(api, timeout=60))["commit"]["message"]
    ok &= check("obstruction-evidence-commit", "n=28" in msg and "triple replay" in msg, msg[:60])
    # Ledger counts: arch theorem status has exactly 26 rows (9/5/3/3/6 derivable at WP-1; here row-count sanity via gate matrix later).
    ok &= check("ledger-counts-recorded", pc["theorem_ledger_counts"]["arch"]["REVIEWED"] == 9, "9/5/3/3/6")
    # Toolchain string exact.
    ok &= check("toolchain", pc["toolchain_string"] == "leanprover/lean4:v4.21.0", pc["toolchain_string"])
    print("[WP-0][STEP 01] verify_parent result: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 2

if __name__ == "__main__":
    sys.exit(main())
