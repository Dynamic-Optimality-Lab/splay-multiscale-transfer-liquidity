"""WP-6 STEP ZA-00: zero/tight path anatomy (setup->first-cash structure).

Collect near-tight histories (cumulative in [-3,0] WITH >=1 cash) from
hostile pump-biased corpus. For the FIRST cash in each: full anatomy
(A/B trees canon, accessed key, e_A/e_B/q, pre-slack, setup accesses
since segment start (last V=0/diagonal-ish point), bystander classes
(rigid/A-path/B-path/both/new/destroyed via rotated/pushed sets),
q-mass per class, A/B splay paths, ancestor relations, what accumulated
during setup, what changed at cash.
Goal: exact equality mechanism for N-FIRST (q <= setup-slack structural?).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_cashchain import to_ptr, clone, evc, splay_sets
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def canon(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return PE.canonical(r)


def main() -> int:
    # WP-6 STEP ZA-00.
    step("ZA-00", "Zero/tight path anatomy")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"za|%s|%d" % (self.s, self.c)).digest()

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

    found = 0
    for t in range(120):
        rng = DRBG(("za%d" % t).encode())
        n = rng.ch([32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-16, -8, 8, 16])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ZA-KILL", "present kill t=%d" % t)
            return 2
        # cumulative + first cash
        eb = sa = 0
        first = None
        for idx, acc in enumerate(pre):
            eA = sum(1 for z in acc["sites"] if z)
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                if eB - 3 * eA > 0 and first is None:
                    first = (idx, acc["x"], eA, eB, 3 * sa - eb)
                eb += eB
            sa += eA
        cum = eb - 3 * sa
        if first is None or cum > 0:
            continue
        # full anatomy of first cash
        idx, xx, eA, eB, slack = first
        A, B = to_ptr(T0), to_ptr(T0)
        for j in range(idx):
            a = pre[j]
            A, _ = PE.splay_trace(A, a["x"])
            if a["mode"] == "KEEP":
                B, _ = PE.splay_trace(B, a["x"])
        # A-rotated / B-pushed sets at cash + bystander classes + q-mass
        _, Arot, _ = splay_sets(clone(A), xx)
        _, _, Bpush = splay_sets(clone(B), xx)
        RA = set()
        for S in Arot:
            RA |= S
        PB = set()
        for S in Bpush:
            PB |= S
        # q-signs pre (exact stepcosts via clones)
        qpre = {}
        for y in range(1, n + 1):
            qpre[y] = evc(B, y) - 3 * evc(A, y)
        A2, _ = PE.splay_trace(A, xx)
        B2, _ = PE.splay_trace(B, xx)
        qpost = {}
        for y in range(1, n + 1):
            qpost[y] = evc(B2, y) - 3 * evc(A2, y)
        cls = {"rigid": 0, "Apath": 0, "Bpath": 0, "both": 0, "new": 0, "dest": 0}
        mass = {"rigid": 0, "Apath": 0, "Bpath": 0, "both": 0, "new": 0, "dest": 0}
        for y in range(1, n + 1):
            if y == xx:
                continue
            pre_pos = qpre[y] > 0
            post_pos = qpost[y] > 0
            inA = y in RA
            inB = y in PB
            if inA and inB:
                c = "both"
            elif inA:
                c = "Apath"
            elif inB:
                c = "Bpath"
            else:
                c = "rigid"
            if pre_pos and not post_pos:
                c = "dest"
            if not pre_pos and post_pos:
                c = "new"
            cls[c] += 1
            mass[c] += qpre[y] if pre_pos else 0
        step("ZA-t%d" % t, "cash x=%d eA=%d eB=%d q=%d slack=%d cum=%d classes=%s" %
             (xx, eA, eB, eB - 3 * eA, slack, cum, cls))
        found += 1
        if found >= 12:
            break
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "zeroanat.json").write_text(
        json.dumps({"tight_histories": found}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
