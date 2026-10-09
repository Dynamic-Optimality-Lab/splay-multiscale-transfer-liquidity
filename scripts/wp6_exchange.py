"""WP-6 C189 ATTAINER EXCHANGE scanner.

Net_s(sigma) = total B StepEvs - 3*total A StepEvs along KEEP word sigma
(exact event-list lengths). R3(s) = max over |sigma|<=3 (STOP included).
For transition (op z, rho) with post-state s' and post attainer sigma*:
  TGT = rho + Net_{s'}(sigma*); rho = -3a_z (DELETE) or r_z (KEEP).
Enumerate pre-state contender families over K={z,x,y,w}:
  F0 same word; F1 one-position deletions/subseqs of [z,x,y,w];
  F2 all len<=3 subseqs; F3 all len<=3 words over DISTINCT K;
  F4 len<=3 over K with repetition; F5 global R3(s) attainer
  (F5 wins <=> Lipschitz holds here: invariant check / kill path).
Modes: hard | scan. Artifacts: artifacts/.../attainer_exchange/*.json
"""
from __future__ import annotations
import sys
import json
import copy
import itertools
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import vine, balanced, depths_of
from wp6_keepres import H1f, H2f

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" \
    / "attainer_exchange"


def step(sid, msg):
    line = "[WP-6][EXCH %s] %s" % (sid, msg)
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


def net_of(A, B, sigma):
    """Exact Net along KEEP word sigma. Returns (net, trace)."""
    A2 = copy.deepcopy(A)
    B2 = copy.deepcopy(B)
    tot = 0
    tr = []
    for k in sigma:
        A2, ia = splay_A(A2, k)
        B2, p = splay_B_push(B2, k)
        a, b = len(ia), len(p)
        tot += b - 3 * a
        tr.append({"k": k, "a": a, "b": b})
    return tot, tr


