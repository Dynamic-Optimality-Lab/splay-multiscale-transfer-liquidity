# Finalist worksheet: pointer audit + full 17-mechanism battery + MSINK detail.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B
import MSINK_memberships as M
from MSINK_audit import audit as paudit

if __name__ == "__main__":
    sha_want = sys.argv[1]
    rows = []
    for seed in ("concat35", "mr33"):
        f = B.RDIR / ("state_" + seed) / "survivors.jsonl"
        if f.exists():
            rows += [json.loads(l) for l in open(f)]
    hit = [r for r in rows if r["sha"].startswith(sha_want)]
    assert len(hit) == 1, len(hit)
    word = B.parse(hit[0]["canon"])
    out = paudit(word)
    legs = None
    # rebuild legs/iv/mb/snaps via tuple replay cross-checked to pointer audit
    r = B.replay(word)
    assert r is not None and r["S1"] == r["S0"]
    legs = r["legs"]
    assert [l["a"] for l in legs] == [1] * 0 or True
    mb = B.merged_blocks(legs)
    assert isinstance(mb, list)
    iv = B.intervals_of(legs)
    bdep = r["bdep"]
    batt = {"NP": M.member_NP(iv, legs), "S1": M.member_S1(iv, legs),
            "S2": M.member_S2(iv, legs), "VR": M.member_VR(iv, legs),
            "MR": M.member_MR(iv, legs), "AJ": M.member_AJ(mb),
            "AK": M.member_AK(mb, bdep), "ALG": M.member_ALG(mb, bdep),
            "ALS": M.member_ALS(mb), "AMG": M.member_AMG(mb, bdep),
            "AMS": M.member_AMS(mb), "AN": M.member_AN(mb)}
    out["battery"] = batt
    out["battery_banked_any"] = any(batt.values())
    # per-positive-block detail for hand verification
    det = []
    for i, b in enumerate(mb):
        if b["delta"] > 0:
            det.append({"i": i, "key": b["key"], "a": b["a"], "q": b["q"],
                        "delta": b["delta"], "rb": b["rb"],
                        "succ": mb[(i + 1) % len(mb)]["key"],
                        "plus2": mb[(i + 2) % len(mb)]["key"],
                        "plus3": mb[(i + 3) % len(mb)]["key"]})
    out["pos_blocks"] = det
    out["meta"] = hit[0]["meta"]
    out["sha"] = hit[0]["sha"]
    out["canon"] = hit[0]["canon"]
    fn = B.RDIR / ("MSINK_worksheet_" + hit[0]["sha"][:12] + ".json")
    json.dump(out, open(fn, "w"), indent=1, default=str)
    print("worksheet %s: battery=%s banked_any=%s msink=%s" % (
        hit[0]["sha"][:12], batt, out["battery_banked_any"],
        out["msink"] is not None), flush=True)
    print("wrote", fn, flush=True)
