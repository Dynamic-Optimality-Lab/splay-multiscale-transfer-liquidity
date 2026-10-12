# SELR strict H1-H6 membership + bank24 domain assembly (Gate-0, post-ZULR).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from CRA_strict_msink_membership import intervals, strict_K, strict_P, E_slots

def relay_len(iv, e):
    """Maximal cyclic successor run after e with c=1,H=1,q<=2."""
    s = len(iv)
    t = 0
    j = (e + 1) % s
    while t < s and iv[j]["c"] == 1 and iv[j]["H"] == 1 and iv[j]["q"] <= 2:
        t += 1
        j = (j + 1) % s
    return t

def strict_selr(legs):
    iv = intervals(legs)
    s = len(iv)
    E = E_slots(iv)
    res = {"s": s, "E": E, "member": False, "e": None, "p": None,
           "t": None, "pos": [], "stage": None}
    U = [j for j in range(s)
         if iv[j]["w"] > 0 and not strict_K(iv[j], legs)
         and not strict_P(iv[j], legs)]
    res["U"] = U
    if len(E) != 1:
        res["stage"] = "E-count-%d" % len(E)
        return res
    e = E[0]
    t = relay_len(iv, e)
    if t not in (0, 1):
        res["stage"] = "relay-%d" % t
        return res
    if e not in U:
        res["stage"] = "U-missing-e-%s" % (U,)
        return res
    others = [j for j in U if j != e]
    if len(others) != 1:
        res["stage"] = "U-shape-%s" % (U,)
        return res
    p = others[0]
    if not (iv[p]["c"] == 1 and iv[p]["q"] == 3 and iv[p]["H"] >= 2):
        res["stage"] = "donor-shape-c%dq%dH%d" % (iv[p]["c"], iv[p]["q"], iv[p]["H"])
        return res
    for j in range(s):
        if j == e or j == p or iv[j]["w"] <= 0:
            continue
        if strict_K(iv[j], legs) or strict_P(iv[j], legs):
            continue
        res["stage"] = "other-untyped-%d" % j
        return res
    res["member"] = True
    res["e"] = e
    res["p"] = p
    res["t"] = t
    res["U"] = U
    res["stage"] = "member"
    for j in range(s):
        if iv[j]["w"] > 0:
            res["pos"].append({"j": j, "x": iv[j]["x"], "H": iv[j]["H"],
                               "c": iv[j]["c"], "q": iv[j]["q"], "w": iv[j]["w"],
                               "R": iv[j]["R"], "dA": legs[iv[j]["gi"]]["dA"],
                               "K": strict_K(iv[j], legs),
                               "P": strict_P(iv[j], legs)})
    return res

def strict_zulr_bank(legs, pairs):
    """ZULR as banked domain (H1 five-genuine/core9 + strict_zulr)."""
    from CRA_segment_memberships import genuine_keys, core_of
    from ZULR_membership import strict_zulr as _zu
    if len(genuine_keys(legs)) != 5:
        return False
    for ps in pairs:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return False
    return _zu(legs)["member"]

def bank24(legs, pairs, snaps):
    """Complete 24-mechanism bank: full_banked(20) + MSINK/DLSS/UESINK/ZULR."""
    from CRA_segment_memberships import full_banked
    from DLSS_membership import strict_msink_bank
    from UESINK_membership import strict_dlss_bank
    from ZULR_membership import strict_uesink_bank
    fb = full_banked(legs, pairs, snaps)
    if fb is None:
        return None
    fb["MSINK"] = strict_msink_bank(legs, pairs)
    fb["DLSS"] = strict_dlss_bank(legs, pairs)
    fb["UESINK"] = strict_uesink_bank(legs, pairs)
    fb["ZULR"] = strict_zulr_bank(legs, pairs)
    return fb

BANK24_NAMES = sorted(["RT2", "CDK4", "CDK5L", "NP", "S1", "S2", "VR", "MR",
                       "MSINK", "DLSS", "UESINK", "ZULR", "AJ", "AK", "ALG",
                       "ALS", "AMG", "AMS", "AN", "AO", "AP", "AQ", "AR", "AS"])
