# SELRP corpus regression: 384 words under corrected rotation-aware checker.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay
from SELRP_recursive_checker import coverP, fresh, bank24_checked

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

if __name__ == "__main__":
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ("concat35", "mr33"):
        for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r["canon"], []).append(r)
    if (len(rows), len(bycanon)) != (420, 384):
        raise SystemExit("corpus identity mismatch")
    from collections import Counter
    cats = Counter()
    mechs = Counter()
    depths = Counter()
    residuals = []
    unknowns = []
    for cs in sorted(bycanon):
        w = parse(cs)
        R = replay(w)
        if not (R["S1"] == R["S0"] and R["agree"]):
            raise SystemExit("corpus validity changed")
        flags, unk = bank24_checked(R["legs"], R["pairs"], R["snaps"])
        direct = sorted(k for k, v in flags.items() if v) if flags is not None else []
        if direct:
            cats["DIRECT-BANKED"] += 1
            for m in direct:
                mechs[m] += 1
            continue
        if unk:
            unknowns.append(cs[:24])
            cats["INDETERMINATE"] += 1
            continue
        fresh()
        cov = coverP(R["S0"], w)
        if cov["disp"] == "COVERED":
            cats["CYCLIC-ADDITIVE-BANKED"] += 1
            depths[cov.get("depth")] += 1
        elif cov["disp"] == "INDETERMINATE":
            cats["INDETERMINATE"] += 1
            unknowns.append(cs[:24])
        else:
            cats["RESIDUAL"] += 1
            residuals.append(cs[:24])
    rec = {"rows": len(rows), "distinct": len(bycanon), "cats": dict(cats),
           "direct_by_mech": dict(mechs), "cyclic_depths": dict(depths),
           "residuals": residuals, "unknowns": unknowns,
           "indeterminate": cats.get("INDETERMINATE", 0)}
    json.dump(rec, open(PDIR + "SELRP_corpus_regression.json", "w"), indent=1, default=str)
    print("CORPUS:", rec["cats"], flush=True)
    print("mechs:", dict(mechs), flush=True)
    if cats.get("INDETERMINATE", 0) != 0 or cats.get("RESIDUAL", 0) != 0:
        raise SystemExit("REGRESSION FAILURE: %s" % rec)
    print("REGRESSION DONE", flush=True)
