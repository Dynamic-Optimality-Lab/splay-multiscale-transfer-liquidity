"""26AS ASmix exact-cover recognizer: banked ARmix packets (imported validators)
+ new AS shared-credit components. All cuts x memoized DP.

Block fields (from trace): key,keys,a,q,delta,genuine,dB,rb,keeps,dA,push
(list of pushed keys of the block's B splay, [] if none).
Trace snapshots: snaps[i] = B-depth dict AFTER access i (for t0 depths).
Accesses indexed 0-based; block b covers legs [b['l0'], b['l1']).
"""
import json, importlib.util
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS')

def _load_banked(name, rel):
    spec = importlib.util.spec_from_file_location(
        name, str(Path('DO_RESEARCH_REBOOT/06_CERTIFICATES') / rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
_AR = _load_banked('ar26_banked', '26AR/26AR_mixed_exact_cover_recognizer.py')
valid_direct = _AR.valid_direct
valid_bridge = _AR.valid_bridge
valid_split = _AR.valid_split

def valid_AS(blocks, snaps, idx, j):
    """AS shared-credit component at linearized position j. Layout:
    run1, sepA(>=1 nonpos), run2, sepB(>=1, contains W), R=KEEP(r), S=KEEP(s).
    Returns (L, comp) with L = linearized length consumed."""
    m = len(blocks)
    r1 = []
    k = j
    while k < m and blocks[idx[k]]["delta"] == 1:
        r1.append(idx[k]); k += 1
    if not r1 or k >= m:
        return None
    mr = len(r1)
    r = blocks[r1[0]]["rb"]
    sepA = []
    while k < m and blocks[idx[k]]["delta"] <= 0:
        sepA.append(idx[k]); k += 1
    if not sepA or k >= m:
        return None
    r2 = []
    while k < m and blocks[idx[k]]["delta"] == 1:
        r2.append(idx[k]); k += 1
    if not r2 or k >= m:
        return None
    ms = len(r2)
    s = blocks[r2[0]]["rb"]
    if r == s:
        return None
    sepB = []
    while k < m and blocks[idx[k]]["delta"] <= 0:
        # stop before returns: peek R,S pattern (leader keys r then s)
        if blocks[idx[k]]["key"] == r and r in blocks[idx[k]]["keeps"]:
            break
        sepB.append(idx[k]); k += 1
    if not sepB or k + 1 >= m:
        return None
    Ro, So = idx[k], idx[k + 1]
    R, Sb = blocks[Ro], blocks[So]
    if R["delta"] > 0 or Sb["delta"] > 0:
        return None
    if not (R["key"] == r and r in R["keeps"]):
        return None
    if not (Sb["key"] == s and s in Sb["keeps"]):
        return None
    if s in R["keeps"] or r in Sb["keeps"]:
        return None
    # lifetimes: r untouched in run1[1:]+sepA+run2+sepB; s in run2[1:]+sepB.
    for o in r1[1:] + sepA + r2 + sepB:
        if r in blocks[o]["keeps"]:
            return None
    for o in r2[1:] + sepB:
        if s in blocks[o]["keeps"]:
            return None
    # W: exactly one designated block in sepB (deterministic order).
    for Wo in sepB:
        W = blocks[Wo]
        if not (W["genuine"] and W["dB"] is not None and 1 <= W["dB"] <= 3
                and W["a"] >= 1 and min(r, s) < W["key"] < max(r, s)):
            continue
        if not (r in W.get("push", []) and s in W.get("push", [])):
            continue
        # t0 = state after run2 end
        t0acc = blocks[r2[-1]]["l1"] - 1
        snap = snaps.get(t0acc)
        if snap is None or r not in snap or s not in snap:
            continue
        dr0, ds0 = snap[r], snap[s]
        # h,g over sepB genuine splays (W included)
        h = sum(1 for o in sepB if blocks[o]["genuine"])
        g = sum(1 for o in sepB
                if blocks[o]["genuine"] and min(r, s) < blocks[o]["key"] < max(r, s))
        eps = 1 if (dr0 % 2 == 1 and ds0 % 2 == 1) else 0
        kap = g - eps
        if kap < 1:
            continue
        Ur = (dr0 + 2 * h) // 2
        Us = (ds0 + 2 * h + 2) // 2
        Urs = (dr0 + ds0 + 4 * h - 2 * g + 2) // 2
        if not (Ur + Us - Urs == kap):
            return None
        Tr = max(1, -(-(Ur + mr - 1) // 2))
        Ts = max(1, -(-(Us + ms - 1) // 2))
        if not (R["dA"] >= 2 * Tr - 1 and Sb["dA"] >= 2 * Ts - 1):
            continue
        ar, qr = R["a"], R["q"]
        as_, qs = Sb["a"], Sb["q"]
        CR, CS = 2 * ar - qr, 2 * as_ - qs
        CW = 2 * W["a"] - W["q"]
        if not (CR >= mr - 1 and CS >= ms - 1 and CW >= 1):
            continue
        if not (CR + CW >= mr and CS + CW >= ms and CR + CW + CS >= mr + ms):
            continue
        frW = max(0, mr - CR); frR = mr - frW
        fsS = min(ms, CS); fsW = ms - fsS
        if not (frR <= CR and fsS <= CS and frW + fsW <= CW):
            continue
        comp = {"type": "AS-shared", "run1": r1, "sepA": sepA, "run2": r2,
                "sepB": sepB, "W": Wo, "R": Ro, "S": So, "r": r, "s": s,
                "mr": mr, "ms": ms, "dr0": dr0, "ds0": ds0, "h": h, "g": g,
                "eps": eps, "kap": kap, "Ur": Ur, "Us": Us, "Urs": Urs,
                "Tr": Tr, "Ts": Ts, "CR": CR, "CS": CS, "CW": CW,
                "flow": {"frR": frR, "frW": frW, "fsW": fsW, "fsS": fsS}}
        L = (k + 1) - j + 1
        return (L, comp)
    return None

def _comp_len(blocks, idx, j, comp):
    # consumed linearized length = (S position - j) + 1
    for t in range(j, len(blocks)):
        if idx[t] == comp["S"]:
            return t - j + 1
    return None

def _chk(cond):
    return bool(cond)

def verify_cert(blocks, cert):
    if not cert.get("accepted"):
        return False
    m = len(blocks)
    seen = set()
    for pc in cert["pieces"]:
        t = pc["type"]
        if t == "AP-direct":
            rng = pc["run"] + [pc["return"]]
            if not (pc["p"] >= 1 and all(blocks[o]["delta"] == 1 for o in pc["run"])):
                return False
            rb = blocks[pc["return"]]
            if not (rb["key"] == pc["r"] and pc["r"] in rb["keeps"] and rb["a"] >= pc["p"]):
                return False
            if not rb["delta"] <= 0:
                return False
        elif t == "AQ-bridge":
            rng = pc["run1"] + [pc["bridge"]] + pc["run2"] + [pc["return"]]
            if not pc["p"] == pc["p1"] + pc["p2"] >= 3:
                return False
            if not all(blocks[o]["delta"] == 1 for o in pc["run1"] + pc["run2"]):
                return False
            if not blocks[pc["bridge"]]["delta"] <= -1:
                return False
            rb = blocks[pc["return"]]
            if not (rb["key"] == pc["r"] and pc["r"] in rb["keeps"] and rb["a"] >= pc["p"]):
                return False
        elif t == "AR-split":
            p = pc["p"]
            if not (p >= 3 and len(pc["run"]) == p):
                return False
            if not all(blocks[o]["delta"] == 1 for o in pc["run"]):
                return False
            r1 = blocks[pc["ret1"]]; r2 = blocks[pc["ret2"]]
            if not (r1["key"] == pc["r"] and pc["r"] in r1["keeps"]):
                return False
            if not (r2["key"] == pc["s"] and pc["s"] in r2["keeps"]):
                return False
            if not (pc["r"] != pc["s"] and r1["a"] < p and r2["a"] < p):
                return False
            u = (p + 2) // 2; v = (p + 1) // 2
            if not (r1["dA"] >= 2 * u - 1 and r2["dA"] >= 2 * v - 1):
                return False
            if not (r1["delta"] <= p - 2 * u and r2["delta"] <= 2 - 2 * v):
                return False
            if not p + r1["delta"] + r2["delta"] <= 0:
                return False
            rng = pc["run"] + [pc["ret1"], pc["ret2"]]
        elif t == "AS-shared":
            r, s = pc["r"], pc["s"]
            if not r != s:
                return False
            if not all(blocks[o]["delta"] == 1 for o in pc["run1"] + pc["run2"]):
                return False
            if not all(blocks[o]["delta"] <= 0 for o in pc["sepA"] + pc["sepB"]):
                return False
            W = blocks[pc["W"]]
            if not (W["genuine"] and 1 <= W["dB"] <= 3 and W["a"] >= 1
                    and min(r, s) < W["key"] < max(r, s)):
                return False
            if not (r in W.get("push", []) and s in W.get("push", [])):
                return False
            R = blocks[pc["R"]]; Sb = blocks[pc["S"]]
            if not (R["key"] == r and r in R["keeps"]):
                return False
            if not (Sb["key"] == s and s in Sb["keeps"]):
                return False
            if not (R["dA"] >= 2 * pc["Tr"] - 1 and Sb["dA"] >= 2 * pc["Ts"] - 1):
                return False
            if not (R["delta"] <= 0 and Sb["delta"] <= 0):
                return False
            if not (pc["CR"] == 2 * R["a"] - R["q"] and pc["CS"] == 2 * Sb["a"] - Sb["q"]
                    and pc["CW"] == 2 * W["a"] - W["q"]):
                return False
            if not (pc["CR"] + pc["CW"] >= pc["mr"] and pc["CS"] + pc["CW"] >= pc["ms"]
                    and pc["CR"] + pc["CW"] + pc["CS"] >= pc["mr"] + pc["ms"]):
                return False
            f = pc["flow"]
            if not (f["frR"] + f["frW"] == pc["mr"] and f["fsW"] + f["fsS"] == pc["ms"]):
                return False
            if not (f["frR"] <= pc["CR"] and f["fsS"] <= pc["CS"]
                    and f["frW"] + f["fsW"] <= pc["CW"]):
                return False
            rng = pc["run1"] + pc["sepA"] + pc["run2"] + pc["sepB"] + [pc["R"], pc["S"]]
        else:
            return False
        for o in rng:
            if o in seen:
                return False
            seen.add(o)
    for o in cert["singles"]:
        if o in seen or blocks[o]["delta"] > 0:
            return False
        seen.add(o)
    return seen == set(range(m))

def synth(key, keys, a, q, genuine, dB, rb, keeps, dA, push=None, l0=0, l1=1):
    return {"key": key, "keys": keys, "a": a, "q": q, "delta": q - 2 * a,
            "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps, "dA": dA,
            "push": push or [], "l0": l0, "l1": l1}

def criticality(blocks, snaps, comp):
    """Conservative separate bounds fail union cut, coupled bounds succeed."""
    mr, ms = comp["mr"], comp["ms"]
    cR = 2 * blocks[comp["R"]]["a"] - comp["Ur"]
    cS = 2 * blocks[comp["S"]]["a"] - comp["Us"]
    sep_fail = (cR + cS + 1 < mr + ms)
    coup_ok = (cR + cS + comp["kap"] + 1 >= mr + ms)
    return {"cR": cR, "cS": cS, "kap": comp["kap"],
            "separate_fail": sep_fail, "coupled_ok": coup_ok,
            "critical": sep_fail and coup_ok}

def recognize(blocks, snaps):
    m = len(blocks)
    if m == 0:
        return None
    if all(b["delta"] <= 0 for b in blocks):
        return {"accepted": True, "pieces": [], "singles": list(range(m)),
                "cut": None, "m": m}
    for cut in range(m):
        idx = [(cut + t) % m for t in range(m)]
        memo = {}
        def dp(p):
            if p == m:
                return []
            if p in memo:
                return memo[p]
            o = idx[p]
            res = None
            if blocks[o]["delta"] <= 0:
                t = dp(p + 1)
                if t is not None:
                    res = [("S", o)] + t
            if res is None:
                d = valid_direct(blocks, idx, p)
                if d is not None:
                    L, piece = d
                    t = dp(p + L)
                    if t is not None:
                        res = [("D", piece)] + t
            if res is None:
                d = valid_bridge(blocks, idx, p)
                if d is not None:
                    L, piece = d
                    t = dp(p + L)
                    if t is not None:
                        res = [("B", piece)] + t
            if res is None:
                d = _AR.valid_split(blocks, idx, p)
                if d is not None:
                    L, piece = d
                    t = dp(p + L)
                    if t is not None:
                        res = [("T", piece)] + t
            if res is None:
                d = valid_AS(blocks, snaps, idx, p)
                if d is not None:
                    _, piece = d
                    L = _comp_len(blocks, idx, p, piece)
                    if L is not None:
                        t = dp(p + L)
                        if t is not None:
                            res = [("A", piece)] + t
            memo[p] = res
            return res
        path = dp(0)
        if path is not None:
            pieces, singles = [], []
            for typ, v in path:
                if typ == "S":
                    singles.append(v)
                else:
                    pieces.append(v)
            return {"accepted": True, "pieces": pieces,
                    "singles": sorted(singles), "cut": cut, "m": m}
    return {"accepted": False, "m": m}
