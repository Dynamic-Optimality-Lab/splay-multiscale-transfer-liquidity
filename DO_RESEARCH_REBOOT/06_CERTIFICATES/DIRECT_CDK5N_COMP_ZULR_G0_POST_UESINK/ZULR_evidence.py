# ZULR IN/OUT evidence bundle: full replay + intervals + strict dispositions
# + recursive negative certificates. All values recomputed from source.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from ZULR_recursive import cover23, bank23, MEMO23, CALLS23
from ZULR_membership import strict_zulr
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_strict_msink_membership import intervals, strict_K, strict_P

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
WORDS = {
 "IN": ("593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9",
        "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
 "OUT": ("8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd",
         "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
}
if __name__ == "__main__":
    for name, (sha, cw) in WORDS.items():
        assert hashlib.sha256(cw.encode("ascii")).hexdigest() == sha, name
        w = parse(cw)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"], name
        tot = totals(R["legs"])
        gk = sorted({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]})
        cores = []
        for ps in R["pairs"]:
            c = core_of(ps[1])
            assert c is not None and len(c) == 9, name
            cores.append(len(c))
        n = len(w)
        pre = R["pairs"][:-1]
        reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n) if pre[a] == pre[b]])
        iv = intervals(R["legs"])
        sm = strict_zulr(R["legs"])
        fb = bank23(R["legs"], R["pairs"], R["snaps"])
        MEMO23.clear(); CALLS23.update({"n": 0, "hit": False})
        cov = cover23(R["S0"], w)
        replay_rec = {"sha": sha, "canon": cw, "tot": tot, "gkeys": gk,
                      "cores9": True, "nboundaries": n + 1, "preclosure": n,
                      "distinct": len(set(pre)), "repeats": reps,
                      "legs": [{"m": l["m"], "x": l["x"], "dA": l["dA"], "dB": l["dB"],
                                "a": l["a"], "q": l["q"], "chg": l["chg"]} for l in R["legs"]],
                      "iv": [{"x": v["x"], "H": v["H"], "c": v["c"], "q": v["q"],
                              "w": v["w"], "R": v["R"], "dA": R["legs"][v["gi"]]["dA"],
                              "K": strict_K(v, R["legs"]), "P": strict_P(v, R["legs"])}
                             for v in iv],
                      "strict": {"member": sm["member"], "E": sm["E"],
                                 "p": sm.get("p"), "stage": sm["stage"],
                                 "pos": sm["pos"]},
                      "direct": sorted(k for k, v in fb.items() if v)}
        json.dump(replay_rec, open(PDIR + "ZULR_%s_replay.json" % name, "w"), indent=1, default=str)
        neg_rec = {"sha": sha, "covered": cov.get("covered"),
                   "indeterminate": cov.get("indeterminate"),
                   "depth": cov.get("depth"),
                   "repeats": reps, "subproblems": CALLS23["n"],
                   "neg": cov.get("neg"),
                   "A": cov.get("A"), "Q": cov.get("Q")}
        json.dump(neg_rec, open(PDIR + "ZULR_%s_negative_certificate.json" % name, "w"), indent=1, default=str)
        print("%s: A=%d Q=%d Ck=%d distinct=%d/%d E=%s strict=%s direct=%s covered=%s ind=%s subs=%d" % (
            name, tot["A"], tot["Q"], tot["Ck"], len(set(pre)), n, sm["E"],
            sm["member"], replay_rec["direct"], cov.get("covered"),
            cov.get("indeterminate"), CALLS23["n"]), flush=True)
        assert cov.get("covered") is False and not cov.get("indeterminate"), name
    print("EVIDENCE: PASS", flush=True)
