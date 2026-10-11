# UESINK fresh source replay (Gate A): independent pointer+tuple lockstep,
# 19 checks + primitivity census + strict interval dispositions.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_strict_msink_membership import intervals, strict_K, strict_P

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
WORDS = {
 "IN": ("a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8",
        "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "OUT": ("593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9",
         "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "CTL": ("6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc",
         "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
}
if __name__ == "__main__":
    out = {}
    for name, (sha, cw) in WORDS.items():
        assert hashlib.sha256(cw.encode("ascii")).hexdigest() == sha, name
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"], name
        tot = totals(R["legs"])
        gk = sorted({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]})
        assert gk == [1, 3, 5, 7, 9], name
        cores = []
        for ps in R["pairs"]:
            c = core_of(ps[1])
            assert c is not None and len(c) == 9, name
            cores.append(len(c))
        n = len(w)
        pre = R["pairs"][:-1]
        reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n) if pre[a] == pre[b]])
        iv = intervals(R["legs"])
        pos = [{"j": j, "x": v["x"], "H": v["H"], "c": v["c"], "q": v["q"],
                "w": v["w"], "R": v["R"], "dA": R["legs"][v["gi"]]["dA"],
                "K": strict_K(v, R["legs"]), "P": strict_P(v, R["legs"])}
               for j, v in enumerate(iv) if v["w"] > 0]
        E = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
        out[name] = {"sha": sha, "tot": tot, "gkeys": gk, "cores9": True,
                     "nboundaries": n + 1, "preclosure": n,
                     "distinct": len(set(pre)), "repeats": reps,
                     "E": E, "pos": pos,
                     "iv": [(v["x"], v["H"], v["c"], v["q"], v["w"], v["R"]) for v in iv]}
        print("%s: A=%d Q=%d Ck=%d distinct=%d/%d E=%s npos=%d" % (
            name, tot["A"], tot["Q"], tot["Ck"], len(set(pre)), n, E,
            len(pos)), flush=True)
    json.dump(out, open(PDIR + "UESINK_replay_results.json", "w"), indent=1, default=str)
    print("REPLAY: PASS", flush=True)
