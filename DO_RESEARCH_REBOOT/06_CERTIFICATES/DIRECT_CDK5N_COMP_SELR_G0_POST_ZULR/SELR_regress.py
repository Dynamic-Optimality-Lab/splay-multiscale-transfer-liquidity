# SELR corpus regression: 384 archived words under bank-24, fresh run.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from SELR_recursive import cover24, MEMO24, CALLS24, bank24
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

if __name__ == "__main__":
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ("concat35", "mr33"):
        f = RDIR + ("state_" + seed) + "/survivors.jsonl"
        for l in open(f):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r["canon"], []).append(r)
    assert (len(rows), len(bycanon)) == (420, 384)
    from collections import Counter
    cats = Counter()
    mechs = Counter()
    depths = Counter()
    residuals = []
    for canon_s in sorted(bycanon):
        w = parse(canon_s)
        R = replay(w)
        assert R["S1"] == R["S0"] and R["agree"]
        fb = bank24(R["legs"], R["pairs"], R["snaps"])
        direct = sorted(k for k, v in fb.items() if v)
        if direct:
            cats["DIRECT-BANKED"] += 1
            for m in direct:
                mechs[m] += 1
            continue
        MEMO24.clear(); CALLS24["n"] = 0; CALLS24["hit"] = False
        cov = cover24(R["S0"], w)
        if cov.get("covered"):
            cats["CYCLIC-ADDITIVE-BANKED"] += 1
            depths[cov.get("depth")] += 1
        elif cov.get("indeterminate"):
            cats["INDETERMINATE"] += 1
        else:
            cats["RESIDUAL"] += 1
            residuals.append(canon_s[:24])
    rec = {"rows": len(rows), "distinct": len(bycanon), "cats": dict(cats),
           "direct_by_mech": dict(mechs), "cyclic_depths": dict(depths),
           "residuals": residuals, "indeterminate": cats.get("INDETERMINATE", 0)}
    json.dump(rec, open(PDIR + "SELR_regressions.json", "w"), indent=1, default=str)
    print("CORPUS:", rec["cats"], "mechs:", dict(mechs), "depths:", dict(depths), flush=True)
    assert cats.get("INDETERMINATE", 0) == 0
    assert cats.get("RESIDUAL", 0) == 0, residuals
    print("REGRESSION DONE", flush=True)
