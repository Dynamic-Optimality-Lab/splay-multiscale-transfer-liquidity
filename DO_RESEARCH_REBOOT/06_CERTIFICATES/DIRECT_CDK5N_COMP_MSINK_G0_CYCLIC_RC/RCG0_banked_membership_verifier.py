# RCG0 banked membership verifier: exact 20-mechanism battery on witnesses,
# controls, and RT2/CDK4/CDK5L/AJ-AS positive paths.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from, canon
from CRA_pointer_tuple_replay import totup, T0
from CRA_segment_memberships import full_banked, m_RT2, m_CDK4, m_CDK5L, ASm
import copy

def ser_of(t):
    from CRA_pointer_tuple_replay import iserial
    return iserial(t)

IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
            "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
NPW = ("D5,D4,K3,K7,K1,D4,K9,D6,K5,K7,K1,K9,D8,D2,D1,D6,D9")
S1W = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9")
S2W = ("D5,D4,K3,K7,D9,D5,K1,D4,K9,K5,K7,K1,K9,D8,D2,D1,D6,D9")
VRW = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
MRW = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
       "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

def S0():
    return (ser_of(totup(copy.deepcopy(T0))), ser_of(totup(copy.deepcopy(T0))))

def batt(cw):
    w = [(t[0], int(t[1:])) for t in cw.split(",")]
    R = replay_from(S0(), w)
    assert R["pairs"][-1] == S0()
    n = len(w)
    snaps = {t: R["snaps"][t] for t in range(n)}
    fb = full_banked(R["legs"], R["pairs"], snaps)
    return sorted(k for k, v in fb.items() if v), R

