# DLSS strict H1-H6 membership (fresh; both-long relays; existential sink).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_strict_msink_membership import intervals, strict_K, strict_P, E_slots, relay_len

def strict_dlss(legs):
    iv = intervals(legs)
    s = len(iv)
    E = E_slots(iv)
    res = {"s": s, "E": E, "member": False, "sinks": [], "t": {},
           "pos": [], "stage": None}
    if len(E) != 2:
        res["stage"] = "E-count-%d" % len(E)
        return res
    tl = [relay_len(iv, e) for e in E]
    res["t"] = dict(zip(E, tl))
    if not (tl[0] >= 2 and tl[1] >= 2):
        res["stage"] = "relay-not-both-long-%s" % (tl,)
        return res
    for p in range(s):
        if p in E or not (iv[p]["c"] == 1 and iv[p]["H"] >= 3):
            continue
        jp = iv[p]
        if jp["q"] > 4 or not (jp["w"] <= jp["R"] - 2):
            continue
        ok = True
        for j in range(s):
            if j in E or j == p or iv[j]["w"] <= 0:
                continue
            if strict_K(iv[j], legs) or strict_P(iv[j], legs):
                continue
            ok = False
            break
        if ok:
            res["sinks"].append(p)
    if not res["sinks"]:
        res["stage"] = "no-joint-sink"
        return res
    res["member"] = True
    res["stage"] = "member"
    for j in range(s):
        if iv[j]["w"] > 0:
            res["pos"].append({"j": j, "x": iv[j]["x"], "H": iv[j]["H"],
                               "c": iv[j]["c"], "q": iv[j]["q"], "w": iv[j]["w"],
                               "R": iv[j]["R"], "dA": legs[iv[j]["gi"]]["dA"],
                               "K": strict_K(iv[j], legs),
                               "P": strict_P(iv[j], legs)})
    return res

def strict_msink_bank(legs, pairs):
    """MSINK as banked domain (H1 five-genuine/core9 + H2-H5 exists-sinks)."""
    from CRA_segment_memberships import genuine_keys, core_of
    if len(genuine_keys(legs)) != 5:
        return False
    for ps in pairs:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return False
    iv = intervals(legs)
    s = len(iv)
    E = [j for j in range(s)
         if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    if len(E) != 2:
        return False
    tl = [relay_len(iv, e) for e in E]
    if not ((tl[0] in (0, 1)) ^ (tl[1] in (0, 1))):
        return False
    for p in range(s):
        if p in E or not (iv[p]["c"] == 1 and iv[p]["H"] >= 3):
            continue
        jp = iv[p]
        if jp["q"] > 4 or not (jp["w"] <= jp["R"] - 2):
            continue
        ok = True
        for j in range(s):
            if j in E or j == p or iv[j]["w"] <= 0:
                continue
            if strict_K(iv[j], legs) or strict_P(iv[j], legs):
                continue
            ok = False
            break
        if ok:
            return True
    return False
