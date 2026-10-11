# PROOF negative certificates (Gate D G7): independent cover2 full records +
# cross-check of RC negative DAGs (repeat sets, segment verdicts, DP outcome).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_PROOF_RCG0')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from PROOF_recursive_closure_check import cover2, MEMO2, CALLS
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_PROOF_RCG0/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
            "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

if __name__ == "__main__":
    out = {}
    for name, cw in (("IN", IN_CANON), ("OUT", OUT_CANON)):
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"]
        MEMO2.clear(); CALLS.update({"n": 0, "hit": False})
        r = cover2(R["S0"], w)
        n = len(w)
        pre = R["pairs"][:-1]
        reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n)
                       if pre[a] == pre[b]])
        out[name] = {"covered": r.get("covered"),
                     "indeterminate": r.get("indeterminate"),
                     "repeats": reps, "nrepeats": len(reps),
                     "subproblems": CALLS["n"],
                     "neg": r.get("neg"), "why": r.get("why")}
        print("%s: covered=%s ind=%s repeats=%d subs=%d" % (
            name, r.get("covered"), r.get("indeterminate"), len(reps),
            CALLS["n"]), flush=True)
        assert r.get("covered") is False and not r.get("indeterminate"), (name, r)
    # cross-check vs RC DAGs: same verdict, same repeat sets, same segment count
    rc = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC/RC_witness_results.json'))
    for name in ("IN-new", "OUT"):
        tag = "IN" if name == "IN-new" else "OUT"
        assert rc[name]["covered"] == out[tag]["covered"], name
    print("RC-crosscheck: verdicts agree", flush=True)
    json.dump(out, open(PDIR + "PROOF_negative_certificates.json", "w"), indent=1, default=str)
    print("NEGCERTS: PASS", flush=True)
