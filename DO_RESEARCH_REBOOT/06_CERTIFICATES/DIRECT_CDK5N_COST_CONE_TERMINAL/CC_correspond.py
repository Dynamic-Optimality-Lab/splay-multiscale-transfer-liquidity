# Correspondence + coverage: every interval maps to a macro edge; path weight <= 2A-Q.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, core_of
from CRA_strict_msink_membership import intervals as miv
from RC_recursive_closure_engine import replay_from
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def depth(t, x):
    d = 0
    cur = t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None

RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
rows = []
for seed in ("concat35", "mr33"):
    for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
        rows.append(json.loads(l))
bycanon = {}
for r in rows:
    bycanon.setdefault(r["canon"], []).append(r)
WORDS = sorted(bycanon)
random.seed(126)
# add rotated + concatenated variants (mutations 5,6)
base = [parse(c) for c in WORDS[:40]]
for w in base:
    R = replay(w)
    n = len(w)
    k = random.randrange(n)
    wq = [w[(k + t) % n] for t in range(n)]
    try:
        Fq = replay_from(R["pairs"][k], wq)
        if Fq["pairs"][-1] == R["pairs"][k]:
            WORDS.append(",".join(m + str(x) for m, x in wq))
    except Exception:
        pass
for a, b in zip(base[::2], base[1::2]):
    WORDS.append(",".join([(m + str(x)) for m, x in a] + [(m + str(x)) for m, x in b]))

def eff_word(legs, segi):
    # effective word: nonzero accesses + terminal KEEP (last element always KEEP by construction)
    nz = [k for k in segi if legs[k]["a"] >= 1]
    term = segi[-1]
    assert legs[term]["m"] == "K"
    seq = sorted(set(nz + [term]))
    return [(legs[k]["m"], legs[k]["x"]) for k in seq]

bad = tot = uncovered_low = hicov = 0
nwords = 0
for cw in WORDS:
    w = parse(cw)
    try:
        R = replay(w)
    except Exception:
        continue
    if not (R["S1"] == R["S0"] and R["agree"]):
        continue
    nwords += 1
    legs = R["legs"]
    iv = miv(legs)
    A = sum(l["a"] for l in legs)
    Q = sum(l["q"] for l in legs)
    if not (Q <= 2 * A):
        bad += 1
        print("COUNTEREXAMPLE-LIKE:", cw[:60], A, Q, flush=True)
        continue
    pw = 0
    for j, v in enumerate(iv):
        tot += 1
        H = v["H"]
        q = v["q"]
        if H <= 2:
            # exact macro must exist: simulate effective word from interval start
            P = R["pairs"][v["segi"][0]]
            ew = eff_word(legs, v["segi"])
            Fr = replay_from(P, ew)
            H2 = sum(l["a"] for l in Fr["legs"])
            Q2 = sum(l["q"] for l in Fr["legs"])
            if not (H2 == H and Q2 == q and Fr["pairs"][-1] == R["pairs"][(v["gi"] + 1) % len(w)]):
                uncovered_low += 1
            pw += 2 * H - q
        else:
            hicov += 1
            pw += 6 - q
            if not (6 - q <= 2 * H - q):
                bad += 1
    if not (pw <= 2 * A - Q):
        bad += 1
print("words=%d intervals=%d exact_low_covered, highcost=%d uncovered_low=%d bad=%d" % (nwords, tot, hicov, uncovered_low, bad), flush=True)
ok = (bad == 0 and uncovered_low == 0)
json.dump({"words": nwords, "intervals": tot, "highcost": hicov, "uncovered": uncovered_low, "bad": bad, "pass": ok}, open(PDIR + "CC_CORRESPONDENCE.json", "w"), indent=1)
print("CORRESPONDENCE: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)
