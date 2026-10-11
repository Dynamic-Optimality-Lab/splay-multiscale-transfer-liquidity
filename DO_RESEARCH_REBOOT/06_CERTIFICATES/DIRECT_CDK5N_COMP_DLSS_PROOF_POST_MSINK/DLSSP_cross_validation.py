# Cross-validation: independent checker vs DLSS_recursive cover21.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
from DLSSP_independent_recursive_checker import coverP, MEMOP, CALLSP
from DLSS_recursive import cover21, MEMO21, CALLS21
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
WORDS = {
 "IN": ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
        "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "OUT": ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
         "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "CTL": ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,"
         "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "old-IN": ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,"
            "K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"),
 "CONCAT": ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
            "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"),
 "NP": ("D5,D4,K3,K7,K1,D4,K9,D6,K5,K7,K1,K9,D8,D2,D1,D6,D9"),
 "S1": ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9"),
 "S2": ("D5,D4,K3,K7,D9,D5,K1,D4,K9,K5,K7,K1,K9,D8,D2,D1,D6,D9"),
 "VR": ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"),
 "MR": ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
        "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
}
cc = [json.loads(l) for l in open(
    'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT/CRA_corpus_classification.jsonl')]
cov = [r for r in cc if r['status'] == 'CYCLIC-ADDITIVE-BANKED']
res = [r for r in cc if r['status'].startswith('CORRECTED')]
for i, r in enumerate((cov[:4] + res[:4])):
    WORDS["sample-%d" % i] = r['canon']

if __name__ == "__main__":
    rows = []
    mismatch = []
    for name, cw in WORDS.items():
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"]
        MEMOP.clear(); CALLSP.update({"n": 0, "hit": False})
        a = coverP(R["S0"], w)
        MEMO21.clear(); CALLS21.update({"n": 0, "hit": False})
        b = cover21(R["S0"], w)
        av = (a.get("covered"), a.get("depth"), bool(a.get("indeterminate")))
        bv = (b.get("covered"), b.get("depth"), bool(b.get("indeterminate")))
        ok = av == bv
        rows.append({"name": name, "n": len(w), "ind": av, "rc": bv,
                     "agree": ok, "calls": CALLSP["n"]})
        print("%s: ind=%s rc=%s %s" % (name, av, bv, "AGREE" if ok else "MISMATCH"), flush=True)
        if not ok:
            mismatch.append(name)
    json.dump({"rows": rows, "mismatch": mismatch, "agree": not mismatch},
              open(PDIR + "DLSSP_cross_validation.json", "w"), indent=1, default=str)
    print("XVAL:", "PASS" if not mismatch else "FAIL %s" % mismatch, flush=True)
    sys.exit(0 if not mismatch else 1)
