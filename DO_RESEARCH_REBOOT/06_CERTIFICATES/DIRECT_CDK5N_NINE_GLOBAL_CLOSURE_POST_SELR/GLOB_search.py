# Frozen 2-seed diagnostic audit (§12): DELETE-only d≤2, canonical order, budgets.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of
from CRA_segment_memberships import genuine_keys
from CRA_strict_msink_membership import intervals as msink_intervals

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR/'
KEYS = list(range(1, 10))
CAP_SEED = 150000
CAP_TOTAL = 300000
M = {1, 3, 5, 7, 9}

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

SEEDS = [
    ("selr-out", "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e"),
    ("selr-in", "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd"),
]

def mutants(word):
    n = len(word)
    dpos = [i for i, (m, _) in enumerate(word) if m == 'D']
    for i in dpos:
        yield ("RM%d" % i, word[:i] + word[i + 1:])
    for i in dpos:
        for k in KEYS:
            if k == word[i][1]:
                continue
            w = list(word); w[i] = ('D', k)
            yield ("REP%dk%d" % (i, k), w)
    for g in range(n + 1):
        for k in KEYS:
            w = list(word); w.insert(g, ('D', k))
            yield ("INS%dk%d" % (g, k), w)

def gaps(ps):
    A = from_serial(ps[0]); B = from_serial(ps[1])
    dA = idepths(A); dB = idepths(B)
    return {x: dB.get(x, 0) - dA.get(x, 0) for x in M}

def screen(w):
    # S1 replay
    try:
        R = replay(w)
    except Exception as e:
        return {"disp": "SOURCE-INVALID", "why": type(e).__name__}
    legs, pairs = R["legs"], R["pairs"]
    n = len(w)
    # S2 closure
    if not (R["S1"] == R["S0"] and R["agree"]):
        return {"disp": "NON-CLOSED"}
    # S3 domain
    if sorted(genuine_keys(legs)) != [1, 3, 5, 7, 9]:
        return {"disp": "OUTSIDE-DOMAIN", "why": "keys"}
    for ps in pairs:
        c = core_of(ps[1])
        if c is None or len(c) != 9:
            return {"disp": "OUTSIDE-DOMAIN", "why": "core"}
    # S4 costs
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    exc = Q - 2 * A
    # S5 excess classification
    iv = msink_intervals(legs)
    E3 = [j for j in range(len(iv)) if iv[j]["H"] == 1 and iv[j]["q"] == 3 and iv[j]["c"] == 1]
    E4 = [j for j in range(len(iv)) if iv[j]["H"] == 1 and iv[j]["q"] == 4 and iv[j]["c"] == 1]
    deltas = [v["q"] - 2 * v["H"] for v in iv]
    # S6 L0 + C1 checks on each E3/E4 interval
    l0_bad = []
    c1_bad = []
    for j in E3 + E4:
        v = iv[j]
        segi = v["segi"]; u = legs[v["gi"] - 0]["x"]  # placeholder
        # roots at interval start
        xp = None
        # find prev keep key: c=1 means x != xp; get xp from legs order
        # recompute via ki list
        ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
        t = ki.index(v["gi"])
        prev = ki[t - 1]
        xp = legs[prev]["x"]
        P = pairs[segi[0]]
        if not (legs[segi[0]]["ra"] == xp and legs[segi[0]]["rb"] == xp):
            l0_bad.append((j, "roots"))
            continue
        nz = [k for k in segi if legs[k]["a"] == 1]
        if not (len(nz) == 1 and legs[nz[0]]["x"] == v["x"] and legs[nz[0]]["dA"] in (1, 2)):
            l0_bad.append((j, "nonce"))
            continue
        for k in segi:
            if k == nz[0]:
                break
            if pairs[k] != P or legs[k]["x"] != xp:
                l0_bad.append((j, "prefix"))
                break
        bP = P[1]
        for k in segi:
            if pairs[k][1] != bP:
                l0_bad.append((j, "Bfrozen"))
                break
        A0 = from_serial(P[0]); B0 = from_serial(P[1])
        dA = idepths(A0).get(v["x"]); dB = idepths(B0).get(v["x"])
        if dA not in (1, 2):
            l0_bad.append((j, "dA"))
        if v["q"] == 3 and dB not in (6, 7):
            l0_bad.append((j, "dB3"))
        if v["q"] == 4 and dB != 8:
            l0_bad.append((j, "dB4"))
        if v["q"] == 3 and not (dB - dA >= 4):
            l0_bad.append((j, "gap3"))
        if v["q"] == 4 and not (dB - dA >= 6):
            l0_bad.append((j, "gap4"))
        # C1-GAP net-drop check (conjectured): Gamma drop >= 1
        Qs = pairs[(v["gi"] + 1) % n]
        gP = gaps(P); gQ = gaps(Qs)
        GamP = sum(max(0, x) for x in gP.values())
        GamQ = sum(max(0, x) for x in gQ.values())
        if not (GamP - GamQ >= 1):
            c1_bad.append((j, GamP - GamQ))
    # S8 adjudication
    if exc > 0:
        return {"disp": "POSSIBLE-COUNTEREXAMPLE", "A": A, "Q": Q, "exc": exc,
                "E3": E3, "E4": E4, "l0": l0_bad, "c1": c1_bad}
    if l0_bad:
        return {"disp": "TRANSPORT-REFUTED", "why": "L0", "detail": l0_bad[:3], "A": A, "Q": Q, "E3": E3, "E4": E4}
    if c1_bad:
        return {"disp": "C1-COUNTEREVIDENCE", "detail": c1_bad[:3], "A": A, "Q": Q, "E3": E3, "E4": E4}
    return {"disp": "INEQUALITY-HOLDS", "A": A, "Q": Q, "exc": exc, "E3": E3, "E4": E4}

