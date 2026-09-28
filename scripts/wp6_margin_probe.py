"""WP-6 STEP: margin-zero instrumentation for P_all|6|2|FLAT(2).

Greedy negation-driven search minimizing per-KEEP margin, preserving every
reached margin-0 state with full structural features (A/B depths, path
overlap, rotations since previous KEEP, accumulated S_A/need, pools, StepEv
class counts, displacement). Discovery only: output feeds invariant
conjecture, never a proof premise.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from solver import predicates as CP
from liquidity import multiplicity as MU

P, K, C, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "margin_probe"


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


class DRBG:
    def __init__(self, stream: bytes):
        self.seed, self.stream, self.ctr = b"wp6-margin-probe", stream, 0

    def _block(self) -> bytes:
        self.ctr += 1
        return hashlib.sha256(self.seed + b"|" + self.stream + b"|"
                              + self.ctr.to_bytes(8, "big")).digest()

    def below(self, n: int) -> int:
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self._block(), "big")
            if v < bound:
                return v % n

    def irange(self, lo: int, hi: int) -> int:
        return lo + self.below(hi - lo + 1)

    def choice(self, seq):
        return seq[self.below(len(seq))]


def features(n, T0, H):
    """Per-KEEP structural features + cumulative S_A/need + pools."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, P, K, C, RHO)
    out = []
    cum_need, cum_SA = 0, 0
    for acc, kp in zip([a for a in pre if a["mode"] == "KEEP"],
                       res["keeps"]):
        evs = acc["Aev"] + acc["Bev"]
        cls = [MU.normalize(c) for (c, _, _) in evs]
        sited = sum(1 for s in acc["sites"] if s)
        cum_SA += sited
        # B-events count from pre (Bev list length)
        cum_need += kp["need"]
        # path overlap: shared interval mass between A path span and B span
        def span(evs):
            lo = min([l for (_, l, _) in evs], default=None)
            hi = max([h for (_, _, h) in evs], default=None)
            return (lo, hi)
        a_span, b_span = span(acc["Aev"]), span(acc["Bev"])
        out.append({"x": acc["x"], "a": acc["a"], "y": acc["y"],
                    "need": kp["need"], "paid": kp["paid"], "margin": kp["margin"],
                    "A_events": len(acc["Aev"]), "B_events": len(acc["Bev"]),
                    "sited_A": sited, "A_classes": sorted(set(
                        MU.normalize(c) for (c, _, _) in acc["Aev"])),
                    "B_classes": sorted(set(
                        MU.normalize(c) for (c, _, _) in acc["Bev"])),
                    "A_span": a_span, "B_span": b_span,
                    "cum_SA": cum_SA, "cum_need": cum_need,
                    "slack6": 6 * cum_SA - cum_need,
                    "y_minus_2a": acc["y"] - 2 * acc["a"]})
    return out, res["violations"]


def main() -> int:
    # WP-6 STEP MZ-00: margin-zero hunt + feature extraction.
    step("MZ-00", "Hunting margin-0 states for P_all|6|2|FLAT(2)")
    zeros = []
    for t in range(3000):
        rng = DRBG(("mz|%d" % t).encode())
        n = rng.choice([28, 64, 128, 192, 384])
        T0 = vine_right(n)
        L = rng.irange(2, 10)
        x = rng.irange(1, n)
        H = []
        for _ in range(L):
            H.append([rng.choice(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.choice([-16, -8, -4, -1, 1, 4, 8, 16])))
        feats, viol = features(n, T0, H)
        if viol:
            step("MZ-KILL", "unexpected kill at t=%d (refutes MSTL-14!)" % t)
            (NS / "kill.json").parent.mkdir(parents=True, exist_ok=True)
            (NS / "kill.json").write_text(json.dumps(
                {"n": n, "T0": T0, "H": H}, indent=2, sort_keys=True), encoding="utf-8")
            return 2
        for f in feats:
            if f["margin"] == 0 and f["need"] > 0:
                zeros.append({"t": t, "n": n, "H": H, "feat": f})
    step("MZ-01", "margin-0 positive-need states: %d/3000 histories" % len(zeros))
    (NS).mkdir(parents=True, exist_ok=True)
    (NS / "margin_zero_states.json").write_text(json.dumps(
        zeros[:400], indent=2, sort_keys=True), encoding="utf-8")
    # WP-6 STEP MZ-02: structural summary at margin zero.
    step("MZ-02", "Summarizing margin-0 structure")
    from collections import Counter
    summ = {"count": len(zeros),
            "need_hist": Counter(f["feat"]["need"] for f in zeros),
            "a_hist": Counter(f["feat"]["a"] for f in zeros),
            "y_hist": Counter(f["feat"]["y"] for f in zeros),
            "Aev_hist": Counter(f["feat"]["A_events"] for f in zeros),
            "Bev_hist": Counter(f["feat"]["B_events"] for f in zeros),
            "slack6_min": min((f["feat"]["slack6"] for f in zeros), default=None),
            "slack6_hist": Counter(f["feat"]["slack6"] // 50 * 50 for f in zeros)}
    (NS / "margin_zero_summary.json").write_text(json.dumps(summ, indent=2, sort_keys=True,
                                                             default=str), encoding="utf-8")
    print(json.dumps({k: (dict(v) if hasattr(v, "items") else v)
                      for k, v in summ.items()}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
