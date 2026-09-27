import hashlib
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
URLS = {
    "obstruction:python/inherited/mstc0002.py": "https://raw.githubusercontent.com/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-/main/python/inherited/mstc0002.py",
    "obstruction:python/inherited/splay.py": "https://raw.githubusercontent.com/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-/main/python/inherited/splay.py",
}
out = {}
for k, u in URLS.items():
    print("WP-0 STEP fetch: downloading %s" % k)
    data = urllib.request.urlopen(u, timeout=60).read()
    out[k] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    print("WP-0 STEP fetch: %s bytes=%d" % (k, len(data)))
import yaml
with open(ROOT / "v03" / "obstruction_content_hashes.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(out, f, sort_keys=False)
