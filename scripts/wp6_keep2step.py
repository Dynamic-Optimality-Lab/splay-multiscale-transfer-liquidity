"""WP-6 C184 KEEP-2STEP decision: KR2 kill hunt + Phi_min state search.

Exact integers, present keys, exact engine semantics (splay_A/splay_B_push).
  r_x(s) = b_x - 3*a_x (exact StepEv counts via event-list lengths).
  Q(s1)  = max(0, max_y [r_y(s1) + H1(K_y(s1))]) via H2f (ceil-formula,
           equal to exact counts by kernel ecount_eq C161-162).
  KR2(h,x) = r_x(s) + Q(K_x(s)) - Phi(h).  Positive = GC kill (mission Sec 21).

Modes (argv[1]): walk | targeted | beam | phimin | triples
Artifacts: artifacts/v04/wp6_present/0909c74a/keep2step/*.json
"""
from __future__ import annotations
import sys
import json
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import vine, balanced, depths_of
from wp6_keepres import H1f, H2f

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "keep2step"


def step(sid, msg):
    line = "[WP-6][KEEP2STEP %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        BD.mkdir(parents=True, exist_ok=True)
        with open(BD / "progress.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def kr2_of(A, B, keys, x, Phi, full_detail=False):
    """Returns (kr2, info). info has r,a,b,Q1,y,z,s1H2 (+rz terms)."""
    A1 = copy.deepcopy(A)
    A1, ia = splay_A(A1, x)
    a = len(ia)
    B1 = copy.deepcopy(B)
    B1, p = splay_B_push(B1, x)
    b = len(p)
    r = b - 3 * a
    h = H2f(A1, B1, keys)
    qmax = h["Qmax"]
    Q1 = qmax if (qmax is not None and qmax > 0) else 0
    kr2 = r + Q1 - Phi
    info = {"x": x, "a": a, "b": b, "r": r, "Q1": Q1,
            "H1s1": h["H1"], "H2s1": h["H2"], "gap": h["gap"]}
    if full_detail or kr2 > 0:
        # maximizing y attaining Q(s1): rescan for argmax with exact counts
        dA = depths_of(A1)
        dB = depths_of(B1)
        best = None
        for y in keys:
            A2 = copy.deepcopy(A1)
            A2, _ = splay_A(A2, y)
            B2 = copy.deepcopy(B1)
            B2, _ = splay_B_push(B2, y)
            da = dA.get(y, 0)
            db = dB.get(y, 0)
            ay, by = (da + 1) // 2, (db + 1) // 2
            hk = H1f(depths_of(A2), depths_of(B2), keys)
            qy = (by - 3 * ay) + hk
            if best is None or qy > best[0]:
                best = (qy, y, (by - 3 * ay), hk, A2, B2)
        if best is not None:
            qy, y, ry, hk, A2, B2 = best
            info["y"] = y
            info["ry"] = ry
            info["H1s2"] = hk
            if hk > 0:
                # maximizing z attaining H1(s2)
                dA2 = depths_of(A2)
                dB2 = depths_of(B2)
                bz = None
                for z in keys:
                    da = dA2.get(z, 0)
                    db = dB2.get(z, 0)
                    v = (db + 1) // 2 - 3 * ((da + 1) // 2)
                    if bz is None or v > bz[0]:
                        bz = (v, z, (db + 1) // 2, (da + 1) // 2)
                if bz is not None:
                    info["z"] = bz[1]
                    info["rz"] = bz[0]
                    info["bz"] = bz[2]
                    info["az"] = bz[3]
    return kr2, info


def scan_state(A, B, keys, Phi, ksample=1, detail=False):
    """Max KR2 over keys (ksample stride). Returns (best_kr2, info)."""
    ks = keys[::ksample]
    best = None
    for x in ks:
        v, info = kr2_of(A, B, keys, x, Phi, full_detail=detail)
        if best is None or v > best[0]:
            best = (v, info)
            if v > 0 and not detail:
                # re-extract full detail on kill
                v2, info2 = kr2_of(A, B, keys, x, Phi, full_detail=True)
                best = (v2, info2)
                break
    return best


def run_history(T0, H, keys, ksample=1, track=None):
    """Walk history; return agg dict + kill record if KR2>0."""
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    agg = {"kr2": None}
    for i, acc in enumerate(H):
        mode, x = acc
        Phi = 3 * SA - EB
        v, info = scan_state(A, B, keys, Phi, ksample=ksample)
        if agg["kr2"] is None or v > agg["kr2"]:
            agg["kr2"] = v
            agg["wit"] = {"step": i, "mode": mode, "x": x, "Phi": Phi,
                          "info": info, "Aroot": A["k"], "Broot": B["k"]}
            if track is not None:
                track.append((v, i, dict(info)))
        if v > 0:
            agg["kill"] = {"step": i, "Phi": Phi, "info": info,
                           "hist": H[:i + 1], "T0": T0}
            return agg, True
        A, invs = splay_A(A, x)
        eB = 0
        if mode == "KEEP":
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
        SA += len(invs)
        EB += eB if mode == "KEEP" else 0
    agg["final_Phi"] = 3 * SA - EB
    return agg, False


def shapes_of(ks):
    if not ks:
        return [None]
    res = []
    for i, k in enumerate(ks):
        for l in shapes_of(ks[:i]):
            for r in shapes_of(ks[i + 1:]):
                res.append([k, l, r])
    return res


def rand_bst(rng, ks):
    r = list(ks)
    rng.shuffle(r)
    t = None

    def ins(t, k):
        if t is None:
            return [k, None, None]
        if k < t[0]:
            t[1] = ins(t[1], k)
        elif k > t[0]:
            t[2] = ins(t[2], k)
        return t

    for k in r:
        t = ins(t, k)
    return t


def mode_walk():
    step("K2-00", "walk mode: random mixed histories, multi-shape")
    out = {}
    kill = None
    cfgs = [(8, 6, 30, 1), (16, 6, 40, 1), (24, 4, 30, 1),
            (32, 3, 25, 2), (48, 3, 25, 4)]
    for n, trials, L, ksamp in cfgs:
        cmax = None
        for t in range(trials):
            m = t % 4
            if m == 0:
                T0 = vine(n)
            elif m == 1:
                T0 = balanced(list(range(1, n + 1)))
            elif m == 2:
                # reverse vine (descending insertion)
                T0 = None
                for kk in range(n, 0, -1):
                    def ins(t_, k):
                        if t_ is None:
                            return [k, None, None]
                        if k < t_[0]:
                            t_[1] = ins(t_[1], k)
                        elif k > t_[0]:
                            t_[2] = ins(t_[2], k)
                        return t_
                    T0 = ins(T0, kk)
            else:
                T0 = rand_bst(random.Random(5000 + t), list(range(1, n + 1)))
            rng = random.Random(8000 + t)
            H = [[rng.choice(["KEEP", "DELETE"]), rng.randint(1, n)]
                 for _ in range(L)]
            keys = list(range(1, n + 1))
            agg, iskill = run_history(T0, H, keys, ksample=ksamp)
            if cmax is None or agg["kr2"] > cmax["kr2"]:
                cmax = {"kr2": agg["kr2"], "wit": agg.get("wit"),
                        "t": t, "m": m}
            if iskill:
                kill = agg["kill"]
                kill["cfg"] = {"n": n, "t": t, "m": m}
                break
        out["walk_n%d" % n] = cmax
        step("K2-01", "walk n=%d best_kr2=%s" % (n, cmax["kr2"]))
        if kill:
            break
    out["kill"] = kill
    save("kr2_walk.json", out)
    step("K2-02", "walk done kill=%s" % (kill is not None))
    return 0 if kill is None else 2


def mode_targeted():
    step("K2-10", "targeted mode: divergence builders + hostile shapes")
    out = {}
    kill = None
    fams = []

    def add(name, T0, H):
        fams.append((name, T0, H))

    # deep KEEP cycles on vines (divergence builders)
    for n in (16, 32):
        T0 = vine(n)
        H = [["KEEP", n]] * 6 + [["KEEP", 1]] * 2 + [["KEEP", n]] * 6
        add("vine%d_deepcycle" % n, T0, H)
        # DELETE epoch then deep KEEP (arrival-divergence C176 shape)
        H2 = [["DELETE", k] for k in range(1, n + 1)] + \
             [["KEEP", n], ["KEEP", n - 1], ["KEEP", n]]
        add("vine%d_delepoch" % n, T0, H2)
        # far-key alternation
        H3 = [["KEEP", 1], ["KEEP", n]] * 8
        add("vine%d_altern" % n, T0, H3)
    # balanced + comb/broom builders
    for n in (16, 32):
        T0 = balanced(list(range(1, n + 1)))
        add("bal%d_mixed" % n, T0,
            [["KEEP", n // 2], ["DELETE", 1], ["KEEP", n],
             ["KEEP", 1], ["DELETE", n], ["KEEP", n // 2]] * 3)

        def comb(nn):
            # comb: path with teeth (use insertion order trick)
            rng = random.Random(31337)
            ks = list(range(1, nn + 1))
            rng.shuffle(ks)
            return rand_bst(rng, ks)
        add("comb%d_rand" % n, comb(n),
            [["KEEP", random.Random(7).randint(1, n)] for _ in range(20)])
    # stale-root: avoid one key for long stretch then hit it deep
    for n in (24,):
        T0 = vine(n)
        rng = random.Random(11)
        H = [[rng.choice(["KEEP", "DELETE"]), rng.randint(2, n)]
             for _ in range(30)] + [["KEEP", 1]]
        add("stale_root%d" % n, T0, H)
    # repeated DELETE builders on single keys
    for n in (16,):
        T0 = vine(n)
        add("delbuild%d" % n, T0,
            [["DELETE", n]] * 10 + [["KEEP", n]] * 4)
    # post-KEEP-heavy: all KEEP deep keys
    for n in (16, 32):
        T0 = vine(n)
        rng = random.Random(21)
        add("keepheavy%d" % n, T0,
            [["KEEP", rng.randint(n // 2, n)] for _ in range(20)])

    for name, T0, H in fams:
        keys = sorted(depths_of(to_ptr(T0)).keys())
        ksamp = 1 if len(keys) <= 24 else 2
        agg, iskill = run_history(T0, H, keys, ksample=ksamp)
        out[name] = {"kr2": agg["kr2"], "wit": agg.get("wit")}
        step("K2-11", "%s best_kr2=%s" % (name, agg["kr2"]))
        if iskill:
            kill = agg["kill"]
            kill["fam"] = name
            break
    out["kill"] = kill
    save("kr2_targeted.json", out)
    step("K2-12", "targeted done kill=%s" % (kill is not None))
    return 0 if kill is None else 2


def mode_beam():
    step("K2-20", "beam mode: greedy max-KR2 descent")
    out = {}
    kill = None
    for n in (12, 20):
        T0 = vine(n)
        A, B = to_ptr(T0), to_ptr(T0)
        keys = list(range(1, n + 1))
        SA = EB = 0
        hist = []
        best = None
        for depth in range(14):
            Phi = 3 * SA - EB
            # all children KR2
            cands = []
            for mode in ("KEEP", "DELETE"):
                for x in keys:
                    A2 = copy.deepcopy(A)
                    A2, ia = splay_A(A2, x)
                    B2 = copy.deepcopy(B)
                    eB = 0
                    if mode == "KEEP":
                        B2, p = splay_B_push(B2, x)
                        eB = len(p)
                    SA2 = SA + len(ia)
                    EB2 = EB + (eB if mode == "KEEP" else 0)
                    v, info = scan_state(A2, B2, keys, 3 * SA2 - EB2)
                    cands.append((v, mode, x, SA2, EB2, info))
            cands.sort(key=lambda c: -c[0])
            v, mode, x = cands[0][:3]
            if best is None or v > best[0]:
                best = (v, {"depth": depth, "mode": mode, "x": x,
                            "info": cands[0][5]})
            step("K2-21", "beam n=%d d=%d child_kr2=%s via %s-%s" %
                 (n, depth, v, mode, x))
            if v > 0:
                kill = {"beam": True, "n": n, "depth": depth,
                        "mode": mode, "x": x, "hist": hist,
                        "info": cands[0][5]}
                break
            hist.append([mode, x])
            A, ia = splay_A(A, x)
            if mode == "KEEP":
                B, p = splay_B_push(B, x)
                EB += len(p)
            SA += len(ia)
        out["beam_n%d" % n] = {"kr2": best[0], "wit": best[1]}
        if kill:
            break
    out["kill"] = kill
    save("kr2_beam.json", out)
    step("K2-22", "beam done kill=%s" % (kill is not None))
    return 0 if kill is None else 2


def mode_phimin():
    step("K2-30", "phimin mode: exact min-Phi BFS + R3 check, small n")
    out = {}
    for n in (3, 4):
        ks = list(range(1, n + 1))
        Sh = shapes_of(ks)
        idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}

        def key(A0, B0):
            return (idx[json.dumps(A0, sort_keys=True)],
                    idx[json.dumps(B0, sort_keys=True)])

        # dist[(ia,ib)] = min Phi; BFS relaxation with step cap
        from collections import deque
        INF = 10 ** 18
        dist = {}
        start = []
        for i, s in enumerate(Sh):
            dist[(i, i)] = 0
            start.append((i, i))

        def ptr_of(i):
            return to_ptr(copy.deepcopy(Sh[i]))

        # Bellman-Ford style: relax up to K rounds or until fixpoint
        # (negative-cost edges exist: KEEP reward). Cap: detect negative
        # dist as GC kill (Phi<0 reachable).
        kill = None
        nodes = [(i, j) for i in range(len(Sh)) for j in range(len(Sh))]
        # BFS layered by steps (bounded lookahead W)
        W = 8 if n == 3 else 6
        cur = dict(dist)
        for rnd in range(W):
            nxt = dict(cur)
            improved = False
            for (ia, ib), dphi in list(cur.items()):
                A = ptr_of(ia)
                B = ptr_of(ib)
                dA = depths_of(A)
                dB = depths_of(B)
                for x in ks:
                    da = dA.get(x, 0)
                    db = dB.get(x, 0)
                    a = (da + 1) // 2
                    b = (db + 1) // 2
                    # DELETE x
                    A2 = copy.deepcopy(A)
                    A2, _ = splay_A(A2, x)
                    # canonical re-encode: find shape index by structure
                    ia2 = shape_index(Sh, idx, A2)
                    kk = (ia2, ib)
                    nd = dphi + 3 * a
                    if kk[0] is not None and nd < nxt.get(kk, INF):
                        nxt[kk] = nd
                        improved = True
                    # KEEP x
                    B2 = copy.deepcopy(B)
                    B2, _ = splay_B_push(B2, x)
                    ib2 = shape_index(Sh, idx, B2)
                    kk2 = (ia2, ib2)
                    nd2 = dphi + 3 * a - b
                    if kk2[0] is not None and kk2[1] is not None and \
                            nd2 < nxt.get(kk2, INF):
                        nxt[kk2] = nd2
                        improved = True
                        if nd2 < 0:
                            kill = {"pair": kk2, "dist": nd2,
                                    "rounds": rnd}
            cur = nxt
            if kill:
                break
            if not improved:
                break
        # R3 check on reached pairs: R3 = max_x(r_x + Q(K_x)) <= dist ?
        worst = None
        checked = 0
        for (ia, ib), dphi in cur.items():
            if dphi == INF:
                continue
            A = ptr_of(ia)
            B = ptr_of(ib)
            v, info = scan_state(A, B, ks, dphi)
            # scan_state returns KR2 = R3 - dist; want max
            if worst is None or v > worst[0]:
                worst = (v, (ia, ib), info)
            checked += 1
            if v > 0:
                kill = {"pair": (ia, ib), "dist": dphi, "kr2": v,
                        "info": info, "via": "R3>dist"}
                break
        out["phimin_n%d" % n] = {"pairs": checked, "worst_kr2":
                                 worst[0] if worst else None,
                                 "wit": worst[2] if worst else None,
                                 "kill": kill}
        step("K2-31", "phimin n=%d pairs=%d worst_kr2=%s kill=%s" %
             (n, checked, worst[0] if worst else None, kill is not None))
        if kill:
            out["kill"] = kill
            break
    out.setdefault("kill", None)
    save("phi_min.json", out)
    step("K2-32", "phimin done")
    return 0


def shape_index(Sh, idx, P):
    # structural shape of ptr tree: normalize to sorted-key skeleton?
    # Shapes are over fixed key labels, so compare inorder-structure
    # by encoding (key, left, right) recursively.
    def enc(t):
        if t is None:
            return None
        return [t["k"], enc(t["l"]), enc(t["r"])]
    return idx.get(json.dumps(enc(P), sort_keys=True))


def mode_triples():
    step("K2-40", "triples mode: maximizing (x,y,z) + reset windows")
    out = {"triples": [], "best": None}
    # collect from walks: states maximizing Q-H1 and min Phi-H2
    for n in (16, 24):
        T0 = vine(n)
        rng = random.Random(1234)
        for t in range(3):
            H = [[rng.choice(["KEEP", "DELETE"]), rng.randint(1, n)]
                 for _ in range(25)]
            A, B = to_ptr(T0), to_ptr(T0)
            keys = list(range(1, n + 1))
            SA = EB = 0
            # last-KEEP reset times
            tau = {}
            for i, acc in enumerate(H):
                mode, x = acc
                Phi = 3 * SA - EB
                h = H2f(A, B, keys)
                qmh = (h["Qmax"] if h["Qmax"] and h["Qmax"] > 0 else 0) - h["H1"]
                # record candidate future triple at this state (all x argmax)
                v, info = scan_state(A, B, keys, Phi,
                                    ksample=1 if n <= 16 else 2)
                rec = {"n": n, "t": t, "step": i, "Phi": Phi,
                       "H1": h["H1"], "Q": qmh + h["H1"], "QH1": qmh,
                       "PhiH2": Phi - h["H2"], "kr2": v,
                       "x": info.get("x"), "y": info.get("y"),
                       "z": info.get("z"),
                       "tau": {str(k): tau.get(k) for k in
                               [info.get("x"), info.get("y"),
                                info.get("z")] if k},
                       "roots": (A["k"], B["k"])}
                out["triples"].append(rec)
                if out["best"] is None or v > out["best"]["kr2"]:
                    out["best"] = rec
                A, invs = splay_A(A, x)
                eB = 0
                if mode == "KEEP":
                    B, pushes = splay_B_push(B, x)
                    eB = len(pushes)
                    tau[x] = i
                SA += len(invs)
                EB += eB if mode == "KEEP" else 0
    save("future_triples.json", out)
    step("K2-41", "triples done best_kr2=%s" %
         (out["best"]["kr2"] if out["best"] else None))
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "walk"
    if mode == "walk":
        return mode_walk()
    if mode == "targeted":
        return mode_targeted()
    if mode == "beam":
        return mode_beam()
    if mode == "phimin":
        return mode_phimin()
    if mode == "triples":
        return mode_triples()
    print("unknown mode", mode)
    return 1


if __name__ == "__main__":
    sys.exit(main())
