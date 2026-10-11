# ZULR driver: census-384, six-seed distance-zero, IN audit.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from ZULR_recursive import cover23, bank23, MEMO23, CALLS23
from ZULR_membership import strict_zulr
from CRA_pointer_tuple_replay import replay, totals, core_of

DDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK/'
def P(p):
    return DDIR + p
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,"
            "K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
EXIN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
              "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
EXDLSS_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,"
                "D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
EXCTL_CANON = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,"
               "D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
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
SEEDS = [("in", parse(IN_CANON), "593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9"),
         ("exin", parse(EXIN_CANON), "a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8"),
         ("exdlss", parse(EXDLSS_CANON), "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"),
         ("exctl", parse(EXCTL_CANON), "6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc"),
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
    fb = bank23(legs, R["pairs"], R["snaps"])
    direct = sorted(k for k, v in fb.items() if v)
    sm = strict_zulr(legs)
    pre = R["pairs"][:-1]
    reps = sorted([(a, b) for a in range(len(word)) for b in range(a + 1, len(word)) if pre[a] == pre[b]])
    return {"R": R, "tot": tot, "gkeys": gk, "cores": cores, "direct": direct,
            "strict": {"member": sm["member"], "E": sm["E"], "p": sm["p"],
                       "stage": sm["stage"], "pos": sm["pos"]},
            "repeats": reps, "primitive": len(reps) == 0}

def classify_role(rec, cov):
    if rec["strict"]["member"]:
        return "ZULR MEMBER — NOT OUT"
    if rec["direct"]:
        return "PREVIOUSLY BANKED — NOT OUT"
    if cov.get("covered"):
        return "RECURSIVE-COVERED — NOT OUT"
    if cov.get("indeterminate"):
        return "INDETERMINATE — BLOCKER"
    if len(rec["gkeys"]) != 5 or not all(c == 9 for c in rec["cores"]):
        return "OUTSIDE FIVE-KEY NINE-CORE — NOT OUT"
    return "RESIDUAL NON-ZULR — QUALIFYING OUT"

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "seeds"
    if mode == "seeds":
        out = {}
        for name, w, h in SEEDS:
            assert hashlib.sha256(canon(w).encode("ascii")).hexdigest() == h, name
            rec = full_record(w)
            MEMO23.clear(); CALLS23.update({"n": 0, "hit": False})
            cov = cover23(rec["R"]["S0"], w)
            role = classify_role(rec, cov)
            out[name] = {"sha": h, "tot": rec["tot"], "gkeys": rec["gkeys"],
                         "cores9": all(c == 9 for c in rec["cores"]),
                         "primitive": rec["primitive"], "direct": rec["direct"],
                         "strict": {k: v for k, v in rec["strict"].items() if k != "pos"},
                         "recursive": {"covered": cov.get("covered"),
                                       "depth": cov.get("depth"),
                                       "ind": cov.get("indeterminate"),
                                       "subs": CALLS23["n"]},
                         "role": role}
            print("%s: A=%d Q=%d Ck=%d prim=%s direct=%s strict=%s rec=%s ROLE=%s" % (
                name, rec["tot"]["A"], rec["tot"]["Q"], rec["tot"]["Ck"],
                rec["primitive"], rec["direct"], rec["strict"]["member"],
                cov.get("covered"), role), flush=True)
        json.dump(out, open(P("ZULR_distance_zero.json"), "w"), indent=1, default=str)
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
            fb = bank23(R["legs"], R["pairs"], R["snaps"])
            direct = sorted(k for k, v in fb.items() if v)
            if direct:
                cats["DIRECT-BANKED"] += 1
                details[canon_s] = {"status": "DIRECT-BANKED", "direct": direct}
                continue
            MEMO23.clear(); CALLS23.update({"n": 0, "hit": False})
            cov = cover23(R["S0"], w)
            if cov.get("covered"):
                cats["CYCLIC-ADDITIVE-BANKED"] += 1
                details[canon_s] = {"status": "CYCLIC-ADDITIVE-BANKED",
                                    "depth": cov.get("depth")}
            elif cov.get("indeterminate"):
                cats["INDETERMINATE"] += 1
                details[canon_s] = {"status": "INDETERMINATE"}
            else:
                sm = strict_zulr(R["legs"])
                cats["RESIDUAL"] += 1
                details[canon_s] = {"status": "RESIDUAL",
                                    "strict_zulr": sm["member"],
                                    "stage": sm["stage"]}
        print("CENSUS:", dict(cats), flush=True)
        from collections import Counter as _C2
        _db = _C2(); _depth = _C2()
        for canon_s, v in details.items():
            if v["status"] == "DIRECT-BANKED":
                for m in v["direct"]:
                    _db[m] += 1
            elif v["status"] == "CYCLIC-ADDITIVE-BANKED":
                _depth[v["depth"]] += 1
        print("DIRECT-BY-MECH:", dict(_db), flush=True)
        print("CYCLIC-DEPTHS:", dict(_depth), flush=True)
        json.dump({"cats": dict(cats), "details": details,
                   "direct_by_mech": dict(_db), "depths": dict(_depth)},
                  open(P("ZULR_post_uesink_census.json"), "w"), indent=1, default=str)
        print("CENSUS DONE", flush=True)
