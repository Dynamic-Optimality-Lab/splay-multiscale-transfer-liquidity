# GLOB independent checker (DFS partition enumeration; shares disclosed primitives).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from, canon
from GLOB_recursive_checker import bank25_checked

MEMOD = {}
CALLSD = {"n": 0, "hit": False}
CAPD = 60000

def _rc(e):
    if type(e).__name__ == "ReplayError" and "absent" in str(e):
        return "SOURCE-INVALID"
    return "INDETERMINATE"

def baseD(word, Fr):
    n = len(word)
    pairs = Fr["pairs"]
    unk = []
    for rr in range(n):
        bs = pairs[rr]
        rw = [word[(rr + t) % n] for t in range(n)]
        try:
            Gr = replay_from(bs, rw)
        except Exception as e:
            return {"disp": "INDETERMINATE", "why": "rotation-replay", "rr": rr}
        if Gr["pairs"][-1] != bs:
            return {"disp": "INDETERMINATE", "why": "rotation-not-closed", "rr": rr}
        legs = Gr["legs"]
        A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
        if A == 0 and Q == 0 and len({l["x"] for l in legs}) == 1:
            return {"disp": "COVERED", "depth": 0, "basis": "Z", "rr": rr, "A": A, "Q": Q}
        if A == 0:
            unk.append("Z-fail")
            continue
        fb, u2 = bank25_checked(legs, Gr["pairs"], Gr["snaps"])
        if fb is None:
            unk.extend(u2)
            continue
        pos = sorted(k for k, v in fb.items() if v)
        if pos:
            return {"disp": "COVERED", "depth": 0, "basis": "RotB25", "mechanisms": pos, "rr": rr, "A": A, "Q": Q}
        unk.extend(u2)
    if unk:
        return {"disp": "INDETERMINATE", "why": "unknown", "unknown": sorted(set(unk))}
    return {"disp": "UNCOVERED", "why": "all-negative"}

def _parts(segs, i, n, mem):
    if i == n:
        return [(0, [])]
    if i in mem:
        return mem[i]
    out = []
    for (a, b) in segs:
        if a != i:
            continue
        ch = mem.get(("c", a, b))
        if ch is None or ch["disp"] != "COVERED":
            continue
        for (d2, rest) in _parts(segs, b, n, mem):
            out.append((max(ch["depth"], d2), [(a, b)] + rest))
    mem[i] = out
    return out

def coverD(start, word):
    key = (start, canon(word))
    if key in MEMOD:
        return MEMOD[key]
    CALLSD["n"] += 1
    if CALLSD["n"] > CAPD:
        CALLSD["hit"] = True
        r = {"disp": "INDETERMINATE", "why": "cap"}
        MEMOD[key] = r
        return r
    n = len(word)
    if n == 0:
        r = {"disp": "SOURCE-INVALID", "why": "empty"}
        MEMOD[key] = r
        return r
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"disp": _rc(e), "why": "replay"}
        MEMOD[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"disp": "SOURCE-INVALID", "why": "not-closed"}
        MEMOD[key] = r
        return r
    legs = Fr["legs"]
    totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
    b = baseD(word, Fr)
    if b["disp"] in ("COVERED", "INDETERMINATE"):
        b.update({"n": n, "A": totA, "Q": totQ})
        MEMOD[key] = b
        return b
    pairs = Fr["pairs"]
    tainted = False
    for rr in range(n):
        bs = pairs[rr]
        rw = [word[(rr + t) % n] for t in range(n)]
        try:
            Gr = replay_from(bs, rw)
        except Exception:
            tainted = True
            continue
        if Gr["pairs"][-1] != bs:
            tainted = True
            continue
        gp = Gr["pairs"]
        segs = []
        for i in range(n):
            for j in range(i + 1, n + 1):
                if j - i == n:
                    continue
                if gp[i] != gp[j % n]:
                    continue
                segs.append((i, j))
        if not segs:
            continue
        mem = {}
        for (a, b2) in segs:
            sw = [rw[(t) % n] for t in range(a, b2)]
            ch = coverD(gp[a], sw)
            mem[("c", a, b2)] = ch
            if ch["disp"] == "INDETERMINATE":
                tainted = True
        cands = _parts(segs, 0, n, mem)
        full = [c for c in cands if len(c[1]) >= 2]
        if full:
            full.sort(key=lambda c: (c[0], len(c[1])))
            dd, path = full[0]
            sA = 0; sQ = 0
            for (a, b2) in path:
                k = mem[("c", a, b2)]
                sA += k["A"]; sQ += k["Q"]
            if sA == totA and sQ == totQ:
                r = {"disp": "COVERED", "depth": dd + 1, "basis": "additive",
                     "frame": rr, "n": n, "A": totA, "Q": totQ}
                MEMOD[key] = r
                return r
            r = {"disp": "INDETERMINATE", "why": "additive-mismatch", "n": n}
            MEMOD[key] = r
            return r
    if tainted or CALLSD["hit"]:
        r = {"disp": "INDETERMINATE", "why": "tainted-or-cap", "n": n}
        MEMOD[key] = r
        return r
    r = {"disp": "UNCOVERED", "why": "no-frame-partition", "n": n, "A": totA, "Q": totQ}
    MEMOD[key] = r
    return r

def fresh():
    MEMOD.clear(); CALLSD["n"] = 0; CALLSD["hit"] = False