if __name__ == "__main__":
    out = {}
    bi, _ = batt(IN_CANON)
    out["IN"] = {"direct": bi}
    print("IN direct:", bi, flush=True)
    assert bi == [], bi
    bo, _ = batt(OUT_CANON)
    out["OUT"] = {"direct": bo}
    print("OUT direct:", bo, flush=True)
    assert bo == [], bo
    for nm, cw, mech in (("NP", NPW, "NP"), ("S1", S1W, "S1"),
                         ("S2", S2W, "S2"), ("VR", VRW, "VR"),
                         ("MR", MRW, "MR")):
        b, _ = batt(cw)
        out[nm] = b
        print(nm, "direct:", b, flush=True)
        assert mech in b, (nm, b)
    # RT2 positive paths (real closed micro-walks)
    for nm, w in (("RT2-D9", [('D', 9)]), ("RT2-K9x2", [('K', 9), ('K', 9)])):
        R = replay_from(S0(), w)
        assert R["pairs"][-1] == S0()
        from CRA_segment_memberships import m_RT2
        assert m_RT2(R["legs"], R["pairs"])
        out[nm] = True
        print(nm, "RT2 True", flush=True)
    # CDK4/CDK5L predicate-True paths (synth legs + valid serials)
    def LG(x, a, q, chg):
        return {'m': 'K', 'x': x, 'dA': 2 * a - 1, 'a': a, 'q': q, 'chg': chg}
    from CRA_segment_memberships import m_CDK4, m_CDK5L
    assert m_CDK4([LG(1, 1, 0, False), LG(3, 1, 0, False),
                   LG(5, 1, 0, False), LG(7, 1, 0, False)], [])
    assert not m_CDK4([LG(1, 1, 0, False), LG(3, 1, 0, False),
                       LG(5, 1, 0, False), LG(7, 1, 0, False),
                       LG(9, 1, 0, False)], [])
    T = (5, (3, (1, '.', (2, '.', '.')), (4, '.', '.')),
         (7, (6, '.', '.'), (9, (8, '.', '.'), '.')))
    legs5 = [LG(k, 1, 0, True) for k in (1, 3, 5, 7, 9)]
    assert m_CDK5L(legs5, [(T, T)] * 2)
    assert not m_CDK5L(legs5[:4], [(T, T)] * 2)
    out["CDK4-synth"] = True
    out["CDK5L-synth"] = True
    print("CDK4/CDK5L synth True-paths PASS", flush=True)
    # AJ-AS positives: banked synth battery (Gate-0 selftest logic on RC imports)
    def SB(key, a, q, genuine, dB, rb, keeps, l1=1):
        return {"key": key, "keys": [key], "a": a, "q": q, "delta": q - 2 * a,
                "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps,
                "dA": 2 * a - 1, "push": [], "l0": l1 - 1, "l1": l1, "nleg": 1}
    from CRA_segment_memberships import (m_AJ, m_AK, m_ALS, m_AMG, m_AMS, m_AN)
    sn = {0: {1: 2, 6: 0, 7: 3}}
    assert m_AJ([SB(6, 1, 3, True, 7, 1, [6]), SB(1, 2, 1, True, 2, 6, [1])])
    assert m_AK([SB(6, 1, 3, True, 7, 1, [6], 1), SB(7, 1, 0, True, 0, 6, [7], 2),
                 SB(1, 2, 1, True, 2, 6, [1], 3)], sn)
    assert m_AN([SB(6, 1, 3, True, 7, 1, [6]), SB(4, 1, 1, True, 2, 6, [4]),
                 SB(2, 1, 3, True, 7, 4, [2]), SB(1, 2, 2, True, 4, 2, [1])])
    def ASsynth(key, keys, a, q, genuine, dB, rb, keeps, dA, push=None, l0=0, l1=1):
        return ASm.synth(key, keys, a, q, genuine, dB, rb, keeps, dA, push, l0, l1)
    as1 = [ASsynth(1, [1], 1, 3, True, 7, 9, [1], 2, [], 0, 1),
           ASsynth(5, [5], 1, 0, False, None, 5, [], 1, [], 1, 2),
           ASsynth(3, [3], 1, 3, True, 6, 2, [3], 2, [], 2, 3),
           ASsynth(4, [4], 1, 1, True, 2, 1, [4], 1, [9, 2], 3, 4),
           ASsynth(9, [9], 1, 0, True, 2, 5, [9], 1, [], 4, 5),
           ASsynth(2, [2], 2, 1, True, 2, 4, [2], 3, [], 5, 6)]
    assert ASm.recognize(as1, {2: {9: 2, 2: 2}})["accepted"]
    out["AJ-AK-AN-AS-synth"] = True
    print("AJ/AK/AN/AS synth positives PASS", flush=True)
    # AO/AP/AQ/AR witness ACCEPTs through RC-loaded banked modules
    import json as J
    ao = J.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO/26AO_ten_key_witness_certificate.json'))
    from CRA_segment_memberships import AO, AP, AQ, AR
    ao_lb = [{"key": l["x"], "keys": [l["x"]], "a": l["a"], "q": l["q"],
              "delta": l["delta"], "genuine": bool(l["bchanged"]),
              "dB": l["dB"], "rb": l["rb"],
              "keeps": [l["x"]] if l["m"] == "K" else []} for l in ao["legs"]]
    assert AO.recognize(ao_lb) is not None
    for tag, path in (("AP", 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/26AP_vine16_witness_certificate.json'),
                      ("AQ", 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ/26AQ_vine16_witness_certificate.json')):
        cert = J.load(open(path))
        assert (AP if tag == "AP" else AQ).recognize(cert["blocks"])["accepted"]
    arc = J.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AR/26AR_vine16_closed_witness.json'))
    assert AR.recognize(AR.enrich(arc["blocks"], arc["legs"]))["accepted"]
    out["AO-AP-AQ-AR-witness"] = True
    print("AO/AP/AQ/AR witness ACCEPTs PASS", flush=True)
    json.dump(out, open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC/RCG0_banked_results.json', "w"), indent=1, default=str)
    print("BANKED: PASS", flush=True)
