"""WP-6 MICRO: micro-coupling census (C163) + tier-ledger scout.

Micro-coupling (synced-trivial branch of prefix-GC): synced accesses have
overflow <= 1 (C162 kernel); overflow 0 is free; overflow 1 must be exactly
the (0,1) splash with buffer >= 1 before. Checks per access over 150
histories (same harness/gen as pushledger):
  A. synced-disjunction: synced => eB <= 3*eA + 1; synced & eA>=1 => eB <= 3*eA
  B. ov1-exactness: overflow>=1 => (eA,eB)==(0,1) & synced & buffer_before>=1
  C. (0,1)-buffer: (eA,eB)==(0,1) => buffer_before>=1 (min reported)
  D. global prefix minimum of Phi (expect >= 0)
  F. ceil-exactness (finite mirror of C161+C162): depths present =>
     eB == (dB+1)//2 and eA == (dA+1)//2
Tier-ledger scout:
  E. heavy bursts (overflow>=2): margin = buffer_before - overflow stats,
     synced flag (expect never synced), (dA,dB,eA,eB) records of extremes.
Artifact: micro.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen, run_hist
from solver import encode as E


def step(sid, msg):
    print("[WP-6][MICRO %s] %s" % (sid, msg), flush=True)


def analyze(n, T0, H):
    _, recs = run_hist(n, T0, H)
    out = Counter()
    out["phi_min"] = None
    out["buf01_min"] = None
    out["margin_min"] = None
    out["triple_min"] = None
    out["ov_max"] = 0
    extremes = []
    SA = EB = 0
    for r in recs:
        buf = 3 * SA - EB
        eA, eB = r["eA"], r["eB"]
        ov = eB - 3 * eA
        dA, dB = r["dA"], r["dB"]
        synced = (dA is not None and dB is not None
                  and abs(dA - dB) <= 2)
        # A. synced disjunction
        if synced:
            out["syn_n"] += 1
            if not (eB <= 3 * eA + 1):
                out["syn_viol"] += 1
            if eA >= 1:
                out["syn_nontriv_n"] += 1
                if not (eB <= 3 * eA):
                    out["syn_nontriv_viol"] += 1
        # B. overflow>=1 on SYNCED accesses is exactly (0,1) with buffer>=1
        if synced and ov >= 1:
            out["ov1_n"] += 1
            if not ((eA, eB) == (0, 1) and buf >= 1):
                out["ov1_viol"] += 1
                if len(extremes) < 8:
                    extremes.append({"x": r["x"], "mode": r["mode"],
                                     "eA": eA, "eB": eB, "dA": dA, "dB": dB,
                                     "buf": buf, "synced": synced})
        # B2. unsynced overflow==1 shape (small-divergent census)
        if not synced and ov == 1:
            out["uns1_n"] += 1
        # C. (0,1) buffer
        if (eA, eB) == (0, 1):
            out["z01_n"] += 1
            if out["buf01_min"] is None or buf < out["buf01_min"]:
                out["buf01_min"] = buf
            if not (buf >= 1):
                out["z01_viol"] += 1
        # E. heavy-burst scout (tier-ledger)
        if ov >= 2:
            out["heavy_n"] += 1
            margin = buf - ov
            if out["margin_min"] is None or margin < out["margin_min"]:
                out["margin_min"] = margin
            triple = buf - 3 * eB
            if out["triple_min"] is None or triple < out["triple_min"]:
                out["triple_min"] = triple
            if synced:
                out["heavy_syn_viol"] += 1
            if ov > out["ov_max"]:
                out["ov_max"] = ov
                out["ov_max_rec"] = {"eA": eA, "eB": eB, "dA": dA,
                                     "dB": dB, "buf": buf}
            if buf <= 20:
                out["heavy_lobuf_n"] += 1
                if ov > out.get("ov_lobuf_max", 0):
                    out["ov_lobuf_max"] = ov
        # F. ceil-exactness on present keys
        if dB is not None and r["mode"] == "KEEP":
            out["ceilB_n"] += 1
            if not (eB == (dB + 1) // 2):
                out["ceilB_viol"] += 1
        if dA is not None:
            out["ceilA_n"] += 1
            if not (eA == (dA + 1) // 2):
                out["ceilA_viol"] += 1
        # advance ledger
        SA += eA
        EB += eB if r["mode"] == "KEEP" else 0
        phi = 3 * SA - EB
        if out["phi_min"] is None or phi < out["phi_min"]:
            out["phi_min"] = phi
    out["extremes"] = extremes
    return out


def main() -> int:
    step("MC-00", "micro-coupling census + tier scout")
    agg = Counter()
    agg["phi_min"] = None
    agg["buf01_min"] = None
    agg["margin_min"] = None
    agg["triple_min"] = None
    agg["ov_max"] = 0
    agg["ov_lobuf_max"] = 0
    done = 0
    for s in range(150):
        n, T0, H = gen(s, b"mc")
        try:
            res = E.precompute(n, T0, H)
            bad = E.exec_counts(res, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        done += 1
        v = analyze(n, T0, H)
        for k in ("syn_n", "syn_viol", "syn_nontriv_n", "syn_nontriv_viol",
                  "ov1_n", "ov1_viol", "uns1_n", "z01_n", "z01_viol",
                  "heavy_n", "heavy_syn_viol", "heavy_lobuf_n", "ceilB_n",
                  "ceilB_viol", "ceilA_n", "ceilA_viol"):
            agg[k] += v[k]
        for k in ("phi_min", "buf01_min", "margin_min", "triple_min"):
            if v[k] is not None and (agg[k] is None or v[k] < agg[k]):
                agg[k] = v[k]
        if v["ov_max"] > agg["ov_max"]:
            agg["ov_max"] = v["ov_max"]
            agg["ov_max_rec"] = v.get("ov_max_rec")
        if v.get("ov_lobuf_max", 0) > agg["ov_lobuf_max"]:
            agg["ov_lobuf_max"] = v.get("ov_lobuf_max", 0)
        if s % 30 == 29:
            step("MC-P", "s=%d done=%d" % (s, done))
    out = dict(agg)
    out.update({"evals": done})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "micro.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("MC-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
