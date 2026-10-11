# RC regression + witness classification driver.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import cover, BUDGET, MEMO, canon
from CRA_pointer_tuple_replay import replay, totals

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC/'
IN_OLD = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,"
          "K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
IN_NEW = ("D5,D4,D3,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
          "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
OUT = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
       "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
CONCAT = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
          "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
NPW = ("D5,D4,K3,K7,K1,D4,K9,D6,K5,K7,K1,K9,D8,D2,D1,D6,D9")
S1W = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9")
S2W = ("D5,D4,K3,K7,D9,D5,K1,D4,K9,K5,K7,K1,K9,D8,D2,D1,D6,D9")
VRW = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
MRW = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
       "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def run(name, cw, expect_covered=None, max_depth=None):
    w = parse(cw)
    R = replay(w)
    assert R["S1"] == R["S0"] and R["agree"]
    t = totals(R["legs"])
    res = cover(R["S0"], w)
    line = {"name": name, "n": len(w), "tot": t,
            "covered": res.get("covered"), "depth": res.get("depth"),
            "indeterminate": res.get("indeterminate"),
            "subproblems": BUDGET["used_subproblems"]}
    print("%s: covered=%s depth=%s ind=%s A=%d Q=%d subs=%d" % (
        name, res.get("covered"), res.get("depth"), res.get("indeterminate"),
        t["A"], t["Q"], BUDGET["used_subproblems"]), flush=True)
    if expect_covered is not None:
        assert res.get("covered") == expect_covered, (name, res.get("covered"))
    if max_depth is not None and res.get("covered"):
        assert res["depth"] <= max_depth, (name, res["depth"])
    return res

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "regress"
    out = {}
    if mode == "regress":
        r = run("old-IN", IN_OLD, True, 1)
        out["old-IN"] = {"covered": r["covered"], "depth": r.get("depth"),
                         "cert": r.get("cert")}
        assert r["depth"] <= 1, r["depth"]
        r = run("CONCAT", CONCAT, True)
        out["CONCAT"] = {"covered": r["covered"], "depth": r.get("depth")}
        for nm, cw, mech in (("NP", NPW, "NP"), ("S1", S1W, "S1"),
                             ("S2", S2W, "S2"), ("VR", VRW, "VR"),
                             ("MR", MRW, "MR")):
            r = run(nm, cw, True, 0)
            assert r["depth"] == 0, (nm, r["depth"])
            out[nm] = {"covered": True, "depth": 0,
                       "mech": r["cert"]["mechanisms"]}
            assert mech in r["cert"]["mechanisms"], (nm, r["cert"])
        json.dump(out, open(PDIR + "RC_regressions.json", "w"), indent=1, default=str)
        print("REGRESS: PASS", flush=True)
    elif mode == "witnesses":
        MEMO.clear()
        BUDGET.update({"used_subproblems": 0, "hit": False})
        r = run("IN-new", IN_NEW)
        out["IN-new"] = r
        MEMO.clear()
        BUDGET.update({"used_subproblems": 0, "hit": False})
        r = run("OUT", OUT)
        out["OUT"] = r
        json.dump(out, open(PDIR + "RC_witness_results.json", "w"), indent=1, default=str)
        print("WITNESSES DONE", flush=True)
