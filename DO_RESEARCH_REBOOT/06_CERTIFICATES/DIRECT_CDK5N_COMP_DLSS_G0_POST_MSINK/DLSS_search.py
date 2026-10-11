# DLSS bounded OUT search: 4 seeds, DELETE-only d1/d2, global order
# (distance, seed-priority, parent first-seen, op, index/gap, key).
# Caps: 60k distinct mutants/seed, 240k total. Seeds (d0) don't consume budget.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from pathlib import Path
from DLSS_recursive import cover21, bank21, MEMO21, CALLS21
from DLSS_membership import strict_dlss
from CRA_pointer_tuple_replay import replay, totals, core_of

DDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
CAP_SEED = 60000
CAP_TOTAL = 240000

def P(*a):
    return str(DDIR.joinpath(*a))
def canon(w):
    return ",".join(m + str(k) for m, k in w)
def sha(w):
    return hashlib.sha256(canon(w).encode("ascii")).hexdigest()
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

IN_W = parse("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
CTL_W = parse("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
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
SEEDS = [("in", IN_W, "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"),
         ("ctl", CTL_W, "6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc"),
         ("mr33", MRW, "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d"),
         ("concat35", S1W + VRW, "7b00897fab01764d14f0c98e6d07daf415839edff31b6f5e90eef93211418bfd")]

def mutants(word):
    n = len(word)
    dpos = [i for i, (m, _) in enumerate(word) if m == 'D']
    for i in dpos:
        yield ("rm%d" % i, word[:i] + word[i + 1:])
    for i in dpos:
        for k in range(1, 10):
            if k == word[i][1]:
                continue
            w = list(word); w[i] = ('D', k)
            yield ("rep%dk%d" % (i, k), w)
    for g in range(n + 1):
        for k in range(1, 10):
            w = list(word); w.insert(g, ('D', k))
            yield ("ins%dk%d" % (g, k), w)

def sdir(seed):
    d = DDIR / ("search_" + seed)
    d.mkdir(parents=True, exist_ok=True)
    return d

def load_state(seed):
    d = sdir(seed)
    seen = set()
    f = d / "seen.txt"
    if f.exists():
        for line in open(f):
            line = line.strip()
            if line:
                seen.add(line)
    c = {"tested": 0, "closed": 0, "r5": 0, "dlss": 0, "banked": 0,
         "hopeful": 0, "out": 0}
    cf = d / "census.json"
    if cf.exists():
        c = json.load(open(cf))
    return seen, c

def save_state(seed, seen_new, census):
    d = sdir(seed)
    if seen_new:
        with open(d / "seen.txt", "a") as fh:
            for h in seen_new:
                fh.write(h + "\n")
    json.dump(census, open(d / "census.json", "w"), indent=1)

def screen(word):
    """Returns (disposition, record-or-None). Full recursive only for hopefuls."""
    try:
        r = replay(word)
    except Exception as e:
        return "invalid", None
    if r["S1"] != r["S0"] or not r["agree"]:
        return "non-closed", None
    gk = sorted({l["x"] for l in r["legs"] if l["m"] == "K" and l["chg"]})
    if len(gk) != 5:
        return "non-R5-keys", None
    for ps in r["pairs"]:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return "non-R5-core", None
    legs = r["legs"]
    sm = strict_dlss(legs)
    if sm["member"]:
        return "DLSS-member", {"tot": totals(legs), "sinks": sm["sinks"]}
    fb = bank21(legs, r["pairs"], r["snaps"])
    if fb is None:
        return "badblocks", None
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        return "banked", {"tot": totals(legs), "flags": flags}
    cov = cover21(r["S0"], word)
    if cov.get("indeterminate"):
        return "INDETERMINATE", {"why": cov["indeterminate"]}
    if cov.get("covered"):
        return "recursive-covered", {"depth": cov.get("depth")}
    tot = totals(legs)
    return "OUT-HOPEFUL", {"tot": tot, "E": sm["E"], "t": sm["t"],
                           "stage": sm["stage"], "subs": CALLS21["n"]}

def cmd_l1(seed):
    name, base, h = [s for s in SEEDS if s[0] == seed][0]
    assert sha(base) == h, seed
    seen, cen = load_state(seed)
    new_hashes = []
    parents = []
    n_out = None
    for op, w2 in mutants(base):
        hh = sha(w2)
        if hh in seen:
            continue
        seen.add(hh)
        new_hashes.append(hh)
        parents.append((op, canon(w2)))
        if len(new_hashes) + (cen.get("distinct", 0)) >= CAP_SEED:
            break
    with open(sdir(seed) / "parents_L1.txt", "w") as fh:
        for op, c in parents:
            fh.write(op + " " + c + "\n")
    # screen L1 in order; STOP at first OUT-HOPEFUL (freeze next step)
    surv = []
    for k, (op, c) in enumerate(parents):
        w = parse(c)
        disp, rec = screen(w)
        cen["tested"] += 1
        if disp not in ("non-closed", "invalid"):
            cen["closed"] += 1
        if disp == "OUT-HOPEFUL":
            rec.update({"canon": c, "sha": sha(w), "seed": seed, "layer": 1,
                        "idx": k, "op": op})
            surv.append(rec)
            cen["hopeful"] += 1
            print("OUT-HOPEFUL %s L1 idx=%d %s %s" % (seed, k, sha(w)[:12], rec["tot"]), flush=True)
            break
        if disp == "INDETERMINATE":
            print("INDETERMINATE %s L1 idx=%d: %s" % (seed, k, rec), flush=True)
            save_state(seed, new_hashes, cen)
            raise SystemExit("INDETERMINATE at %s L1 %d" % (seed, k))
    cen["distinct"] = cen.get("distinct", 0) + len(new_hashes)
    save_state(seed, new_hashes, cen)
    with open(sdir(seed) / "survivors_L1.jsonl", "w") as fh:
        for r in surv:
            fh.write(json.dumps(r, default=str) + "\n")
    print("%s L1 done: parents=%d tested=%d hopeful=%d" % (
        seed, len(parents), cen["tested"], cen["hopeful"]), flush=True)

if __name__ == "__main__":
    a = sys.argv
    if a[1] == "L1":
        cmd_l1(a[2])
    else:
        raise ValueError(a[1:])
