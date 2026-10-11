# MSINK deterministic bounded discovery: DELETE-only mutants of 2 seeds.
#
# Order: edit distance asc; seed order; parent first-seen; op order
# (removal, replacement, insertion); gap/index order; key asc. Dedup by canonical
# sha (disk-backed per seed). Caps: 250k distinct per seed, 500k total.
# Early STOP once IN and OUT roles are both frozen. Tuple-engine screening;
# pointer replay only for audit. Additive exclusion via pair-state splits.
import sys, copy, json, hashlib, importlib.util
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import splay as S

def _load(modname, relpath):
    spec = importlib.util.spec_from_file_location(
        modname, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/' + relpath)
    mo = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mo
    spec.loader.exec_module(mo)
    return mo
AO = _load('msink_AO', '26AO/26AO_two_order_recognizer.py')
AP = _load('msink_AP', '26AP/26AP_maximal_run_recognizer.py')
AQ = _load('msink_AQ', '26AQ/26AQ_mixed_cyclic_dp_recognizer.py')
AR = _load('msink_AR', '26AR/26AR_mixed_exact_cover_recognizer.py')
ASm = _load('msink_AS', '26AS/26AS_mixed_cyclic_recognizer.py')

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
SEEDS = {"concat35": S1W + VRW, "mr33": MRW}
CAP_SEED = 250000
CAP_TOTAL = 500000
MSET = {1, 3, 5, 7, 9}

def canon(word):
    return ",".join(m + str(k) for m, k in word)
def sha(word):
    return hashlib.sha256(canon(word).encode("ascii")).hexdigest()
def parse(canon_s):
    return [(tok[0], int(tok[1:])) for tok in canon_s.split(",")]

def mutants(word):
    n = len(word)
    dpos = [i for i, (m, _) in enumerate(word) if m == 'D']
    for i in dpos:
        yield word[:i] + word[i + 1:]
    for i in dpos:
        for k in range(1, 10):
            if k == word[i][1]:
                continue
            w = list(word); w[i] = ('D', k)
            yield w
    for g in range(n + 1):
        for k in range(1, 10):
            w = list(word); w.insert(g, ('D', k))
            yield w

def T(t, x):
    return S.trace(t, x)[0]
def dep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def ser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, ser(l), ser(r))
def totup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], totup(t[1]), totup(t[2]))
def core(s, M):
    c = set()
    def path(nd, x, p):
        if nd == '.':
            return None
        k, l, r = nd
        p = p + [k]
        if k == x:
            return p
        return path(l, x, p) or path(r, x, p)
    for m in M:
        pp = path(s, m, [])
        if pp is None:
            return None
        c.update(pp)
    return c

def banked_T0():
    return [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
              [8, [7, None, None], None]], None]
T0T = totup(banked_T0())

def replay(word):
    A = copy.deepcopy(T0T); B = copy.deepcopy(T0T)
    sA0, sB0 = ser(A), ser(B)
    S0 = (sA0, sB0)
    legs, aser, bser, bdep = [], [sA0], [sB0], []
    for (md, x) in word:
        dAm = dep(A)
        da = dAm.get(x, -1)
        if da < 0:
            return None
        sA, sB = ser(A), ser(B)
        a = (da + 1) // 2
        ra = sA[0] if sA != '.' else None
        rb = sB[0] if sB != '.' else None
        if md == 'K':
            dBm = dep(B)
            db = dBm.get(x, -1)
            if db < 0:
                return None
            q = db // 2
        else:
            db = None; q = 0
        A = T(A, x)
        if md == 'K':
            B = T(B, x)
        nsA, nsB = ser(A), ser(B)
        chg = (nsB != sB) if md == 'K' else False
        dBn = dep(B)
        aser.append(nsA); bser.append(nsB); bdep.append(dBn)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg})
    return {"legs": legs, "S0": S0, "S1": (nsA, nsB),
            "aser": aser, "bser": bser, "bdep": bdep}

def perleg_blocks(legs):
    out = []
    for lg in legs:
        out.append({"key": lg["x"], "keys": [lg["x"]], "a": lg["a"],
                    "q": lg["q"], "delta": lg["delta"],
                    "genuine": bool(lg["chg"]), "dB": lg["dB"], "rb": lg["rb"],
                    "keeps": [lg["x"]] if lg["m"] == "K" else []})
    return out

