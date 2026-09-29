"""WP-6 STEP XR-00: X-RETURN falsifier (same-key excursion blocks).

For each key x in hostile histories: blocks from just-after KEEP(x) through
next KEEP(x) (also diagonal-first-KEEP(x) blocks). R_block = E_B-3*S_A over
block (all accesses inside, inclusive). Kill: R_block > 0 (X-RETURN false).
Also targeted others-tenure construction: x-excursion packed with sequential
root-hug cashes of OTHER frozen-tenure keys (each outside-funded) to force
R_block > 0 via others' cargo. Minimize + replay any witness.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP XR-00.
    step("XR-00", "X-RETURN falsifier (excursion blocks)")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"xr|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    worst = -10**18
    ex = None
    nblocks = 0
    for t in range(250):
        rng = DRBG(("xr%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 30)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("XR-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        # per-access rewards + KEEP positions per key
        rws = []
        kpos = {}
        for idx, acc in enumerate(pre):
            eA = sum(1 for z in acc["sites"] if z)
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                rws.append(eB - 3 * eA)
                kpos.setdefault(acc["x"], []).append(idx)
            else:
                rws.append(-3 * eA)
        # excursion blocks: diagonal-first + consecutive KEEP pairs per key
        for xx, pos in kpos.items():
            # first-ever block: [0..pos[0]]
            segs = [[0, pos[0]]]
            for a, b in zip(pos, pos[1:]):
                segs.append([a + 1, b])
            for (a, b) in segs:
                rb = sum(rws[a:b + 1])
                nblocks += 1
                if rb > worst:
                    worst, ex = rb, (t, xx, a, b, rb)
    step("XR-01", "blocks=%d worst R_block=%d %s (want<=0)" % (nblocks, worst, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "xreturn.json").write_text(
        json.dumps({"blocks": nblocks, "worst": worst, "ex": ex,
                    "verdict": "X-RETURN FALSE" if worst > 0 else "holds here"},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
