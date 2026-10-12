# SELRP rotation-aware C24* checker (proof stage; DP over pair-closed boundaries).
# Four dispositions: COVERED / UNCOVERED / INDETERMINATE / SOURCE-INVALID.
# Unknown theorem predicates propagate INDETERMINATE (never silent false).
# No assert controls any verdict (Erratum E). Shared primitives disclosed:
# replay_from/canon (RC engine), replay (CRA tuple replay), bank24 domain
# recognizers (Gate-0 SELR_membership + audited bank modules).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from RC_recursive_closure_engine import replay_from, canon

MEMOP = {}
CALLSP = {"n": 0, "hit": False}
CAPP = 60000

def _coerce(name, val, unknown):
    if isinstance(val, bool):
        return val
    unknown.append("%s:%r" % (name, val))
    return None

def bank24_checked(legs, pairs, snaps):
    """(flags|None, unknown:list). Exceptions/None/malformed -> unknown.
    Recognizers resolved dynamically each call so unavailability propagates
    (Erratum D); never silently coerced to false."""
    # Function-local imports: rebind every call (monkeypatch-visible).
    from CRA_segment_memberships import full_banked
    from DLSS_membership import strict_msink_bank
    from UESINK_membership import strict_dlss_bank
    from ZULR_membership import strict_uesink_bank
    from SELR_membership import strict_zulr_bank
    unknown = []
    try:
        fb = full_banked(legs, pairs, snaps)
    except Exception as e:
        return None, ["full_banked:%s" % type(e).__name__]
    if fb is None:
        return None, ["battery-none"]
    out = {}
    for k, v in fb.items():
        r = _coerce(k, v, unknown)
        if r is not None:
            out[k] = r
    for name, fn in (("MSINK", strict_msink_bank), ("DLSS", strict_dlss_bank),
                     ("UESINK", strict_uesink_bank), ("ZULR", strict_zulr_bank)):
        try:
            v = fn(legs, pairs)
        except Exception as e:
            unknown.append("%s:%s" % (name, type(e).__name__))
            continue
        r = _coerce(name, v, unknown)
        if r is not None:
            out[name] = r
    return out, unknown

def _replay_class(err):
    if type(err).__name__ == "ReplayError" and "absent" in str(err):
        return "SOURCE-INVALID"
    return "INDETERMINATE"

def base24_rot(start, word, Fr):
    """Rotation-aware base on replayed Fr (n>0, closed). Returns dict with
    disp in {COVERED, UNCOVERED, INDETERMINATE} + evidence."""
    n = len(word)
    pairs = Fr["pairs"]
    unk_all = []
    rots = []
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
            unk_all.append("rr%d:Z-fail" % rr)
            rots.append({"rr": rr, "A": A, "Q": Q, "flags": [], "unknown": ["Z-fail"]})
            continue
        flags, unk = bank24_checked(legs, Gr["pairs"], Gr["snaps"])
        if flags is None:
            unk_all.extend(unk)
            rots.append({"rr": rr, "A": A, "Q": Q, "flags": [], "unknown": unk})
            continue
        pos = sorted(k for k, v in flags.items() if v)
        rots.append({"rr": rr, "A": A, "Q": Q, "flags": pos, "unknown": unk})
        if pos:
            return {"disp": "COVERED", "depth": 0, "basis": "RotB24",
                    "mechanisms": pos, "rr": rr, "A": A, "Q": Q}
        unk_all.extend(unk)
    if unk_all:
        return {"disp": "INDETERMINATE", "why": "unknown-predicates",
                "unknown": sorted(set(unk_all)), "rots": len(rots)}
    return {"disp": "UNCOVERED", "why": "all-rotations-negative", "rots": len(rots)}

