"""WP-6 ASYM: asymmetric ancestor-pair net measurement (C180).

Phi(A,B) = #{(u,v): u ancestor_B(v) AND NOT u ancestor_A(v)}
(B-only ordered ancestor pairs; zero on diagonal; nonnegative).
Euler-tour ancestor tests (O(1) per pair after O(n) tours).
Measures per SPLAY (A-phase incl. DELETEs, B-phase on KEEPs):
  net Delta_Phi (signed), vs cost (depth+1) and StepEvs.
Questions (all §17-targeted, bounded):
  Q1 B-splay of x with x=root(A): net <= -lambda*dB + O(1)? (RELEASE)
  Q2 A-splay: net <= alpha*cost_A? (CREATE, per access AND per StepEv)
  Q3 worst-case nets vs n (bounded or growing? which shapes/keys?)
  Q4 sign distribution (systematic destroy/create or mixed?)
A net bounded above by O(cost) on A-moves + net <= -Omega(dB) on
rooted B-bursts would BE the bridge (compose to PA-LOCAL-C).
Unbounded both-ways nets = corpse with witness.
Artifact: asym.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import vine, balanced, comb, depths_of
from solver import encode as E


def step(sid, msg):
    print("[WP-6][ASYM %s] %s" % (sid, msg), flush=True)


def euler(T, n):
    """tin/tout arrays by iterative DFS."""
    tin = {}
    tout = {}
    t = [0]
    stack = [(T, False)]
    while stack:
        nd, done = stack.pop()
        if nd is None:
            continue
        if not done:
            tin[nd["k"]] = t[0]
            t[0] += 1
            stack.append((nd, True))
            stack.append((nd["r"], False))
            stack.append((nd["l"], False))
        else:
            tout[nd["k"]] = t[0]
            t[0] += 1
    return tin, tout


def asym_count(A, B, keys, tinA, toutA, tinB, toutB):
    c = 0
    for u in keys:
        iu = tinB.get(u)
        if iu is None:
            continue
        ou = toutB.get(u)
        iau = tinA.get(u)
        oau = toutA.get(u)
        for v in keys:
            if u == v:
                continue
            iv = tinB.get(v)
            if iv is None:
                continue
            if iu <= iv and toutB.get(v, -1) <= ou:
                # u ancestor_B v; check NOT ancestor_A
                ivv = tinA.get(v)
                if ivv is None:
                    continue
                if not (iau <= ivv and toutA.get(v, -1) <= oau):
                    c += 1
    return c


def main() -> int:
    step("AS-00", "asymmetric ancestor-pair net measurement")
    out = {"by_n": {}}
    import random
    for n in (32, 128, 512):
        rec = Counter()
        rec["b_net_min"] = 0
        rec["b_net_max"] = 0
        rec["a_net_min"] = 0
        rec["a_net_max"] = 0
        rec["b_rel_worst"] = 0.0  # net/dB (want <= -lambda)
        rec["a_rel_worst"] = 0.0  # net/cost_A (want <= alpha)
        done = 0
        for s in range(8):
            r = s % 4
            if r == 0:
                T0 = vine(n)
            elif r == 1:
                T0 = balanced(list(range(1, n + 1)))
            elif r == 2:
                T0 = comb(n)
            else:
                ks = list(range(1, n + 1))
                random.Random(9000 + s).shuffle(ks)
                t = None
                for k in ks:
                    # bst insert tuple form
                    def ins(t, k):
                        if t is None:
                            return [k, None, None]
                        if k < t[0]:
                            t[1] = ins(t[1], k)
                        elif k > t[0]:
                            t[2] = ins(t[2], k)
                        return t
                    t = ins(t, k)
                T0 = t
            _, _, H = gen(9500 + s, b"as")
            H = [st for st in H if st[1] <= n]
            if not H:
                continue
            try:
                pre = E.precompute(n, T0, H)
                bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
            except Exception:
                continue
            if bad:
                continue
            done += 1
            A, B = to_ptr(T0), to_ptr(T0)
            keys = list(range(1, n + 1))
            for acc in pre:
                x, mode = acc["x"], acc["mode"]
                tinA, toutA = euler(A, n)
                tinB, toutB = euler(B, n)
                ph0 = asym_count(A, B, keys, tinA, toutA, tinB, toutB)
                da = depths_of(A).get(x, 0)
                A, invs = splay_A(A, x)
                eA = len(invs)
                tinA2, toutA2 = euler(A, n)
                ph1 = asym_count(A, B, keys, tinA2, toutA2, tinB, toutB)
                dA = (ph1 - ph0) - 0  # Delta_A Phi
                if dA < rec["a_net_min"]:
                    rec["a_net_min"] = dA
                    rec["a_min_rec"] = {"eA": eA, "da": da}
                if dA > rec["a_net_max"]:
                    rec["a_net_max"] = dA
                rr = dA / (da + 1) if (da + 1) > 0 else 0
                if rr > rec["a_rel_worst"]:
                    rec["a_rel_worst"] = rr
                if mode == "KEEP":
                    # B-release: only meaningful if x at A-root post-A-splay
                    db = depths_of(B).get(x, 0)
                    B, pushes = splay_B_push(B, x)
                    eB = len(pushes)
                    tinB2, toutB2 = euler(B, n)
                    ph2 = asym_count(A, B, keys, tinA2, toutA2, tinB2,
                                     toutB2)
                    dB = ph2 - ph1
                    if dB < rec["b_net_min"]:
                        rec["b_net_min"] = dB
                    if dB > rec["b_net_max"]:
                        rec["b_net_max"] = dB
                        rec["b_max_rec"] = {"eB": eB, "db": db}
                    if db > 0:
                        rel = -dB / db  # want >= lambda (destroys fraction)
                        if rel < rec.get("b_rel_best", 10 ** 9):
                            rec["b_rel_best"] = rel
        rec["evals"] = done
        out["by_n"][str(n)] = dict(rec)
        step("AS-P", "n=%d done=%d A[net %s..%s rel %s] B[net %s..%s rel %s]" % (
            n, done, rec["a_net_min"], rec["a_net_max"],
            round(rec["a_rel_worst"], 2), rec["b_net_min"],
            rec["b_net_max"], round(rec.get("b_rel_best", 0), 3)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "asym.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("AS-01", "done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
