# Cross-validation: independent checker vs RC engine verdicts + depths.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_PROOF_RCG0')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from PROOF_recursive_closure_check import cover2, MEMO2, CALLS
from RC_recursive_closure_engine import cover as coverRC, MEMO as MEMORC, BUDGET
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_PROOF_RCG0/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

WORDS = {
 "IN-new": ("D5,D4,D3,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
            "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"),
 "OUT": ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
         "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "old-IN": ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,"
            "K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"),
 "CONCAT": ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
            "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"),
}
# sample: 6 covered (incl non-anchored r!=0 + multi-part) + 6 residuals from audit
cc = [json.loads(l) for l in open(
    'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT/CRA_corpus_classification.jsonl')]
cov = [r for r in cc if r['status'] == 'CYCLIC-ADDITIVE-BANKED']
res = [r for r in cc if r['status'].startswith('CORRECTED')]
nonanch = [r for r in cov if r['decomp']['r'] != 0][:2]
multi = [r for r in cov if len(r['decomp']['cuts']) > 3][:1]
anch = [r for r in cov if r['decomp']['r'] == 0][:3]
for i, r in enumerate(nonanch + multi + anch):
    WORDS["sample-cov-%d" % i] = r['canon']
for i, r in enumerate(res[:6]):
    WORDS["sample-res-%d" % i] = r['canon']

if __name__ == "__main__":
    rows = []
    mismatch = []
    for name, cw in WORDS.items():
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"]
        MEMO2.clear(); CALLS.update({"n": 0, "hit": False})
        a = cover2(R["S0"], w)
        MEMORC.clear(); BUDGET.update({"used_subproblems": 0, "hit": False})
        b = coverRC(R["S0"], w)
        agree_v = (a.get("covered") == b.get("covered"))
        agree_d = (a.get("depth") == b.get("depth"))
        agree_i = (bool(a.get("indeterminate")) == bool(b.get("indeterminate")))
        rows.append({"name": name, "n": len(w),
                     "ind": (a.get("covered"), a.get("depth"), a.get("indeterminate")),
                     "rc": (b.get("covered"), b.get("depth"), b.get("indeterminate")),
                     "agree_verdict": agree_v, "agree_depth": agree_d,
                     "agree_ind": agree_i,
                     "calls_ind": CALLS["n"]})
        print("%s: ind=%s rc=%s %s" % (
            name, (a.get("covered"), a.get("depth")),
            (b.get("covered"), b.get("depth")),
            "AGREE" if agree_v and agree_d and agree_i else "MISMATCH"), flush=True)
        if not (agree_v and agree_d and agree_i):
            mismatch.append(name)
    json.dump({"rows": rows, "mismatch": mismatch,
               "agree": not mismatch},
              open(PDIR + "PROOF_cross_validation.json", "w"), indent=1, default=str)
    print("CROSSVAL:", "PASS" if not mismatch else "FAIL %s" % mismatch, flush=True)
    sys.exit(0 if not mismatch else 1)
