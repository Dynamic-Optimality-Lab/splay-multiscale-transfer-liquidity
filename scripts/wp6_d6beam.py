"""WP-6 D6BEAM: beam assault on the isolated rate hypothesis (C171).

Target: GC-def - slack/2 > 0 (equivalently D6-deficit > 0), the single
open kernel hypothesis for DIRECT-D6 (d6_of_rate). Beam search with
multi-step setup planning (beyond myopic greedy): width W, depth L,
objective = max terminal D6-deficit over prefixes. Reuses access_stats
from wp6_d6 (exact need/eA/eB/S_A ledger, present domain).
Any D6-def > 0 re-validated via LG.check + independent recompute
(REFUTATION protocol: kills DIRECT-D6 and, since D6-def>0 => GC-def>0
when slack>=0... precisely D6-def = 2*GC-def - slack, kills GC too).
Artifact: d6beam.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_d6 import access_stats, validate
from wp6_adv import vine, balanced
from wp6_eventflow import to_ptr
from solver import legality as LG


def step(sid, msg):
    print("[WP-6][D6BEAM %s] %s" % (sid, msg), flush=True)


def beam_run(n, T0, L, W):
    A0, B0 = to_ptr(T0), to_ptr(T0)
    beam = [(0, A0, B0, 0, 0, 0, [])]  # (d6def, A,B,SA,EB,D,H)
    best = {"d6": None, "H": None}
    for _ in range(L):
        cands = []
        for _, A, B, SA, EB, D, H in beam:
            for x in range(1, n + 1):
                for mode in ("KEEP", "DELETE"):
                    r = access_stats(A, B, SA, 0, EB, D, mode, x)
                    if r is None:
                        continue
                    (A2, B2, SA2, EB2, D2, eA, eB, a, y, need,
                     d6def, gcdef, slack) = r
                    cands.append((d6def, A2, B2, SA2, EB2, D2,
                                  H + [[mode, x]]))
        if not cands:
            break
        cands.sort(key=lambda c: c[0], reverse=True)
        # diversity: top half by deficit + bottom half random far
        import hashlib
        keep = cands[:W // 2]
        rest = cands[W // 2:]
        if rest:
            h = int.from_bytes(
                hashlib.sha256(repr(len(H) if H else 0).encode()).digest()[:4],
                "big")
            keep = keep + [rest[(h + 7 * i) % len(rest)]
                           for i in range(min(W - len(keep), len(rest)))]
        beam = keep
        for d6def, A, B, SA, EB, D, H in beam:
            if best["d6"] is None or d6def > best["d6"]:
                best = {"d6": d6def, "H": list(H)}
    return best


def main() -> int:
    step("DB-00", "beam assault on isolated rate hypothesis")
    out = {"runs": [], "kills": []}
    for n in (16, 32):
        for nm, T0 in (("vine%d" % n, vine(n)),
                       ("bal%d" % n, balanced(list(range(1, n + 1))))):
            for (L, W) in ((35, 40), (50, 24)):
                try:
                    b = beam_run(n, T0, L, W)
                except Exception as ex:
                    step("DB-ERR", "%s: %r" % (nm, ex))
                    continue
                rec = {"shape": nm, "L": L, "W": W, "d6": b["d6"]}
                out["runs"].append(rec)
                step("DB-R", "%s L=%d W=%d d6=%s" % (nm, L, W, b["d6"]))
                if b["d6"] is not None and b["d6"] > 0 and b["H"]:
                    try:
                        v = validate(n, T0, b["H"])
                    except Exception as ex:
                        rec["validate"] = "invalid:%r" % (ex,)
                        continue
                    rec["validate"] = v
                    if v is not None and v > 0:
                        out["kills"].append({"shape": nm, "H": b["H"],
                                            "d6": v})
                        step("DB-KILL", "D6-DEFICIT POSITIVE %s" % nm)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "d6beam.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("DB-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
