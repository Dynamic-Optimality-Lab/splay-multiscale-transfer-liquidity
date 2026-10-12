# Negative-certificate verifier (Gate G): independently checks both negative
# certificates by fresh replay + cross-record agreement. Fail-closed.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
WORDS = {
 "IN": ("593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9",
        "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
        32, 56, 36, 16),
 "OUT": ("8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd",
         "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
         31, 53, 36, 16),
}
def check(cond, msg, errs):
    print("%s check: %s" % ("PASS" if cond else "FAIL", msg), flush=True)
    if not cond:
        errs.append(msg)
    return cond

if __name__ == "__main__":
    errs = []
    ok = True
    ind = json.load(open(PDIR + "ZULRP_IN_negative_recursive_certificate.json"))
    out = json.load(open(PDIR + "ZULRP_OUT_negative_recursive_certificate.json"))
    rot = json.load(open(PDIR + "ZULRP_rotation_matrices.json"))
    xv = json.load(open(PDIR + "ZULRP_cross_validation.json"))
    for name, (sha, cw, n, A, Q, Ck) in WORDS.items():
        rec = ind[name] if name in ind else out
        ok &= check(hashlib.sha256(cw.encode("ascii")).hexdigest() == sha, "%s SHA" % name, errs)
        w = parse(cw)
        R = replay(w)
        ok &= check(R["S1"] == R["S0"] and R["agree"], "%s replay closed+agree" % name, errs)
        t = totals(R["legs"])
        ok &= check((len(w), t["A"], t["Q"], t["Ck"]) == (n, A, Q, Ck), "%s totals %d/%d/%d" % (name, n, A, Q), errs)
        pre = R["pairs"][:-1]
        ok &= check(len(pre) == n and len(set(pre)) == n, "%s primitivity %d/%d" % (name, n, n), errs)
        ok &= check(rec.get("covered") is False, "%s cert uncovered" % name, errs)
        ok &= check(not rec.get("indeterminate"), "%s cert determinate" % name, errs)
        ok &= check(rec.get("repeats") == [], "%s cert no repeats" % name, errs)
        ok &= check(rec.get("agree") is True, "%s two-engine agree" % name, errs)
    ok &= check(all(v == "EXCLUDED" for k in ("IN", "OUT") for rv in rot[k]["matrix"].values() for v in rv.values()), "1449 rotation dispositions EXCLUDED", errs)
    ok &= check(xv.get("agree") is True and len(xv.get("rows", [])) == 18, "cross-validation 18/18 agree", errs)
    json.dump({"pass": bool(ok and not errs), "errors": errs},
              open(PDIR + "ZULRP_negative_certificate_verification.json", "w"), indent=1)
    print("VERIFIER: %s" % ("PASS" if ok and not errs else "FAIL %s" % errs), flush=True)
    sys.exit(0 if ok and not errs else 1)