def merged_blocks(legs):
    n = len(legs)
    f = next((i for i, lg in enumerate(legs) if lg["a"] >= 1), None)
    if f is None:
        return "A0"
    order = [(f + k) % n for k in range(n)]
    out, cur = [], None
    for pos, gi in enumerate(order):
        lg = legs[gi]
        if lg["a"] >= 1:
            if cur is not None:
                out.append(cur)
            cur = {"key": lg["x"], "keys": [lg["x"]], "a": lg["a"],
                   "q": lg["q"], "genuine": bool(lg["chg"]), "dB": lg["dB"],
                   "rb": lg["rb"],
                   "keeps": sorted({lg["x"]} if lg["m"] == "K" else set()),
                   "dA": lg["dA"],
                   "push": sorted(set(lg.get("push") or [])),
                   "l0": gi, "l1": gi + 1, "nleg": 1}
        else:
            if cur is None or lg["x"] != cur["key"]:
                return None
            cur["a"] += lg["a"]; cur["q"] += lg["q"]
            cur["genuine"] = cur["genuine"] or bool(lg["chg"])
            if lg["m"] == "K":
                cur["keeps"] = sorted(set(cur["keeps"]) | {lg["x"]})
            cur["push"] = sorted(set(cur["push"]) | set(lg.get("push") or []))
            cur["nleg"] += 1
    if cur is not None:
        out.append(cur)
    for b in out:
        b["delta"] = b["q"] - 2 * b["a"]
    return out

def intervals_of(legs):
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    out = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        if prev < i:
            segi = list(range(prev + 1, i + 1))
        else:
            segi = list(range(prev + 1, len(legs))) + list(range(0, i + 1))
        seg = [legs[k] for k in segi]
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        out.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                    "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c), "gi": i,
                    "segi": segi})
    return out

def pcond(iv_j, legs):
    x = iv_j["x"]
    for k in iv_j["segi"]:
        lg = legs[k]
        if lg["m"] == "D" and lg["x"] != x:
            return True
    return False

