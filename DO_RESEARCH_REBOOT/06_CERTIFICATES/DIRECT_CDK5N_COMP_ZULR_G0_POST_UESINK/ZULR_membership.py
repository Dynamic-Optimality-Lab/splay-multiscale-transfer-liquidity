# ZULR strict H1–H6 membership (fresh; zero-exception + unique self-payer).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from CRA_strict_msink_membership import intervals, strict_K, strict_P, E_slots

def strict_zulr(legs):
    iv = intervals(legs)
    s = len(iv)
    E = E_slots(iv)
    res = {"s": s, "E": E, "member": False, "p": None, "pos": [],
           "stage": None}
    if len(E) != 0:
        res["stage"] = "E-nonempty-%d" % len(E)
        return res
    U = [j for j in range(s)
         if iv[j]["w"] > 0 and not strict_K(iv[j], legs)
         and not strict_P(iv[j], legs)]
    if len(U) != 1:
        res["stage"] = "U-count-%d" % len(U)
        return res
    p = U[0]
    if not (iv[p]["H"] >= 2):
        res["stage"] = "p-H-short-%d" % iv[p]["H"]
        return res
    for j in range(s):
        if j == p or iv[j]["w"] <= 0:
            continue
        if strict_K(iv[j], legs) or strict_P(iv[j], legs):
            continue
        res["stage"] = "other-untyped-%d" % j
        return res
    res["member"] = True
    res["p"] = p
    res["stage"] = "member"
    for j in range(s):
        if iv[j]["w"] > 0:
            res["pos"].append({"j": j, "x": iv[j]["x"], "H": iv[j]["H"],
                               "c": iv[j]["c"], "q": iv[j]["q"], "w": iv[j]["w"],
                               "R": iv[j]["R"], "dA": legs[iv[j]["gi"]]["dA"],
                               "K": strict_K(iv[j], legs),
                               "P": strict_P(iv[j], legs)})
    return res

def strict_uesink_bank(legs, pairs):
    """UESINK as banked domain (H1 five-genuine/core9 + H2-H5 exists)."""
    from CRA_segment_memberships import genuine_keys, core_of
    from UESINK_membership import strict_uesink as _ue
    if len(genuine_keys(legs)) != 5:
        return False
    for ps in pairs:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return False
    return _ue(legs)["member"]
