"""PIVOT-25R-X §1: freeze the 41,036-row active system.

Reload every row from its witness via the canonical engine, verify M/b
exactly, gcd-normalize, dedupe identical rows (retaining all provenance).
Saves dual_mine/joint_frozen7.json. No new cuts.
"""
from __future__ import annotations
import sys
import math
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_jointlp import edge_row
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[JFR %s] %s" % (sid, msg), flush=True)


def main():
    SH = {7: O.shapes_of(list(range(1, 8))),
          8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    st = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     "joint_texact7.json").read_text())
    rows = st["rows"]
    step("L", "loaded %d rows" % len(rows))
    normed = 0
    buckets = defaultdict(list)
    bad = 0
    for i, r in enumerate(rows):
        w = r["wit"]
        if "A" in w and "B" in w:
            A, B, n = w["A"], w["B"], w["n"]
        else:
            n = w["n"]
            A, B = SH[n][w["ia"]], SH[n][w["ib"]]
        x, mo = w["x"], w["mo"]
        h, b = edge_row(A, B, x, mo, n)
        # Canonical form: strip zero-valued cells (Counter keeps them for
        # unchanged keys; scans skip them; both are the same constraint).
        M = {str(k): v for k, v in h.items() if v != 0}
        if M != {k: v for k, v in r["M"].items() if v != 0} or \
                b != r["b"]:
            bad += 1
            if bad <= 3:
                step("MM", "row %d (%s) REAL mismatch" % (i, r["tag"]))
            continue
        vals = [abs(v) for v in h.values()] + [abs(b)]
        g = 0
        for v in vals:
            g = math.gcd(g, v)
        if g > 1:
            normed += 1
            M = {k: v // g for k, v in M.items()}
            b = b // g
        buckets[(frozenset(M.items()), b)].append(r["tag"])
        if (i + 1) % 8000 == 0:
            step("G", "%d/%d mismatch=%d" % (i + 1, len(rows), bad))
    step("S", "verified=%d mismatch=%d normalized=%d distinct=%d" %
         (len(rows) - bad, bad, normed, len(buckets)))
    frozen = [{"M": dict(kv[0]), "b": kv[1], "wits": v}
              for kv, v in buckets.items()]
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "joint_frozen7.json").write_text(
        json.dumps({"rows": frozen, "n_rows": len(rows),
                    "n_distinct": len(frozen), "mismatch": bad,
                    "normalized": normed}, indent=1, default=str),
        encoding="utf-8")
    step("S", "saved joint_frozen7.json")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