def msink(iv, legs):
    s = len(iv)
    E = [j for j in range(s)
         if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    if len(E) != 2:
        return None
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
        return None
    P = [j for j in range(s)
         if j not in E and iv[j]["c"] == 1 and iv[j]["H"] >= 3]
    if not P:
        return None
    p = min(P)
    jp = iv[p]
    if jp["q"] > 4:
        return None
    if not (jp["w"] <= jp["R"] - 2):
        return None
    cases = {}
    for j in range(s):
        if j in E or j == p:
            continue
        w, R = iv[j]["w"], iv[j]["R"]
        if w <= 0:
            cases[j] = "nonpos"
        elif iv[j]["c"] == 1 and iv[j]["H"] >= 2:
            cases[j] = "K"
        elif pcond(iv[j], legs) and iv[j]["H"] >= 2:
            cases[j] = "P"
        else:
            return None
        if not (w <= R):
            return None
    return {"E": E, "t": tl, "p": p, "Hp": jp["H"], "qp": jp["q"],
            "cases": cases}

def np_covered(iv, legs):
    for j in range(len(iv)):
        if iv[j]["w"] > 0:
            if iv[j]["c"] == 1 and iv[j]["H"] >= 2:
                continue
            if pcond(iv[j], legs) and iv[j]["H"] >= 2:
                continue
            return False
    return True

def eshape(iv):
    E = [j for j in range(len(iv))
         if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    return {"nE": len(E), "E": E}

def union_exec(lb, mb):
    rAO = AO.recognize(lb)
    rAP = AP.recognize(mb)
    rAQ = AQ.recognize(mb)
    rAR = AR.recognize(mb)
    return {"AO": rAO is not None,
            "AP": bool(rAP.get("accepted", False)),
            "AQ": bool(rAQ.get("accepted", False)),
            "AR": bool(rAR.get("accepted", False))}

def r5_status(r):
    legs = r["legs"]
    gk = sorted({lg["x"] for lg in legs if lg["m"] == "K" and lg["chg"]})
    if len(gk) != 5:
        return None
    for s in r["bser"]:
        if core(s, MSET) is None or len(core(s, MSET)) != 9:
            return None
    return gk

def splits_of(r):
    S0 = r["S0"]
    n = len(r["legs"])
    return [i for i in range(1, n)
            if (r["aser"][i], r["bser"][i]) == S0]

def totals_of(legs):
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    return {"A": A, "Q": Q, "Ck": Ck, "W": Q - 2 * Ck, "n": len(legs)}

def process_word(word):
    r = replay(word)
    if r is None or r["S1"] != r["S0"]:
        return None, "rejected"
    gk = r5_status(r)
    if gk is None:
        return None, "closed-nonR5"
    legs = r["legs"]
    lb = perleg_blocks(legs)
    mb = merged_blocks(legs)
    if mb is None or mb == "A0":
        return None, ("closed-R5-A0" if mb == "A0" else "closed-R5-badblocks")
    u = union_exec(lb, mb)
    if any(u.values()):
        return None, "closed-R5-banked"
    iv = intervals_of(legs)
    ms = msink(iv, legs)
    rec = {"canon": canon(word), "sha": sha(word), "tot": totals_of(legs),
           "gkeys": gk, "union": u, "msink": ms,
           "np": np_covered(iv, legs), "eshape": eshape(iv),
           "nsplits": len(splits_of(r)),
           "iv": [(v["x"], v["H"], v["c"], v["q"], v["w"], v["R"])
                  for v in iv]}
    return rec, ("msink-survivor" if ms is not None else "nonmsink-survivor")

# ---------------- drivers ----------------
def sdir(seed):
    d = RDIR / ("state_" + seed)
    d.mkdir(parents=True, exist_ok=True)
    return d

def load_seen(seed):
    d = sdir(seed)
    f = d / "seen.txt"
    s = set()
    if f.exists():
        for line in open(f):
            line = line.strip()
            if line:
                s.add(line)
    return s

def save_seen(seed, seen, new_hashes):
    d = sdir(seed)
    with open(d / "seen.txt", "a") as fh:
        for h in new_hashes:
            fh.write(h + "\n")
    for h in new_hashes:
        seen.add(h)

def load_census(seed):
    d = sdir(seed)
    f = d / "census.json"
    if f.exists():
        return json.load(open(f))
    return {"tested": 0, "closed": 0, "closedR5": 0, "banked": 0,
            "msink_survivors": 0, "nonmsink_survivors": 0}

def save_census(seed, c):
    json.dump(c, open(sdir(seed) / "census.json", "w"), indent=1)

def cmd_validate():
    ok = True
    # positives: banked witness certs must ACCEPT (format check)
    ao_cert = json.load(open(
        'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO/26AO_ten_key_witness_certificate.json'))
    ao_lb = [{"key": l["x"], "keys": [l["x"]], "a": l["a"], "q": l["q"],
              "delta": l["delta"], "genuine": bool(l["bchanged"]),
              "dB": l["dB"], "rb": l["rb"],
              "keeps": [l["x"]] if l["m"] == "K" else []}
             for l in ao_cert["legs"]]
    r = AO.recognize(ao_lb)
    print("AO witness:", "ACCEPT" if r is not None else "REJECT", flush=True)
    ok = ok and (r is not None)
    for tag, path in (("AP", 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/26AP_vine16_witness_certificate.json'),
                      ("AQ", 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ/26AQ_vine16_witness_certificate.json')):
        cert = json.load(open(path))
        rr = (AP if tag == "AP" else AQ).recognize(cert["blocks"])
        print(tag, "witness:", "ACCEPT" if rr.get("accepted") else "REJECT", flush=True)
        ok = ok and bool(rr.get("accepted"))
    ar_cert = json.load(open(
        'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AR/26AR_vine16_closed_witness.json'))
    wb = AR.enrich(ar_cert["blocks"], ar_cert["legs"])
    r0 = AR.recognize(wb)
    print("AR witness:", "ACCEPT" if r0.get("accepted") else "REJECT", flush=True)
    ok = ok and bool(r0.get("accepted"))
    # controls: S1/VR/MR/concat must process + report (no crash); union+msink noted
    for name, w in (("S1", S1W), ("VR", VRW), ("CONCAT", S1W + VRW), ("MR", MRW)):
        rec, cls = process_word(w)
        ms = (rec is not None and rec["msink"] is not None)
        print("%s: class=%s msink=%s" % (name, cls, ms), flush=True)
    print("VALIDATE:", "PASS" if ok else "FAIL", flush=True)
    return ok

def cmd_census(seed, layer, start=0, count=None):
    assert seed in SEEDS
    t0 = __import__("time").time()
    seen = load_seen(seed)
    census = load_census(seed)
    d = sdir(seed)
    new_hashes = []
    survivors = []
    if layer == "L0L1":
        parents = []
        base = SEEDS[seed]
        if sha(base) not in seen:
            new_hashes.append(sha(base))
        rec, cls = process_word(base)
        census["tested"] += 1
        if cls.startswith("closed"):
            census["closed"] += 1
        if cls == "closed-R5-banked":
            census["banked"] += 1
        if cls.endswith("survivor"):
            census["closedR5"] += 1
            if cls.startswith("msink"):
                census["msink_survivors"] += 1
            else:
                census["nonmsink_survivors"] += 1
            rec["meta"] = {"seed": seed, "layer": 0, "idx": 0}
            survivors.append(rec)
        for w2 in mutants(base):
            if len(w2) < 25 or len(w2) > 45:
                continue
            h = sha(w2)
            if h in seen:
                continue
            seen.add(h)
            new_hashes.append(h)
            parents.append(canon(w2))
        with open(d / "parents_L1.txt", "w") as fh:
            for c in parents:
                fh.write(c + "\n")
        census["L1_parents"] = len(parents)
        idx0 = 0
        todo = parents
    elif layer == "L2":
        lines = [l.strip() for l in open(d / "parents_L1.txt") if l.strip()]
        todo = lines[start:(start + count) if count else None]
        idx0 = start
    else:
        raise ValueError(layer)
    spill = open(d / "parents_L2.txt", "a") if layer == "L2" else None
    for k, cs in enumerate(todo):
        w = parse(cs)
        rec, cls = process_word(w)
        census["tested"] += 1
        if cls.startswith("closed"):
            census["closed"] += 1
        if cls == "closed-R5-banked":
            census["banked"] += 1
        if cls.endswith("survivor"):
            census["closedR5"] += 1
            if cls.startswith("msink"):
                census["msink_survivors"] += 1
            else:
                census["nonmsink_survivors"] += 1
            rec["meta"] = {"seed": seed, "layer": layer, "idx": idx0 + k}
            survivors.append(rec)
        if layer == "L2":
            for w2 in mutants(w):
                if len(w2) < 25 or len(w2) > 45:
                    continue
                h = sha(w2)
                if h in seen:
                    continue
                seen.add(h)
                new_hashes.append(h)
                spill.write(canon(w2) + "\n")
        if (k + 1) % 2000 == 0:
            dt = __import__("time").time() - t0
            print("  %s %s progress %d/%d tested=%d closed=%d R5surv=%d time=%.0fs" % (
                seed, layer, k + 1, len(todo), census["tested"],
                census["closed"],
                census["msink_survivors"] + census["nonmsink_survivors"], dt),
                flush=True)
    if spill:
        spill.close()
    save_seen(seed, seen, new_hashes)
    save_census(seed, census)
    with open(d / "survivors.jsonl", "a") as fh:
        for rec in survivors:
            fh.write(json.dumps(rec, default=str) + "\n")
    dt = __import__("time").time() - t0
    print("%s %s done: n=%d tested=%d closed=%d banked=%d msink=%d nonmsink=%d new=%d time=%.1fs" % (
        seed, layer, len(todo), census["tested"], census["closed"],
        census["banked"], census["msink_survivors"],
        census["nonmsink_survivors"], len(new_hashes), dt), flush=True)

if __name__ == "__main__":
    a = sys.argv
    if a[1] == "validate":
        sys.exit(0 if cmd_validate() else 1)
    elif a[1] == "census":
        cmd_census(a[2], a[3], int(a[4]) if len(a) > 4 else 0,
                   int(a[5]) if len(a) > 5 else None)
    else:
        raise ValueError(a[1:])
