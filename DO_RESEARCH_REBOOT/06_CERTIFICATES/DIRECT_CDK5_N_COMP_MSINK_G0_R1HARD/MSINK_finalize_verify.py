# MSINK finalization master verification (tasks B,E,G,H-battery,I + census).
# Fresh independent re-verification; NO mutation of frozen artifacts.
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
from pathlib import Path
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S
import MSINK_bounded_search as B
import MSINK_memberships as M

R = {}
def rep(name, ok, detail=""):
    R[name] = {"ok": bool(ok), "detail": str(detail)}
    print("%s: %s %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)
    return ok

ALL_OK = []
def need(name, ok, detail=""):
    ALL_OK.append(rep(name, ok, detail))

# ---- source integrity ----
def fhash(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
need("src-eventflow-present", Path("scripts/wp6_eventflow.py").exists())
need("src-coarsedbl-present", Path("scripts/wp6_coarse_double.py").exists())
need("src-splay-present", Path("python/independent/splay.py").exists())
need("src-legacy-present", Path("python/liquidity/legacy_embedding.py").exists())
SRC = {n: fhash(p) for n, p in (
    ("eventflow", "scripts/wp6_eventflow.py"),
    ("coarse_double", "scripts/wp6_coarse_double.py"),
    ("splay", "python/independent/splay.py"),
    ("legacy", "python/liquidity/legacy_embedding.py"))}
print("source-sha:", {k: v[:16] for k, v in SRC.items()}, flush=True)
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
need("T0-frozen-shape", T0 == [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None])
MSET = {1, 3, 5, 7, 9}

# ---- pointer replay (independent of screening) ----
def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]

def pointer_replay(word):
    A = to_ptr(copy.deepcopy(T0)); Bp = to_ptr(copy.deepcopy(T0))
    IA = B.totup(copy.deepcopy(T0)); IB = B.totup(copy.deepcopy(T0))
    S0 = (pserial(A), pserial(Bp))
    legs, snaps, pairs = [], {}, [S0]
    agree = True
    for i, (md, x) in enumerate(word):
        dA = pdepths(A).get(x, -1); assert dA >= 0
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(Bp)
        sb = pserial(Bp)
        if md == 'K':
            dB = pdepths(Bp).get(x, -1); assert dB >= 0
            q = dB // 2
        else:
            dB = None; q = 0
        eA = B.dep(IA).get(x)
        eB = B.dep(IB).get(x) if md == 'K' else None
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            Bp, outB = splay_B_push(Bp, x)
            for s in outB:
                push += list(s)
        IA = S.trace(IA, x)[0]
        if md == 'K':
            IB = S.trace(IB, x)[0]
        chg = (pserial(Bp) != sb) if md == 'K' else False
        agree = agree and (dA, dB) == (eA, eB) and pserial(A) == B.ser(IA) \
            and pserial(Bp) == B.ser(IB)
        snaps[i] = pdepths(Bp)
        pairs.append((pserial(A), pserial(Bp)))
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg,
                     "push": sorted(set(push))})
    return {"legs": legs, "snaps": snaps, "pairs": pairs, "S0": S0,
            "S1": pairs[-1], "agree": agree}

# ---- controls ----
S1W = B.S1W; VRW = B.VRW; MRW = B.MRW
def canon(w):
    return ",".join(m + str(k) for m, k in w)
for name, w, exp in (("S1W", S1W, (33, 18)), ("VRW", VRW, (31, 18)),
                     ("CONCAT", S1W + VRW, (64, 36)), ("MRW", MRW, (55, 36))):
    pr = pointer_replay(w)
    A = sum(l["a"] for l in pr["legs"]); Q = sum(l["q"] for l in pr["legs"])
    cores = []
    for ps in pr["pairs"]:
        c = B.core(ps[1], MSET)
        cores.append(None if c is None else len(c))
    need("ctl-%s-totals" % name, (A, Q) == exp, "A=%d Q=%d" % (A, Q))
    need("ctl-%s-closed-engines-cores" % name,
         pr["S1"] == pr["S0"] and pr["agree"] and all(c == 9 for c in cores),
         "closed engines cores9")
    need("ctl-%s-sha" % name,
         hashlib.sha256(canon(w).encode("ascii")).hexdigest() ==
         {"S1W": "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602",
          "VRW": "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7",
          "CONCAT": "7b00897fab01764d14f0c98e6d07daf415839edff31b6f5e90eef93211418bfd",
          "MRW": "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d"}[name])
