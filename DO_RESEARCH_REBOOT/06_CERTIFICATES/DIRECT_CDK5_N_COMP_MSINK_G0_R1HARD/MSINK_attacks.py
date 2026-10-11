# MSINK 30-attack battery: single-DELETE removals + targeted hypothesis-breakers.
# PASS conditions: (i) every closed attack satisfies Q<=2A; (ii) wherever msink
# holds, the joint+local payment identities hold; (iii) no attack is both
# msink-clean Novel (that would be a second witness, not a contradiction --
# reported, not failed). Any Q>2A on a closed walk = HARD FAIL.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B
import MSINK_memberships as M

def assess(word):
    r = B.replay(word)
    if r is None:
        return {"replay": False}
    legs = r["legs"]
    tot = B.totals_of(legs)
    out = {"replay": True, "closed": r["S1"] == r["S0"], "A": tot["A"],
           "Q": tot["Q"], "Ck": tot["Ck"], "Qle2A": tot["Q"] <= 2 * tot["A"]}
    if not out["closed"]:
        return out
    gk = B.r5_status(r)
    out["R5"] = gk is not None
    mb = B.merged_blocks(legs)
    iv = B.intervals_of(legs)
    ms = B.msink(iv, legs)
    out["msink"] = ms is not None
    if ms is not None:
        sw = sum(v["w"] for v in iv); sR = sum(v["R"] for v in iv)
        out["pay_id"] = (sw == tot["Q"] - 2 * tot["Ck"]
                         and sR == 2 * (tot["A"] - tot["Ck"]) and sw <= sR)
    if gk is not None and isinstance(mb, list):
        lb = B.perleg_blocks(legs)
        u = B.union_exec(lb, mb)
        batt = {"NP": M.member_NP(iv, legs), "S1": M.member_S1(iv, legs),
                "S2": M.member_S2(iv, legs), "VR": M.member_VR(iv, legs),
                "MR": M.member_MR(iv, legs), "AJ": M.member_AJ(mb),
                "AK": M.member_AK(mb, r["bdep"]),
                "ALG": M.member_ALG(mb, r["bdep"]),
                "ALS": M.member_ALS(mb),
                "AMG": M.member_AMG(mb, r["bdep"]),
                "AMS": M.member_AMS(mb), "AN": M.member_AN(mb)}
        flag = [k for k, v in list(u.items()) + list(batt.items()) if v]
        out["banked_flag"] = flag
    return out

def load_word(prefix):
    rows = []
    for seed in ("concat35", "mr33"):
        f = B.RDIR / ("state_" + seed) / "survivors.jsonl"
        if f.exists():
            rows += [json.loads(l) for l in open(f)]
    hit = [x for x in rows if x["sha"].startswith(prefix)][0]
    return B.parse(hit["canon"]), hit["sha"]

if __name__ == "__main__":
    attacks = []
    for tag, prefix in (("IN", "19ff110a"), ("OUT", "b8b02be7")):
        word, sha = load_word(prefix)
        # A: all single-position DELETE removals
        for i, (m2, k) in enumerate(word):
            if m2 != "D":
                continue
            w2 = word[:i] + word[i + 1:]
            a = assess(w2)
            a["id"] = "%s-rm%d" % (tag, i)
            attacks.append(a)
        # B: targeted breakers
        dpos = [i for i, (m2, _) in enumerate(word) if m2 == "D"]
        # exception-key replacement: find first E-slot KEEP, change preceding DELETE key
        r = B.replay(word)
        iv = B.intervals_of(r["legs"])
        E = M.E_slots(iv)
        e0 = E[0]
        gi = iv[e0]["gi"]
        prev = None
        for k2 in iv[e0]["segi"]:
            if r["legs"][k2]["m"] == "D":
                prev = k2
                break
        if prev is not None:
            w2 = list(word); w2[prev] = ("D", 1 if word[prev][1] != 1 else 2)
            a = assess(w2); a["id"] = tag + "-excP"; attacks.append(a)
        # sink-region: replace a DELETE inside sink interval with another key
        ms = B.msink(iv, r["legs"])
        if ms is not None:
            p = ms["p"]
            hit2 = None
            for k2 in iv[p]["segi"]:
                if r["legs"][k2]["m"] == "D":
                    hit2 = k2
                    break
            if hit2 is not None:
                w2 = list(word); w2[hit2] = ("D", 9 if word[hit2][1] != 9 else 8)
                a = assess(w2); a["id"] = tag + "-sinkP"; attacks.append(a)
        # seam insertion
        w2 = list(word); w2.insert(0, ("D", 9))
        a = assess(w2); a["id"] = tag + "-seamI"; attacks.append(a)
        # swap two DELETE keys
        if len(dpos) >= 2:
            w2 = list(word)
            i1, i2 = dpos[0], dpos[-1]
            w2[i1], w2[i2] = ("D", w2[i2][1]), ("D", w2[i1][1])
            a = assess(w2); a["id"] = tag + "-swap"; attacks.append(a)
    hard_fail = [a for a in attacks
                 if a.get("replay") and a.get("closed") and not a.get("Qle2A")]
    pay_fail = [a for a in attacks
                if a.get("msink") and not a.get("pay_id", False)]
    closed_n = sum(1 for a in attacks if a.get("closed"))
    json.dump(attacks, open(B.RDIR / "MSINK_attacks.json", "w"), indent=1,
              default=str)
    print("attacks=%d closed=%d hard_fail=%d pay_fail=%d" % (
        len(attacks), closed_n, len(hard_fail), len(pay_fail)), flush=True)
    for a in attacks:
        if a.get("closed"):
            print("  %(id)s closed A=%(A)s Q=%(Q)s msink=%(msink)s banked=%(banked_flag)s" % a,
                  flush=True)
    print("ATTACKS:", "PASS" if not hard_fail and not pay_fail else "FAIL",
          flush=True)
    sys.exit(0 if not hard_fail and not pay_fail else 1)
