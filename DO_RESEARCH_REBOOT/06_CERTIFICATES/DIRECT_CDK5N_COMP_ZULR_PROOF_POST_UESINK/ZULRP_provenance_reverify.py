# Proof-stage provenance re-verification: first-5 L1 candidates + OUT through
# the proof-stage battery (replay, strict ZULR, bank-23 direct, coverI).
# Read-only wrt history (reads committed parents file; writes here only).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from ZULRP_independent_recursive_checker import coverI, MEMOI, CALLSI, bank23i
from ZULR_membership import strict_zulr
from CRA_pointer_tuple_replay import replay, totals, core_of

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

if __name__ == "__main__":
    pars = [l.rstrip("\n") for l in open(
        'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK/zsearch_in/parents_L1.txt') if l.strip()]
    assert len(pars) == 425, len(pars)
    out = {"nparents": len(pars), "cands": []}
    for k in range(5):
        op, c = pars[k].split(" ", 1)
        w = parse(c)
        rec = {"idx": k, "op": op, "sha": hashlib.sha256(c.encode("ascii")).hexdigest()}
        try:
            R = replay(w)
        except Exception as e:
            rec["disp"] = "non-closed"
            rec["why"] = "replay-%s" % e
            out["cands"].append(rec)
            print("idx%d %s non-closed (replay)" % (k, op), flush=True)
            continue
        if R["S1"] != R["S0"] or not R["agree"]:
            rec["disp"] = "non-closed"
            out["cands"].append(rec)
            print("idx%d %s non-closed" % (k, op), flush=True)
            continue
        rec["tot"] = totals(R["legs"])
        gk = sorted({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]})
        if len(gk) != 5 or any(not (lambda cc: cc is not None and len(cc) == 9)(core_of(p[1])) for p in R["pairs"]):
            rec["disp"] = "non-R5"
            out["cands"].append(rec)
            print("idx%d %s non-R5" % (k, op), flush=True)
            continue
        sm = strict_zulr(R["legs"])
        if sm["member"]:
            rec["disp"] = "ZULR-member"
            out["cands"].append(rec)
            print("idx%d %s ZULR-member" % (k, op), flush=True)
            continue
        fb = bank23i(R["legs"], R["pairs"], R["snaps"])
        flags = sorted(key for key, v in fb.items() if v)
        if flags:
            rec["disp"] = "banked"
            rec["flags"] = flags
            out["cands"].append(rec)
            print("idx%d %s banked %s" % (k, op, flags), flush=True)
            continue
        MEMOI.clear(); CALLSI.update({"n": 0, "hit": False})
        cov = coverI(R["S0"], w)
        if cov.get("indeterminate"):
            rec["disp"] = "INDETERMINATE"
            out["cands"].append(rec)
            print("idx%d %s INDETERMINATE" % (k, op), flush=True)
            continue
        if cov.get("covered"):
            rec["disp"] = "recursive-covered"
            out["cands"].append(rec)
            print("idx%d %s recursive-covered" % (k, op), flush=True)
            continue
        rec["disp"] = "OUT-HOPEFUL"
        rec["strict_stage"] = sm["stage"]
        out["cands"].append(rec)
        print("idx%d %s OUT-HOPEFUL" % (k, op), flush=True)
    json.dump(out, open(PDIR + "ZULRP_provenance_reverification.json", "w"), indent=1, default=str)
    disp = [c["disp"] for c in out["cands"]]
    ok = disp == ["non-closed", "non-closed", "banked", "ZULR-member", "OUT-HOPEFUL"]
    print("PROVENANCE-REVERIFY: %s %s" % ("PASS" if ok else "FAIL", disp), flush=True)
    sys.exit(0 if ok else 1)
