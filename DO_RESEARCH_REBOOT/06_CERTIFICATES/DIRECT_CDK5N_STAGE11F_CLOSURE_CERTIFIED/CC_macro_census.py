# STEP 02: effective-macro completeness + nongenuine-KEEP audit + m count + event skeletons.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay
from CRA_strict_msink_membership import intervals as miv
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
rows = []
for seed in ("concat35", "mr33"):
    for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
        rows.append(json.loads(l))
bycanon = {}
for r in rows:
    bycanon.setdefault(r["canon"], []).append(r)
WORDS = sorted(bycanon)
WORDS.append("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

from collections import Counter
pats = Counter()
evkinds = Counter()
maxrots = 0
nong_a0 = 0
nong_tot = 0
nH = Counter()
bad = 0
for cw in WORDS:
    w = parse(cw)
    try:
        R = replay(w)
    except Exception:
        continue
    if not (R["S1"] == R["S0"] and R["agree"]):
        continue
    legs = R["legs"]
    # nongenuine audit: KEEPs with a=0 (A-root): check B-change status vs chg flag
    for l in legs:
        if l["m"] == "K" and l["a"] == 0:
            nong_tot += 1
            if l["chg"]:
                nong_a0 += 1  # A-root KEEP that still changes B (B root differs): genuine B-side!
    for v in miv(legs):
        H = v["H"]
        nH[H] += 1
        if H > 2:
            continue
        # effective pattern by nonzero structure (sequential costs)
        nz = [(k, legs[k]["m"], legs[k]["a"]) for k in v["segi"] if legs[k]["a"] >= 1]
        term = v["segi"][-1]
        if legs[term]["m"] != "K":
            bad += 1
            continue
        pat = tuple(['D' if m == 'D' else 'K' for _, m, _ in nz] + (['K'] if (not nz or nz[-1][0] != term) else []))
        pats[pat] += 1
        # rotation-event skeleton: replay effective word, count rotations + event kinds
        ew = [(legs[k]["m"], legs[k]["x"]) for k in sorted(set([k for k, _, _ in nz] + [term]))]
        t = None
        from CRA_pointer_tuple_replay import from_serial
        # reconstruct start A tree from pairs
        t = from_serial(R["pairs"][v["segi"][0]][0])
        rots = 0
        kinds = []
        for (m, x) in ew:
            # depth before
            from CRA_pointer_tuple_replay import idepths
            d = idepths(t).get(x)
            t2, evs = S.trace(t, x)
            for e in evs:
                kinds.append(e[0])
                rots += 2 if e[0] in ("LL", "RR", "LR", "RL") else 1
            t = t2
        evkinds[tuple(kinds)] += 1
        maxrots = max(maxrots, rots)
        if rots > 4:
            bad += 1
            print("ROT-OVER", cw[:40], rots, flush=True)
print("patterns:", dict(pats), flush=True)
print("nH dist keys:", sorted(nH.items())[:12], flush=True)
print("maxrots=%d nong_a0=%d/%d bad=%d" % (maxrots, nong_a0, nong_tot, bad), flush=True)
print("distinct event-kind seqs:", len(evkinds), flush=True)
json.dump({"patterns": {str(k): v for k, v in pats.items()}, "maxrots": maxrots,
           "nong_a0_genuine": nong_a0, "nong_a0_total": nong_tot, "bad": bad,
           "event_seqs": len(evkinds), "m": 3}, open(PDIR + "CC_MACRO_CENSUS.json", "w"), indent=1)