def coverP(start, word):
    key = (start, canon(word))
    if key in MEMOP:
        return MEMOP[key]
    CALLSP["n"] += 1
    if CALLSP["n"] > CAPP:
        CALLSP["hit"] = True
        r = {"disp": "INDETERMINATE", "why": "cap"}
        MEMOP[key] = r
        return r
    n = len(word)
    if n == 0:
        r = {"disp": "SOURCE-INVALID", "why": "empty-word"}
        MEMOP[key] = r
        return r
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"disp": _replay_class(e), "why": "replay-%s:%s" % (type(e).__name__, str(e)[:80])}
        MEMOP[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"disp": "SOURCE-INVALID", "why": "not-closed"}
        MEMOP[key] = r
        return r
    legs = Fr["legs"]
    totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
    b = base24_rot(start, word, Fr)
    if b["disp"] in ("COVERED", "INDETERMINATE"):
        b.update({"n": n, "A": totA, "Q": totQ})
        MEMOP[key] = b
        return b
    pairs = Fr["pairs"]
    pre = pairs[:-1]
    prim = len(set(pre)) == n
    segs = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            if j - i == n:
                continue
            a = i; bb = j % n
            if pairs[a] != pairs[bb]:
                continue
            segs.append((i, j))
    if not segs:
        r = {"disp": "UNCOVERED", "why": "primitive-no-proper-segments",
             "n": n, "A": totA, "Q": totQ, "primitive": prim,
             "rotations_checked": b.get("rots"), "nsegments": 0}
        MEMOP[key] = r
        return r
    # DP over boundaries with recursive child decisions
    cov = {}
    tainted = False
    for (i, j) in segs:
        a = i; bb = j % n
        sw = [word[(t) % n] for t in range(i, j)]
        ch = coverP(pairs[a], sw)
        if ch["disp"] == "INDETERMINATE":
            tainted = True
            cov[(i, j)] = None
        elif ch["disp"] == "COVERED":
            cov[(i, j)] = ch
        else:
            cov[(i, j)] = False
    reach = {0: -1}
    prev = {}
    for j in range(1, n + 1):
        best = None
        for i in range(j):
            if i not in reach:
                continue
            c = cov.get((i, j))
            if c is None or c is False:
                continue
            d = c["depth"] if reach[i] == -1 else max(reach[i], c["depth"])
            if best is None or d < best[0]:
                best = (d, i)
        if best is not None:
            reach[j] = best[0]
            prev[j] = best[1]
    # reconstruct a valid >=2-part partition
    if n in reach:
        path = [n]; cur = n
        while cur > 0:
            cur = prev[cur]
            path.append(cur)
        path = sorted(path)
        if len(path) - 1 >= 2:
            kids = []
            sA = 0; sQ = 0
            for ii, jj in zip(path[:-1], path[1:]):
                a = ii; bb = jj % n
                sw = [word[(t) % n] for t in range(ii, jj)]
                k = coverP(pairs[a], sw)
                kids.append(k); sA += k["A"]; sQ += k["Q"]
            if sA == totA and sQ == totQ:
                dd = max(k["depth"] for k in kids) + 1
                r = {"disp": "COVERED", "depth": dd, "basis": "additive",
                     "cuts": path, "n": n, "A": totA, "Q": totQ, "additive": True}
                MEMOP[key] = r
                return r
            r = {"disp": "INDETERMINATE", "why": "additive-mismatch",
                 "n": n, "A": totA, "Q": totQ}
            MEMOP[key] = r
            return r
    if tainted or CALLSP["hit"]:
        r = {"disp": "INDETERMINATE", "why": "tainted-or-cap",
             "n": n, "A": totA, "Q": totQ, "nsegments": len(segs)}
        MEMOP[key] = r
        return r
    r = {"disp": "UNCOVERED", "why": "no-covering-partition",
         "n": n, "A": totA, "Q": totQ, "primitive": prim,
         "rotations_checked": b.get("rots"), "nsegments": len(segs)}
    MEMOP[key] = r
    return r

def fresh():
    MEMOP.clear(); CALLSP["n"] = 0; CALLSP["hit"] = False
