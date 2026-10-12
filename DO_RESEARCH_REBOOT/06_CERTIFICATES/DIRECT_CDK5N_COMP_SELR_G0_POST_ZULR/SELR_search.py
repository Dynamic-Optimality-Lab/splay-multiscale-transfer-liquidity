# SELR streaming deterministic OUT search (§12): DELETE-only d1/d2, global order
# (distance, seed-priority, parent first-seen, op removal>replacement>insertion,
# index/gap, key). Exact-canonical seen set (SHA index only). Strictly sequential
# generate->register->screen->decide with stop-checks; stops at first OUT.
# Caps: 60k distinct screened mutants/seed, 300k total. Counters persisted.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from SELR_membership import strict_selr, bank24
from SELR_recursive import cover24, MEMO24, CALLS24

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
CAP_SEED = 60000
CAP_TOTAL = 300000
KEYS = list(range(1, 10))

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)
def sha(w):
    return hashlib.sha256(canon(w).encode("ascii")).hexdigest()

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
SEEDS = [
    ("selr-in", "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
    ("zulr-in", "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
    ("uesink-in", "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
    ("dlss-in", "D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
    ("dlss-ctl", "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"),
    ("mr33", None),
    ("concat35", None),
]
WORDMAP = {"mr33": MRW, "concat35": S1W + VRW}

def seed_word(name):
    for n, c in SEEDS:
        if n == name:
            return parse(c) if c else WORDMAP[name]
    raise KeyError(name)

def mutants(word):
    n = len(word)
    dpos = [i for i, (m, _) in enumerate(word) if m == 'D']
    for i in dpos:
        yield ("rm%d" % i, word[:i] + word[i + 1:])
    for i in dpos:
        for k in KEYS:
            if k == word[i][1]:
                continue
            w = list(word); w[i] = ('D', k)
            yield ("rep%dk%d" % (i, k), w)
    for g in range(n + 1):
        for k in KEYS:
            w = list(word); w.insert(g, ('D', k))
            yield ("ins%dk%d" % (g, k), w)

def screen(word):
    try:
        r = replay(word)
    except Exception:
        return "invalid", None, None
    if r["S1"] != r["S0"] or not r["agree"]:
        return "non-closed", None, None
    gk = sorted(genuine_keys(r["legs"]))
    if len(gk) != 5:
        return "non-R5-keys", None, None
    for ps in r["pairs"]:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return "non-R5-core", None, None
    legs = r["legs"]
    sm = strict_selr(legs)
    if sm["member"]:
        return "SELR-member", {"tot": totals(legs)}, sm
    fb = bank24(legs, r["pairs"], r["snaps"])
    if fb is None:
        return "badblocks", None, sm
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        return "banked", {"tot": totals(legs), "flags": flags}, sm
    cov = cover24(r["S0"], word)
    if cov.get("indeterminate"):
        return "INDETERMINATE", {"why": cov["indeterminate"]}, sm
    if cov.get("covered"):
        return "recursive-covered", {"depth": cov.get("depth")}, sm
    tot = totals(legs)
    return "OUT-HOPEFUL", {"tot": tot, "E": sm["E"], "U": sm.get("U"),
                            "t": sm.get("t"), "stage": sm["stage"]}, sm

def main():
    seen = set()
    ctr = {"raw": 0, "distinct": 0, "replayed": 0, "screened": 0,
           "bank24_tested": 0, "recursive_tested": 0, "rejected": 0,
           "banked": 0, "indeterminate": 0, "per_seed": {}, "truncated": []}
    logf = open(PDIR + "SELR_screened_log.jsonl", "w")
    frozen_out = None
    # distance-major: all d1 (seed order), then d2 (seed order, L1-first-seen parents)
    l1_parents = {}
    for dist in (1, 2):
        for pri, (sname, _) in enumerate(SEEDS):
            if frozen_out:
                break
            base = seed_word(sname)
            if dist == 1:
                gen = mutants(base)
                parent_tag = "seed:%s" % sname
            else:
                plist = l1_parents.get(sname, [])
                if not plist:
                    continue
                parent_tag = None
                def gen2():
                    for pcanon in plist:
                        for op, w2 in mutants(parse(pcanon)):
                            yield ("L2[%s]/%s" % (pcanon[:24], op), w2)
                gen = gen2()
            l1words = []
            for op, w2 in gen:
                if frozen_out:
                    break
                ctr["raw"] += 1
                c = canon(w2)
                if c in seen:
                    continue
                seen.add(c)
                ctr["distinct"] += 1
                sd = ctr["per_seed"].get(sname, 0) + 1
                ctr["per_seed"][sname] = sd
                if sd > CAP_SEED or ctr["distinct"] > CAP_TOTAL:
                    ctr["truncated"].append({"seed": sname, "dist": dist, "op": op})
                    print("BUDGET-TRUNCATED %s d%d" % (sname, dist), flush=True)
                    break
                if dist == 1:
                    l1words.append(c)
                ctr["screened"] += 1
                disp, rec, sm = screen(w2)
                ctr["replayed"] += 1
                if disp in ("banked",):
                    ctr["banked"] += 1
                    ctr["bank24_tested"] += 1
                elif disp in ("recursive-covered", "OUT-HOPEFUL", "INDETERMINATE"):
                    ctr["bank24_tested"] += 1
                    ctr["recursive_tested"] += 1
                elif disp == "SELR-member":
                    pass
                else:
                    ctr["rejected"] += 1
                entry = {"dist": dist, "seed": sname, "parent": parent_tag if dist == 1 else op.split("/")[0],
                         "op": op if dist == 1 else op.split("/", 1)[1], "canon": c,
                         "sha": hashlib.sha256(c.encode("ascii")).hexdigest(), "disp": disp,
                         "rec": rec}
                logf.write(json.dumps(entry, default=str) + "\n")
                logf.flush()
                if disp == "INDETERMINATE":
                    ctr["indeterminate"] += 1
                    json.dump(ctr, open(PDIR + "SELR_search_counters.json", "w"), indent=1)
                    print("INDETERMINATE at %s d%d %s" % (sname, dist, op), flush=True)
                    raise SystemExit("INDETERMINATE")
                if disp == "OUT-HOPEFUL":
                    entry["tot"] = rec["tot"]
                    frozen_out = entry
                    print("FROZEN-OUT %s d%d %s %s" % (sname, dist, op, entry["sha"]), flush=True)
                    break
            if dist == 1:
                l1_parents[sname] = l1words
                print("%s L1: distinct=%d screened=%d" % (sname, len(l1words), ctr["screened"]), flush=True)
    json.dump(ctr, open(PDIR + "SELR_search_counters.json", "w"), indent=1)
    if frozen_out:
        json.dump(frozen_out, open(PDIR + "SELR_OUT.json", "w"), indent=1, default=str)
        print("SEARCH: OUT-FROZEN", flush=True)
    else:
        print("SEARCH: NO-OUT (R1 OPEN)", flush=True)
    print(json.dumps({k: v for k, v in ctr.items() if k != "per_seed"}), flush=True)

if __name__ == "__main__":
    main()
