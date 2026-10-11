# UESINK strict H1-H6 membership (fresh; unique exception + long relay).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
from CRA_strict_msink_membership import intervals, strict_K, strict_P, E_slots, relay_len

def strict_uesink(legs):
    iv = intervals(legs)
    s = len(iv)
    E = E_slots(iv)
    res = {"s": s, "E": E, "member": False, "sinks": [], "t": {},
           "pos": [], "stage": None}
    if len(E) != 1:
        res["stage"] = "E-count-%d" % len(E)
        return res
    e = E[0]
    t = relay_len(iv, e)
    res["t"] = {e: t}
    if not (t >= 2):
        res["stage"] = "relay-short-%d" % t
        return res
    for p in range(s):
        if p == e or not (iv[p]["c"] == 1 and iv[p]["H"] >= 3):
            continue
        jp = iv[p]
        if jp["q"] > 4 or not (jp["w"] <= jp["R"] - 2):
            continue
        ok = True
        for j in range(s):
            if j == e or j == p or iv[j]["w"] <= 0:
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

def strict_dlss_bank(legs, pairs):
    """DLSS as banked domain (H1 five-genuine/core9 + H2-H5 exists-sinks:
    |E|==2, both relays long, joint sink. Exists over all p, like MSINK.)"""
    from CRA_segment_memberships import genuine_keys, core_of
    from CRA_strict_msink_membership import intervals as _iv, E_slots as _E, relay_len as _rl, strict_K as _K, strict_P as _P
    if len(genuine_keys(legs)) != 5:
        return False
    for ps in pairs:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return False
    iv = _iv(legs)
    s = len(iv)
    E = _E(iv)
    if len(E) != 2:
        return False
    tl = [_rl(iv, e) for e in E]
    if not (tl[0] >= 2 and tl[1] >= 2):
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
            if _K(iv[j], legs) or _P(iv[j], legs):
                continue
            ok = False
            break
        if ok:
            return True
    return False
