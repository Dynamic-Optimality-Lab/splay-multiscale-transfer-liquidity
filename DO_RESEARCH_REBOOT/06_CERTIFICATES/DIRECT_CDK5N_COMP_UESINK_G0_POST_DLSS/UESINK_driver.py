# UESINK driver: census-384, seeds-5, IN audit.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from UESINK_recursive import cover22, bank22, MEMO22, CALLS22
from UESINK_membership import strict_uesink
from CRA_pointer_tuple_replay import replay, totals, core_of

DDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS/'
def P(p):
    return DDIR + p
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
            "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
CTL_CANON = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
S1W = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
VRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
MRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 5),
       ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9), ('D', 8),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 4),
       ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]
SEEDS = [("in", parse(IN_CANON), "a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8"),
         ("exIN", parse("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"), "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"),
         ("exCTL", parse(CTL_CANON), "6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc"),
         ("mr33", MRW, "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d"),
         ("concat35", S1W + VRW, "7b00897fab01764d14f0c98e6d07daf415839edff31b6f5e90eef93211418bfd")]

def full_record(word):
    R = replay(word)
    assert R["S1"] == R["S0"] and R["agree"]
    legs = R["legs"]
    tot = totals(legs)
    gk = sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})
    cores = []
    for ps in R["pairs"]:
        c = core_of(ps[1])
        cores.append(None if c is None else len(c))
    fb = bank22(legs, R["pairs"], R["snaps"])
    direct = sorted(k for k, v in fb.items() if v)
    sm = strict_uesink(legs)
    pre = R["pairs"][:-1]
    reps = sorted([(a, b) for a in range(len(word)) for b in range(a + 1, len(word)) if pre[a] == pre[b]])
    return {"R": R, "tot": tot, "gkeys": gk, "cores": cores, "direct": direct,
            "strict": {"member": sm["member"], "E": sm["E"], "t": sm["t"],
                       "sinks": sm["sinks"], "stage": sm["stage"], "pos": sm["pos"]},
            "repeats": reps, "primitive": len(reps) == 0}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "seeds"
    if mode == "seeds":
        out = {}
        for name, w, h in SEEDS:
            assert hashlib.sha256(canon(w).encode("ascii")).hexdigest() == h, name
            rec = full_record(w)
            MEMO22.clear(); CALLS22.update({"n": 0, "hit": False})
            cov = cover22(rec["R"]["S0"], w)
            pre = rec["R"]["pairs"][:-1]
            role = None
            if rec["strict"]["member"]:
                role = "UESINK MEMBER — NOT OUT"
            elif rec["direct"]:
                role = "PREVIOUSLY BANKED — NOT OUT"
            elif cov.get("covered"):
                role = "RECURSIVE-COVERED — NOT OUT"
            elif cov.get("indeterminate"):
                role = "INDETERMINATE — BLOCKER"
            elif len(rec["gkeys"]) != 5 or not all(c == 9 for c in rec["cores"]):
                role = "OUTSIDE FIVE-KEY NINE-CORE — NOT OUT"
            else:
                role = "RESIDUAL NON-UESINK — QUALIFYING OUT"
            out[name] = {"sha": h, "tot": rec["tot"], "gkeys": rec["gkeys"],
                         "cores9": all(c == 9 for c in rec["cores"]),
                         "primitive": rec["primitive"], "direct": rec["direct"],
                         "strict": {k: v for k, v in rec["strict"].items() if k != "pos"},
                         "recursive": {"covered": cov.get("covered"),
                                       "depth": cov.get("depth"),
                                       "ind": cov.get("indeterminate"),
                                       "subs": CALLS22["n"]},
                         "role": role}
            print("%s: A=%d Q=%d Ck=%d prim=%s direct=%s strict=%s rec=%s ROLE=%s" % (
                name, rec["tot"]["A"], rec["tot"]["Q"], rec["tot"]["Ck"],
                rec["primitive"], rec["direct"], rec["strict"]["member"],
                cov.get("covered"), role), flush=True)
        json.dump(out, open(P("UESINK_distance_zero.json"), "w"), indent=1, default=str)
        print("SEEDS DONE", flush=True)
    if mode == "census":
        RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
        rows = []
        for seed in ("concat35", "mr33"):
            f = RDIR + ("state_" + seed) + "/survivors.jsonl"
            for l in open(f):
                rows.append(json.loads(l))
        bycanon = {}
        for r in rows:
            bycanon.setdefault(r["canon"], []).append(r)
        print("rows=%d distinct=%d" % (len(rows), len(bycanon)), flush=True)
        from collections import Counter
        cats = Counter()
        details = {}
        for canon_s in sorted(bycanon):
            w = parse(canon_s)
            R = replay(w)
            assert R["S1"] == R["S0"] and R["agree"]
            fb = bank22(R["legs"], R["pairs"], R["snaps"])
            direct = sorted(k for k, v in fb.items() if v)
            if direct:
                cats["DIRECT-BANKED"] += 1
                details[canon_s] = {"status": "DIRECT-BANKED", "direct": direct}
                continue
            MEMO22.clear(); CALLS22.update({"n": 0, "hit": False})
            cov = cover22(R["S0"], w)
            if cov.get("covered"):
                cats["CYCLIC-ADDITIVE-BANKED"] += 1
                details[canon_s] = {"status": "CYCLIC-ADDITIVE-BANKED",
                                    "depth": cov.get("depth")}
            elif cov.get("indeterminate"):
                cats["INDETERMINATE"] += 1
                details[canon_s] = {"status": "INDETERMINATE"}
            else:
                sm = strict_uesink(R["legs"])
                cats["RESIDUAL"] += 1
                details[canon_s] = {"status": "RESIDUAL",
                                    "strict_ues": sm["member"],
                                    "stage": sm["stage"]}
        print("CENSUS:", dict(cats), flush=True)
        from collections import Counter as _C2
        _db = _C2(); _depth = _C2(); _sm = 0
        for canon_s, v in details.items():
            if v["status"] == "DIRECT-BANKED":
                for m in v["direct"]:
                    _db[m] += 1
            elif v["status"] == "CYCLIC-ADDITIVE-BANKED":
                _depth[v["depth"]] += 1
        print("DIRECT-BY-MECH:", dict(_db), flush=True)
        print("CYCLIC-DEPTHS:", dict(_depth), flush=True)
        json.dump({"cats": dict(cats), "details": details},
                  open(P("UESINK_post_dlss_census.json"), "w"), indent=1, default=str)
        print("CENSUS DONE", flush=True)
