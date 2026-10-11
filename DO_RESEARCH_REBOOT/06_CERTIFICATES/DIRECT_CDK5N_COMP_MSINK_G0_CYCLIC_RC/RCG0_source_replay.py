# RCG0 fresh source verifier (task L): RC replay_from lockstep from T0 +
# full L-checks for both witnesses. Fail-closed (RCFailClosedError).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from, canon
from CRA_pointer_tuple_replay import totup, MSET, core_of, T0
from CRA_strict_msink_membership import intervals, E_slots, relay_len, strict_K, strict_P

class RCFailClosedError(ValueError):
    pass

def check(cond, msg):
    if not cond:
        raise RCFailClosedError(msg)
    return True

IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
            "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
IN_SHA = "788b459d061ed11693490727d48bd4a1a86e7627c1b889390db6914f0efd6d0a"
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"

def ser_of(tup):
    from CRA_pointer_tuple_replay import iserial
    return iserial(tup)

def verify(name, cw, sha, exp):
    check(hashlib.sha256(cw.encode("ascii")).hexdigest() == sha, "SHA %s" % name)
    w = [(t[0], int(t[1:])) for t in cw.split(",")]
    check(len(w) == exp["n"], "n %s" % name)
    S0 = (ser_of(totup(__import__("copy").deepcopy(T0))),
          ser_of(totup(__import__("copy").deepcopy(T0))))
    R = replay_from(S0, w)
    legs = R["legs"]
    check(R["pairs"][-1] == S0, "closure %s" % name)
    t = {"A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
    ks = [l["x"] for l in legs if l["m"] == "K"]
    t["Ck"] = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    check((t["A"], t["Q"], t["Ck"]) == (exp["A"], exp["Q"], exp["Ck"]),
          "totals %s %s" % (name, t))
    gk = sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})
    check(gk == [1, 3, 5, 7, 9], "gkeys %s" % name)
    for ps in R["pairs"]:
        c = core_of(ps[1])
        check(c is not None and len(c) == 9, "core9 %s" % name)
    iv = intervals(legs)
    check(sum(v["H"] for v in iv) == t["A"], "sumH %s" % name)
    check(sum(v["q"] for v in iv) == t["Q"], "sumq %s" % name)
    check(sum(v["c"] for v in iv) == t["Ck"], "sumc %s" % name)
    check(all(v["H"] >= v["c"] for v in iv), "baseline %s" % name)
    check(max(v["q"] for v in iv) <= 4, "qbound %s" % name)
    E = E_slots(iv)
    check(E == exp["E"], "E %s %s" % (name, E))
    tl = {e: relay_len(iv, e) for e in E}
    check(tl == exp["t"], "relays %s %s" % (name, tl))
    pos = []
    for j in range(len(iv)):
        if iv[j]["w"] > 0:
            pos.append({"j": j, "x": iv[j]["x"], "H": iv[j]["H"],
                        "c": iv[j]["c"], "q": iv[j]["q"], "w": iv[j]["w"],
                        "R": iv[j]["R"], "dA": legs[iv[j]["gi"]]["dA"],
                        "K": strict_K(iv[j], legs),
                        "P": strict_P(iv[j], legs)})
    return {"tot": dict(t, n=len(w)), "E": E, "t": tl, "pos": pos,
            "iv": [(v["x"], v["H"], v["c"], v["q"], v["w"], v["R"]) for v in iv]}

if __name__ == "__main__":
    out = {}
    out["IN"] = verify("IN", IN_CANON, IN_SHA,
                       {"n": 36, "A": 64, "Q": 36, "Ck": 16,
                        "E": [4, 12], "t": {4: 0, 12: 2}})
    out["OUT"] = verify("OUT", OUT_CANON, OUT_SHA,
                        {"n": 34, "A": 55, "Q": 36, "Ck": 16,
                         "E": [4, 12], "t": {4: 2, 12: 2}})
    json.dump(out, open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC/RCG0_source_replay_results.json', "w"), indent=1, default=str)
    print("IN:", out["IN"]["tot"], "E:", out["IN"]["E"], "t:", out["IN"]["t"], flush=True)
    print("OUT:", out["OUT"]["tot"], "E:", out["OUT"]["E"], "t:", out["OUT"]["t"], flush=True)
    print("REPLAY: PASS", flush=True)
