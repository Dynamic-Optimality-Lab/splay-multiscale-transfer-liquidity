# DLSS census + distance-zero driver: post-MSINK 384-word reclassification,
# IN/control replay, four-seed baseline audit.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from DLSS_recursive import cover21, bank21, MEMO21, CALLS21
from DLSS_membership import strict_dlss
from CRA_pointer_tuple_replay import replay, totals, core_of
from RC_recursive_closure_engine import replay_from

DDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK/'
def P(p):
    return DDIR + p
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
            "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
CTL_CANON = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

def full_word_record(word):
    R = replay(word)
    assert R["S1"] == R["S0"] and R["agree"]
    n = len(word)
    tot = totals(R["legs"])
    gk = sorted({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]})
    cores = []
    for ps in R["pairs"]:
        c = core_of(ps[1])
        cores.append(None if c is None else len(c))
    fb = bank21(R["legs"], R["pairs"], R["snaps"])
    direct = sorted(k for k, v in fb.items() if v)
    sm = strict_dlss(R["legs"])
    return {"R": R, "tot": tot, "gkeys": gk, "cores": cores, "direct": direct,
            "strict": {"member": sm["member"], "E": sm["E"], "t": sm["t"],
                       "sinks": sm["sinks"], "stage": sm["stage"]}}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "seeds"
    if mode == "seeds":
        # Exact seed words (banked fixtures; SHAs frozen below, no substitutes)
        S1W = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1),
               ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9),
               ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]
        VRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1),
               ('D', 9), ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1),
               ('K', 9), ('D', 8), ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
        MRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1),
               ('D', 9), ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1),
               ('K', 9), ('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5),
               ('K', 1), ('D', 9), ('D', 8), ('K', 9), ('K', 5), ('K', 7),
               ('K', 1), ('K', 9), ('D', 8), ('D', 4), ('D', 2), ('D', 5),
               ('D', 6), ('D', 1), ('D', 9)]
        for nm, w, h in (("S1W", S1W, "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"),
                         ("VRW", VRW, "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"),
                         ("MRW", MRW, "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d")):
            assert hashlib.sha256(canon(w).encode("ascii")).hexdigest() == h, nm
        seeds = {"IN": parse(IN_CANON), "CTL": parse(CTL_CANON),
                 "mr33": MRW, "concat35": S1W + VRW}
        exp = {"IN": ("b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3", 55, 36, 16, 34),
               "CTL": ("6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc", 55, 36, 16, 34)}
        out = {}
        for name, w in seeds.items():
            rec = full_word_record(w)
            h = hashlib.sha256(canon(w).encode("ascii")).hexdigest()
            MEMO21.clear(); CALLS21.update({"n": 0, "hit": False})
            cov = cover21(rec["R"]["S0"], w)
            pre = rec["R"]["pairs"][:-1]
            prim = (len(set(pre)) == len(w))
            role = None
            if rec["strict"]["member"]:
                role = "DLSS MEMBER — NOT OUT"
            elif rec["direct"]:
                role = "PREVIOUSLY BANKED — NOT OUT"
            elif cov.get("covered"):
                role = "RECURSIVE-COVERED — NOT OUT"
            elif cov.get("indeterminate"):
                role = "INDETERMINATE — BLOCKER"
            elif len(rec["gkeys"]) != 5 or not all(c == 9 for c in rec["cores"]):
                role = "OUTSIDE FIVE-KEY NINE-CORE — NOT OUT"
            else:
                role = "RESIDUAL NON-DLSS — QUALIFYING OUT"
            out[name] = {"sha": h, "tot": rec["tot"], "gkeys": rec["gkeys"],
                         "cores9": all(c == 9 for c in rec["cores"]),
                         "primitive": prim, "direct": rec["direct"],
                         "strict": rec["strict"],
                         "recursive": {"covered": cov.get("covered"),
                                       "depth": cov.get("depth"),
                                       "ind": cov.get("indeterminate"),
                                       "subs": CALLS21["n"]},
                         "role": role}
            print("%s: sha=%s A=%d Q=%d Ck=%d prim=%s direct=%s strict=%s rec=%s ROLE=%s" % (
                name, h[:12], rec["tot"]["A"], rec["tot"]["Q"], rec["tot"]["Ck"],
                prim, rec["direct"], rec["strict"]["member"],
                cov.get("covered"), role), flush=True)
            if name in exp:
                assert h == exp[name][0], name
                assert (rec["tot"]["A"], rec["tot"]["Q"], rec["tot"]["Ck"], len(w)) == exp[name][1:], name
        json.dump(out, open(P("DLSS_distance_zero.json"), "w"), indent=1, default=str)
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
        msink_flip = 0
        dlss_members = 0
        for canon_s in sorted(bycanon):
            w = parse(canon_s)
            R = replay(w)
            assert R["S1"] == R["S0"] and R["agree"]
            fb = bank21(R["legs"], R["pairs"], R["snaps"])
            direct = sorted(k for k, v in fb.items() if v)
            sm = strict_dlss(R["legs"])
            if sm["member"]:
                dlss_members += 1
            if direct:
                cats["DIRECT-BANKED"] += 1
                details[canon_s] = {"status": "DIRECT-BANKED", "direct": direct}
                if "MSINK" in direct:
                    msink_flip += 1
                continue
            MEMO21.clear(); CALLS21.update({"n": 0, "hit": False})
            cov = cover21(R["S0"], w)
            if cov.get("covered"):
                cats["CYCLIC-ADDITIVE-BANKED"] += 1
                details[canon_s] = {"status": "CYCLIC-ADDITIVE-BANKED",
                                    "depth": cov.get("depth")}
            elif cov.get("indeterminate"):
                cats["INDETERMINATE"] += 1
                details[canon_s] = {"status": "INDETERMINATE"}
            else:
                cats["RESIDUAL"] += 1
                details[canon_s] = {"status": "RESIDUAL",
                                    "strict_dlss": sm["member"],
                                    "stage": sm["stage"]}
        print("CENSUS:", dict(cats), flush=True)
        print("MSINK-direct flips:", msink_flip, "strict-DLSS members:", dlss_members, flush=True)
        json.dump({"cats": dict(cats), "msink_flip": msink_flip,
                   "dlss_members": dlss_members, "details": details},
                  open(P("DLSS_post_msink_census.json"), "w"), indent=1, default=str)
        print("CENSUS DONE", flush=True)