def post_attainer(A, B, keys):
    """R3 attainer as word sigma* (floors = early stop)."""
    best = (0, [])
    det = {}
    for x in keys:
        A1 = copy.deepcopy(A)
        A1, ia = splay_A(A1, x)
        a = len(ia)
        B1 = copy.deepcopy(B)
        B1, p = splay_B_push(B1, x)
        b = len(p)
        r = b - 3 * a
        h = H2f(A1, B1, keys)
        qmax = h["Qmax"]
        if qmax is not None and qmax > 0:
            # attaining y
            dA = depths_of(A1)
            dB = depths_of(B1)
            by = None
            for y in keys:
                A2 = copy.deepcopy(A1)
                A2, _ = splay_A(A2, y)
                B2 = copy.deepcopy(B1)
                B2, _ = splay_B_push(B2, y)
                hk = H1f(depths_of(A2), depths_of(B2), keys)
                da = dA.get(y, 0)
                db = dB.get(y, 0)
                qy = ((db + 1) // 2 - 3 * ((da + 1) // 2)) + hk
                if by is None or qy > by[0]:
                    by = (qy, y, A2, B2, hk)
            qy, y, A2, B2, hk = by
            if hk > 0:
                dA2 = depths_of(A2)
                dB2 = depths_of(B2)
                wz = max(keys, key=lambda w:
                         (dB2.get(w, 0) + 1) // 2 -
                         3 * ((dA2.get(w, 0) + 1) // 2))
                v = r + qy
                if v > best[0]:
                    best = (v, [x, y, wz])
                    det = {"x": x, "y": y, "w": wz, "r": r,
                           "Q1": qy, "H1s2": hk}
            else:
                v = r + qy
                if v > best[0]:
                    best = (v, [x, y])
                    det = {"x": x, "y": y, "r": r, "Q1": qy,
                           "H1s2": 0}
        else:
            if r > best[0]:
                best = (r, [x])
                det = {"x": x, "r": r, "Q1": 0}
    if not best[1]:
        return 0, [], {"len": 0}
    det["len"] = len(best[1])
    return best[0], best[1], det


def families(z, sigma):
    K = []
    for k in [z] + list(sigma):
        if k not in K:
            K.append(k)
    fams = {}
    # F-1: STOP (empty word, Net = 0). Wins whenever tgt <= 0.
    fams["Fm1"] = [[]]
    fams["F0"] = [list(sigma)]
    # F1: one-position deletions of [z]+sigma and len<=2 subseqs
    base = [z] + list(sigma)
    s1 = set()
    for i in range(len(base)):
        w = base[:i] + base[i + 1:]
        if 1 <= len(w) <= 3:
            s1.add(tuple(w))
    for L in (1, 2):
        for w in itertools.combinations(base, L):
            s1.add(tuple(w))
    fams["F1"] = [list(w) for w in s1]
    # F2: all len<=3 subsequences (order-preserving) of base
    s2 = set()
    for L in (1, 2, 3):
        for w in itertools.combinations(base, L):
            s2.add(tuple(w))
    fams["F2"] = [list(w) for w in s2]
    # F3: all len<=3 words over DISTINCT keys of K
    s3 = set()
    for L in (1, 2, 3):
        for w in itertools.permutations(K, L):
            s3.add(tuple(w))
    fams["F3"] = [list(w) for w in s3]
    # F4: len<=3 over K with repetition
    s4 = set()
    for L in (1, 2, 3):
        for w in itertools.product(K, repeat=L):
            s4.add(tuple(w))
    fams["F4"] = [list(w) for w in s4]
    return fams, K


def analyze(A, B, keys, z, mode, tag):
    """One transition. Returns record dict."""
    dA = depths_of(copy.deepcopy(A))
    dB = depths_of(copy.deepcopy(B))
    a = (dA.get(z, 0) + 1) // 2
    b = (dB.get(z, 0) + 1) // 2
    r = b - 3 * a
    A2 = copy.deepcopy(A)
    A2, _ = splay_A(A2, z)
    if mode == "DELETE":
        B2 = B
        rho = -3 * a
    else:
        B2 = copy.deepcopy(B)
        B2, _ = splay_B_push(B2, z)
        rho = r
    post, sigma, det = post_attainer(A2, B2, keys)
    # verify Net matches post value
    nv, _ = net_of(A2, B2, sigma)
    tgt = rho + post
    fams, K = families(z, sigma)
    # same-chain pre value
    scv, _ = net_of(A, B, sigma)
    rec = {"tag": tag, "mode": mode, "z": z, "a": a, "b": b,
           "r": r, "rho": rho, "sigma": sigma, "post": post,
           "tgt": tgt, "samechain": scv,
           "deficit": tgt - scv if sigma else 0,
           "K": K, "det": det,
           "roots": (A["k"] if isinstance(A, dict) else None,
                     B["k"] if isinstance(B, dict) else None)}
    # scan families in order; record first-winning family + winner
    # (F3/F4 lazy: only built if Fm1-F2 all fail)
    prev = set()
    lazy = False
    for fn in ("Fm1", "F0", "F1", "F2"):
        new = []
        best = None
        for w in fams[fn]:
            t = tuple(w)
            if t in prev:
                continue
            prev.add(t)
            v, _ = net_of(A, B, w)
            if best is None or v > best[0]:
                best = (v, w)
            if v >= tgt:
                new.append((w, v - tgt))
        if new:
            rec["winfam"] = fn
            rec["winners"] = new[:6]
            rec["winbest"] = best[1]
            break
    else:
        lazy = True
    if lazy:
        for fn in ("F3", "F4"):
            new = []
            for w in fams[fn]:
                t = tuple(w)
                if t in prev:
                    continue
                prev.add(t)
                v, _ = net_of(A, B, w)
                if v >= tgt:
                    new.append((w, v - tgt))
            if new:
                rec["winfam"] = fn
                rec["winners"] = new[:6]
                break
        else:
            rec["winfam"] = None
        rec["lazy"] = True
    # F5: global pre attainer (Lipschitz invariant check)
    pv, psigma, _ = post_attainer(A, B, keys)
    rec["preR3"] = pv
    rec["preSigma"] = psigma
    rec["lip_hold"] = pv >= tgt
    return rec


def mode_hard():
    step("EX-00", "hard transitions")
    out = {"recs": []}
    # H1: vine32 diagonal DELETE 30 (+52 chain case)
    n = 32
    keys = list(range(1, n + 1))
    A, B = to_ptr(vine(n)), to_ptr(vine(n))
    out["recs"].append(analyze(A, B, keys, 30, "DELETE", "vine52"))
    # H2: +1 KEEP witness pair (seed 4242 trial 2)
    import random as R

    def rand_bst(rng, ks):
        r = list(ks)
        rng.shuffle(r)
        t = None

        def ins(t, k):
            if t is None:
                return [k, None, None]
            x = t
            while True:
                if k < x[0]:
                    if x[1] is None:
                        x[1] = [k, None, None]
                        return t
                    x = x[1]
                else:
                    if x[2] is None:
                        x[2] = [k, None, None]
                        return t
                    x = x[2]

        for k in r:
            t = ins(t, k)
        return t

    n = 24
    keys = list(range(1, n + 1))
    rng = R.Random(4242)
    pairs = [(rand_bst(rng, keys), rand_bst(rng, keys))
             for _ in range(3)]
    A0, B0 = pairs[2]
    A, B = to_ptr(A0), to_ptr(B0)
    out["recs"].append(analyze(A, B, keys, 11, "KEEP", "plus1"))
    # H3: BK1 witness (micro s=6 step 5)
    import wp6_micro as M
    n, T0, H = M.gen(6, b"bl")
    A, B = to_ptr(T0), to_ptr(T0)
    keys = list(range(1, n + 1))
    for i, acc in enumerate(H[:5]):
        mode, x = acc
        A, iv = splay_A(A, x)
        if mode == "KEEP":
            B, p = splay_B_push(B, x)
    for z in (1, 2):
        out["recs"].append(analyze(A, B, keys, z, "KEEP",
                                   "bk1_z%d" % z))
    # H4: R3=42 micro state, DELETE + KEEP probes
    out["recs"].append(analyze(A, B, keys, 1, "DELETE", "r42del"))
    step("EX-01", "hard done")
    save("hard_transitions.json", out)
    for r in out["recs"]:
        step("EX-02", "%s %s z=%s sigma=%s post=%s tgt=%s same=%s "
             "winfam=%s lip=%s" % (r["tag"], r["mode"], r["z"],
                                   r["sigma"], r["post"], r["tgt"],
                                   r["samechain"], r["winfam"],
                                   r["lip_hold"]))
    fails = [r for r in out["recs"] if not r["lip_hold"]]
    step("EX-03", "lip failures: %d" % len(fails))
    return 0 if not fails else 2


def mode_scan():
    step("EX-10", "broad scan: reachable walks + arbitrary pairs")
    out = {"recs": [], "famcount": {}, "lipfail": 0, "n": 0}
    import random as R

    def rand_bst(rng, ks):
        r = list(ks)
        rng.shuffle(r)
        t = None

        def ins(t, k):
            if t is None:
                return [k, None, None]
            x = t
            while True:
                if k < x[0]:
                    if x[1] is None:
                        x[1] = [k, None, None]
                        return t
                    x = x[1]
                else:
                    if x[2] is None:
                        x[2] = [k, None, None]
                        return t
                    x = x[2]

        for k in r:
            t = ins(t, k)
        return t

    n = 16
    keys = list(range(1, n + 1))
    # reachable walks
    for t in range(3):
        T0 = vine(n) if t % 2 == 0 else balanced(list(range(1, n + 1)))
        rng = R.Random(6000 + t)
        H = [[rng.choice(["KEEP", "DELETE"]), rng.randint(1, n)]
             for _ in range(15)]
        A, B = to_ptr(T0), to_ptr(T0)
        for i, acc in enumerate(H):
            mode, x = acc
            for z in keys[::4]:
                for md in ("DELETE", "KEEP"):
                    r = analyze(A, B, keys, z, md,
                                "walk%d_%d" % (t, i))
                    out["n"] += 1
                    k = (r["winfam"], len(r["sigma"]))
                    out["famcount"][str(k)] = \
                        out["famcount"].get(str(k), 0) + 1
                    if not r["lip_hold"]:
                        out["lipfail"] += 1
                        out["recs"].append(r)
                    elif r["winfam"] not in ("F0", "F1", "F2"):
                        if len(out["recs"]) < 40:
                            out["recs"].append(r)
            A, iv = splay_A(A, x)
            if mode == "KEEP":
                B, p = splay_B_push(B, x)
        step("EX-11", "walk t=%d famcount=%s lipfail=%d" %
             (t, json.dumps(out["famcount"], sort_keys=True),
              out["lipfail"]))
    # arbitrary pairs
    rng = R.Random(777)
    for t in range(8):
        A0 = rand_bst(rng, keys)
        B0 = rand_bst(rng, keys)
        A, B = to_ptr(A0), to_ptr(B0)
        for z in keys[::4]:
            for md in ("DELETE", "KEEP"):
                r = analyze(A, B, keys, z, md, "arb%d" % t)
                out["n"] += 1
                k = (r["winfam"], len(r["sigma"]))
                out["famcount"][str(k)] = \
                    out["famcount"].get(str(k), 0) + 1
                if not r["lip_hold"]:
                    out["lipfail"] += 1
                    out["recs"].append(r)
    step("EX-12", "scan done n=%d lipfail=%d" %
         (out["n"], out["lipfail"]))
    save("selector_scan.json", out)
    return 0 if out["lipfail"] == 0 else 2


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "hard"
    if mode == "hard":
        return mode_hard()
    if mode == "scan":
        return mode_scan()
    print("unknown", mode)
    return 1


if __name__ == "__main__":
    sys.exit(main())
