# CRA corpus classification driver: regressions + 384-word census.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, pair_classes, core_of, MSET, ReplayError
from CRA_strict_msink_membership import strict_msink
from CRA_segment_memberships import full_banked, keep_support, genuine_keys
from CRA_cyclic_coverage_engine import cyclic_covers, oracle_selftest

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT/'
def P(p):
    return PDIR + p
def canon(w):
    return ",".join(m + str(k) for m, k in w)
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

IN_CANON = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,"
            "K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
CONCAT_CANON = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
                "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
NPW = ("D5,D4,K3,K7,K1,D4,K9,D6,K5,K7,K1,K9,D8,D2,D1,D6,D9")
S1W = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9")
S2W = ("D5,D4,K3,K7,D9,D5,K1,D4,K9,K5,K7,K1,K9,D8,D2,D1,D6,D9")
VRW = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
MRW = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
       "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

def classify(word, old_msink=None):
    rec = {}
    try:
        W = replay(word)
    except ReplayError as e:
        return {"status": "SOURCE-INVALID", "why": str(e)}
    n = len(word)
    tot = totals(W["legs"])
    rec["tot"] = tot
    if W["S1"] != W["S0"] or not W["agree"]:
        return {"status": "SOURCE-INVALID", "why": "non-closed-or-engines",
                "tot": tot}
    gk = genuine_keys(W["legs"])
    cores = []
    for ps in W["pairs"]:
        c = core_of(ps[1])
        cores.append(None if c is None else len(c))
    rec["gkeys"] = gk
    rec["cores9"] = all(c == 9 for c in cores)
    rec["mincore"] = min(c for c in cores if c is not None)
    if len(gk) != 5 or not rec["cores9"]:
        rec["w59"] = False
    else:
        rec["w59"] = True
    sm = strict_msink(W["legs"])
    rec["strict_msink"] = {"member": sm["member"], "E": sm["E"], "t": sm["t"],
                           "sinks": sm["sinks"], "stage": sm["stage"]}
    if old_msink is not None:
        rec["old_msink"] = old_msink
        rec["msink_discrepancy"] = (bool(old_msink) != sm["member"])
    fb = full_banked(W["legs"], W["pairs"], W["snaps"])
    if fb is None:
        return dict(rec, status="INDETERMINATE", why="battery-none")
    direct = sorted(k for k, v in fb.items() if v)
    rec["direct"] = direct
    if direct:
        return dict(rec, status="DIRECT-BANKED")
    cyc = cyclic_covers(word, W)
    rec["cyclic"] = {k: v for k, v in cyc.items() if k != "certificate"}
    rec["cyclic"]["ncerts"] = cyc.get("ncerts", 1 if cyc.get("covered") else 0)
    if cyc.get("covered"):
        cert = cyc["certificate"]
        rec["decomp"] = {"r": cert["r"], "cuts": cert["cuts"], "A": cert["A"],
                         "Q": cert["Q"], "additive": cert["additive"],
                         "parts": [{"bounds": p["bounds"],
                                    "why": p["why"], "A": p["A"], "Q": p["Q"],
                                    "canon": p.get("canon")} for p in cert["parts"]]}
        return dict(rec, status="CYCLIC-ADDITIVE-BANKED")
    if cyc.get("primitive"):
        rec["primitive"] = True
    if cyc.get("exhaustive") is False:
        return dict(rec, status="INDETERMINATE", why="segment-budget")
    if sm["member"]:
        return dict(rec, status="CORRECTED-RESIDUAL/STRICT-MSINK")
    return dict(rec, status="CORRECTED-RESIDUAL/NON-MSINK")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "regress"
    if mode == "oracle":
        T = oracle_selftest()
        bad = [t for t in T if not t[1]]
        for (nm, ok, got, want) in T:
            print("%s oracle-%s: %s" % ("PASS" if ok else "FAIL", nm, got), flush=True)
        print("ORACLE:", "PASS" if not bad else "FAIL %s" % bad, flush=True)
        sys.exit(0 if not bad else 1)
    if mode == "regress":
        # G1: IN must be CYCLIC-COVERED (S1 30/18 + VR 31/18)
        r = classify(parse(IN_CANON))
        print("IN status:", r["status"], flush=True)
        assert r["status"] == "CYCLIC-ADDITIVE-BANKED", r["status"]
        d = r["decomp"]
        print("IN decomp r=%s cuts=%s A=%s Q=%s" % (d["r"], d["cuts"], d["A"], d["Q"]), flush=True)
        for p in d["parts"]:
            print("  part", p, flush=True)
        assert (d["A"], d["Q"]) == (61, 36), (d["A"], d["Q"])
        tot1 = [(p["A"], p["Q"], p["why"]) for p in d["parts"]]
        assert ("S1" in d["parts"][0]["why"] or "S1" in str(d["parts"])) , d["parts"]
        # G2: CONCAT covered (anchored split 17)
        r2 = classify(parse(CONCAT_CANON))
        print("CONCAT status:", r2["status"], flush=True)
        assert r2["status"] == "CYCLIC-ADDITIVE-BANKED", r2["status"]
        # G3: OUT re premio — full record, no presumed PASS
        r3 = classify(parse(OUT_CANON))
        print("OUT status:", r3["status"], flush=True)
        print("OUT strict:", r3.get("strict_msink"), flush=True)
        print("OUT cyclic:", r3.get("cyclic"), flush=True)
        json.dump({"IN": r, "CONCAT": r2, "OUT": r3},
                  open(P("CRA_cyclic_coverage_regressions.json"), "w"), indent=1, default=str)
        # G4: banked controls positive
        for nm, cw, mech in (("NP", NPW, "NP"), ("S1", S1W, "S1"),
                             ("S2", S2W, "S2"), ("VR", VRW, "VR"),
                             ("MR", MRW, "MR")):
            rc = classify(parse(cw))
            print(nm, "status:", rc["status"], "direct:", rc.get("direct"), flush=True)
            assert rc["status"] == "DIRECT-BANKED" and mech in rc["direct"], (nm, rc.get("direct"))
        print("REGRESS: PASS", flush=True)
    if mode == "census":
        RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
        rows = []
        for seed in ("concat35", "mr33"):
            f = RDIR + ("state_" + seed) + "/survivors.jsonl"
            for l in open(f):
                rows.append((seed, json.loads(l)))
        bycanon = {}
        for seed, r in rows:
            bycanon.setdefault(r["canon"], []).append((seed, r))
        print("rows=%d distinct=%d" % (len(rows), len(bycanon)), flush=True)
        out = open(P("CRA_corpus_classification.jsonl"), "w")
        summary = {"rows": len(rows), "distinct": len(bycanon)}
        cats = {}
        n_old45 = 0
        for canon_s, provs in sorted(bycanon.items()):
            seed0, r0 = provs[0]
            old_ms = r0["msink"] is not None
            rec = classify(parse(canon_s), old_msink=old_ms)
            rec["sha"] = hashlib.sha256(canon_s.encode("ascii")).hexdigest()
            rec["canon"] = canon_s
            rec["provenance"] = [{"seed": s, "layer": r["meta"].get("layer"),
                                  "idx": r["meta"].get("idx"),
                                  "old_msink": r["msink"] is not None,
                                  "old_tot": r["tot"]} for s, r in provs]
            out.write(json.dumps(rec, default=str) + "\n")
            cats[rec["status"]] = cats.get(rec["status"], 0) + 1
        out.close()
        summary["categories"] = cats
        json.dump(summary, open(P("CRA_corpus_summary.json"), "w"), indent=1)
        print("CENSUS:", cats, flush=True)