def main():
    seen = set()
    ctr = {"raw": 0, "distinct": 0, "screened": 0, "per_seed": {},
           "cats": {}, "truncated": None, "stopped": None}
    logf = open(PDIR + "GLOB_screened_log.jsonl", "w")
    l1_parents = {}
    for dist in (0, 1, 2):
        for pri, (sname, sc, sh) in enumerate(SEEDS):
            if ctr["stopped"]:
                break
            assert hashlib.sha256(sc.encode()).hexdigest() == sh, sname
            base = parse(sc)
            if dist == 0:
                cands = [("SEED", base)]
                ptag = "seed"
            elif dist == 1:
                cands = list(mutants(base))
                ptag = "seed"
            else:
                plist = l1_parents.get(sname, [])
                if not plist:
                    continue
                cands = []
                for pc in plist:
                    for op, w2 in mutants(parse(pc)):
                        cands.append(("L2[%s]/%s" % (pc[:20], op), w2))
                ptag = None
            l1words = []
            for op, w2 in cands:
                if ctr["stopped"]:
                    break
                if dist == 0:
                    c = sc
                else:
                    ctr["raw"] += 1
                    c = canon(w2)
                    if c in seen:
                        continue
                    seen.add(c)
                    ctr["distinct"] += 1
                    sd = ctr["per_seed"].get(sname, 0) + 1
                    ctr["per_seed"][sname] = sd
                    if sd > CAP_SEED or ctr["distinct"] > CAP_TOTAL:
                        ctr["truncated"] = {"seed": sname, "dist": dist, "op": op}
                        ctr["stopped"] = "BUDGET-EXHAUSTED"
                        print("BUDGET-EXHAUSTED at %s d%d" % (sname, dist), flush=True)
                        break
                    if dist == 1:
                        l1words.append(c)
                ctr["screened"] += 1
                r = screen(w2 if dist > 0 else base)
                ctr["cats"][r["disp"]] = ctr["cats"].get(r["disp"], 0) + 1
                e = {"dist": dist, "seed": sname, "op": op if dist > 0 else "SEED",
                     "canon": c if dist > 0 else sc,
                     "sha": hashlib.sha256((c if dist > 0 else sc).encode()).hexdigest(),
                     "disp": r["disp"], "info": {k: v for k, v in r.items() if k != "disp"}}
                logf.write(json.dumps(e, default=str) + "\n")
                if ctr["screened"] % 20000 == 0:
                    logf.flush()
                    print("... screened=%d distinct=%d %s" % (ctr["screened"], ctr["distinct"], ctr["cats"]), flush=True)
                if r["disp"] == "POSSIBLE-COUNTEREXAMPLE":
                    ctr["stopped"] = "COUNTEREXAMPLE-CANDIDATE"
                    print("CANDIDATE %s %s exc=%s" % (sname, op, r.get("exc")), flush=True)
                    break
                if r["disp"] == "TRANSPORT-REFUTED":
                    ctr["stopped"] = "TRANSPORT-REFUTED"
                    print("REFUTED %s %s %s" % (sname, op, r.get("detail")), flush=True)
                    break
                if r["disp"] not in ("SOURCE-INVALID", "NON-CLOSED", "OUTSIDE-DOMAIN", "INEQUALITY-HOLDS", "C1-COUNTEREVIDENCE"):
                    ctr["stopped"] = "INDETERMINATE-LIKE"
                    break
            if dist == 1 and not ctr["stopped"]:
                l1_parents[sname] = l1words
                print("%s L1 parents=%d" % (sname, len(l1words)), flush=True)
    json.dump(ctr, open(PDIR + "GLOB_search_counters.json", "w"), indent=1, default=str)
    print("AUDIT:", json.dumps({k: v for k, v in ctr.items() if k != "per_seed"}), flush=True)
    print("per_seed:", ctr["per_seed"], flush=True)

if __name__ == "__main__":
    main()