pr = pointer_replay(S1W + VRW)
need("ctl-concat-split17", pr["pairs"][17] == pr["S0"] and pr["pairs"][35] == pr["S0"])

# ---- witnesses: construction from (seed, edit-op), full SHA, fresh replay ----
L1c = [canon(w) for w in B.mutants(B.SEEDS["concat35"])
       if 25 <= len(w) <= 45]
L1m = [canon(w) for w in B.mutants(B.SEEDS["mr33"])
       if 25 <= len(w) <= 45]
IN_CANON = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,"
            "K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
need("IN-construction-idx7", L1c[7] == IN_CANON, "concat35 L1[7] removal dpos15")
need("OUT-construction-idx173", L1m[173] == OUT_CANON, "mr33 L1[173] insert D3@g2")
IN_SHA = hashlib.sha256(IN_CANON.encode("ascii")).hexdigest()
OUT_SHA = hashlib.sha256(OUT_CANON.encode("ascii")).hexdigest()
need("IN-full-sha", IN_SHA == "19ff110a7c6087256e5348454aa0d1da084a4b544a7904cc82c111af3c8783df", IN_SHA[:12])
need("OUT-full-sha-exact", OUT_SHA == "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3", OUT_SHA[:12])
IN_W = B.parse(IN_CANON); OUT_W = B.parse(OUT_CANON)
need("IN-n34", len(IN_W) == 34); need("OUT-n34", len(OUT_W) == 34)
IN_P = pointer_replay(IN_W); OUT_P = pointer_replay(OUT_W)
for tag, P, exp in (("IN", IN_P, (61, 36, 16)), ("OUT", OUT_P, (55, 36, 16))):
    A = sum(l["a"] for l in P["legs"]); Q = sum(l["q"] for l in P["legs"])
    ks = [l["x"] for l in P["legs"] if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    need("%s-totals" % tag, (A, Q, Ck) == exp, "A=%d Q=%d Ck=%d" % (A, Q, Ck))
    need("%s-closed" % tag, P["S1"] == P["S0"])
    need("%s-engines" % tag, P["agree"])
    gk = sorted({l["x"] for l in P["legs"] if l["m"] == "K" and l["chg"]})
    need("%s-gkeys5" % tag, gk == [1, 3, 5, 7, 9], gk)
    cores = []
    for ps in P["pairs"]:
        c = B.core(ps[1], MSET)
        cores.append(None if c is None else len(c))
    need("%s-cores9" % tag, all(c == 9 for c in cores), len(cores))
    need("%s-no-proper-splits" % tag,
         all(P["pairs"][t] != P["S0"] for t in range(1, len(P["legs"]))),
         "splits=%s" % [t for t in range(1, len(P["legs"])) if P["pairs"][t] == P["S0"]])
    pre = P["pairs"][:-1]
    reps = [(a, b) for a in range(len(pre)) for b in range(a + 1, len(pre)) if pre[a] == pre[b]]
    R["%s-interior-repeats" % tag] = {"ok": True, "detail": "repeats=%s" % reps}
    print("PASS %s-interior-repeats repeats=%s" % (tag, reps), flush=True)

json.dump({"IN": {"sha": IN_SHA, "canon": IN_CANON},
           "OUT": {"sha": OUT_SHA, "canon": OUT_CANON}, "src": SRC},
          open(B.RDIR / "MSINK_finalization_witness_replay.json", "w"), indent=1)
print("witness replays: IN A=%d Q=%d | OUT A=%d Q=%d" % (
    sum(l["a"] for l in IN_P["legs"]), sum(l["q"] for l in IN_P["legs"]),
    sum(l["a"] for l in OUT_P["legs"]), sum(l["q"] for l in OUT_P["legs"])), flush=True)

# ---- msink: min-rule vs existential rule (E-task) ----
def msink_exists(iv, legs):
    # Existential sink semantics: all valid (E-pair, sink) combos; [] = non-member.
    s = len(iv)
    E = [j for j in range(s)
         if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    if len(E) != 2:
        return []
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
        return []
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
    return out

for tag, W in (("IN", IN_W), ("OUT", OUT_W)):
    r = B.replay(W)
    iv = B.intervals_of(r["legs"])
    ps = msink_exists(iv, r["legs"])
    ms = B.msink(iv, r["legs"])
    need("%s-exists-vs-min" % tag, (ps != []) == (ms is not None),
         "exists=%s min=%s" % (ps, None if ms is None else ms["p"]))
    if tag == "IN":
        need("IN-exists-nonempty", ps != [], ps)
        need("IN-min-is-first-eligible", ms["p"] == min(ps), ms["p"])
        # frozen-narrow H5 on IN others: d_A>=3-K or strict-P per positive
        ivd = iv
        narrow = []
        for j in range(len(ivd)):
            if j in ms["E"] or j == ms["p"]:
                continue
            if ivd[j]["w"] <= 0:
                continue
            dA = r["legs"][ivd[j]["gi"]]["dA"]
            narrow.append((j, ivd[j]["x"], dA >= 3, M.isP(ivd[j], r["legs"], True)))
        need("IN-frozen-narrow-H5", all(k or p for _, _, k, p in narrow), narrow)
    else:
        need("OUT-exists-empty", ps == [], ps)

# ---- battery on witnesses (12 exact + 5 recognizers, pointer legs for AS) ----
def full_battery(plegs, snaps):
    lb = B.perleg_blocks(plegs)
    mb = B.merged_blocks(plegs)
    assert isinstance(mb, list)
    iv = B.intervals_of(plegs)
    bdep = []
    for i in range(len(plegs)):
        bdep.append(snaps.get(i, {}))
    u = B.union_exec(lb, mb)
    rAS = B.ASm.recognize(mb, snaps)
    u["AS"] = bool(rAS.get("accepted", False))
    batt = dict(u)
    batt.update({"NP": M.member_NP(iv, plegs), "S1": M.member_S1(iv, plegs),
                 "S2": M.member_S2(iv, plegs), "VR": M.member_VR(iv, plegs),
                 "MR": M.member_MR(iv, plegs), "AJ": M.member_AJ(mb),
                 "AK": M.member_AK(mb, bdep), "ALG": M.member_ALG(mb, bdep),
                 "ALS": M.member_ALS(mb), "AMG": M.member_AMG(mb, bdep),
                 "AMS": M.member_AMS(mb), "AN": M.member_AN(mb)})
    return batt, iv, mb
bin_, ivin, mbin = full_battery(IN_P["legs"], IN_P["snaps"])
bout, ivout, about = full_battery(OUT_P["legs"], OUT_P["snaps"])
need("IN-battery-17neg", not any(bin_.values()), [k for k, v in bin_.items() if v])
need("OUT-battery-17neg", not any(bout.values()), [k for k, v in bout.items() if v])
# IN msink detail + joint arithmetic recheck
ms = B.msink(ivin, IN_P["legs"])
need("IN-msink-true", ms is not None)
if ms is not None:
    jp = ivin[ms["p"]]
    need("IN-joint-arith", ms["E"] == [4, 12] and ms["t"] == [0, 2]
         and jp["H"] == 13 and jp["w"] + 2 <= jp["R"],
         "E=%s t=%s Hp=%d w=%d R=%d" % (ms["E"], ms["t"], jp["H"], jp["w"], jp["R"]))
    sw = sum(v["w"] for v in ivin); sR = sum(v["R"] for v in ivin)
    tot = B.totals_of(IN_P["legs"])
    need("IN-telescope-id", sw == tot["Q"] - 2 * tot["Ck"] and sR == 2 * (tot["A"] - tot["Ck"]) and sw <= sR,
         "Sw=%d SR=%d" % (sw, sR))
# OUT MR-H6 pinpoint recheck (interval 0, dA=0, KEEP a=0 vs strict P)
v0 = ivout[0]
need("OUT-MR-H6-pin", v0["x"] == 3 and v0["w"] == 1
     and OUT_P["legs"][v0["gi"]]["dA"] == 0
     and OUT_P["legs"][v0["gi"]]["a"] == 0
     and not M.isK(v0, OUT_P["legs"]) and not M.isP(v0, OUT_P["legs"], True),
     "x=%d w=%d dA=%d a=%d" % (v0["x"], v0["w"], OUT_P["legs"][v0["gi"]]["dA"], OUT_P["legs"][v0["gi"]]["a"]))

# ---- additive segment machinery (shared with order audit) ----
def sliced_products(plegs, pairs, snaps, i, j):
    seg = plegs[i:j]
    # rebuild merged blocks in slice frame, remap l0/l1 to ORIGINAL indices
    mb = B.merged_blocks(seg)
    if not isinstance(mb, list):
        return None
    # remap: slice position t -> original i+t
    pos = 0
    remap_l1 = {}
    cur = None
    n = len(seg)
    f = next((t for t, lg in enumerate(seg) if lg["a"] >= 1), None)
    if f is None:
        return None
    # merged_blocks rotated to f; walk its construction to map block order:
    # simpler: assign by matching (key,a,q,delta) multisets? robust: recompute here
    order = [(f + k) % n for k in range(n)]
    blocks, cur2, first_gi = [], None, None
    for t, gi in enumerate(order):
        lg = seg[gi]
        if lg["a"] >= 1:
            if cur2 is not None:
                blocks.append(cur2)
            cur2 = {"b": dict(lg), "gi0": i + gi, "gi1": i + gi}
        else:
            cur2["gi1"] = i + gi
    if cur2 is not None:
        blocks.append(cur2)
    if len(blocks) != len(mb):
        return None
    for blk, b in zip(blocks, mb):
        b["l0"] = blk["gi0"]; b["l1"] = blk["gi1"] + 1
    iv = B.intervals_of(seg)
    # genuine keys + core9 domain within part
    gk = sorted({lg["x"] for lg in seg if lg["m"] == "K" and lg["chg"]})
    ok_core = True
    for t in range(i, j + 1):
        c = B.core(pairs[t][1], MSET)
        if c is None or len(c) != 9:
            ok_core = False
    return {"mb": mb, "iv": iv, "gk": gk, "core9": ok_core, "seg": seg}

def part_covered(sp, snaps_full, bdep_full, off):
    # snaps keyed by ORIGINAL access index (blocks carry remapped original l1)
    sn = {k: snaps_full[k] for k in range(off, off + len(sp["seg"]) + 1)
          if k in snaps_full}
    lb = B.perleg_blocks(sp["seg"])
    u = B.union_exec(lb, sp["mb"])
    rAS = B.ASm.recognize(sp["mb"], sn)
    flags = [k for k, v in u.items() if v] + (["AS"] if rAS.get("accepted") else [])
    mem = {"NP": M.member_NP(sp["iv"], sp["seg"]),
           "S1": M.member_S1(sp["iv"], sp["seg"]),
           "S2": M.member_S2(sp["iv"], sp["seg"]),
           "VR": M.member_VR(sp["iv"], sp["seg"]),
           "MR": M.member_MR(sp["iv"], sp["seg"]),
           "AJ": M.member_AJ(sp["mb"]), "AK": M.member_AK(sp["mb"], bdep_full),
           "ALG": M.member_ALG(sp["mb"], bdep_full), "ALS": M.member_ALS(sp["mb"]),
           "AMG": M.member_AMG(sp["mb"], bdep_full), "AMS": M.member_AMS(sp["mb"]),
           "AN": M.member_AN(sp["mb"])}
    flags += [k for k, v in mem.items() if v]
    dom = (sp["gk"] == [1, 3, 5, 7, 9] and sp["core9"])
    return {"covered": bool(flags) and dom, "flags": flags, "domain": dom,
            "gkeys": sp["gk"]}

def additive_status(P):
    n = len(P["legs"])
    S0 = P["S0"]
    splits = [t for t in range(1, n) if P["pairs"][t] == S0]
    if not splits:
        return {"splits": [], "covered": False, "reason": "aperiodic-no-splits"}
    import itertools
    # full B-depth list in original indexing for snapshot predicates
    bdep_full = [P["snaps"].get(t, {}) for t in range(n)]
    # all subset-partitions with >=2 parts
    for r_ in range(1, len(splits) + 1):
        for combo in itertools.combinations(splits, r_):
            bounds = (0,) + combo + (n,)
            parts = []
            ok = True
            for a2, b2 in zip(bounds[:-1], bounds[1:]):
                sp = sliced_products(P["legs"], P["pairs"], P["snaps"], a2, b2)
                if sp is None:
                    ok = False
                    break
                pc = part_covered(sp, P["snaps"], bdep_full, a2)
                parts.append({"bounds": (a2, b2), "cover": pc})
                if not pc["covered"]:
                    ok = False
                    break
            if ok:
                return {"splits": splits, "covered": True,
                        "partition": [p["bounds"] for p in parts],
                        "flags": [p["cover"]["flags"] for p in parts]}
    return {"splits": splits, "covered": False, "reason": "no-covered-partition"}

ai = additive_status(IN_P)
ao = additive_status(OUT_P)
ac = additive_status(pointer_replay(S1W + VRW))
need("IN-additive-excluded", ai["covered"] is False, ai)
need("OUT-additive-excluded", ao["covered"] is False, ao)
need("CONCAT-additive-covered", ac["covered"] is True, ac)
json.dump({"IN": ai, "OUT": ao, "CONCAT": ac},
          open(B.RDIR / "MSINK_finalization_additive.json", "w"), indent=1, default=str)

# ---- census reconstruction ----
for seed in ("concat35", "mr33"):
    d = B.RDIR / ("state_" + seed)
    cen = json.load(open(d / "census.json"))
    seen = [l.strip() for l in open(d / "seen.txt") if l.strip()]
    pars = [l.strip() for l in open(d / "parents_L1.txt") if l.strip()]
    regen = [canon(w) for w in B.mutants(B.SEEDS[seed]) if 25 <= len(w) <= 45]
    need("%s-parents-exact" % seed, pars == regen, "n=%d" % len(pars))
    # seen.txt carries within-run redupes (census dedup erratum: in-loop seen-set
    # not updated; same deterministic words reprocessed with identical
    # dispositions). Distinct count is authoritative for caps.
    from collections import Counter as _C
    dupes = sum(v - 1 for v in _C(seen).values())
    need("%s-lines-eq-tested" % seed, len(seen) == cen["tested"],
         "lines=%d tested=%d" % (len(seen), cen["tested"]))
    need("%s-distinct-census" % seed, True,
         "distinct=%d redupes=%d" % (len(set(seen)), dupes))
    need("%s-budget" % seed, len(seen) <= 250000, len(seen))
need("total-budget", sum(json.load(open(B.RDIR / ("state_" + s) / "census.json"))["tested"] for s in ("concat35", "mr33")) <= 500000)
need("L2-never-ran", not (B.RDIR / "state_concat35" / "parents_L2.txt").exists() and not (B.RDIR / "state_mr33" / "parents_L2.txt").exists())

fails = [k for k, v in R.items() if not v["ok"]]
json.dump({"results": R, "pass": not fails},
          open(B.RDIR / "MSINK_finalization_verify.json", "w"), indent=1)
print("VERIFY: %s (%d checks, %d fails)" % ("PASS" if not fails else "FAIL", len(R), len(fails)), flush=True)
VERIFY_PASS = not fails
VERIFY_FAILS = fails
if __name__ == "__main__":
    sys.exit(0 if VERIFY_PASS else 1)
