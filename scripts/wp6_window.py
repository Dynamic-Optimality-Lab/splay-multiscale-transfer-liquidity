"""WP-6 WINDOW: diverged-burst window attribution (C164, mission §5).

For each heavy KEEP burst (overflow>=2) on key x, walk back to x's last
B-rooting r (last KEEP on x; genesis if none) and attribute the window
net Phi(r)+sum(3eA-eB) by funder class:
  deep-supplying: B-push deepening x (delta>0) with eA>=1
  deep-free:      B-push deepening x with eA==0 (supply-free deepening)
  nondeep:       B-push with delta<=0 (incl. up-moves)
  delete:        DELETE accesses (B untouched, banks eA)
  rootbuf:       Phi(r) carried from the rooting point
Checks: telescoping dB(t) == dB0 + sum(delta) (delta accounting valid);
window inequality Phi(r)+sum(net) >= overflow (== the diverged step).
Anatomy dumps for min-margin and max-eB bursts (incl. (0,127)-shape).
Artifact: window.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push, root_key
from wp6_pushledger import gen
from solver import encode as E


def step(sid, msg):
    print("[WP-6][WINDOW %s] %s" % (sid, msg), flush=True)


def depths_of(T):
    dd = {}
    stack = [(T, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        dd[nd["k"]] = d
        stack.append((nd["l"], d + 1))
        stack.append((nd["r"], d + 1))
    return dd


def run(n, T0, H):
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    T0dB = depths_of(B)
    recs = []
    SA = EB = 0
    for idx, acc in enumerate(pre):
        x, mode = acc["x"], acc["mode"]
        da = depths_of(A).get(x)
        dBb = depths_of(B).get(x)
        A, invs = splay_A(A, x)
        eA = len(invs)
        if mode == "KEEP":
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
        else:
            eB = 0
        dBa = depths_of(B).get(x)
        buf_pre = 3 * SA - EB
        SA += eA
        EB += eB if mode == "KEEP" else 0
        recs.append({"x": x, "mode": mode, "eA": eA, "eB": eB,
                     "dA": da, "dBb": dBb, "dBa": dBa, "buf_pre": buf_pre,
                     "phi_post": 3 * SA - EB})
    return pre, recs, T0dB


def main() -> int:
    step("WN-00", "diverged-burst window attribution")
    # NOTE: analyze() needs per-access B-depths before/after each push for
    # delta; run() records dBb/dBa per access. Deltas per window push are
    # derived below in a second pass.
    agg = Counter()
    agg["win_min"] = None
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
        # second pass: attach per-access delta of each key is per-burst;
        # simpler: recompute depths per access here via run() records:
        # delta for window push u (on key z) re x = dBa_x(u) - dBb_x(u)
        # but run() only stores x-access depths. REDO inline below.
        pre, recs, T0dB = run(n, T0, H)
        # build per-access full B-depth maps is O(n) each; do targeted:
        A, B = to_ptr(T0), to_ptr(T0)
        for idx, acc in enumerate(pre):
            x, mode = acc["x"], acc["mode"]
            dmap_b = depths_of(B)
            A, invs = splay_A(A, x)
            eA = len(invs)
            if mode == "KEEP":
                B, pushes = splay_B_push(B, x)
                eB = len(pushes)
            else:
                eB = 0
            dmap_a = depths_of(B)
            recs[idx]["dmap_b"] = dmap_b
            recs[idx]["dmap_a"] = dmap_a
        for t, r in enumerate(recs):
            if r["mode"] != "KEEP":
                continue
            ov = r["eB"] - 3 * r["eA"]
            if ov < 2:
                continue
            x = r["x"]
            agg["heavy_n"] += 1
            ridx = -1
            for u in range(t - 1, -1, -1):
                ru = recs[u]
                if ru["x"] == x and ru["mode"] == "KEEP":
                    ridx = u
                    break
            phi_r = recs[ridx]["phi_post"] if ridx >= 0 else 0
            dB0 = 0 if ridx >= 0 else T0dB.get(x, 0)
            tele = 0
            nets = Counter()
            cnts = Counter()
            deep_free_max = 0
            for u in range(ridx + 1, t):
                ru = recs[u]
                net = 3 * ru["eA"] - (ru["eB"] if ru["mode"] == "KEEP" else 0)
                if ru["mode"] == "DELETE":
                    cls = "delete"
                    delta = 0
                else:
                    delta = (ru["dmap_a"].get(x, 0)
                             - ru["dmap_b"].get(x, 0))
                    if delta > 0:
                        cls = ("deep-supplying"
                               if ru["eA"] >= 1 else "deep-free")
                    else:
                        cls = "nondeep"
                nets[cls] += net
                cnts[cls] += 1
                tele += delta
                if cls == "deep-free" and ru["eB"] > deep_free_max:
                    deep_free_max = ru["eB"]
            if r["dBb"] is not None and r["dBb"] != dB0 + tele:
                agg["tele_viol"] += 1
            win_ineq = phi_r + sum(nets.values()) - ov
            if agg["win_min"] is None or win_ineq < agg["win_min"]:
                agg["win_min"] = win_ineq
                agg["minrec"] = {"x": x, "eA": r["eA"], "eB": r["eB"],
                                 "dBb": r["dBb"], "buf_pre": r["buf_pre"],
                                 "ov": ov, "win": win_ineq, "phi_r": phi_r,
                                 "dB0": dB0, "nets": dict(nets),
                                 "cnts": dict(cnts),
                                 "deep_free_max": deep_free_max}
            if agg.get("maxeb", -1) < r["eB"]:
                agg["maxeb"] = r["eB"]
                agg["maxrec"] = {"x": x, "eA": r["eA"], "eB": r["eB"],
                                 "dBb": r["dBb"], "buf_pre": r["buf_pre"],
                                 "ov": ov, "win": win_ineq, "phi_r": phi_r,
                                 "dB0": dB0, "nets": dict(nets),
                                 "cnts": dict(cnts),
                                 "deep_free_max": deep_free_max}
            for k, v in nets.items():
                agg["net_" + k] += v
            for k, v in cnts.items():
                agg["cnt_" + k] += v
        if s % 30 == 29:
            step("WN-P", "s=%d done=%d" % (s, done))
    out = dict(agg)
    out.update({"evals": done})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "window.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("WN-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
