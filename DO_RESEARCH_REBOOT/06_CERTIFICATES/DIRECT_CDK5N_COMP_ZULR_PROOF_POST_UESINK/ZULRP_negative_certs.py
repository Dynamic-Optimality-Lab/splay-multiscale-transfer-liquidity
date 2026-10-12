# IN/OUT negative recursive certificates (Gate G): full per-subproblem
# records from the independent checker + RC-cross-check agreement.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from ZULRP_independent_recursive_checker import coverI, MEMOI, CALLSI
from ZULR_recursive import cover23, MEMO23, CALLS23
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
WORDS = {
 "IN": "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
 "OUT": "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
}
if __name__ == "__main__":
    out = {}
    for name, cw in WORDS.items():
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"]
        n = len(w)
        pre = R["pairs"][:-1]
        reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n) if pre[a] == pre[b]])
        MEMOI.clear(); CALLSI.update({"n": 0, "hit": False})
        a = coverI(R["S0"], w)
        MEMO23.clear(); CALLS23.update({"n": 0, "hit": False})
        b = cover23(R["S0"], w)
        assert (a.get("covered"), bool(a.get("indeterminate"))) == (False, False), (name, "IND")
        assert (b.get("covered"), bool(b.get("indeterminate"))) == (False, False), (name, "RC")
        assert a.get("covered") == b.get("covered"), name
        out[name] = {"covered": False, "repeats": reps,
                     "ind_subproblems": CALLSI["n"], "rc_subproblems": CALLS23["n"],
                     "ind_neg": a.get("neg"), "agree": True,
                     "A": a.get("A"), "Q": a.get("Q")}
        print("%s: uncovered both; ind-subs=%d rc-subs=%d repeats=%d" % (
            name, CALLSI["n"], CALLS23["n"], len(reps)), flush=True)
    json.dump(out, open(PDIR + "ZULRP_negative_certificates.json", "w"), indent=1, default=str)
    json.dump(out["IN"], open(PDIR + "ZULRP_IN_negative_recursive_certificate.json", "w"), indent=1, default=str)
    json.dump(out["OUT"], open(PDIR + "ZULRP_OUT_negative_recursive_certificate.json", "w"), indent=1, default=str)
    print("NEGCERTS: PASS", flush=True)
