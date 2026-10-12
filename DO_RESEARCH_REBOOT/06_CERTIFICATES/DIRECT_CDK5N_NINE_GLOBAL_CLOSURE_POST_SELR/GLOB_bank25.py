# Bank25-backed C25* membership (global-closure baseline; SELR included).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from CRA_segment_memberships import full_banked
from DLSS_membership import strict_msink_bank
from UESINK_membership import strict_dlss_bank
from ZULR_membership import strict_uesink_bank
from SELR_membership import strict_zulr_bank, strict_selr

def strict_selr_bank(legs, pairs):
    from CRA_segment_memberships import genuine_keys, core_of
    if len(genuine_keys(legs)) != 5:
        return False
    for ps in pairs:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return False
    return strict_selr(legs)["member"]

def bank25(legs, pairs, snaps):
    fb = full_banked(legs, pairs, snaps)
    if fb is None:
        return None
    fb["MSINK"] = strict_msink_bank(legs, pairs)
    fb["DLSS"] = strict_dlss_bank(legs, pairs)
    fb["UESINK"] = strict_uesink_bank(legs, pairs)
    fb["ZULR"] = strict_zulr_bank(legs, pairs)
    fb["SELR"] = strict_selr_bank(legs, pairs)
    return fb

BANK25_NAMES = sorted(["RT2", "CDK4", "CDK5L", "NP", "S1", "S2", "VR", "MR",
                       "MSINK", "DLSS", "UESINK", "ZULR", "SELR", "AJ", "AK",
                       "ALG", "ALS", "AMG", "AMS", "AN", "AO", "AP", "AQ",
                       "AR", "AS"])
