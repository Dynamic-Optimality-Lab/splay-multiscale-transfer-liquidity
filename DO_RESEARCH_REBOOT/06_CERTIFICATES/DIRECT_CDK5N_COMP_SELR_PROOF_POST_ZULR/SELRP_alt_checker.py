# SELRP alternative recursive checker (proof stage; top-down DFS enumeration).
# Independent structure from SELRP_recursive_checker (boundary DP): explicit
# rotation-frame loop outermost, recursive splitting with minimax-depth
# choice. SHARED components (disclosed): replay_from/canon, bank24_checked
# semantics (imported), memo key format. Agreement measured in cross-validation.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from, canon
from SELRP_recursive_checker import bank24_checked

MEMOA = {}
CALLSA = {"n": 0, "hit": False}
CAPA = 60000

def _replay_class(err):
    if type(err).__name__ == "ReplayError" and "absent" in str(err):
        return "SOURCE-INVALID"
    return "INDETERMINATE"

def baseA(start, word, Fr):
    n = len(word)
    pairs = Fr["pairs"]
    unk = []
    for rr in range(n):
        bstart = pairs[rr]
        rword = [word[(rr + t) % n] for t in range(n)]
        try:
            Gr = replay_from(bstart, rword)
        except Exception as e:
            return {"disp": "INDETERMINATE", "why": "rotation-replay-%s" % type(e).__name__, "rr": rr}
        if Gr["pairs"][-1] != bstart:
            return {"disp": "INDETERMINATE", "why": "rotation-not-closed", "rr": rr}
        legs = Gr["legs"]
        A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
        if A == 0 and Q == 0 and len({l["x"] for l in legs}) == 1:
            return {"disp": "COVERED", "depth": 0, "basis": "Z", "rr": rr, "A": A, "Q": Q}
        if A == 0:
            unk.append("rr%d:Z-fail" % rr)
            continue
        flags, u2 = bank24_checked(legs, Gr["pairs"], Gr["snaps"])
        if flags is None:
            unk.extend(u2)
            continue
        pos = sorted(k for k, v in flags.items() if v)
        if pos:
            return {"disp": "COVERED", "depth": 0, "basis": "RotB24",
                    "mechanisms": pos, "rr": rr, "A": A, "Q": Q}
        unk.extend(u2)
    if unk:
        return {"disp": "INDETERMINATE", "why": "unknown-predicates",
                "unknown": sorted(set(unk))}
    return {"disp": "UNCOVERED", "why": "all-rotations-negative"}

def _splits(segs, i, n, mem):
    """All covered partitions of [i,n] via DFS; mem caches i -> list."""
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
        for (d2, rest) in _splits(segs, b, n, mem):
            out.append((max(ch["depth"], d2), [(a, b)] + rest))
    mem[i] = out
    return out

def coverA(start, word):
    key = (start, canon(word))
    if key in MEMOA:
        return MEMOA[key]
    CALLSA["n"] += 1
    if CALLSA["n"] > CAPA:
        CALLSA["hit"] = True
        r = {"disp": "INDETERMINATE", "why": "cap"}
        MEMOA[key] = r
        return r
    n = len(word)
    if n == 0:
        r = {"disp": "SOURCE-INVALID", "why": "empty-word"}
        MEMOA[key] = r
        return r
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"disp": _replay_class(e), "why": "replay-%s:%s" % (type(e).__name__, str(e)[:80])}
        MEMOA[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"disp": "SOURCE-INVALID", "why": "not-closed"}
        MEMOA[key] = r
        return r
    legs = Fr["legs"]
    totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
    b = baseA(start, word, Fr)
    if b["disp"] in ("COVERED", "INDETERMINATE"):
        b.update({"n": n, "A": totA, "Q": totQ})
        MEMOA[key] = b
        return b
    pairs = Fr["pairs"]
    segs = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            if j - i == n:
                continue
            if pairs[i] != pairs[j % n]:
                continue
            segs.append((i, j))
    if not segs:
        r = {"disp": "UNCOVERED", "why": "primitive-no-proper-segments",
             "n": n, "A": totA, "Q": totQ}
        MEMOA[key] = r
        return r
    mem = {}
    tainted = False
    for (a, b2) in segs:
        sw = [word[(t) % n] for t in range(a, b2)]
        ch = coverA(pairs[a], sw)
        mem[("c", a, b2)] = ch
        if ch["disp"] == "INDETERMINATE":
            tainted = True
    cands = _splits(segs, 0, n, mem)
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
                 "cuts": [p[0] for p in path] + [n],
                 "n": n, "A": totA, "Q": totQ, "additive": True}
            MEMOA[key] = r
            return r
        r = {"disp": "INDETERMINATE", "why": "additive-mismatch",
             "n": n, "A": totA, "Q": totQ}
        MEMOA[key] = r
        return r
    if tainted or CALLSA["hit"]:
        r = {"disp": "INDETERMINATE", "why": "tainted-or-cap",
             "n": n, "A": totA, "Q": totQ, "nsegments": len(segs)}
        MEMOA[key] = r
        return r
    r = {"disp": "UNCOVERED", "why": "no-covering-partition",
         "n": n, "A": totA, "Q": totQ, "nsegments": len(segs)}
    MEMOA[key] = r
    return r

def fresh():
    MEMOA.clear(); CALLSA["n"] = 0; CALLSA["hit"] = False
