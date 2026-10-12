# GLOB rotation-aware C25* checker (§10): Rot base every level + every cyclic
# origin for additive decomposition. Dispositions COVERED/UNCOVERED/
# INDETERMINATE/SOURCE-INVALID. Unknowns/caps never negatives. No asserts.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from RC_recursive_closure_engine import replay_from, canon

MEMOC = {}
CALLSC = {"n": 0, "hit": False}
CAPC = 60000

def _coerce(name, val, unknown):
    if isinstance(val, bool):
        return val
    unknown.append("%s:%r" % (name, val))
    return None

def bank25_checked(legs, pairs, snaps):
    from CRA_segment_memberships import full_banked
    from DLSS_membership import strict_msink_bank
    from UESINK_membership import strict_dlss_bank
    from ZULR_membership import strict_uesink_bank
    from SELR_membership import strict_zulr_bank, strict_selr
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
    try:
        from CRA_segment_memberships import genuine_keys, core_of
        if len(genuine_keys(legs)) != 5:
            out["SELR"] = False
        else:
            bad = False
            for ps in pairs:
                c = core_of(ps[1])
                if c is None or len(c) != 9:
                    bad = True
                    break
            out["SELR"] = False if bad else bool(strict_selr(legs)["member"])
            if not isinstance(out["SELR"], bool):
                unknown.append("SELR:%r" % out["SELR"])
                del out["SELR"]
    except Exception as e:
        unknown.append("SELR:%s" % type(e).__name__)
    return out, unknown

def _replay_class(err):
    if type(err).__name__ == "ReplayError" and "absent" in str(err):
        return "SOURCE-INVALID"
    return "INDETERMINATE"

def base25_cover(word, Fr):
    """Rotation-aware base over all n rotations with true starts."""
    n = len(word)
    pairs = Fr["pairs"]
    unk_all = []
    nrots = 0
    for rr in range(n):
        bstart = pairs[rr]
        rword = [word[(rr + t) % n] for t in range(n)]
        try:
            Gr = replay_from(bstart, rword)
        except Exception as e:
            return {"disp": "INDETERMINATE", "why": "rotation-replay-%s" % type(e).__name__, "rr": rr}
        if Gr["pairs"][-1] != bstart:
            return {"disp": "INDETERMINATE", "why": "rotation-not-closed", "rr": rr}
        nrots += 1
        legs = Gr["legs"]
        A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
        if A == 0 and Q == 0 and len({l["x"] for l in legs}) == 1:
            return {"disp": "COVERED", "depth": 0, "basis": "Z", "rr": rr, "A": A, "Q": Q, "rots": nrots}
        if A == 0:
            unk_all.append("rr%d:Z-fail" % rr)
            continue
        flags, unk = bank25_checked(legs, Gr["pairs"], Gr["snaps"])
        if flags is None:
            unk_all.extend(unk)
            continue
        pos = sorted(k for k, v in flags.items() if v)
        if pos:
            return {"disp": "COVERED", "depth": 0, "basis": "RotB25",
                    "mechanisms": pos, "rr": rr, "A": A, "Q": Q, "rots": nrots}
        unk_all.extend(unk)
    if unk_all:
        return {"disp": "INDETERMINATE", "why": "unknown-predicates",
                "unknown": sorted(set(unk_all)), "rots": nrots}
    return {"disp": "UNCOVERED", "why": "all-rotations-negative", "rots": nrots}

def coverC(start, word):
    key = (start, canon(word))
    if key in MEMOC:
        return MEMOC[key]
    CALLSC["n"] += 1
    if CALLSC["n"] > CAPC:
        CALLSC["hit"] = True
        r = {"disp": "INDETERMINATE", "why": "cap"}
        MEMOC[key] = r
        return r
    n = len(word)
    if n == 0:
        r = {"disp": "SOURCE-INVALID", "why": "empty-word"}
        MEMOC[key] = r
        return r
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"disp": _replay_class(e), "why": "replay-%s:%s" % (type(e).__name__, str(e)[:80])}
        MEMOC[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"disp": "SOURCE-INVALID", "why": "not-closed"}
        MEMOC[key] = r
        return r
    legs = Fr["legs"]
    totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
    b = base25_cover(word, Fr)
    if b["disp"] in ("COVERED", "INDETERMINATE"):
        b.update({"n": n, "A": totA, "Q": totQ})
        MEMOC[key] = b
        return b
    # Cyclic-origin decomposition: every rotation frame's segments/partitions.
    pairs = Fr["pairs"]
    tainted = False
    for rr in range(n):
        bstart = pairs[rr]
        rword = [word[(rr + t) % n] for t in range(n)]
        try:
            Gr = replay_from(bstart, rword)
        except Exception:
            tainted = True
            continue
        if Gr["pairs"][-1] != bstart:
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
        cov = {}
        for (i, j) in segs:
            sw = [rword[(t) % n] for t in range(i, j)]
            ch = coverC(gp[i], sw)
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
        if n in reach:
            path = [n]; cur = n
            while cur > 0:
                cur = prev[cur]
                path.append(cur)
            path = sorted(path)
            if len(path) - 1 >= 2:
                sA = 0; sQ = 0
                kids = []
                for ii, jj in zip(path[:-1], path[1:]):
                    sw = [rword[(t) % n] for t in range(ii, jj)]
                    k = coverC(gp[ii], sw)
                    kids.append(k); sA += k["A"]; sQ += k["Q"]
                if sA == totA and sQ == totQ:
                    dd = max(k["depth"] for k in kids) + 1
                    r = {"disp": "COVERED", "depth": dd, "basis": "additive",
                         "frame": rr, "cuts": path, "n": n, "A": totA, "Q": totQ,
                         "additive": True}
                    MEMOC[key] = r
                    return r
                r = {"disp": "INDETERMINATE", "why": "additive-mismatch",
                     "n": n, "A": totA, "Q": totQ}
                MEMOC[key] = r
                return r
    if tainted or CALLSC["hit"]:
        r = {"disp": "INDETERMINATE", "why": "tainted-or-cap",
             "n": n, "A": totA, "Q": totQ}
        MEMOC[key] = r
        return r
    r = {"disp": "UNCOVERED", "why": "no-frame-partition",
         "n": n, "A": totA, "Q": totQ, "rots": b.get("rots")}
    MEMOC[key] = r
    return r

def fresh():
    MEMOC.clear(); CALLSC["n"] = 0; CALLSC["hit"] = False
