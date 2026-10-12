# Bank25 regression: 384 corpus words under corrected cyclic-origin checker.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay
from GLOB_recursive_checker import coverC, fresh, bank25_checked

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR/'
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
    for cs in sorted(bycanon):
        w = parse(cs)
        R = replay(w)
        if not (R["S1"] == R["S0"] and R["agree"]):
            raise SystemExit("validity changed")
        fb, unk = bank25_checked(R["legs"], R["pairs"], R["snaps"])
        direct = sorted(k for k, v in fb.items() if v) if fb is not None else []
        if direct:
            cats["DIRECT-BANKED"] += 1
            for m in direct:
                mechs[m] += 1
            continue
        if unk:
            cats["INDETERMINATE"] += 1
            continue
        fresh()
        cov = coverC(R["S0"], w)
        if cov["disp"] == "COVERED":
            cats["CYCLIC-ADDITIVE-BANKED"] += 1
        elif cov["disp"] == "INDETERMINATE":
            cats["INDETERMINATE"] += 1
        else:
            cats["RESIDUAL"] += 1
    rec = {"rows": len(rows), "distinct": len(bycanon), "cats": dict(cats),
           "direct_by_mech": dict(mechs), "indeterminate": cats.get("INDETERMINATE", 0)}
    json.dump(rec, open(PDIR + "GLOB_corpus_regression.json", "w"), indent=1, default=str)
    print("CORPUS:", rec["cats"], flush=True)
    print("SELR flags:", mechs.get("SELR", 0), "ZULR:", mechs.get("ZULR", 0), flush=True)
    if cats.get("INDETERMINATE", 0) != 0 or cats.get("RESIDUAL", 0) != 0:
        raise SystemExit("REGRESSION FAILURE")
    print("REGRESSION DONE", flush=True)
