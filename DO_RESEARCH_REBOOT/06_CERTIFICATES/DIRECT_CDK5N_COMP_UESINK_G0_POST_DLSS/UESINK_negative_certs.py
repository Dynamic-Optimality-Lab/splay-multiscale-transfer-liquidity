# UESINK negative recursive certificates (Gate E G7): full per-subproblem
# records for IN + OUT (rotations, closed segments, banked decisions,
# children, DP results). Verdicts cross-checked against census records.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from UESINK_recursive import cover22, MEMO22, CALLS22
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
WORDS = {
 "IN": "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
 "OUT": "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
}
if __name__ == "__main__":
    out = {}
    for name, cw in WORDS.items():
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"]
        MEMO22.clear(); CALLS22.update({"n": 0, "hit": False})
        r = cover22(R["S0"], w)
        n = len(w)
        pre = R["pairs"][:-1]
        reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n) if pre[a] == pre[b]])
        out[name] = {"covered": r.get("covered"),
                     "indeterminate": r.get("indeterminate"),
                     "repeats": reps, "subproblems": CALLS22["n"],
                     "neg": r.get("neg"),
                     "A": r.get("A"), "Q": r.get("Q")}
        print("%s: covered=%s ind=%s repeats=%d subs=%d" % (
            name, r.get("covered"), r.get("indeterminate"), len(reps),
            CALLS22["n"]), flush=True)
        assert r.get("covered") is False and not r.get("indeterminate"), name
    json.dump(out, open(PDIR + "UESINK_negative_certificates.json", "w"), indent=1, default=str)
    print("NEGCERTS: PASS", flush=True)
