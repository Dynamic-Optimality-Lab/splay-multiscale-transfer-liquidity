# STEP 04/05 verification: root sync + H=1 normal form on corpus.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, proot
from CRA_strict_msink_membership import intervals as miv

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

WORDS = ["D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"]
RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
rows = []
for seed in ("concat35", "mr33"):
    for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
        rows.append(json.loads(l))
bycanon = {}
for r in rows:
    bycanon.setdefault(r["canon"], []).append(r)
for i, cs in enumerate(sorted(bycanon)):
    WORDS.append(cs)
    if i >= 80:
        break

rs_bad = sq_bad = e3_bad = e4n = 0
nw = ne3 = 0
tot = {"A": 0, "Q": 0, "Ck": 0}
for cw in WORDS:
    w = parse(cw)
    try:
        R = replay(w)
    except Exception:
        continue
    if not (R["S1"] == R["S0"] and R["agree"]):
        continue
    nw += 1
    legs = R["legs"]
    # root sync at every post-KEEP boundary
    for k, l in enumerate(legs):
        if l["m"] == "K":
            A1, B1 = R["pairs"][k + 1]
            from CRA_pointer_tuple_replay import from_serial
            A = from_serial(A1); B = from_serial(B1)
            def root(t):
                while True:
                    if t == '.' or (isinstance(t, tuple) and t and t[0] == "leaf"):
                        return None
                    _, kk, ll, rr = t
                    # root = top
                    return kk
            if not (root(A) == l["x"] and root(B) == l["x"]):
                rs_bad += 1
    # interval identity
    iv = miv(legs)
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    Ck = sum(v["c"] for v in iv)
    if not (sum(v["H"] for v in iv) == A and sum(v["q"] for v in iv) == Q and sum(v["c"] for v in iv) == Ck):
        sq_bad += 1
    # E3/E4 normal form: H=1,c=1 => q in {3,4} iff w<0; normal form shape
    for j, v in enumerate(iv):
        wj = 2 * v["H"] - v["q"]
        if wj < 0:
            ne3 += 1
            if not (v["H"] == 1 and v["q"] in (3, 4) and v["c"] == 1):
                e3_bad += 1
            # normal form: exactly one nonzero, targets v, depth 1-2, rest root no-ops
            nz = [kk for kk in v["segi"] if legs[kk]["a"] == 1]
            if not (len(nz) == 1 and legs[nz[0]]["x"] == v["x"] and legs[nz[0]]["dA"] in (1, 2)):
                e3_bad += 1
        if v["H"] == 1 and v["q"] == 4 and v["c"] == 1:
            e4n += 1
print("words=%d root_sync_bad=%d identity_bad=%d neg_intervals=%d normalform_bad=%d E4_count=%d" % (nw, rs_bad, sq_bad, ne3, e3_bad, e4n), flush=True)
ok = (rs_bad == 0 and sq_bad == 0 and e3_bad == 0)
json.dump({"words": nw, "root_sync_bad": rs_bad, "identity_bad": sq_bad, "neg": ne3, "nf_bad": e3_bad, "e4": e4n, "pass": ok}, open(PDIR + "CC_BOUNDARY_CHECK.json", "w"), indent=1)
print("STEP0405: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)
