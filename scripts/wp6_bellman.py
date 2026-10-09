"""WP-6 BELLMAN (v2 fast): all-key H1 barrier + BD1/BK1 falsifier (C181).

Same mathematics as v1, but H1 via exact depth formulas instead of
replayed splays per key:
  H1(A,B) = max_x max(ceil(dB/2) - 3*ceil(dA/2), 0)   [present keys]
justified by micro F-check (ceil-exactness 0 violations / 16776) and
re-validated here by spot-checks (formula-H1 vs replay-H1 must agree
exactly; mismatches recorded, abort on any).
Post-states D_x/K_x still replayed exactly (one splay each); H1 on those
states via formula. Per (state,key): O(n) instead of O(n^3).
Residuals (positive = BARRIER FAILURE):
  residual_DELETE(x) = H1(D_x) - H1 - 3*a_x
  residual_KEEP(x)   = b_x + H1(K_x) - H1 - 3*a_x
  with a_x = ceil(dA/2), b_x = ceil(dB/2) (present).
Modes: walk (history corpora, all keys) + beam-max-residual (pair-states)
+ exhaustive small-n (all BST pairs). Tracks min(Phi-H1).
Artifact: bellman/h1_attack.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import vine, balanced, depths_of
from solver import encode as E


def step(sid, msg):
    line = "[WP-6][BELLMAN %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bellman"
        bd.mkdir(parents=True, exist_ok=True)
        with open(bd / "progress.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def H1f(dA, dB, keys):
    best = 0
    arg = None
    for x in keys:
        da = dA.get(x)
        db = dB.get(x)
        if da is None or db is None:
            continue
        v = (db + 1) // 2 - 3 * ((da + 1) // 2)
        if v > best:
            best = v
            arg = x
    return best, arg


def H1replay(A, B, keys):
    best = 0
    for x in keys:
        A2 = copy.deepcopy(A)
        A2, invs = splay_A(A2, x)
        B2 = copy.deepcopy(B)
        B2, pushes = splay_B_push(B2, x)
        v = len(pushes) - 3 * len(invs)
        if v > best:
            best = v
    return best


def residuals(A, B, keys, spot=None):
    dA = depths_of(A)
    dB = depths_of(B)
    h, _ = H1f(dA, dB, keys)
    if spot is not None and spot[0] % spot[1] == 0:
        hr = H1replay(A, B, keys)
        if hr != h:
            return {"mismatch": (hr, h)}
    out = {"H1": h, "rd_max": None, "rk_max": None, "rd_arg": None,
           "rk_arg": None, "rk_info": None}
    for x in keys:
        da = dA.get(x, 0)
        db = dB.get(x, 0)
        a = (da + 1) // 2
        b = (db + 1) // 2
        A2 = copy.deepcopy(A)
        A2, _ = splay_A(A2, x)
        hd, _ = H1f(depths_of(A2), dB, keys)
        rd = hd - h - 3 * a
        if out["rd_max"] is None or rd > out["rd_max"]:
            out["rd_max"] = rd
            out["rd_arg"] = x
        B2 = copy.deepcopy(B)
        B2, _ = splay_B_push(B2, x)
        hk, _ = H1f(depths_of(A2), depths_of(B2), keys)
        rk = b + hk - h - 3 * a
        if out["rk_max"] is None or rk > out["rk_max"]:
            out["rk_max"] = rk
            out["rk_arg"] = x
            out["rk_info"] = {"a": a, "b": b, "h": h, "hk": hk,
                              "da": da, "db": db}
    return out


def walk_histories(nH=60):
    agg = Counter()
    agg["rd_max"] = None
    agg["rk_max"] = None
    agg["min_phih1"] = None
    agg["mismatch"] = 0
    for s in range(nH):
        n, T0, H = gen(s, b"bl")
        if n > 64:
            continue
        try:
            pre = E.precompute(n, T0, H)
            bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        A, B = to_ptr(T0), to_ptr(T0)
        keys = sorted(depths_of(A).keys())
        SA = EB = 0
        for i, acc in enumerate(pre):
            x, mode = acc["x"], acc["mode"]
            r = residuals(A, B, keys, spot=(i, 25))
            if "mismatch" in r:
                agg["mismatch"] += 1
                step("BL-MM", "H1 formula mismatch %s" % (r["mismatch"],))
                return agg
            if agg["rd_max"] is None or r["rd_max"] > agg["rd_max"]:
                agg["rd_max"] = r["rd_max"]
                agg["rd_wit"] = {"s": s, "x": r["rd_arg"]}
            if agg["rk_max"] is None or r["rk_max"] > agg["rk_max"]:
                agg["rk_max"] = r["rk_max"]
                agg["rk_wit"] = {"s": s, "x": r["rk_arg"],
                                 "info": r["rk_info"]}
            phi = 3 * SA - EB
            mh = phi - r["H1"]
            if agg["min_phih1"] is None or mh < agg["min_phih1"]:
                agg["min_phih1"] = mh
            A, invs = splay_A(A, x)
            eA = len(invs)
            eB = 0
            if mode == "KEEP":
                B, pushes = splay_B_push(B, x)
                eB = len(pushes)
            SA += eA
            EB += eB if mode == "KEEP" else 0
        if s % 10 == 9:
            step("BL-W", "s=%d rd=%s rk=%s mh=%s mm=%s" % (
                s, agg["rd_max"], agg["rk_max"], agg["min_phih1"],
                agg["mismatch"]))
    return agg


def beam_max(T0, L, W):
    A0, B0 = to_ptr(T0), to_ptr(T0)
    keys = sorted(depths_of(A0).keys())
    beam = [(0, A0, B0, [])]
    best = {"v": None, "H": None, "which": None}
    for _ in range(L):
        cands = []
        for _, A, B, H in beam:
            dA = depths_of(A)
            dB = depths_of(B)
            h, _ = H1f(dA, dB, keys)
            for x in keys:
                da = dA.get(x, 0)
                a = (da + 1) // 2
                A2 = copy.deepcopy(A)
                A2, _ = splay_A(A2, x)
                hd, _ = H1f(depths_of(A2), dB, keys)
                cands.append((hd - h - 3 * a, A2, copy.deepcopy(B),
                              H + [["DELETE", x]], "rd"))
                B2 = copy.deepcopy(B)
                B2, _ = splay_B_push(B2, x)
                db = dB.get(x, 0)
                b = (db + 1) // 2
                hk, _ = H1f(depths_of(A2), depths_of(B2), keys)
                cands.append((b + hk - h - 3 * a, A2, B2,
                              H + [["KEEP", x]], "rk"))
        if not cands:
            break
        cands.sort(key=lambda c: c[0], reverse=True)
        beam = [(c[0], c[1], c[2], c[3]) for c in cands[:W]]
        for v, A, B, H in beam:
            if best["v"] is None or v > best["v"]:
                h, _ = H1f(depths_of(A), depths_of(B), keys)
                best = {"v": v, "H": list(H), "H1": h}
                if v is not None and v > 0:
                    # which mode was it? recover from last op
                    best["which"] = H[-1][0].lower() if H else None
                    return best, True
    return best, False


def exhaustive(n):
    def shapes(ks):
        if not ks:
            return [None]
        out = []
        for i, k in enumerate(ks):
            for l in shapes(ks[:i]):
                for r in shapes(ks[i + 1:]):
                    out.append([k, l, r])
        return out

    best = {"rd": None, "rk": None}
    keys = list(range(1, n + 1))
    for A0 in shapes(keys):
        for B0 in shapes(keys):
            A, B = to_ptr(A0), to_ptr(B0)
            r = residuals(A, B, keys)
            if "mismatch" in r:
                best["mismatch"] = True
                return best
            if best["rd"] is None or r["rd_max"] > best["rd"]:
                best["rd"] = r["rd_max"]
                best["rd_wit"] = {"A": A0, "B": B0, "x": r["rd_arg"]}
            if best["rk"] is None or r["rk_max"] > best["rk"]:
                best["rk"] = r["rk_max"]
                best["rk_wit"] = {"A": A0, "B": B0, "x": r["rk_arg"],
                                  "info": r["rk_info"]}
    return best


def main() -> int:
    step("BL-00", "H1 barrier + BD1/BK1 falsification (fast v2)")
    out = {}
    w = walk_histories(60)
    out["walk"] = dict(w)
    step("BL-01", "walk: %s" % json.dumps(dict(w), sort_keys=True,
                                          default=str))
    for nm, T0, L, W in (("vine32", vine(32), 30, 24),
                         ("bal32", balanced(list(range(1, 33))), 30, 24),
                         ("vine64", vine(64), 20, 16)):
        b, kill = beam_max(T0, L, W)
        out["beam_%s" % nm] = {"v": b["v"], "H1": b.get("H1"),
                               "which": b.get("which"), "kill": kill}
        step("BL-02", "beam %s: v=%s which=%s kill=%s" % (
            nm, b["v"], b.get("which"), kill))
    for n in (3, 4, 5):
        e = exhaustive(n)
        out["exhaustive_n%d" % n] = e
        step("BL-03", "exhaustive n=%d rd=%s rk=%s" % (n, e.get("rd"),
                                                       e.get("rk")))
    bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bellman"
    bd.mkdir(parents=True, exist_ok=True)
    (bd / "h1_attack.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    step("BL-04", "done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
