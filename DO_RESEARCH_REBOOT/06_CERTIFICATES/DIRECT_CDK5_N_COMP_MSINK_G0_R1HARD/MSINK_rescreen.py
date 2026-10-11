# Batch re-screen of survivors through full battery (tuple-only; AS deferred).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B
import MSINK_memberships as M

if __name__ == "__main__":
    role = sys.argv[1]  # IN or OUT
    rows = []
    for seed in ("concat35", "mr33"):
        f = B.RDIR / ("state_" + seed) / "survivors.jsonl"
        if f.exists():
            for l in open(f):
                r = json.loads(l)
                rows.append((r["meta"].get("seed", "?"), r))
    # enumeration order: seed concat35 first, then layer, idx
    order = {"concat35": 0, "mr33": 1}
    rows.sort(key=lambda sr: (order.get(sr[0], 9),
                              str(sr[1]["meta"].get("layer")),
                              sr[1]["meta"].get("idx", 0)))
    shown = 0
    for seed, r in rows:
        is_ms = r["msink"] is not None
        if role == "IN" and not is_ms:
            continue
        if role == "OUT" and is_ms:
            continue
        if r["nsplits"] != 0 or r["np"]:
            continue
        if r["meta"].get("layer") == 0:
            continue
        word = B.parse(r["canon"])
        rp = B.replay(word)
        legs = rp["legs"]
        mb = B.merged_blocks(legs)
        iv = B.intervals_of(legs)
        lb = B.perleg_blocks(legs)
        u = B.union_exec(lb, mb)
        batt = {"NP": M.member_NP(iv, legs), "S1": M.member_S1(iv, legs),
                "S2": M.member_S2(iv, legs), "VR": M.member_VR(iv, legs),
                "MR": M.member_MR(iv, legs), "AJ": M.member_AJ(mb),
                "AK": M.member_AK(mb, rp["bdep"]),
                "ALG": M.member_ALG(mb, rp["bdep"]),
                "ALS": M.member_ALS(mb),
                "AMG": M.member_AMG(mb, rp["bdep"]),
                "AMS": M.member_AMS(mb), "AN": M.member_AN(mb)}
        flag = [k for k, v in list(u.items()) + list(batt.items()) if v]
        if not flag:
            print("CANDIDATE %s %s idx=%s A=%d Q=%d Ck=%d nE=%s" % (
                r["sha"][:12], seed, r["meta"].get("idx"),
                r["tot"]["A"], r["tot"]["Q"], r["tot"]["Ck"],
                r["eshape"]["nE"]), flush=True)
            shown += 1
            if shown >= 5:
                break
    if shown == 0:
        print("NO CANDIDATE for role %s" % role, flush=True)
