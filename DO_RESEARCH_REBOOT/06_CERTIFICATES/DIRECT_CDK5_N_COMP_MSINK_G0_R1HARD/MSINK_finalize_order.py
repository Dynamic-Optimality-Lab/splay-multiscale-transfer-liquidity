# C+F: predecessor eligibility audit with segment analysis (original predicates).
# Order: concat35 L0, concat35 L1[0..], mr33 L0, mr33 L1[0..].
# Eligibility (NO nsplits/np triage): valid+closed+R5+msink-role+16clean(incl AS)+seg-clean.
import sys, json, itertools
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B
import MSINK_memberships as M
from MSINK_finalize_verify import pointer_replay, sliced_products, part_covered, MSET

def exists_sinks(iv, legs):
    s = len(iv)
    E = [j for j in range(s)
         if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    if len(E) != 2:
        return None, []
    tl = []
    for e in E:
        k = 1
        while k < s:
            j = (e + k) % s
            if iv[j]["c"] == 1 and iv[j]["H"] == 1 and iv[j]["q"] <= 2:
                k += 1
            else:
                break
        tl.append(k - 1)
    if not ((tl[0] in (0, 1)) ^ (tl[1] in (0, 1))):
        return E, []
    out = []
    for p in range(s):
        if p in E or not (iv[p]["c"] == 1 and iv[p]["H"] >= 3):
            continue
        jp = iv[p]
        if jp["q"] > 4 or not (jp["w"] <= jp["R"] - 2):
            continue
        ok = True
        for j in range(s):
            if j in E or j == p:
                continue
            w, R = iv[j]["w"], iv[j]["R"]
            if w <= 0:
                pass
            elif iv[j]["c"] == 1 and iv[j]["H"] >= 2:
                pass
            elif M.pcond(iv[j], legs) and iv[j]["H"] >= 2:
                pass
            else:
                ok = False
                break
            if not (w <= R):
                ok = False
                break
        if ok:
            out.append(p)
    return E, out

def battery16_tuple(legs, bdep):
    lb = B.perleg_blocks(legs)
    mb = B.merged_blocks(legs)
    if not isinstance(mb, list):
        return None
    iv = B.intervals_of(legs)
    u = B.union_exec(lb, mb)
    d = dict(u)
    d.update({"NP": M.member_NP(iv, legs), "S1": M.member_S1(iv, legs),
              "S2": M.member_S2(iv, legs), "VR": M.member_VR(iv, legs),
              "MR": M.member_MR(iv, legs), "AJ": M.member_AJ(mb),
              "AK": M.member_AK(mb, bdep), "ALG": M.member_ALG(mb, bdep),
              "ALS": M.member_ALS(mb), "AMG": M.member_AMG(mb, bdep),
              "AMS": M.member_AMS(mb), "AN": M.member_AN(mb)})
    return d, iv, mb

def seg_clean(P):
    # True => no certified banked additive decomposition (S0-split partitions)
    n = len(P["legs"])
    S0 = P["S0"]
    splits = [t for t in range(1, n) if P["pairs"][t] == S0]
    if not splits:
        return True, "no-splits"
    bdep_full = [P["snaps"].get(t, {}) for t in range(n)]
    for r_ in range(1, len(splits) + 1):
        for combo in itertools.combinations(splits, r_):
            bounds = (0,) + combo + (n,)
            ok = True
            for a2, b2 in zip(bounds[:-1], bounds[1:]):
                sp = sliced_products(P["legs"], P["pairs"], P["snaps"], a2, b2)
                if sp is None:
                    ok = False
                    break
                if not part_covered(sp, P["snaps"], bdep_full, a2)["covered"]:
                    ok = False
                    break
            if ok:
                return False, "covered-partition-%s" % (list(combo),)
    return True, "no-covered-partition"

def audit_word(word, role):
    # role IN: needs exists!=[] ; OUT: needs exists==[]
    r = B.replay(word)
    if r is None:
        return False, "invalid"
    if r["S1"] != r["S0"]:
        return False, "non-closed"
    gk = B.r5_status(r)
    if gk is None:
        return False, "non-R5"
    legs = r["legs"]
    iv = B.intervals_of(legs)
    E, sinks = exists_sinks(iv, legs)
    ms = (sinks != [])
    if role == "IN" and not ms:
        return False, "non-MSINK"
    if role == "OUT" and ms:
        return False, "MSINK-member"
    b16 = battery16_tuple(legs, r["bdep"])
    if b16 is None:
        return False, "badblocks"
    d, iv2, mb = b16
    flag = [k for k, v in d.items() if v]
    if flag:
        return False, "banked-%s" % "+".join(sorted(flag))
    # pointer pass: AS + segments
    P = pointer_replay(word)
    assert P["S1"] == P["S0"] and P["agree"]
    lb = B.perleg_blocks(P["legs"])
    mbp = B.merged_blocks(P["legs"])
    rAS = B.ASm.recognize(mbp, P["snaps"])
    if rAS.get("accepted"):
        return False, "banked-AS"
    sc, why = seg_clean(P)
    if not sc:
        return False, "additive-%s" % why
    return True, "ELIGIBLE"

if __name__ == "__main__":
    L1c = [B.parse(c) for c in
           [l.strip() for l in open(B.RDIR / "state_concat35" / "parents_L1.txt") if l.strip()]]
    L1m = [B.parse(c) for c in
           [l.strip() for l in open(B.RDIR / "state_mr33" / "parents_L1.txt") if l.strip()]]
    IN_W = B.parse("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
    OUT_W = B.parse("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
    # IN audit: concat35 L0 + L1[0..7]
    res_in = {}
    seq_in = [("concat35-L0", B.SEEDS["concat35"])] + \
        [("concat35-L1-%d" % k, w) for k, w in enumerate(L1c[:8])]
    for tag, w in seq_in:
        el, why = audit_word(w, "IN")
        res_in[tag] = {"eligible": el, "why": why}
        print(tag, "ELIGIBLE" if el else why, flush=True)
    # OUT audit: all concat35 + mr33 L0 + L1[0..173]
    res_out = {}
    seq_out = [("concat35-L0", B.SEEDS["concat35"])] + \
        [("concat35-L1-%d" % k, w) for k, w in enumerate(L1c)] + \
        [("mr33-L0", B.SEEDS["mr33"])] + \
        [("mr33-L1-%d" % k, w) for k, w in enumerate(L1m[:174])]
    n_elig = 0
    for tag, w in seq_out:
        el, why = audit_word(w, "OUT")
        res_out[tag] = {"eligible": el, "why": why}
        if el:
            n_elig += 1
            print(tag, "ELIGIBLE", flush=True)
    from collections import Counter
    print("OUT-pred-dispositions:", Counter(v["why"] for v in res_out.values()), flush=True)
    # interior-loop battery for IN loops [1,17) and [15,32)
    P = pointer_replay(IN_W)
    res_loops = {}
    for (a2, b2) in ((1, 17), (15, 32)):
        sp = sliced_products(P["legs"], P["pairs"], P["snaps"], a2, b2)
        bdep_full = [P["snaps"].get(t, {}) for t in range(len(P["legs"]))]
        pc = part_covered(sp, P["snaps"], bdep_full, a2)
        print("IN-loop-%d-%d covered=%s flags=%s domain=%s gkeys=%s" % (
            a2, b2, pc["covered"], pc["flags"], pc["domain"], pc["gkeys"]), flush=True)
        res_loops["IN-loop-%d-%d" % (a2, b2)] = pc
    json.dump({"IN_audit": res_in, "OUT_audit": res_out,
               "loops": {k: v for k, v in res_loops.items()}},
              open(B.RDIR / "MSINK_finalization_order.json", "w"), indent=1, default=str)
    in_first = [t for t in ["concat35-L0"] + ["concat35-L1-%d" % k for k in range(8)]
                if res_in[t]["eligible"]]
    print("IN-first-eligible:", in_first, flush=True)
    out_elig = [t for t in res_out if res_out[t]["eligible"]]
    print("OUT-eligible-list:", out_elig, flush=True)
